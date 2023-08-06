from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dialing:
	"""Dialing commands group definition. 3 total commands, 1 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dialing", core, parent)

	@property
	def mode(self):
		"""mode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mode'):
			from .Dialing_.Mode import Mode
			self._mode = Mode(self._core, self._base)
		return self._mode

	def start(self, internalGen=repcap.InternalGen.Default) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:IGENerator<nr>:DIALing:STARt \n
		Snippet: driver.source.afRf.generator.internalGenerator.dialing.start(internalGen = repcap.InternalGen.Default) \n
		No command help available \n
			:param internalGen: optional repeated capability selector. Default value: Nr1 (settable in the interface 'InternalGenerator')"""
		internalGen_cmd_val = self._base.get_repcap_cmd_value(internalGen, repcap.InternalGen)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:IGENerator{internalGen_cmd_val}:DIALing:STARt')

	def start_with_opc(self, internalGen=repcap.InternalGen.Default) -> None:
		internalGen_cmd_val = self._base.get_repcap_cmd_value(internalGen, repcap.InternalGen)
		"""SCPI: SOURce:AFRF:GENerator<Instance>:IGENerator<nr>:DIALing:STARt \n
		Snippet: driver.source.afRf.generator.internalGenerator.dialing.start_with_opc(internalGen = repcap.InternalGen.Default) \n
		No command help available \n
		Same as start, but waits for the operation to complete before continuing further. Use the RsCma.utilities.opc_timeout_set() to set the timeout value. \n
			:param internalGen: optional repeated capability selector. Default value: Nr1 (settable in the interface 'InternalGenerator')"""
		self._core.io.write_with_opc(f'SOURce:AFRF:GENerator<Instance>:IGENerator{internalGen_cmd_val}:DIALing:STARt')

	def set(self, dialing_state: bool, internalGen=repcap.InternalGen.Default) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:IGENerator<nr>:DIALing \n
		Snippet: driver.source.afRf.generator.internalGenerator.dialing.set(dialing_state = False, internalGen = repcap.InternalGen.Default) \n
		Starts or stops dialing a digit sequence. This command is relevant for dialing modes like SELCAL, DTMF, SelCall or free
		dialing. For dialing measurements, ensure a delay between starting the measurement and dialing the sequence via this
		command. Otherwise, the measurement misses the first tones and fails. Required delays depending on the input path: for AF
		/ SPDIF path 400 ms, for RF path 800 ms. \n
			:param dialing_state: OFF | ON
			:param internalGen: optional repeated capability selector. Default value: Nr1 (settable in the interface 'InternalGenerator')"""
		param = Conversions.bool_to_str(dialing_state)
		internalGen_cmd_val = self._base.get_repcap_cmd_value(internalGen, repcap.InternalGen)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:IGENerator{internalGen_cmd_val}:DIALing {param}')

	def get(self, internalGen=repcap.InternalGen.Default) -> bool:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:IGENerator<nr>:DIALing \n
		Snippet: value: bool = driver.source.afRf.generator.internalGenerator.dialing.get(internalGen = repcap.InternalGen.Default) \n
		Starts or stops dialing a digit sequence. This command is relevant for dialing modes like SELCAL, DTMF, SelCall or free
		dialing. For dialing measurements, ensure a delay between starting the measurement and dialing the sequence via this
		command. Otherwise, the measurement misses the first tones and fails. Required delays depending on the input path: for AF
		/ SPDIF path 400 ms, for RF path 800 ms. \n
			:param internalGen: optional repeated capability selector. Default value: Nr1 (settable in the interface 'InternalGenerator')
			:return: dialing_state: OFF | ON"""
		internalGen_cmd_val = self._base.get_repcap_cmd_value(internalGen, repcap.InternalGen)
		response = self._core.io.query_str(f'SOURce:AFRF:GENerator<Instance>:IGENerator{internalGen_cmd_val}:DIALing?')
		return Conversions.str_to_bool(response)

	def clone(self) -> 'Dialing':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Dialing(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
