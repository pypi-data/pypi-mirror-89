from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Slevel:
	"""Slevel commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("slevel", core, parent)

	# noinspection PyTypeChecker
	class FetchStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: No parameter help available
			- Lower_Signal_Level: float: Range: -150 dBm to 150 dBm, Unit: dBm
			- Higher_Signal_Level: float: Range: -150 dBm to 150 dBm, Unit: dBm"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float('Lower_Signal_Level'),
			ArgStruct.scalar_float('Higher_Signal_Level')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Lower_Signal_Level: float = None
			self.Higher_Signal_Level: float = None

	def fetch(self) -> FetchStruct:
		"""SCPI: FETCh:AFRF:MEASurement<Instance>:SROutines:RIFBandwidth:SLEVel \n
		Snippet: value: FetchStruct = driver.afRf.measurement.searchRoutines.rifBandwidth.slevel.fetch() \n
		Fetches the signal quality / noise level at the lower and higher frequency. \n
			:return: structure: for return value, see the help for FetchStruct structure arguments."""
		return self._core.io.query_struct(f'FETCh:AFRF:MEASurement<Instance>:SROutines:RIFBandwidth:SLEVel?', self.__class__.FetchStruct())
