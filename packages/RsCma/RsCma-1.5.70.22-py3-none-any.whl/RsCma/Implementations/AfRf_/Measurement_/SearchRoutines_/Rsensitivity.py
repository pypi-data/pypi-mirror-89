from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Rsensitivity:
	"""Rsensitivity commands group definition. 6 total commands, 3 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rsensitivity", core, parent)

	@property
	def rfLevel(self):
		"""rfLevel commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_rfLevel'):
			from .Rsensitivity_.RfLevel import RfLevel
			self._rfLevel = RfLevel(self._core, self._base)
		return self._rfLevel

	@property
	def signalQuality(self):
		"""signalQuality commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_signalQuality'):
			from .Rsensitivity_.SignalQuality import SignalQuality
			self._signalQuality = SignalQuality(self._core, self._base)
		return self._signalQuality

	@property
	def sensitivity(self):
		"""sensitivity commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_sensitivity'):
			from .Rsensitivity_.Sensitivity import Sensitivity
			self._sensitivity = Sensitivity(self._core, self._base)
		return self._sensitivity

	# noinspection PyTypeChecker
	class FetchStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: See 'Reliability indicator values'
			- Sensitivity_Level: float: Measured RX sensitivity level (RF level) Unit: dBm
			- Signal_Quality: float: Audio signal quality value measured at the RX sensitivity level Unit: dB"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float('Sensitivity_Level'),
			ArgStruct.scalar_float('Signal_Quality')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Sensitivity_Level: float = None
			self.Signal_Quality: float = None

	def fetch(self) -> FetchStruct:
		"""SCPI: FETCh:AFRF:MEASurement<Instance>:SROutines:RSENsitivity \n
		Snippet: value: FetchStruct = driver.afRf.measurement.searchRoutines.rsensitivity.fetch() \n
		Returns the single results of the RX sensitivity search routine. CALCulate commands return error indicators instead of
		measurement values. \n
			:return: structure: for return value, see the help for FetchStruct structure arguments."""
		return self._core.io.query_struct(f'FETCh:AFRF:MEASurement<Instance>:SROutines:RSENsitivity?', self.__class__.FetchStruct())

	# noinspection PyTypeChecker
	class CalculateStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: See 'Reliability indicator values'
			- Sensitivity_Level: enums.ResultStatus: Measured RX sensitivity level (RF level) Unit: dBm
			- Signal_Quality: enums.ResultStatus: Audio signal quality value measured at the RX sensitivity level Unit: dB"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_enum('Sensitivity_Level', enums.ResultStatus),
			ArgStruct.scalar_enum('Signal_Quality', enums.ResultStatus)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Sensitivity_Level: enums.ResultStatus = None
			self.Signal_Quality: enums.ResultStatus = None

	def calculate(self) -> CalculateStruct:
		"""SCPI: CALCulate:AFRF:MEASurement<Instance>:SROutines:RSENsitivity \n
		Snippet: value: CalculateStruct = driver.afRf.measurement.searchRoutines.rsensitivity.calculate() \n
		Returns the single results of the RX sensitivity search routine. CALCulate commands return error indicators instead of
		measurement values. \n
			:return: structure: for return value, see the help for CalculateStruct structure arguments."""
		return self._core.io.query_struct(f'CALCulate:AFRF:MEASurement<Instance>:SROutines:RSENsitivity?', self.__class__.CalculateStruct())

	def clone(self) -> 'Rsensitivity':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Rsensitivity(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
