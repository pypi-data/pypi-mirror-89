from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FilterPy:
	"""FilterPy commands group definition. 11 total commands, 2 Sub-groups, 6 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("filterPy", core, parent)

	@property
	def bpass(self):
		"""bpass commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_bpass'):
			from .FilterPy_.Bpass import Bpass
			self._bpass = Bpass(self._core, self._base)
		return self._bpass

	@property
	def notch(self):
		"""notch commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_notch'):
			from .FilterPy_.Notch import Notch
			self._notch = Notch(self._core, self._base)
		return self._notch

	# noinspection PyTypeChecker
	def get_lpass(self) -> enums.LowpassFilterExtended:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:VOIP:FILTer:LPASs \n
		Snippet: value: enums.LowpassFilterExtended = driver.configure.afRf.measurement.voip.filterPy.get_lpass() \n
		Configures the lowpass filter in the VoIP input path. \n
			:return: filter_py: OFF | F255 | F3K | F3K4 | F4K | F15K OFF Filter disabled F255, F3K, F3K4, F4K, F15K Cutoff frequency 255 Hz / 3 kHz / 3.4 kHz / 4 kHz / 15 kHz
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:VOIP:FILTer:LPASs?')
		return Conversions.str_to_scalar_enum(response, enums.LowpassFilterExtended)

	def set_lpass(self, filter_py: enums.LowpassFilterExtended) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:VOIP:FILTer:LPASs \n
		Snippet: driver.configure.afRf.measurement.voip.filterPy.set_lpass(filter_py = enums.LowpassFilterExtended.F15K) \n
		Configures the lowpass filter in the VoIP input path. \n
			:param filter_py: OFF | F255 | F3K | F3K4 | F4K | F15K OFF Filter disabled F255, F3K, F3K4, F4K, F15K Cutoff frequency 255 Hz / 3 kHz / 3.4 kHz / 4 kHz / 15 kHz
		"""
		param = Conversions.enum_scalar_to_str(filter_py, enums.LowpassFilterExtended)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:VOIP:FILTer:LPASs {param}')

	# noinspection PyTypeChecker
	def get_hpass(self) -> enums.HighpassFilterExtended:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:VOIP:FILTer:HPASs \n
		Snippet: value: enums.HighpassFilterExtended = driver.configure.afRf.measurement.voip.filterPy.get_hpass() \n
		Configures the highpass filter in the VoIP input path. \n
			:return: filter_py: OFF | F6 | F50 | F300 OFF Filter disabled F6, F50, F300 Cutoff frequency 6 Hz / 50 Hz / 300 Hz
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:VOIP:FILTer:HPASs?')
		return Conversions.str_to_scalar_enum(response, enums.HighpassFilterExtended)

	def set_hpass(self, filter_py: enums.HighpassFilterExtended) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:VOIP:FILTer:HPASs \n
		Snippet: driver.configure.afRf.measurement.voip.filterPy.set_hpass(filter_py = enums.HighpassFilterExtended.F300) \n
		Configures the highpass filter in the VoIP input path. \n
			:param filter_py: OFF | F6 | F50 | F300 OFF Filter disabled F6, F50, F300 Cutoff frequency 6 Hz / 50 Hz / 300 Hz
		"""
		param = Conversions.enum_scalar_to_str(filter_py, enums.HighpassFilterExtended)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:VOIP:FILTer:HPASs {param}')

	# noinspection PyTypeChecker
	class DwidthStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Dwidth: enums.PwrFilterType: WIDE | NARRow Wide or narrow bandwidth
			- Relative: enums.Relative: RELative | CONStant Proportional to reference frequency or constant"""
		__meta_args_list = [
			ArgStruct.scalar_enum('Dwidth', enums.PwrFilterType),
			ArgStruct.scalar_enum('Relative', enums.Relative)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Dwidth: enums.PwrFilterType = None
			self.Relative: enums.Relative = None

	# noinspection PyTypeChecker
	def get_dwidth(self) -> DwidthStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:VOIP:FILTer:DWIDth \n
		Snippet: value: DwidthStruct = driver.configure.afRf.measurement.voip.filterPy.get_dwidth() \n
		Configures the bandwidth of the distortion filter in the VoIP input path. \n
			:return: structure: for return value, see the help for DwidthStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:AFRF:MEASurement<Instance>:VOIP:FILTer:DWIDth?', self.__class__.DwidthStruct())

	def set_dwidth(self, value: DwidthStruct) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:VOIP:FILTer:DWIDth \n
		Snippet: driver.configure.afRf.measurement.voip.filterPy.set_dwidth(value = DwidthStruct()) \n
		Configures the bandwidth of the distortion filter in the VoIP input path. \n
			:param value: see the help for DwidthStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:AFRF:MEASurement<Instance>:VOIP:FILTer:DWIDth', value)

	# noinspection PyTypeChecker
	def get_weighting(self) -> enums.WeightingFilter:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:VOIP:FILTer:WEIGhting \n
		Snippet: value: enums.WeightingFilter = driver.configure.afRf.measurement.voip.filterPy.get_weighting() \n
		Configures the weighting filter in the VoIP input path. \n
			:return: filter_py: OFF | AWEighting | CCITt | CMESsage OFF Filter disabled AWEighting A-weighting filter CCITt CCITT weighting filter CMESsage C-message weighting filter
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:VOIP:FILTer:WEIGhting?')
		return Conversions.str_to_scalar_enum(response, enums.WeightingFilter)

	def set_weighting(self, filter_py: enums.WeightingFilter) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:VOIP:FILTer:WEIGhting \n
		Snippet: driver.configure.afRf.measurement.voip.filterPy.set_weighting(filter_py = enums.WeightingFilter.AWEighting) \n
		Configures the weighting filter in the VoIP input path. \n
			:param filter_py: OFF | AWEighting | CCITt | CMESsage OFF Filter disabled AWEighting A-weighting filter CCITt CCITT weighting filter CMESsage C-message weighting filter
		"""
		param = Conversions.enum_scalar_to_str(filter_py, enums.WeightingFilter)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:VOIP:FILTer:WEIGhting {param}')

	def get_dfrequency(self) -> float:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:VOIP:FILTer:DFRequency \n
		Snippet: value: float = driver.configure.afRf.measurement.voip.filterPy.get_dfrequency() \n
		Configures the reference frequency for single-tone measurements via the VoIP input path. \n
			:return: distor_freq: Range: 1 Hz to 10.5 kHz, Unit: Hz
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:VOIP:FILTer:DFRequency?')
		return Conversions.str_to_float(response)

	def set_dfrequency(self, distor_freq: float) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:VOIP:FILTer:DFRequency \n
		Snippet: driver.configure.afRf.measurement.voip.filterPy.set_dfrequency(distor_freq = 1.0) \n
		Configures the reference frequency for single-tone measurements via the VoIP input path. \n
			:param distor_freq: Range: 1 Hz to 10.5 kHz, Unit: Hz
		"""
		param = Conversions.decimal_value_to_str(distor_freq)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:VOIP:FILTer:DFRequency {param}')

	def get_robust_auto(self) -> bool:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:VOIP:FILTer:ROBustauto \n
		Snippet: value: bool = driver.configure.afRf.measurement.voip.filterPy.get_robust_auto() \n
		Enables or disables robust automatic mode for distortion signal filtering in the VoIP input path. \n
			:return: automatic_mode: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:VOIP:FILTer:ROBustauto?')
		return Conversions.str_to_bool(response)

	def set_robust_auto(self, automatic_mode: bool) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:VOIP:FILTer:ROBustauto \n
		Snippet: driver.configure.afRf.measurement.voip.filterPy.set_robust_auto(automatic_mode = False) \n
		Enables or disables robust automatic mode for distortion signal filtering in the VoIP input path. \n
			:param automatic_mode: OFF | ON
		"""
		param = Conversions.bool_to_str(automatic_mode)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:VOIP:FILTer:ROBustauto {param}')

	def clone(self) -> 'FilterPy':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = FilterPy(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
