from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ptt:
	"""Ptt commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ptt", core, parent)

	def get_state(self) -> bool:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:VOIP:PTT:STATe \n
		Snippet: value: bool = driver.source.afRf.generator.voip.ptt.get_state() \n
		Sets the DUT's PTT state. Disable PTT at the DUT side, if you are finished with the TX testing. \n
			:return: ptt_state: OFF | ON
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:VOIP:PTT:STATe?')
		return Conversions.str_to_bool(response)
