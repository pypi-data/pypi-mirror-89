from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........Internal.ArgSingleSuppressed import ArgSingleSuppressed
from ........Internal.Types import DataType
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Average:
	"""Average commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("average", core, parent)

	def fetch(self, audioInput=repcap.AudioInput.Default) -> float:
		"""SCPI: FETCh:AFRF:MEASurement<Instance>:MEValuation:AIN<nr>:FREQuency:DELTa:AVERage \n
		Snippet: value: float = driver.afRf.measurement.multiEval.audioInput.frequency.delta.average.fetch(audioInput = repcap.AudioInput.Default) \n
		No command help available \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:param audioInput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioInput')
			:return: frequency: Unit: Hz"""
		audioInput_cmd_val = self._base.get_repcap_cmd_value(audioInput, repcap.AudioInput)
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'FETCh:AFRF:MEASurement<Instance>:MEValuation:AIN{audioInput_cmd_val}:FREQuency:DELTa:AVERage?', suppressed)
		return Conversions.str_to_float(response)

	def read(self, audioInput=repcap.AudioInput.Default) -> float:
		"""SCPI: READ:AFRF:MEASurement<Instance>:MEValuation:AIN<nr>:FREQuency:DELTa:AVERage \n
		Snippet: value: float = driver.afRf.measurement.multiEval.audioInput.frequency.delta.average.read(audioInput = repcap.AudioInput.Default) \n
		No command help available \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:param audioInput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioInput')
			:return: frequency: Unit: Hz"""
		audioInput_cmd_val = self._base.get_repcap_cmd_value(audioInput, repcap.AudioInput)
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'READ:AFRF:MEASurement<Instance>:MEValuation:AIN{audioInput_cmd_val}:FREQuency:DELTa:AVERage?', suppressed)
		return Conversions.str_to_float(response)
