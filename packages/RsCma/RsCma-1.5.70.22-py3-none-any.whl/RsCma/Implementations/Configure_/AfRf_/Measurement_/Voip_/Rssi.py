from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Rssi:
	"""Rssi commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rssi", core, parent)

	def get_code(self) -> int:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:VOIP:RSSI:CODE \n
		Snippet: value: int = driver.configure.afRf.measurement.voip.rssi.get_code() \n
		No command help available \n
			:return: code: No help available
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:VOIP:RSSI:CODE?')
		return Conversions.str_to_int(response)
