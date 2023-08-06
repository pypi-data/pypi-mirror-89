from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.ArgSingleSuppressed import ArgSingleSuppressed
from ....Internal.Types import DataType


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Talignment:
	"""Talignment commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("talignment", core, parent)

	def fetch(self) -> float:
		"""SCPI: FETCh:GPRF:MEASurement<Instance>:IQRecorder:TALignment \n
		Snippet: value: float = driver.gprfMeasurement.iqRecorder.talignment.fetch() \n
		No command help available \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: time_alignment: No help available"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'FETCh:GPRF:MEASurement<Instance>:IQRecorder:TALignment?', suppressed)
		return Conversions.str_to_float(response)

	def read(self) -> float:
		"""SCPI: READ:GPRF:MEASurement<Instance>:IQRecorder:TALignment \n
		Snippet: value: float = driver.gprfMeasurement.iqRecorder.talignment.read() \n
		No command help available \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: time_alignment: No help available"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'READ:GPRF:MEASurement<Instance>:IQRecorder:TALignment?', suppressed)
		return Conversions.str_to_float(response)
