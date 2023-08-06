from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........Internal.ArgSingleSuppressed import ArgSingleSuppressed
from ........Internal.Types import DataType


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Average:
	"""Average commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("average", core, parent)

	def fetch(self) -> float:
		"""SCPI: FETCh:AFRF:MEASurement<Instance>:MEValuation:TONes:DCS:FSKDeviation:AVERage \n
		Snippet: value: float = driver.afRf.measurement.multiEval.tones.dcs.fskDeviation.average.fetch() \n
		Queries the FSK deviation measured for a DCS signal. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: fsk_deviation: Unit: Hz"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'FETCh:AFRF:MEASurement<Instance>:MEValuation:TONes:DCS:FSKDeviation:AVERage?', suppressed)
		return Conversions.str_to_float(response)

	def read(self) -> float:
		"""SCPI: READ:AFRF:MEASurement<Instance>:MEValuation:TONes:DCS:FSKDeviation:AVERage \n
		Snippet: value: float = driver.afRf.measurement.multiEval.tones.dcs.fskDeviation.average.read() \n
		Queries the FSK deviation measured for a DCS signal. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: fsk_deviation: Unit: Hz"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'READ:AFRF:MEASurement<Instance>:MEValuation:TONes:DCS:FSKDeviation:AVERage?', suppressed)
		return Conversions.str_to_float(response)
