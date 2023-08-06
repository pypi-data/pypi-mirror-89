"""
     esbmtk: A general purpose Earth Science box model toolkit
     Copyright (C), 2020 Ulrich G. Wortmann

     This program is free software: you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation, either version 3 of the License, or
     (at your option) any later version.

     This program is distributed in the hope that it will be useful,
     but WITHOUT ANY WARRANTY; without even the implied warranty of
     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
     GNU General Public License for more details.

     You should have received a copy of the GNU General Public License
     along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

# from pint import UnitRegistry
from numbers import Number
from nptyping import *
from typing import *
from numpy import array, set_printoptions, arange, zeros, interp, mean
from pandas import DataFrame
from copy import deepcopy, copy
from time import process_time

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import logging
import time
import builtins
set_printoptions(precision=4)
from .utility_functions import *
from .esbmtk import *

class Connect(esbmtkBase):
    """Name:

        Connect

    Description: Two reservoirs connect to each other via at least 1
    flux. This module creates the connecting flux and creates a
    connecctor object which stores all connection properties

    Connection properties include:
       - the direction of the flux (from A to B)
       - any processes which act on the flux, and whether these processes depend on the upstream, downstream or both reservoirs
       - the type of flux:
           - Fixed: both flux-rate and delta are given, allowed processes include signal and fractionation
           - Reservoir-Driven: delta and or flux rate depend on the reservoir data (upstream/downstream both)
               - if nothing assume upstream reservoir passive flux with var delta
               - if only flux it assume upstream reservoir with fixed flux and var delta
               - if only delta assume varflux with fixed delta
               - if both delta and flux are given print warning and suggest to use a static flux
               - if only alpha assume upstream var flux and fractionation process
               - Allowed processes: ALL

    Example:
    
    Connect(source =  upstream reservoir
	   sink = downstrean reservoir
           delta = optional
           alpha = optional
           rate = optional
           ref = optional
           species = optional
           ctype = optional
	   pl = [list]) process list. optional
           id = optional identifier
           plot = "yes/no" # defaults to yes

    You can aditionally define connection properties via the ctype keyword. The following values are reckognized

   - scale_with_flux: flux-reference, k-value
   - scale_with_mass: reservoir-reference, k-value
   - scale_with_concentration: reservoir-ref, k-value
   - scale_with_mass_normalized: reservoir-ref, k-value, ref-value
   - scale_with_concentration_normalized:  reservoir-ref, k-value, ref-value
   - monod_type_limit: ref_value, a-value, b-value

    where k_value represents a scaling factor. For details, see the help system

    useful methods in this class

    Name.list_processes() which will list all the processes which are associated with this connection.
    
    """
    def __init__(self, **kwargs):
        """ The init method of the connector obbjects performs sanity checks e.g.:
               - whether the reservoirs exist
               - correct flux properties (this will be handled by the process object)
               - whether the processes do exist (hmmh, that implies that the optional processes do get registered with the model)
               - creates the correct default processes
               - and connects the reservoirs

        Arguments:
           name = name of the connector object : string
           source   = upstream reservoir    : object handle
           sink  = downstream reservoir  : object handle
           fp   = connection_properties : dictionary {delta, rate, alpha, species, type}
           pl[optional]   = optional processes : list
        
        """

        from . import ureg, Q_

        # provide a dict of all known keywords and their type
        self.lkk: Dict[str, any] = {
            "name": str,
            "id": str,
            "source": (Source, Reservoir),
            "sink": (Sink, Reservoir),
            "delta": Number,
            "rate": (str, Number, Q_),
            "pl": list,
            "alpha": Number,
            "species": Species,
            "ctype": str,
            "ref": (Flux, list),
            "react_with": Flux,
            "ratio": Number,
            "scale": Number,
            "ref_value": (str, Number, Q_),
            "ref_reservoir": (list, Reservoir),
            "k_value": (Number, str, Q_),
            "a_value": Number,
            "b_value": Number,
            "left": (list, Number, Reservoir),
            "right": (list, Number, Reservoir),
            "plot": str,
        }

        n = kwargs["source"].n + "_" + kwargs[
            "sink"].n + "_connector"  # set the name
        kwargs.update({"name": n})  # and add it to the kwargs

        # provide a list of absolutely required keywords
        self.lrk: list = ["name", "source", "sink"]

        # list of default values if none provided
        self.lod: Dict[any, any] = {"id": "", "plot": "yes", "ctype": "None"}

        # validate and initialize instance variables
        self.__initerrormessages__()

        self.bem.update({
            "k_concentration": "a number",
            "k_mass": "a number",
            "k_value": "a number",
            "a_value": "a number",
            "ref_value": "a number, string, or quantity",
            "b_value": "a number",
            "name": "a string",
            "id": "a string",
            "plot": "a string",
            "left": "Number, list or Reservoir",
            "right": "Number, list or Reservoir",
        })

        self.__validateandregister__(kwargs)

        if len(kwargs["id"]) > 0:
            self.name = self.name + f"_{self.id}"
        if 'pl' in kwargs:
            self.lop: list[Process] = self.pl
        else:
            self.lop: list[Process] = []

        # if no reference reservoir is specified, default to the upstream reservoir
        if not 'ref_reservoir' in kwargs:
            self.ref_reservoir = kwargs["source"]

        # legacy names
        self.influx: int = 1
        self.outflux: int = -1
        self.n = self.name
        self.mo = self.source.sp.mo

        # convert units into model units rate, k_mass, k_concentrationn
        if "rate" in kwargs:
            self.rate = Q_(self.rate).to(self.mo.f_unit)

        self.p = 0  # the default process handle
        self.r1: (Process, Reservoir) = self.source
        self.r2: (Process, Reservoir) = self.sink

        self.get_species(self.r1, self.r2)  #
        self.mo: Model = self.sp.mo  # the current model handle
        self.lof: list[Flux] = []  # list of fluxes in this connection
        self.lor: list[
            Reservoir] = self.mo.lor  # get a list of all reservoirs registered for this species

        self.source.loc.add(self)  # register connector with reservoir
        self.sink.loc.add(self)  # register connector with reservoir
        self.mo.loc.add(self)  # register connector with model

        self.__register_fluxes__()  # Source/Sink/Regular
        self.__set_process_type__()  # derive flux type and create flux(es)
        self.__register_process__(
        )  # This should probably move to register fluxes
        self.__register_name__()

    def get_species(self, r1, r2) -> None:
        """In most cases the species is set by r2. However, if we have
        backward fluxes the species depends on the r2

        """
        #print(f"r1 = {r1.n}, r2 = {r2.n}")
        if isinstance(self.r1, Source):
            self.r = r1
        else:  # in this case we do have an upstream reservoir
            self.r = r2

        # test if species was explicitly given
        if "species" in self.kwargs:  # this is a quick fix only
            self.sp = self.kwargs["species"]
        else:
            self.sp = self.r.sp  # get the parent species

    def __register_fluxes__(self) -> None:
        """Create flux object, and register with reservoir and global namespace

        """

        # test if default arguments present
        if "delta" in self.kwargs:
            d = self.kwargs["delta"]
        else:
            d = 0

        if "rate" in self.kwargs:
            r = self.kwargs["rate"]
        else:
            r = "1 mol/year"

        # flux name
        if not self.id == "":
            n = self.r1.n + '_to_' + self.r2.n + "_" + self.id  # flux name r1_to_r2
        else:
            n = self.r1.n + '_to_' + self.r2.n

        # derive flux unit from species obbject
        funit = self.sp.mu + "/" + str(self.sp.mo.bu)  # xxx

        self.fh = Flux(
            name=n,  # flux name
            species=self.sp,  # Species handle
            delta=d,  # delta value of flux
            rate=r,  # flux value
            plot=self.plot  # display this flux?
        )

        # register flux with its reservoirs
        if isinstance(self.r1, Source):
            # add the flux name direction/pair
            self.r2.lio[self.fh.n] = self.influx
            # add the handle to the list of fluxes
            self.r2.lof.append(self.fh)
            # register flux and element in the reservoir.
            self.__register_species__(self.r2, self.r1.sp)

        elif isinstance(self.r2, Sink):
            # add the flux name direction/pair
            self.r1.lio[self.fh.n] = self.outflux
            # add flux to the upstream reservoir
            self.r1.lof.append(self.fh)
            # register flux and element in the reservoir.
            self.__register_species__(self.r1, self.r2.sp)

        elif isinstance(self.r1, Sink):
            raise NameError(
                "The Sink must be specified as a destination (i.e., as second argument"
            )

        elif isinstance(self.r2, Source):
            raise NameError("The Source must be specified as first argument")

        else:  # this is a regular connection
            # add the flux name direction/pair
            self.r1.lio[self.fh.n] = self.outflux
            # add the flux name direction/pair
            self.r2.lio[self.fh.n] = self.influx
            # add flux to the upstream reservoir
            self.r1.lof.append(self.fh)
            # add flux to the downstream reservoir
            self.r2.lof.append(self.fh)
            self.__register_species__(self.r1, self.r1.sp)
            self.__register_species__(self.r2, self.r2.sp)

        self.lof.append(self.fh)

    def __register_species__(self, r, sp) -> None:
        """ Add flux to the correct element dictionary"""
        # test if element key is present in reservoir
        if sp.eh in r.doe:
            # add flux handle to dictionary list
            r.doe[sp.eh].append(self.fh)
        else:  # add key and first list value
            r.doe[sp.eh] = [self.fh]

    def __register_process__(self) -> None:
        """ Register all flux related processes"""

        # first test if we have a signal in the list. If so,
        # remove signal and replace with process

        p_copy = copy(self.lop)
        for p in p_copy:
            if isinstance(p, Signal):
                self.lop.remove(p)
                if p.ty == "addition":
                    # create AddSignal Process object
                    n = AddSignal(name=p.n + "_addition_process",
                                  reservoir=self.r,
                                  flux=self.fh,
                                  lt=p.data)
                    self.lop.append(n)
                else:
                    raise ValueError(f"Signal type {p.ty} is not defined")

        # nwo we can register everythig on lop
        for p in self.lop:
            # print(f"Registering Process {p.n}")
            # print(f"with reservoir {self.r.n} and flux {self.fh.n}")
            p.__register__(self.r, self.fh)

    def __set_process_type__(self) -> None:
        """ Deduce flux type based on the provided flux properties. The method returns the 
        flux handle, and the process handle(s).
        """

        if isinstance(self.r1, Source):
            self.r = self.r2
        else:
            self.r = self.r1

        # set process name
        if len(self.kwargs["id"]) > 0:
            self.pn = self.r1.n + "_to_" + self.r2.n + f"_{self.id}"
        else:
            self.pn = self.r1.n + "_to_" + self.r2.n

        # set the fundamental flux type
        if "delta" in self.kwargs and "rate" in self.kwargs:
            pass  # static flux
        elif "delta" in self.kwargs:
            self.__passivefluxfixeddelta__()  # variable flux with fixed delta
        elif "rate" in self.kwargs:
            self.__vardeltaout__()  # variable delta with fixed flux

        #elif "scale" in self.kwargs:
        #    self.__scaleflux__()  # scaled variable flux with fixed delta
        #elif "react_with" in self.kwargs:
        #    self.__reaction__()  # this flux will react with another flux
        else:  # if neither are given -> default varflux type
            if isinstance(self.r1, Source):
                raise ValueError(
                    f"{self.r1.n} requires a rate and delta value")
            self.__passiveflux__()

        # Set optional flux processes
        if "alpha" in self.kwargs:  # isotope enrichment
            self.__alpha__()

        # set complex flux types
        if self.ctype == "None":
            pass
        elif self.ctype == "flux_diff":
            self.__flux_diff__()
        elif self.ctype == "scale_with_flux":
            self.__scaleflux__()
        elif self.ctype == "copy_flux":
            self.__scaleflux__()
        elif self.ctype == "scale_with_mass":
            self.__rateconstant__()
        elif self.ctype == "scale_with_concentration":
            self.__rateconstant__()
        elif self.ctype == "scale_with_concentration_normalized":
            self.__rateconstant__()
        elif self.ctype == "scale_with_mass_normalized":
            self.__rateconstant__()
        elif self.ctype == "scale_relative_to_multiple_reservoirs":
            self.__rateconstant__()
        elif self.ctype == "flux_balance":
            self.__rateconstant__()
        elif self.ctype == "monod_type_limit":
            self.__rateconstant__()
        else:
            print(f"Connection Type {self.type} is unknown")
            raise ValueError(f"Unknown connection type {self.ctype}")

    def __passivefluxfixeddelta__(self) -> None:
        """ Just a wrapper to keep the if statement manageable

        """

        ph = PassiveFlux_fixed_delta(
            name=self.pn + "_Pfd",
            reservoir=self.r,
            flux=self.fh,
            delta=self.delta)  # initialize a passive flux process object
        self.lop.append(ph)

    def __vardeltaout__(self) -> None:
        """ Just a wrapper to keep the if statement manageable

        """

        ph = VarDeltaOut(name=self.pn + "_Pvdo",
                         reservoir=self.r,
                         flux=self.fh,
                         rate=self.kwargs["rate"])
        self.lop.append(ph)

    def __scaleflux__(self) -> None:
        """ Scale a flux relative to another flux
        
        """

        if not isinstance(self.kwargs["ref"], Flux):
            raise ValueError("Scale reference must be a flux")

        ph = ScaleFlux(name=self.pn + "_PSF",
                       reservoir=self.r,
                       flux=self.fh,
                       scale=self.kwargs["scale"],
                       ref=self.kwargs["ref"])
        self.lop.append(ph)

    def __flux_diff__(self) -> None:
        """ Scale a flux relative to the difference between
        two fluxes
        
        """

        if not isinstance(self.kwargs["ref"], list):
            raise ValueError("ref must be a list")

        ph = FluxDiff(name=self.pn + "_PSF",
                      reservoir=self.r,
                      flux=self.fh,
                      scale=self.kwargs["scale"],
                      ref=self.kwargs["ref"])
        self.lop.append(ph)

    def __reaction__(self) -> None:
        """ Just a wrapper to keep the if statement manageable

        """

        if not isinstance(self.kwargs["react_with"], Flux):
            raise ValueError("Scale reference must be a flux")
        ph = Reaction(name=self.pn + "_RF",
                      reservoir=self.r,
                      flux=self.fh,
                      scale=self.kwargs["ratio"],
                      ref=self.kwargs["react_with"])
        # we need to make sure to remove the flux referenced by
        # react_with is removed from the list of fluxes in this
        # reservoir.
        self.r2.lof.remove(self.kwargs["react_with"])
        self.lop.append(ph)

    def __passiveflux__(self) -> None:
        """ Just a wrapper to keep the if statement manageable

        """

        ph = PassiveFlux(
            name=self.pn + "_PF", reservoir=self.r,
            flux=self.fh)  # initialize a passive flux process object
        self.lop.append(ph)  # add this process to the process list

    def __alpha__(self) -> None:
        """ Just a wrapper to keep the if statement manageable

        """

        ph = Fractionation(name=self.pn + "_Pa",
                           reservoir=self.r,
                           flux=self.fh,
                           alpha=self.kwargs["alpha"])
        self.lop.append(ph)  #

    def __rateconstant__(self) -> None:
        """ Add rate constant type process

        """

        from . import ureg, Q_

        if "rate" not in self.kwargs:
            raise ValueError(
                "The rate constant process requires that the flux rate for this reservoir is being set explicitly"
            )

        if self.ctype == "scale_with_mass":
            self.k_value = map_units(self.k_value, self.mo.m_unit)
            ph = ScaleRelativeToMass(name=self.pn + "_PkM",
                                     reservoir=self.ref_reservoir,
                                     flux=self.fh,
                                     k_value=self.k_value)

        elif self.ctype == "scale_with_mass_normalized":
            self.k_value = map_units(self.k_value, self.mo.m_unit)
            self.ref_value = map_units(self.ref_value, self.mo.m_unit)
            ph = ScaleRelativeToNormalizedMass(name=self.pn + "_PknM",
                                               reservoir=self.ref_reservoir,
                                               flux=self.fh,
                                               ref_value=self.ref_value,
                                               k_value=self.k_value)

        elif self.ctype == "scale_with_concentration":
            self.k_value = map_units(self.k_value, self.mo.c_unit,
                                     self.mo.f_unit, self.mo.r_unit)
            ph = ScaleRelativeToConcentration(name=self.pn + "_PkC",
                                              reservoir=self.ref_reservoir,
                                              flux=self.fh,
                                              k_value=self.k_value)

        elif self.ctype == "scale_relative_to_multiple_reservoirs":
            self.k_value = map_units(self.k_value, self.mo.c_unit,
                                     self.mo.f_unit, self.mo.r_unit)
            ph = ScaleRelative2otherReservoir(name=self.pn + "_PkC",
                                              reservoir=self.source,
                                              ref_reservoir=self.ref_reservoir,
                                              flux=self.fh,
                                              k_value=self.k_value)

        elif self.ctype == "flux_balance":
            self.k_value = map_units(self.k_value, self.mo.c_unit,
                                     self.mo.f_unit, self.mo.r_unit)
            ph = Flux_Balance(name=self.pn + "_Pfb",
                              reservoir=self.source,
                              left=self.left,
                              right=self.right,
                              flux=self.fh,
                              k_value=self.k_value)

        elif self.ctype == "scale_with_concentration_normalized":
            self.k_value = map_units(self.k_value, self.mo.c_unit,
                                     self.mo.f_unit, self.mo.r_unit)
            self.ref_value = map_units(self.ref_value, self.mo.c_unit)
            ph = ScaleRelativeToNormalizedConcentration(
                name=self.pn + "_PknC",
                reservoir=self.ref_reservoir,
                flux=self.fh,
                ref_value=self.ref_value,
                k_value=self.k_value)

        elif self.ctype == "monod_ctype_limit":
            self.ref_value = map_units(self.ref_value, self.mo.c_unit)
            ph = Monod(name=self.pn + "_PMonod",
                       reservoir=self.ref_reservoir,
                       flux=self.fh,
                       ref_value=self.ref_value,
                       a_value=self.a_value,
                       b_value=self.b_value)

        else:
            raise ValueError(
                f"This should not happen,and points to a keywords problem in {self.name}"
            )

        self.lop.append(ph)

    def describe(self, **kwargs) -> None:
        """ Show an overview of the object properties.
        Optional arguments are
        index  :int = 0 this will show data at the given index
        indent :int = 0 indentation 

        """
        off: str = "  "
        if "index" not in kwargs:
            index = 0
        else:
            index = kwargs["index"]

        if "indent" not in kwargs:
            indent = 0
            ind = ""
        else:
            indent = kwargs["indent"]
            ind = ' ' * indent

        # print basic data bout this Connection
        print(f"{ind}{self.__str__(indent=indent)}")

        print(f"{ind}Fluxes:")
        for f in sorted(self.lof):
            f.describe(indent=indent, index=index)


class Connection(Connect):
    """ Alias for the Connect class

    """

class Process(esbmtkBase):
    """This class defines template for process which acts on one or more
     reservoir flux combinations. To use it, you need to create an
     subclass which defines the actual process implementation in their
     call method. See 'PassiveFlux as example'
    """
    def __init__(self, **kwargs: Dict[str, any]) -> None:
        """
          Create a new process object with a given process type and options
          """

        self.__defaultnames__()  # default kwargs names
        self.__initerrormessages__()  # default error messages
        self.bem.update({"rate": "a string"})
        self.__validateandregister__(kwargs)  # initialize keyword values
        self.__postinit__()  # do some housekeeping
        self.__register_name__()

    def __postinit__(self) -> None:
        """ Do some housekeeping for the process class
          """

        # legacy name aliases
        self.n: str = self.name  # display name of species
        self.r: Reservoir = self.reservoir
        self.f: Flux = self.flux
        self.m: Model = self.r.sp.mo  # the model handle
        self.mo: Model = self.m

        # Create a list of fluxes wich excludes the flux this process
        # will be acting upon
        self.fws: List[Flux] = self.r.lof.copy()
        self.fws.remove(self.f)  # remove this handle

        self.rm0: float = self.r.m[0]  # the initial reservoir mass
        self.direction: Dict[Flux, int] = self.r.lio[self.f.n]

        self.__misc_init__()

    def __misc_init__(self) -> None:
        """This is just a place holder method which will be called by default
        in __post_init__() This can be overloaded to add additional
        code to the init procedure without the need to redefine
        init. This useful for processes which only define a call method.

        """

        pass

    def __defaultnames__(self) -> None:
        """Set up the default names and dicts for the process class. This
          allows us to extend these values without modifying the entire init process"""

        # provide a dict of known keywords and types
        self.lkk: Dict[str, any] = {
            "name": str,
            "reservoir": Reservoir,
            "flux": Flux,
            "rate": Number,
            "delta": Number,
            "lt": Flux,
            "alpha": Number,
            "scale": Number,
            "ref": (Flux, list),
        }

        # provide a list of absolutely required keywords
        self.lrk: list[str] = ["name"]

        # list of default values if none provided
        self.lod: Dict[str, any] = {}

        # default type hints
        self.scale: t
        self.delta: Number
        self.alpha: Number

    def __register__(self, reservoir: Reservoir, flux: Flux) -> None:
        """Register the flux/reservoir pair we are acting upon, and register
          the process with the reservoir
          """

        # register the reservoir flux combination we are acting on
        self.f: Flux = flux
        self.r: Reservoir = reservoir
        # add this process to the list of processes acting on this reservoir
        reservoir.lop.append(self)
        flux.lop.append(self)

    def show_figure(self, x, y) -> None:
        """ Apply the current process to the vector x, and show the result as y.
          The resulting figure will be automatically saved.

          Example:
               process_name.show_figure(x,y)
          """
        pass

class LookupTable(Process):
     """This process replaces the flux-values with values from a static
lookup table

     Example:

     LookupTable("name", upstream_reservoir_handle, lt=flux-object)

     where the flux-object contains the mass, li, hi, and delta values
     which will replace the current flux values.

     """
     
     def __call__(self, r: Reservoir, i: int) -> None:
          """Here we replace the flux value with the value from the flux object 
          which we use as a lookup-table

          """
          self.m[i] :float  = self.lt.m[i]
          self.d[i] :float  = self.lt.d[i]
          self.l[i] :float = self.lt.l[i]
          self.h[i] :float = self.lt.h[i]

class AddSignal(Process):
    """This process adds values to the current flux based on the values provided by the sifnal object.
    This class is typically invoked through the connector object

     Example:

     AddSignal(name = "name",
               reservoir = upstream_reservoir_handle,
               flux = flux_to_act_upon,
               lt = flux with lookup values)

     where - the upstream reservoir is the reservoir the process belongs too
             the flux is the flux to act upon
             lt= contains the flux object we lookup from

    """

    def __init__(self, **kwargs: Dict[str, any]) -> None:
        """
        Create a new process object with a given process type and options
        """

        # get default names and update list for this Process
        self.__defaultnames__()  # default kwargs names
        self.lrk.extend(["lt", "flux", "reservoir"])  # new required keywords

        self.__initerrormessages__()
        #self.bem.update({"rate": "a string"})
        self.__validateandregister__(kwargs)  # initialize keyword values

        #legacy variables
        self.mo = self.reservoir.mo
        self.__postinit__()  # do some housekeeping
        self.__register_name__()

    def __call__(self, r, i) -> None:
        """Each process is associated with a flux (self.f). Here we replace
          the flux value with the value from the signal object which
          we use as a lookup-table (self.lt)

        """
        # add signal mass to flux mass
        self.f.m[i] = self.f.m[i] + self.lt.m[i]
        # add signal delta to flux delta
        self.f.d[i] = self.f.d[i] + self.lt.d[i]

        self.f.l[i], self.f.h[i] = get_imass(self.f.m[i], self.f.d[i], r.sp.r)
        # signals may have zero mass, but may have a delta offset. Thus, we do not know
        # the masses for the light and heavy isotope. As such we have to calculate the masses
        # after we add the signal to a flux

class PassiveFlux(Process):
     """This process sets the output flux from a reservoir to be equal to
     the sum of input fluxes, so that the reservoir concentration does
     not change. Furthermore, the isotopic ratio of the output flux
     will be set equal to the isotopic ratio of the reservoir The init
     and register methods are inherited from the process class. The
     overall result can be scaled, i.e., in order to create a split flow etc.
     Example:

     PassiveFlux(name = "name",
                 reservoir = upstream_reservoir_handle
                 flux = flux handle)

     """

     def __init__(self, **kwargs :Dict[str,any]) -> None:
          """ Initialize this Process """
          
         
          # get default names and update list for this Process
          self.__defaultnames__()  # default kwargs names
          self.lrk.extend(["reservoir", "flux"]) # new required keywords
          self.__initerrormessages__()
          #self.bem.update({"rate": "a string"})
          self.__validateandregister__(kwargs)  # initialize keyword values
          #legacy variables
          self.mo = self.reservoir.mo
          self.__postinit__()  # do some housekeeping
          self.__register_name__()
     
     def __call__(self,reservoir :Reservoir, i :int) -> None:
          """Here we re-balance the flux. That is, we calculate the sum of all fluxes
          excluding this flux. This sum will be equl to this flux. This will likely only
          work for outfluxes though
          
          """

          new :float = 0
          for j, f in enumerate(self.fws):
               new += f.m[i] * reservoir.lio[f.n]
               
          self.f[i] = get_flux_data(new,reservoir.d[i-1],reservoir.sp.r)

class PassiveFlux_fixed_delta(Process):
     """This process sets the output flux from a reservoir to be equal to
     the sum of input fluxes, so that the reservoir concentration does
     not change. However, the isotopic ratio of the output flux is set
     at a fixed value. The init and register methods are inherited
     from the process class. The overall result can be scaled, i.e.,
     in order to create a split flow etc.  Example:

     PassiveFlux_fixed_delta(name = "name",
                             reservoir = upstream_reservoir_handle,
                             flux handle,
                             delta = delta offset)

     """

     def __init__(self, **kwargs :Dict[str, any]) -> None:
          """ Initialize this Process """


          self.__defaultnames__()  # default kwargs names
          self.lrk.extend(["reservoir","delta", "flux"]) # new required keywords

          self.__initerrormessages__()
          #self.bem.update({"rate": "a string"})
          self.__validateandregister__(kwargs)  # initialize keyword values
          self.__postinit__()  # do some housekeeping

          # legacy names
          self.f :Flux = self.flux
          #legacy variables
          self.mo = self.reservoir.mo

          print("\nn *** Warning, you selected the PassiveFlux_fixed_delta method ***\n ")
          print(" This is not a particularly phyiscal process is this really what you want?\n")
          print(self.__doc__)
          self.__register_name__()
     
     def __call__(self, reservoir :Reservoir, i :int) -> None:
          """Here we re-balance the flux. This code will be called by the
          apply_flux_modifier method of a reservoir which itself is
          called by the model execute method

          """

          r :float = reservoir.sp.r # the isotope reference value

          varflux :Flux = self.f 
          flux_list :List[Flux] = reservoir.lof.copy()
          flux_list.remove(varflux)  # remove this handle

          # sum up the remaining fluxes
          newflux :float = 0
          for f in flux_list:
               newflux = newflux + f.m[i-1] * reservoir.lio[f.n]

          # set isotope mass according to keyword value
          self.f[i] = array(get_flux_data(newflux, self.delta, r))

class VarDeltaOut(Process):
     """Unlike a passive flux, this process sets the output flux from a
     reservoir to a fixed value, but the isotopic ratio of the output
     flux will be set equal to the isotopic ratio of the reservoir The
     init and register methods are inherited from the process
     class. The overall result can be scaled, i.e., in order to create
     a split flow etc.  Example:

     VarDeltaOut(name = "name",
                 reservoir = upstream_reservoir_handle,
                 flux = flux handle,
                 rate = rate,)

     """

     def __init__(self, **kwargs :Dict[str, any]) -> None:
          """ Initialize this Process
          
          """

          from . import ureg, Q_
          
          # get default names and update list for this Process
          self.__defaultnames__()   
          self.lkk: Dict[str, any] = {
               "name": str,
               "reservoir" : Reservoir,
               "flux": Flux,
               "rate": (str,Q_),
               }
          self.lrk.extend(["reservoir", "rate"]) # new required keywords
          self.__initerrormessages__()
          self.bem.update({"rate": "a string"})
          self.__validateandregister__(kwargs)  # initialize keyword values

          # parse rate term, and map to legacy name
          self.rateq = Q_(self.rate)
          self.rate = Q_(self.rate).to(self.reservoir.mo.f_unit).magnitude
          #legacy variables
          self.mo = self.reservoir.mo
          self.__postinit__()  # do some housekeeping
          self.__register_name__()
     
     def __call__(self, reservoir:Reservoir ,i :int) -> None:
          """Here we re-balance the flux. This code will be called by the
          apply_flux_modifier method of a reservoir which itself is
          called by the model execute method"""

          # set flux according to keyword value
          self.f[i] = get_flux_data(self.rate,reservoir.d[i-1], reservoir.sp.r)

class ScaleFlux(Process):
    """This process scales the mass of a flux (m,l,h) relative to another
     flux but does not affect delta. The scale factor "scale" and flux
     reference must be present when the object is being initalized

     Example:
          ScaleFlux(name = "Name",
                    reservoir = upstream_reservoir_handle,
                    scale = 1
                    ref = flux we use for scale)

     """
    def __init__(self, **kwargs: Dict[str, any]) -> None:
        """ Initialize this Process 

        """
        # get default names and update list for this Process
        self.__defaultnames__()  # default kwargs names
        self.lrk.extend(["reservoir", "flux", "scale",
                         "ref"])  # new required keywords

        self.__validateandregister__(kwargs)  # initialize keyword values

        #legacy variables
        self.mo = self.reservoir.mo
        self.__postinit__()  # do some housekeeping
        self.__register_name__()

    def __call__(self, reservoir: Reservoir, i: int) -> None:
        """Apply the scale factor. This is typically done through the the
          model execute method.
          Note that this will use the mass of the reference object, but that we will set the 
          delta according to the reservoir (or the flux?)

          """
        self.f[i] = self.ref[i] * self.scale
        self.f[i] = get_flux_data(self.f.m[i], reservoir.d[i - 1],
                                  reservoir.sp.r)


class FluxDiff(Process):
    """ The new flux will be the difference of two fluxes

    """
    """This process scales the mass of a flux (m,l,h) relative to another
     flux but does not affect delta. The scale factor "scale" and flux
     reference must be present when the object is being initalized

     Example:
          ScaleFlux(name = "Name",
                    reservoir = upstream_reservoir_handle,
                    scale = 1
                    ref = flux we use for scale)

     """
    def __init__(self, **kwargs: Dict[str, any]) -> None:
        """ Initialize this Process 

        """
        # get default names and update list for this Process
        self.__defaultnames__()  # default kwargs names
        self.lrk.extend(["reservoir", "flux", "scale",
                         "ref"])  # new required keywords

        self.__validateandregister__(kwargs)  # initialize keyword values
        self.__postinit__()  # do some housekeeping

        #legacy variables
        self.mo = self.reservoir.mo
        self.__register_name__()


    
    def __call__(self, reservoir :Reservoir, i: int) -> None:
        """Apply the scale factor. This is typically done through the the
        model execute method.
        Note that this will use the mass of the reference object, but that we will set the 
        delta according to the reservoir (or the flux?)

        """

        self.f[i] = (self.ref[0][i] - self.ref[1][i]) * self.scale

class Fractionation(Process):
    """This process offsets the isotopic ratio of the flux by a given
        delta value. In other words, we add a fractionation factor

     Example:
          Fractionation(name = "Name",
                        reservoir = upstream_reservoir_handle,
                        flux = flux handle
                        alpha = 12 in permil (e.f)

     """
    def __init__(self, **kwargs: Dict[str, any]) -> None:
        """ Initialize this Process """
        # get default names and update list for this Process
        self.__defaultnames__()  # default kwargs names
        self.lrk.extend(["reservoir", "flux",
                         "alpha"])  # new required keywords

        self.__validateandregister__(kwargs)  # initialize keyword values
        self.__postinit__()  # do some housekeeping

        # alpha is given in permil, but the fractionation routine expects
        # it as 1 + permil, i.e., 70 permil would 1.007
        #legacy variables
        self.alpha = 1 + self.alpha/1000
        self.mo = self.reservoir.mo
        self.__register_name__()

    def __call__(self, reservoir: Reservoir, i: int) -> None:
        """
        Set flux isotope masses based on fractionation factor

        """

        self.f.l[i], self.f.h[i] = get_frac(self.f.m[i],
                                            self.f.l[i],
                                            self.alpha)

        #update delta
        self.d = get_delta(self.f.l,
                           self.f.h,
                           self.f.sp.r)

        return

class RateConstant(Process):
    """This is a wrapper for a variety of processes which depend on rate constants
    Please see the below class definitions for details on how to call them
    At present, the following processes are defined

    ScaleRelativeToNormalizedConcentration
    ScaleRelativeToConcentration

    """

    def __init__(self, **kwargs: Dict[str, any]) -> None:
        """ Initialize this Process

        """

        from . import ureg, Q_

        # Note that self.lkk values also need to be added to the lkk
        # list of the connector object.

        # get default names and update list for this Process
        self.__defaultnames__()  # default kwargs names

        # update the allowed keywords
        self.lkk = {
            "k_value": Number,
            "ref_value": Number,
            "name": str,
            "reservoir": Reservoir,
            "flux": Flux,
            "ref_reservoir": list,
            "left": (list, Reservoir, Number),
            "right": (list, Reservoir, Number),
        }

        # new required keywords
        self.lrk.extend(["reservoir", "k_value"])

        # dict with default values if none provided
        # self.lod = {r

        self.__initerrormessages__()

        # add these terms to the known error messages
        self.bem.update({
            "k_value": "a number",
            "reservoir": "Reservoir handle",
            "ref_reservoirs": "List of Reservoir handle(s)",
            "ref_value": "a number or flux quantity",
            "name": "a string value",
            "flux": "a flux handle",
            "left": "list, reservoir or number",
            "right": "list, reservoir or number",
        })

        # initialize keyword values
        self.__validateandregister__(kwargs)
        self.__postinit__()  # do some housekeeping
        # legacy variables
        self.mo = self.reservoir.mo
        self.__register_name__()


class ScaleRelativeToNormalizedConcentration(RateConstant):
    """This process scales the flux as a function of the upstream
     reservoir concentration C and a constant which describes the
     strength of relation between the reservoir concentration and
     the flux scaling

     F = (C/C0 -1) * k

     where C denotes the concentration in the ustream reservoir, C0
     denotes the baseline concentration and k is a constant
     This process is typically called by the connector
     instance. However you can instantiate it manually as


     ScaleRelativeToNormalizedConcentration(
                       name = "Name",
                       reservoir= upstream_reservoir_handle,
                       flux = flux handle,
                       K_value =  1000,
                       ref_value = 2 # reference_concentration
    )

    """

    def __call__(self, reservoir: Reservoir, i: int) -> None:
        """
          this will be called by the Model.run() method
          """

        scale: float = (reservoir.c[i - 1] / self.ref_value - 1) * self.k_value
        # scale = scale * (scale >= 0)  # prevent negative fluxes.
        self.f[i] = self.f[i] + self.f[i] * array([scale, scale, scale, 1])


class ScaleRelativeToConcentration(RateConstant):
    """This process scales the flux as a function of the upstream
     reservoir concentration C and a constant which describes the
     strength of relation between the reservoir concentration and
     the flux scaling

     F = C * k

     where C denotes the concentration in the ustream reservoir, k is a
     constant. This process is typically called by the connector
     instance. However you can instantiate it manually as


     ScaleRelativeToConcentration(
                       name = "Name",
                       reservoir= upstream_reservoir_handle,
                       flux = flux handle,
                       K_value =  1000,
    )

    """

    def __call__(self, reservoir: Reservoir, i: int) -> None:
        """
          this will be called by the Model.run() method
          """
        #print(f"k= {self.k_value}")
        scale: float = reservoir.c[i - 1] * self.k_value
        # scale = scale * (scale >= 0)  # prevent negative fluxes.
        self.f[i] = self.f[i] * array([scale, scale, scale, 1])


class ScaleRelativeToMass(RateConstant):
    """This process scales the flux as a function of the upstream
     reservoir Mass M and a constant which describes the
     strength of relation between the reservoir mass and
     the flux scaling

     F = F0 *  M * k

     where M denotes the mass in the ustream reservoir, k is a
     constant and F0 is the initial unscaled flux. This process is
     typically called by the connector instance. However you can
     instantiate it manually as

     Note that we scale the flux, rather than compute the flux!

     This is faster than setting a new flux, computing the isotope
     ratio and setting delta. So you either have to set the initial
     flux F0 to 1, or calculate the k_value accordingly

     ScaleRelativeToMass(
                       name = "Name",
                       reservoir= upstream_reservoir_handle,
                       flux = flux handle,
                       K_value =  1000,
    )

    """

    def __call__(self, reservoir: Reservoir, i: int) -> None:
        """
          this will be called by the Model.run() method
          """
        scale: float = reservoir.m[i - 1] * self.k_value
        self.f[i] = self.f[i] * array([scale, scale, scale, 1])


class ScaleRelativeToNormalizedMass(RateConstant):
    """This process scales the flux as a function of the upstream
     reservoir mass M and a constant which describes the
     strength of relation between the reservoir concentration and
     the flux scaling

     F = (M/M0 -1) * k

     where M denotes the mass in the ustream reservoir, M0
     denotes the reference mass, and k is a constant
     This process is typically called by the connector
     instance. However you can instantiate it manually as


     ScaleRelativeToNormalizedConcentration(
                       name = "Name",
                       reservoir= upstream_reservoir_handle,
                       flux = flux handle,
                       K_value =  1,
                       ref_value = 1e5 # reference_mass
    )

    """

    def __call__(self, reservoir: Reservoir, i: int) -> None:
        """
          this will be called by the Model.run() method
          """
        scale: float = (reservoir.m[i - 1] / self.ref_value - 1) * self.k_value
        # scale = scale * (scale >= 0)  # prevent negative fluxes.
        self.f[i] = self.f[i] + self.f[i] * array([scale, scale, scale, 1])


class ScaleRelative2otherReservoir(RateConstant):
    """This process scales the flux as a function one or more reservoirs
     constant which describes the
     strength of relation between the reservoir mass(ese) and
     the flux scaling

     F = M1 * M2 * k

     where Mi denotes the mass in one  or more reservoirs, k is a
     constant. This process is typically called by the connector
     instance. However you can instantiate it manually as

     ScaleRelativeToMass(
                       name = "Name",
                       reservoir = upstream_reservoir_handle,
                       ref_reservoirs = [r1, r2]
                       flux = flux handle,
                       k_value =  1000,
    )

    """

    def __call__(self, reservoir: Reservoir, i: int) -> None:
        """
        this will be called by the Model.run() method

        """

        c: float = 1
        for r in self.ref_reservoir:
            c = c * r.c[i - 1]

        scale: float = c * self.k_value
        # scale = scale * (scale >= 0)  # prevent negative fluxes.
        self.f[i] = self.f[i] * array([scale, scale, scale, 1])

class Flux_Balance(RateConstant):
    """This process calculates a flux between two reservoirs as a function
    of multiple reservoir concentrations and constants.

    Note that could result in negative fluxes. which might cause
    issues with isotope ratios (untested)

    This will work with equilibrium reactions between two reservoirs where the
    reaction can be described as

    K * [R1] = R[2] * [R3]

    you can have more than two terms on each side as long as they are
    constants or reservoirs

    Equilibrium(
                name = "Name",
                reservoir = reservoir handle,
                left = [] # list with reservoir names or constants
                right = [] # list with reservoir names or constants
                flux = flux handle,
                k_value = a constant, defaults to 1
    )

    """

    # redefine misc_init which is being called by post-init
    def __misc_init__(self):
        """ Sort out input variables

        """

        Rl: List[Reservoir] = []
        Rr: List[Reservoir] = []
        Cl: List[float] = []
        Cr: List[float] = []
        # parse the left hand side

        em = "left/right values must be constants or reservoirs"
        [self.Rl, self.Cl] = sort_by_type(self.left, [Reservoir, Number], em)
        [self.Rr, self.Cr] = sort_by_type(self.right, [Reservoir, Number], em)

    def __call__(self, reservoir: Reservoir, i: int) -> None:
        """
        this will be called by the Model.run() method

        """

        kl: NDArray    = np.array([1.0, 1.0, 1.0, 1.0])
        kr: NDArray    = np.array([1.0, 1.0, 1.0, 1.0])
        scale: NDArray = np.array([1.0, 1.0, 1.0, 1.0])

        # calculate the product of reservoir concentrations for left side
        for r in self.Rl:
            kl *= r[i - 1]
        # multiply with any any constants on the right
        for c in self.Cl:
            kl *= c

        # calculate the product of reservoir concentrations for right side
        for r in self.Rr:
            kr *= r[i - 1]
        # multiply with any any constants on the right
        for c in self.Cr:
            kr *= c

        # set flux
        self.f[i] = (kl - kr) *  self.k_value

class Monod(Process):
    """This process scales the flux as a function of the upstream
     reservoir concentration using a Michaelis Menten type
     relationship

     F = F * a * F0 x C/(b+C)

     where F0 denotes the unscaled flux (i.e., at t=0), C denotes
     the concentration in the ustream reservoir, and a and b are
     constants.

     Example:
          Monod(name = "Name",
                reservoir =  upstream_reservoir_handle,
                flux = flux handle ,
                ref_value = reference concentration
                a_value = constant,
                b_value = constant )

     """

    def __init__(self, **kwargs: Dict[str, any]) -> None:
        """

        """

        from . import ureg, Q_

        """ Initialize this Process """
        # get default names and update list for this Process
        self.__defaultnames__()  # default kwargs names
        
        # update the allowed keywords
        self.lkk = {
            "a_value": Number,
            "b_value": Number,
            "ref_value": (Number,str, Q_),
            "name": str,
            "reservoir": Reservoir,
            "flux": Flux,
        }

        self.lrk.extend(["reservoir", "a_value", "b_value",
                         "ref_value"])  # new required keywords

        self.__initerrormessages__()
        self.bem.update({
            "a_value": "a number",
            "b_value": "a number",
            "reservoir": "Reservoir handle",
            "ref_value": "a number",
            "name": "a string value",
            "flux": "a flux handle",
        })

        self.__validateandregister__(kwargs)  # initialize keyword values
        self.__postinit__()  # do some housekeeping
        #legacy variables
        self.mo = self.reservoir.mo
        self.__register_name__()

    def __call__(self, reservoir: Reservoir, i: int) -> None:
        """
          this willbe called by Model.execute apply_processes
          """

        scale: float = self.a_value * (self.ref_value * reservoir.c[i - 1]) / (
            self.b_value + reservoir.c[i - 1])

        scale = scale * (scale >= 0)  # prevent negative fluxes.
        self.f[i] + self.f[i] * scale

    def __plot__(self, start: int, stop: int, ref: float, a: float,
                 b: float) -> None:
        """ Test the implementation

          """

        y = []
        x = range(start, stop)

        for e in x:
            y.append(a * ref * e / (b + e))

        fig, ax = plt.subplots()  #
        ax.plot(x, y)
        # Create a scatter plot for ax
        plt.show()
