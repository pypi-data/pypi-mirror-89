from typing import List

from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.ArgSingleSuppressed import ArgSingleSuppressed
from .......Internal.Types import DataType


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Trace:
	"""Trace commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("trace", core, parent)

	def fetch(self) -> List[float]:
		"""SCPI: FETCh:AFRF:MEASurement<Instance>:SROutines:RSQuelch:SQUality:TRACe \n
		Snippet: value: List[float] = driver.afRf.measurement.searchRoutines.rsquelch.signalQuality.trace.fetch() \n
		Fetches the list of signal quality values for the squelch measurement. These are the y-values for the points in the RX
		squelch diagram. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: sig_qual_list: Unit: dB"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:AFRF:MEASurement<Instance>:SROutines:RSQuelch:SQUality:TRACe?', suppressed)
		return response
