from typing import List

from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.ArgSingleSuppressed import ArgSingleSuppressed
from ........Internal.Types import DataType


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Current:
	"""Current commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("current", core, parent)

	def fetch(self) -> List[float]:
		"""SCPI: FETCh:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:DEMLeft:FDEViation:CURRent \n
		Snippet: value: List[float] = driver.afRf.measurement.multiEval.oscilloscope.demodLeft.fdeviation.current.fetch() \n
		Queries the contents of the AF oscilloscope diagram for the left demodulator channel and FM demodulation or FM stereo
		demodulation. For FM stereo, the results are related to the left audio channel. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: dvt_time: Comma-separated list of 960 frequency deviation or audio deviation values (diagram from left to right) Unit: Hz"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:DEMLeft:FDEViation:CURRent?', suppressed)
		return response

	def read(self) -> List[float]:
		"""SCPI: READ:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:DEMLeft:FDEViation:CURRent \n
		Snippet: value: List[float] = driver.afRf.measurement.multiEval.oscilloscope.demodLeft.fdeviation.current.read() \n
		Queries the contents of the AF oscilloscope diagram for the left demodulator channel and FM demodulation or FM stereo
		demodulation. For FM stereo, the results are related to the left audio channel. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: dvt_time: Comma-separated list of 960 frequency deviation or audio deviation values (diagram from left to right) Unit: Hz"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'READ:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:DEMLeft:FDEViation:CURRent?', suppressed)
		return response
