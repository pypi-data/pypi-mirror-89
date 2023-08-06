from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.ArgSingleSuppressed import ArgSingleSuppressed
from ......Internal.Types import DataType


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Tlevel:
	"""Tlevel commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("tlevel", core, parent)

	def fetch(self) -> float:
		"""SCPI: FETCh:AFRF:MEASurement<Instance>:SROutines:RSQuelch:TLEVel \n
		Snippet: value: float = driver.afRf.measurement.searchRoutines.rsquelch.tlevel.fetch() \n
		Fetches the RF level at which the DUT opens the squelch for the case that the DUT has a a squelch control and has
		adjusted it to the maximum squelch switch-off level. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: tight_level: Range: -158 dBm to 16 dBm, Unit: dBm"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'FETCh:AFRF:MEASurement<Instance>:SROutines:RSQuelch:TLEVel?', suppressed)
		return Conversions.str_to_float(response)
