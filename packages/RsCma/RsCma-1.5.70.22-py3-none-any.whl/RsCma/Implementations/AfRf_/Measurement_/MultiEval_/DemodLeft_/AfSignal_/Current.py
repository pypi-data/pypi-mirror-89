from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.ArgSingleSuppressed import ArgSingleSuppressed
from .......Internal.Types import DataType


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Current:
	"""Current commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("current", core, parent)

	def fetch(self) -> float:
		"""SCPI: FETCh:AFRF:MEASurement<Instance>:MEValuation:DEMLeft:AFSignal:CURRent \n
		Snippet: value: float = driver.afRf.measurement.multiEval.demodLeft.afSignal.current.fetch() \n
		Queries the AF frequency results for the left demodulator channel. For FM stereo, these results are related to the left
		audio channel. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: frequency: Frequency of the AF signal Unit: Hz"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'FETCh:AFRF:MEASurement<Instance>:MEValuation:DEMLeft:AFSignal:CURRent?', suppressed)
		return Conversions.str_to_float(response)

	def read(self) -> float:
		"""SCPI: READ:AFRF:MEASurement<Instance>:MEValuation:DEMLeft:AFSignal:CURRent \n
		Snippet: value: float = driver.afRf.measurement.multiEval.demodLeft.afSignal.current.read() \n
		Queries the AF frequency results for the left demodulator channel. For FM stereo, these results are related to the left
		audio channel. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: frequency: Frequency of the AF signal Unit: Hz"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'READ:AFRF:MEASurement<Instance>:MEValuation:DEMLeft:AFSignal:CURRent?', suppressed)
		return Conversions.str_to_float(response)
