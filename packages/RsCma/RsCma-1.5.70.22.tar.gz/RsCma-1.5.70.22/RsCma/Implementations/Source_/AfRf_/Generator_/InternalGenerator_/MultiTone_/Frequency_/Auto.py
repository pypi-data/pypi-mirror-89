from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.StructBase import StructBase
from ........Internal.ArgStruct import ArgStruct
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Auto:
	"""Auto commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("auto", core, parent)

	# noinspection PyTypeChecker
	class AutoStruct(StructBase):
		"""Structure for setting input parameters. Fields: \n
			- Start_Freq: float: Frequency for tone 1 in the multitone list Range: 20 Hz to 20 kHz, Unit: Hz
			- Freq_Increment: float: Frequency increment for subsequent tones in the list Range: 1 Hz to 20 kHz, Unit: Hz"""
		__meta_args_list = [
			ArgStruct.scalar_float('Start_Freq'),
			ArgStruct.scalar_float('Freq_Increment')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Start_Freq: float = None
			self.Freq_Increment: float = None

	def set(self, structure: AutoStruct, internalGen=repcap.InternalGen.Default) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:IGENerator<nr>:MTONe:FREQuency:AUTO \n
		Snippet: driver.source.afRf.generator.internalGenerator.multiTone.frequency.auto.set(value = [PROPERTY_STRUCT_NAME](), internalGen = repcap.InternalGen.Default) \n
		Configures increasing equidistant frequencies for multitone generation. \n
			:param structure: for set value, see the help for AutoStruct structure arguments.
			:param internalGen: optional repeated capability selector. Default value: Nr1 (settable in the interface 'InternalGenerator')"""
		internalGen_cmd_val = self._base.get_repcap_cmd_value(internalGen, repcap.InternalGen)
		self._core.io.write_struct(f'SOURce:AFRF:GENerator<Instance>:IGENerator{internalGen_cmd_val}:MTONe:FREQuency:AUTO', structure)

	def get(self, internalGen=repcap.InternalGen.Default) -> AutoStruct:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:IGENerator<nr>:MTONe:FREQuency:AUTO \n
		Snippet: value: AutoStruct = driver.source.afRf.generator.internalGenerator.multiTone.frequency.auto.get(internalGen = repcap.InternalGen.Default) \n
		Configures increasing equidistant frequencies for multitone generation. \n
			:param internalGen: optional repeated capability selector. Default value: Nr1 (settable in the interface 'InternalGenerator')
			:return: structure: for return value, see the help for AutoStruct structure arguments."""
		internalGen_cmd_val = self._base.get_repcap_cmd_value(internalGen, repcap.InternalGen)
		return self._core.io.query_struct(f'SOURce:AFRF:GENerator<Instance>:IGENerator{internalGen_cmd_val}:MTONe:FREQuency:AUTO?', self.__class__.AutoStruct())
