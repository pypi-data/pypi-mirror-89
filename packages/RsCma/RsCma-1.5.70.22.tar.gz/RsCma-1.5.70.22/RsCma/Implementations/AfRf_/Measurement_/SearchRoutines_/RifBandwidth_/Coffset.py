from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.ArgSingleSuppressed import ArgSingleSuppressed
from ......Internal.Types import DataType


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Coffset:
	"""Coffset commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("coffset", core, parent)

	def fetch(self) -> float:
		"""SCPI: FETCh:AFRF:MEASurement<Instance>:SROutines:RIFBandwidth:COFFset \n
		Snippet: value: float = driver.afRf.measurement.searchRoutines.rifBandwidth.coffset.fetch() \n
		Fetches the center frequency offset. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: center_offset: Range: -100 kHz to 100 kHz, Unit: Hz"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'FETCh:AFRF:MEASurement<Instance>:SROutines:RIFBandwidth:COFFset?', suppressed)
		return Conversions.str_to_float(response)
