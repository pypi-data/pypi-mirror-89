from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.ArgSingleSuppressed import ArgSingleSuppressed
from ......Internal.Types import DataType


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Bandwidth:
	"""Bandwidth commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("bandwidth", core, parent)

	def fetch(self) -> float:
		"""SCPI: FETCh:AFRF:MEASurement<Instance>:SROutines:RIFBandwidth:BANDwidth \n
		Snippet: value: float = driver.afRf.measurement.searchRoutines.rifBandwidth.bandwidth.fetch() \n
		Fetches the bandwidth as difference between higher frequency and lower frequency. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: bandwidth: Range: 1 Hz to 1 MHz, Unit: Hz"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'FETCh:AFRF:MEASurement<Instance>:SROutines:RIFBandwidth:BANDwidth?', suppressed)
		return Conversions.str_to_float(response)
