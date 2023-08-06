from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Event:
	"""Event commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("event", core, parent)

	def get(self, bit=repcap.Bit.Default) -> bool:
		"""SCPI: STATus:QUEStionable:BIT<bitno>[:EVENt] \n
		Snippet: value: bool = driver.status.questionable.bit.event.get(bit = repcap.Bit.Default) \n
		No command help available \n
			:param bit: optional repeated capability selector. Default value: Nr8 (settable in the interface 'Bit')
			:return: register_bit: No help available"""
		bit_cmd_val = self._base.get_repcap_cmd_value(bit, repcap.Bit)
		response = self._core.io.query_str(f'STATus:QUEStionable:BIT{bit_cmd_val}:EVENt?')
		return Conversions.str_to_bool(response)
