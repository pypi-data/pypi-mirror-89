from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Utilities import trim_str_response
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Zigbee:
	"""Zigbee commands group definition. 9 total commands, 0 Sub-groups, 9 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("zigbee", core, parent)

	def get_snumber(self) -> str:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:ZIGBee:SNUMber \n
		Snippet: value: str = driver.source.afRf.generator.zigbee.get_snumber() \n
		No command help available \n
			:return: snum: Range: 0 to 255
		"""
		response = self._core.io.query_str_with_opc('SOURce:AFRF:GENerator<Instance>:ZIGBee:SNUMber?')
		return trim_str_response(response)

	def set_snumber(self, snum: str) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:ZIGBee:SNUMber \n
		Snippet: driver.source.afRf.generator.zigbee.set_snumber(snum = r1) \n
		No command help available \n
			:param snum: Range: 0 to 255
		"""
		param = Conversions.value_to_str(snum)
		self._core.io.write_with_opc(f'SOURce:AFRF:GENerator<Instance>:ZIGBee:SNUMber {param}')

	def get_dpan(self) -> str:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:ZIGBee:DPAN \n
		Snippet: value: str = driver.source.afRf.generator.zigbee.get_dpan() \n
		No command help available \n
			:return: dpan: Range: 0 to 65.535E+3
		"""
		response = self._core.io.query_str_with_opc('SOURce:AFRF:GENerator<Instance>:ZIGBee:DPAN?')
		return trim_str_response(response)

	def set_dpan(self, dpan: str) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:ZIGBee:DPAN \n
		Snippet: driver.source.afRf.generator.zigbee.set_dpan(dpan = r1) \n
		No command help available \n
			:param dpan: Range: 0 to 65.535E+3
		"""
		param = Conversions.value_to_str(dpan)
		self._core.io.write_with_opc(f'SOURce:AFRF:GENerator<Instance>:ZIGBee:DPAN {param}')

	def get_daddress(self) -> str:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:ZIGBee:DADDress \n
		Snippet: value: str = driver.source.afRf.generator.zigbee.get_daddress() \n
		Configures the destination address, i.e. the DUT's address, to be signaled to the DUT, for ZigBee. \n
			:return: daddr: decimal Range: 0 to 65.535E+3
		"""
		response = self._core.io.query_str_with_opc('SOURce:AFRF:GENerator<Instance>:ZIGBee:DADDress?')
		return trim_str_response(response)

	def set_daddress(self, daddr: str) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:ZIGBee:DADDress \n
		Snippet: driver.source.afRf.generator.zigbee.set_daddress(daddr = r1) \n
		Configures the destination address, i.e. the DUT's address, to be signaled to the DUT, for ZigBee. \n
			:param daddr: decimal Range: 0 to 65.535E+3
		"""
		param = Conversions.value_to_str(daddr)
		self._core.io.write_with_opc(f'SOURce:AFRF:GENerator<Instance>:ZIGBee:DADDress {param}')

	def get_span(self) -> str:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:ZIGBee:SPAN \n
		Snippet: value: str = driver.source.afRf.generator.zigbee.get_span() \n
		No command help available \n
			:return: span: Range: 0 to 65.535E+3
		"""
		response = self._core.io.query_str_with_opc('SOURce:AFRF:GENerator<Instance>:ZIGBee:SPAN?')
		return trim_str_response(response)

	def set_span(self, span: str) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:ZIGBee:SPAN \n
		Snippet: driver.source.afRf.generator.zigbee.set_span(span = r1) \n
		No command help available \n
			:param span: Range: 0 to 65.535E+3
		"""
		param = Conversions.value_to_str(span)
		self._core.io.write_with_opc(f'SOURce:AFRF:GENerator<Instance>:ZIGBee:SPAN {param}')

	def get_saddress(self) -> str:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:ZIGBee:SADDress \n
		Snippet: value: str = driver.source.afRf.generator.zigbee.get_saddress() \n
		No command help available \n
			:return: saddress: Range: 0 to 65.535E+3
		"""
		response = self._core.io.query_str_with_opc('SOURce:AFRF:GENerator<Instance>:ZIGBee:SADDress?')
		return trim_str_response(response)

	def set_saddress(self, saddress: str) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:ZIGBee:SADDress \n
		Snippet: driver.source.afRf.generator.zigbee.set_saddress(saddress = r1) \n
		No command help available \n
			:param saddress: Range: 0 to 65.535E+3
		"""
		param = Conversions.value_to_str(saddress)
		self._core.io.write_with_opc(f'SOURce:AFRF:GENerator<Instance>:ZIGBee:SADDress {param}')

	def get_payload(self) -> str:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:ZIGBee:PAYLoad \n
		Snippet: value: str = driver.source.afRf.generator.zigbee.get_payload() \n
		No command help available \n
			:return: pay_load: No help available
		"""
		response = self._core.io.query_str_with_opc('SOURce:AFRF:GENerator<Instance>:ZIGBee:PAYLoad?')
		return trim_str_response(response)

	def set_payload(self, pay_load: str) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:ZIGBee:PAYLoad \n
		Snippet: driver.source.afRf.generator.zigbee.set_payload(pay_load = '1') \n
		No command help available \n
			:param pay_load: No help available
		"""
		param = Conversions.value_to_quoted_str(pay_load)
		self._core.io.write_with_opc(f'SOURce:AFRF:GENerator<Instance>:ZIGBee:PAYLoad {param}')

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.ZigBeeMode:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:ZIGBee:MODE \n
		Snippet: value: enums.ZigBeeMode = driver.source.afRf.generator.zigbee.get_mode() \n
		No command help available \n
			:return: mode: OQPSk
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:ZIGBee:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.ZigBeeMode)

	def get_standard_dev(self) -> List[float]:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:ZIGBee:SDEViation \n
		Snippet: value: List[float] = driver.source.afRf.generator.zigbee.get_standard_dev() \n
		No command help available \n
			:return: sdeviation: Range: -180 deg to 180 deg, Unit: deg
		"""
		response = self._core.io.query_bin_or_ascii_float_list('SOURce:AFRF:GENerator<Instance>:ZIGBee:SDEViation?')
		return response

	def get_symbol_rate(self) -> float:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:ZIGBee:SRATe \n
		Snippet: value: float = driver.source.afRf.generator.zigbee.get_symbol_rate() \n
		No command help available \n
			:return: srate: Range: 0 symbol/s to 1E+6 symbol/s, Unit: bit/s
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:ZIGBee:SRATe?')
		return Conversions.str_to_float(response)
