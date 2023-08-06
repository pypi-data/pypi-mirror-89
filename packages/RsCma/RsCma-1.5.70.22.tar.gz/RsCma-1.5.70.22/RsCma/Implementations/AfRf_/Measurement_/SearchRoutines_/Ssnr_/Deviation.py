from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.ArgSingleSuppressed import ArgSingleSuppressed
from ......Internal.Types import DataType


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Deviation:
	"""Deviation commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("deviation", core, parent)

	def fetch(self) -> float:
		"""SCPI: FETCh:AFRF:MEASurement<Instance>:SROutines:SSNR:DEViation \n
		Snippet: value: float = driver.afRf.measurement.searchRoutines.ssnr.deviation.fetch() \n
		Fetches the SNR result value for switched SNR measurement. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: ssnr: Unit: dB"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'FETCh:AFRF:MEASurement<Instance>:SROutines:SSNR:DEViation?', suppressed)
		return Conversions.str_to_float(response)
