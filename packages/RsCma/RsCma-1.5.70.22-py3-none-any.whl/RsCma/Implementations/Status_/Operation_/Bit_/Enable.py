from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Enable:
	"""Enable commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("enable", core, parent)

	def set(self, register_bit: float, bit=repcap.Bit.Default) -> None:
		"""SCPI: STATus:OPERation:BIT<bitno>:ENABle \n
		Snippet: driver.status.operation.bit.enable.set(register_bit = 1.0, bit = repcap.Bit.Default) \n
		No command help available \n
			:param register_bit: No help available
			:param bit: optional repeated capability selector. Default value: Nr8 (settable in the interface 'Bit')"""
		param = Conversions.decimal_value_to_str(register_bit)
		bit_cmd_val = self._base.get_repcap_cmd_value(bit, repcap.Bit)
		self._core.io.write(f'STATus:OPERation:BIT{bit_cmd_val}:ENABle {param}')

	def get(self, bit=repcap.Bit.Default) -> float:
		"""SCPI: STATus:OPERation:BIT<bitno>:ENABle \n
		Snippet: value: float = driver.status.operation.bit.enable.get(bit = repcap.Bit.Default) \n
		No command help available \n
			:param bit: optional repeated capability selector. Default value: Nr8 (settable in the interface 'Bit')
			:return: register_bit: No help available"""
		bit_cmd_val = self._base.get_repcap_cmd_value(bit, repcap.Bit)
		response = self._core.io.query_str(f'STATus:OPERation:BIT{bit_cmd_val}:ENABle?')
		return Conversions.str_to_float(response)
