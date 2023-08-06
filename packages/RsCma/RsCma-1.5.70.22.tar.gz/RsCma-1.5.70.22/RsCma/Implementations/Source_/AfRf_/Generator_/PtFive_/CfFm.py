from typing import List

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CfFm:
	"""CfFm commands group definition. 5 total commands, 0 Sub-groups, 5 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("cfFm", core, parent)

	# noinspection PyTypeChecker
	def get_ilength(self) -> enums.ImpulseLength:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:PTFive:CFFM:ILENgth \n
		Snippet: value: enums.ImpulseLength = driver.source.afRf.generator.ptFive.cfFm.get_ilength() \n
		Queries the impulse length of the filter used for pulse shaping for P25 with C4FM modulation. \n
			:return: impulse_length: T2
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:PTFive:CFFM:ILENgth?')
		return Conversions.str_to_scalar_enum(response, enums.ImpulseLength)

	def get_symbol_rate(self) -> float:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:PTFive:CFFM:SRATe \n
		Snippet: value: float = driver.source.afRf.generator.ptFive.cfFm.get_symbol_rate() \n
		Queries the symbol rate for P25 with C4FM modulation. \n
			:return: srate: Range: 4800 symbol/s to 4800 symbol/s , Unit: symbol/s
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:PTFive:CFFM:SRATe?')
		return Conversions.str_to_float(response)

	# noinspection PyTypeChecker
	def get_filter_py(self) -> enums.PtFiveFilter:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:PTFive:CFFM:FILTer \n
		Snippet: value: enums.PtFiveFilter = driver.source.afRf.generator.ptFive.cfFm.get_filter_py() \n
		Queries the filter type used for pulse shaping for P25 with C4FM modulation. \n
			:return: filter_py: RRC
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:PTFive:CFFM:FILTer?')
		return Conversions.str_to_scalar_enum(response, enums.PtFiveFilter)

	def get_ro_factor(self) -> float:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:PTFive:CFFM:ROFactor \n
		Snippet: value: float = driver.source.afRf.generator.ptFive.cfFm.get_ro_factor() \n
		Queries the roll-off factor of the filter used for pulse shaping for P25 with C4FM modulation. \n
			:return: ro_factor: Range: 0.2 to 0.2
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:PTFive:CFFM:ROFactor?')
		return Conversions.str_to_float(response)

	def get_standard_dev(self) -> List[float]:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:PTFive:CFFM:SDEViation \n
		Snippet: value: List[float] = driver.source.afRf.generator.ptFive.cfFm.get_standard_dev() \n
		Queries the deviations used for C4FM modulation, for P25. \n
			:return: sdeviation: List of four deviations, for the symbols 01, 00, 10, 11. Range: -2000 Hz to 2000 Hz, Unit: Hz
		"""
		response = self._core.io.query_bin_or_ascii_float_list('SOURce:AFRF:GENerator<Instance>:PTFive:CFFM:SDEViation?')
		return response
