"""
Unit handling makes use of the `Pint <https://github.com/hgrecco/pint>`_ library. This
allows us to easily define units as well as contexts. Contexts allow us to perform
conversions which would not normally be allowed e.g. in the 'AR4GWP100'
context we can convert from CO2 to CH4 using the AR4GWP100 equivalence metric.

An illustration of how the ``unit_regsitry`` can be used is shown below:

.. code:: python

    >>> from openscm_units import unit_registry
    >>> unit_registry("CO2")
    <Quantity(1, 'CO2')>

    >>> emissions_aus = 0.34 * unit_registry("Gt C / yr")
    >>> emissions_aus
    <Quantity(0.34, 'C * gigametric_ton / a')>

    >>> emissions_aus.to("Mt CO2 / yr")
    <Quantity(1246.666666666667, 'CO2 * megametric_ton / a')>

    >>> with unit_registry.context("AR4GWP100"):
    ...     (100 * unit_registry("Mt CH4 / yr")).to("Mt CO2 / yr")
    <Quantity(2500.0, 'CO2 * megametric_ton / a')>

**More details on emissions units**

Emissions are a flux composed of three parts: mass, the species being emitted and the
time period e.g. "t CO2 / yr". As mass and time are part of SI units, all we need to
define here are emissions units i.e. the stuff. Here we include as many of the canonical
emissions units, and their conversions, as possible.

For emissions units, there are a few cases to be considered:

- fairly obvious ones e.g. carbon dioxide emissions can be provided in 'C' or 'CO2' and
  converting between the two is possible
- less obvious ones e.g. nitrous oxide emissions can be provided in 'N', 'N2O' or
  'N2ON' (a short-hand which indicates that only the mass of the nitrogen is being counted),
  we provide conversions between these three
- case-sensitivity. In order to provide a simplified interface, using all uppercase
  versions of any unit is also valid e.g. ``unit_registry("HFC4310mee")`` is the same as
  ``unit_registry("HFC4310MEE")``
- hyphens and underscores in units. In order to be Pint compatible and to simplify
  things, we strip all hyphens and underscores from units.

As a convenience, we allow users to combine the mass and the type of emissions to make a
'joint unit' e.g. "tCO2". It should be recognised that this joint unit is a derived
unit and not a base unit.

By defining these three separate components, it is much easier to track what conversions
are valid and which are not. For example, as the emissions units are all defined as
emissions units, and not as atomic masses, we are able to prevent invalid conversions.
If emissions units were simply atomic masses, it would be possible to convert between
e.g. C and N2O which would be a problem. Conventions such as allowing carbon dioxide
emissions to be reported in C or CO2, despite the fact that they are fundamentally
different chemical species, is a convention which is particular to emissions (as far as
we can tell).

Pint's contexts are particularly useful for emissions as they facilitate
metric conversions. With a context, a conversion which wouldn't normally be allowed
(e.g. tCO2 --> tN2O) is allowed and will use whatever metric conversion is appropriate
for that context (e.g. AR4GWP100).

Finally, we discuss namespace collisions.

*CH4*

Methane emissions are defined as 'CH4'. In order to prevent inadvertent conversions of
'CH4' to e.g. 'CO2' via 'C', the conversion 'CH4' <--> 'C' is by default forbidden.
However, it can be performed within the context 'CH4_conversions' as shown below:

.. code:: python

    >>> from openscm_units import unit_registry
    >>> unit_registry("CH4").to("C")
    pint.errors.DimensionalityError: Cannot convert from 'CH4' ([methane]) to 'C' ([carbon])

    # with a context, the conversion becomes legal again
    >>> with unit_registry.context("CH4_conversions"):
    ...     unit_registry("CH4").to("C")
    <Quantity(0.75, 'C')>

    # as an unavoidable side effect, this also becomes possible
    >>> with unit_registry.context("CH4_conversions"):
    ...     unit_registry("CH4").to("CO2")
    <Quantity(2.75, 'CO2')>

*NOx*

Like for methane, NOx emissions also suffer from a namespace collision. In order to
prevent inadvertent conversions from 'NOx' to e.g. 'N2O', the conversion 'NOx' <-->
'N' is by default forbidden. It can be performed within the 'NOx_conversions' context:

.. code:: python

    >>> from openscm_units import unit_registry
    >>> unit_registry("NOx").to("N")
    pint.errors.DimensionalityError: Cannot convert from 'NOx' ([NOx]) to 'N' ([nitrogen])

    # with a context, the conversion becomes legal again
    >>> with unit_registry.context("NOx_conversions"):
    ...     unit_registry("NOx").to("N")
    <Quantity(0.30434782608695654, 'N')>

    # as an unavoidable side effect, this also becomes possible
    >>> with unit_registry.context("NOx_conversions"):
    ...     unit_registry("NOx").to("N2O")
    <Quantity(0.9565217391304348, 'N2O')>
"""
from os import path

import pandas as pd
import pint

# Standard gases. If the value is:
# - str: this entry defines a base gas unit
# - list: this entry defines a derived unit
#    - the first entry defines how to convert from base units
#    - other entries define other names i.e. aliases
_STANDARD_GASES = {
    # CO2, CH4, N2O
    "C": "carbon",
    "CO2": ["12/44 * C", "carbon_dioxide"],
    "CH4": "methane",
    "N": "nitrogen",
    "N2O": ["14/44 * N", "nitrous_oxide"],
    "N2ON": ["14/28 * N", "nitrous_oxide_farming_style"],
    "NO2": ["14/46 * N", "nitrogen_dioxide"],
    # aerosol precursors
    "NOx": "NOx",
    "nox": ["NOx"],
    "NH3": ["14/17 * N", "ammonia"],
    "S": "sulfur",
    "SO2": ["32/64 * S", "sulfur_dioxide"],
    "SOx": ["SO2"],
    "BC": "black_carbon",
    "OC": "OC",
    "CO": "carbon_monoxide",
    "VOC": "VOC",
    "NMVOC": ["VOC", "non_methane_volatile_organic_compounds"],
    # CFCs
    "CFC11": "CFC11",
    "CFC12": "CFC12",
    "CFC13": "CFC13",
    "CFC113": "CFC113",
    "CFC114": "CFC114",
    "CFC115": "CFC115",
    # HCFCs
    "HCFC21": "HCFC21",
    "HCFC22": "HCFC22",
    "HCFC123": "HCFC123",
    "HCFC124": "HCFC124",
    "HCFC141b": "HCFC141b",
    "HCFC142b": "HCFC142b",
    "HCFC225ca": "HCFC225ca",
    "HCFC225cb": "HCFC225cb",
    # HFCs
    "HFC23": "HFC23",
    "HFC32": "HFC32",
    "HFC41": "HFC41",
    "HFC125": "HFC125",
    "HFC134": "HFC134",
    "HFC134a": "HFC134a",
    "HFC143": "HFC143",
    "HFC143a": "HFC143a",
    "HFC152": "HFC152",
    "HFC152a": "HFC152a",
    "HFC161": "HFC161",
    "HFC227ea": "HFC227ea",
    "HFC236cb": "HFC236cb",
    "HFC236ea": "HFC236ea",
    "HFC236fa": "HFC236fa",
    "HFC245ca": "HFC245ca",
    "HFC245fa": "HFC245fa",
    "HFC365mfc": "HFC365mfc",
    "HFC4310mee": "HFC4310mee",
    "HFC4310": ["HFC4310mee"],
    # Halogenated gases
    "Halon1201": "Halon1201",
    "Halon1202": "Halon1202",
    "Halon1211": "Halon1211",
    "Halon1301": "Halon1301",
    "Halon2402": "Halon2402",
    # PFCs
    "CF4": "CF4",
    "C2F6": "C2F6",
    "cC3F6": "cC3F6",
    "C3F8": "C3F8",
    "cC4F8": "cC4F8",
    "C4F10": "C4F10",
    "C5F12": "C5F12",
    "C6F14": "C6F14",
    "C7F16": "C7F16",
    "C8F18": "C8F18",
    "C10F18": "C10F18",
    # Fluorinated ethers
    "HFE125": "HFE125",
    "HFE134": "HFE134",
    "HFE143a": "HFE143a",
    "HCFE235da2": "HCFE235da2",
    "HFE245cb2": "HFE245cb2",
    "HFE245fa2": "HFE245fa2",
    "HFE347mcc3": "HFE347mcc3",
    "HFE347pcf2": "HFE347pcf2",
    "HFE356pcc3": "HFE356pcc3",
    "HFE449sl": "HFE449sl",
    "HFE569sf2": "HFE569sf2",
    "HFE4310pccc124": "HFE4310pccc124",
    "HFE236ca12": "HFE236ca12",
    "HFE338pcc13": "HFE338pcc13",
    "HFE227ea": "HFE227ea",
    "HFE236ea2": "HFE236ea2",
    "HFE236fa": "HFE236fa",
    "HFE245fa1": "HFE245fa1",
    "HFE263fb2": "HFE263fb2",
    "HFE329mcc2": "HFE329mcc2",
    "HFE338mcf2": "HFE338mcf2",
    "HFE347mcf2": "HFE347mcf2",
    "HFE356mec3": "HFE356mec3",
    "HFE356pcf2": "HFE356pcf2",
    "HFE356pcf3": "HFE356pcf3",
    "HFE365mcf3": "HFE365mcf3",
    "HFE374pc2": "HFE374pc2",
    # Perfluoropolyethers
    "PFPMIE": "PFPMIE",
    # Misc
    "CCl4": "CCl4",
    "CHCl3": "CHCl3",
    "CH2Cl2": "CH2Cl2",
    "CH3CCl3": "CH3CCl3",
    "CH3Cl": "CH3Cl",
    "CH3Br": "CH3Br",
    "SF5CF3": "SF5CF3",
    "SF6": "SF6",
    "SO2F2": "SO2F2",
    "NF3": "NF3",
}


class ScmUnitRegistry(pint.UnitRegistry):
    """
    Unit registry class.

    Provides some convenience methods to add standard units and contexts with
    lazy loading from disk.
    """

    _contexts_loaded = False

    def add_standards(self):
        """
        Add standard units.

        Has to be done separately because of pint's weird initializing.
        """
        self._add_gases(_STANDARD_GASES)

        self.define("a = 1 * year = annum = yr")
        self.define("h = hour")
        self.define("d = day")
        self.define("degreeC = degC")
        self.define("degreeF = degF")
        self.define("kt = 1000 * t")  # since kt is used for "knot" in the defaults
        self.define(
            "Tt = 1000000000000 * t"
        )  # since Tt is used for "tex" in the defaults

        self.define("ppt = [concentrations]")
        self.define("ppb = 1000 * ppt")
        self.define("ppm = 1000 * ppb")

    def enable_contexts(self, *names_or_contexts, **kwargs):
        """
        Overload pint's :func:`enable_contexts` to load contexts once (the first time
        they are used) to avoid (unnecessary) file operations on import.
        """
        if not self._contexts_loaded:
            self._load_contexts()
        self._contexts_loaded = True
        super().enable_contexts(*names_or_contexts, **kwargs)

    def _add_mass_emissions_joint_version(self, symbol):
        """
        Add a unit which is the combination of mass and emissions.

        This allows users to units like e.g. ``"tC"`` rather than requiring a space
        between the mass and the emissions i.e. ``"t C"``

        Parameters
        ----------
        symbol
            The unit to add a joint version for
        """
        self.define("g{symbol} = g * {symbol}".format(symbol=symbol))
        self.define("t{symbol} = t * {symbol}".format(symbol=symbol))

    def _add_gases(self, gases):
        for symbol, value in gases.items():
            if isinstance(value, str):
                # symbol is base unit
                self.define("{} = [{}]".format(symbol, value))
                if value != symbol:
                    self.define("{} = {}".format(value, symbol))
            else:
                # symbol has conversion and aliases
                self.define("{} = {}".format(symbol, value[0]))
                for alias in value[1:]:
                    self.define("{} = {}".format(alias, symbol))

            self._add_mass_emissions_joint_version(symbol)

            # Add alias for upper case symbol:
            if symbol.upper() != symbol:
                self.define("{} = {}".format(symbol.upper(), symbol))
                self._add_mass_emissions_joint_version(symbol.upper())

    def _load_contexts(self):
        """
        Load contexts.
        """
        _ch4_context = pint.Context("CH4_conversions")
        _ch4_context = self._add_transformations_to_context(
            _ch4_context,
            "[methane]",
            self.CH4,
            "[carbon]",
            self.C,
            12 / 16,
        )
        self.add_context(_ch4_context)

        _n2o_context = pint.Context("NOx_conversions")
        _n2o_context = self._add_transformations_to_context(
            _n2o_context,
            "[nitrogen]",
            self.nitrogen,
            "[NOx]",
            self.NOx,
            (14 + 2 * 16) / 14,
        )
        self.add_context(_n2o_context)

        self._load_metric_conversions()

    def _load_metric_conversions(self):
        """
        Load metric conversion contexts from file.

        This is done only when contexts are needed to avoid reading files on import.
        """
        metric_conversions = pd.read_csv(
            path.join(
                path.dirname(path.abspath(__file__)),
                "data",
                "metric_conversions.csv",
            ),
            skiprows=1,  # skip source row
            header=0,
            index_col=0,
        ).iloc[
            1:, :
        ]  # drop out 'SCMData base unit' row

        other_unit_ureg = self.carbon

        for col in metric_conversions:
            transform_context = pint.Context(col)
            for label, val in metric_conversions[col].iteritems():
                conv_val = (
                    val
                    * (self("CO2").to_base_units()).magnitude
                    / (self(label).to_base_units()).magnitude
                )
                base_unit = [
                    s
                    for s, _ in self._get_dimensionality(
                        self(label)  # pylint: disable=protected-access
                        .to_base_units()
                        ._units
                    ).items()
                ][0]

                base_unit_ureg = getattr(
                    self, base_unit.replace("[", "").replace("]", "")
                )

                transform_context = self._add_transformations_to_context(
                    transform_context,
                    base_unit,
                    base_unit_ureg,
                    "[carbon]",
                    other_unit_ureg,
                    conv_val,
                )

            self.add_context(transform_context)

    @staticmethod
    def _add_transformations_to_context(
        context, base_unit, base_unit_ureg, other_unit, other_unit_ureg, conv_val
    ):
        """
        Add all the transformations between units to a context for the two
        given units

        Transformations are mass x unit per time, mass x unit etc.
        """

        def _get_transform_func(forward):
            if forward:

                def result_forward(_, strt):
                    return strt * other_unit_ureg / base_unit_ureg * conv_val

                return result_forward

            def result_backward(_, strt):
                return strt * (base_unit_ureg / other_unit_ureg) / conv_val

            return result_backward

        formatters = [
            "{}",
            "[mass] * {} / [time]",
            "[mass] * {}",
            "{} / [time]",
        ]
        for fmt_str in formatters:
            context.add_transformation(
                fmt_str.format(base_unit),
                fmt_str.format(other_unit),
                _get_transform_func(forward=True),
            )
            context.add_transformation(
                fmt_str.format(other_unit),
                fmt_str.format(base_unit),
                _get_transform_func(forward=False),
            )

        return context


unit_registry = ScmUnitRegistry()  # pylint:disable=invalid-name
"""
Standard unit registry

The unit registry contains all of the recognised units. Be careful, if you
edit this registry in one place then it will also be edited in any other
places that use ``openscm_units``. If you want multiple, separate registries,
create multiple instances of ``ScmUnitRegistry``.
"""
unit_registry.add_standards()
