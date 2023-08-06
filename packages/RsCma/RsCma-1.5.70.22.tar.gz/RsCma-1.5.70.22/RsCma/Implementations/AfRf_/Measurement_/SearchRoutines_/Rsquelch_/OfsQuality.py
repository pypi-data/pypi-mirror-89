from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.ArgSingleSuppressed import ArgSingleSuppressed
from ......Internal.Types import DataType


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class OfsQuality:
	"""OfsQuality commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ofsQuality", core, parent)

	def fetch(self) -> float:
		"""SCPI: FETCh:AFRF:MEASurement<Instance>:SROutines:RSQuelch:OFSQuality \n
		Snippet: value: float = driver.afRf.measurement.searchRoutines.rsquelch.ofsQuality.fetch() \n
		Fetches the signal quality at the squelch off level. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: off_sig_quality: Range: -150 dB to 150 dB, Unit: dB"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'FETCh:AFRF:MEASurement<Instance>:SROutines:RSQuelch:OFSQuality?', suppressed)
		return Conversions.str_to_float(response)
