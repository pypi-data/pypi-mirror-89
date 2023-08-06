from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Frequency:
	"""Frequency commands group definition. 2 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("frequency", core, parent)

	@property
	def trace(self):
		"""trace commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_trace'):
			from .Frequency_.Trace import Trace
			self._trace = Trace(self._core, self._base)
		return self._trace

	# noinspection PyTypeChecker
	class FetchStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: No parameter help available
			- Lower_Freq: float: Range: 100 kHz to 3 GHz, Unit: Hz
			- Higher_Freq: float: Range: 100 kHz to 3 GHz, Unit: Hz"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float('Lower_Freq'),
			ArgStruct.scalar_float('Higher_Freq')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Lower_Freq: float = None
			self.Higher_Freq: float = None

	def fetch(self) -> FetchStruct:
		"""SCPI: FETCh:AFRF:MEASurement<Instance>:SROutines:RIFBandwidth:FREQuency \n
		Snippet: value: FetchStruct = driver.afRf.measurement.searchRoutines.rifBandwidth.frequency.fetch() \n
		Fetches the lower and higher RF frequencies left and right from the nominal frequency at which the noise has increased to
		the noise target value (noise level method) or the SINAD audio signal quality has dropped down to the target value
		(TIA-603-D method) . \n
			:return: structure: for return value, see the help for FetchStruct structure arguments."""
		return self._core.io.query_struct(f'FETCh:AFRF:MEASurement<Instance>:SROutines:RIFBandwidth:FREQuency?', self.__class__.FetchStruct())

	def clone(self) -> 'Frequency':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Frequency(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
