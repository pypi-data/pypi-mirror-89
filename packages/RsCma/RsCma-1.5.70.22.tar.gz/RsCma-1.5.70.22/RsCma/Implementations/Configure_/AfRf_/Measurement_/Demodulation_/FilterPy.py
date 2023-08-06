from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FilterPy:
	"""FilterPy commands group definition. 13 total commands, 2 Sub-groups, 8 group commands"""

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
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DEModulation:FILTer:LPASs \n
		Snippet: value: enums.LowpassFilterExtended = driver.configure.afRf.measurement.demodulation.filterPy.get_lpass() \n
		Configures the lowpass filter in the RF input path. \n
			:return: lowpass: OFF | F255 | F3K | F3K4 | F4K | F15K OFF Filter disabled F255, F3K, F3K4, F4K, F15K Cutoff frequency 255 Hz / 3 kHz / 3.4 kHz / 4 kHz / 15 kHz
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:DEModulation:FILTer:LPASs?')
		return Conversions.str_to_scalar_enum(response, enums.LowpassFilterExtended)

	def set_lpass(self, lowpass: enums.LowpassFilterExtended) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DEModulation:FILTer:LPASs \n
		Snippet: driver.configure.afRf.measurement.demodulation.filterPy.set_lpass(lowpass = enums.LowpassFilterExtended.F15K) \n
		Configures the lowpass filter in the RF input path. \n
			:param lowpass: OFF | F255 | F3K | F3K4 | F4K | F15K OFF Filter disabled F255, F3K, F3K4, F4K, F15K Cutoff frequency 255 Hz / 3 kHz / 3.4 kHz / 4 kHz / 15 kHz
		"""
		param = Conversions.enum_scalar_to_str(lowpass, enums.LowpassFilterExtended)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:DEModulation:FILTer:LPASs {param}')

	# noinspection PyTypeChecker
	def get_hpass(self) -> enums.HighpassFilterExtended:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DEModulation:FILTer:HPASs \n
		Snippet: value: enums.HighpassFilterExtended = driver.configure.afRf.measurement.demodulation.filterPy.get_hpass() \n
		Configures the highpass filter in the RF input path. \n
			:return: highpass: OFF | F6 | F50 | F300 OFF Filter disabled F6, F50, F300 Cutoff frequency 6 Hz / 50 Hz / 300 Hz
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:DEModulation:FILTer:HPASs?')
		return Conversions.str_to_scalar_enum(response, enums.HighpassFilterExtended)

	def set_hpass(self, highpass: enums.HighpassFilterExtended) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DEModulation:FILTer:HPASs \n
		Snippet: driver.configure.afRf.measurement.demodulation.filterPy.set_hpass(highpass = enums.HighpassFilterExtended.F300) \n
		Configures the highpass filter in the RF input path. \n
			:param highpass: OFF | F6 | F50 | F300 OFF Filter disabled F6, F50, F300 Cutoff frequency 6 Hz / 50 Hz / 300 Hz
		"""
		param = Conversions.enum_scalar_to_str(highpass, enums.HighpassFilterExtended)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:DEModulation:FILTer:HPASs {param}')

	# noinspection PyTypeChecker
	class DwidthStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Dwidth_Left: enums.PwrFilterType: WIDE | NARRow Wide or narrow bandwidth
			- Relative_Left: enums.Relative: RELative | CONStant Bandwidth proportional to reference frequency or constant
			- Dwidth_Right: enums.PwrFilterType: WIDE | NARRow
			- Relative_Right: enums.Relative: RELative | CONStant"""
		__meta_args_list = [
			ArgStruct.scalar_enum('Dwidth_Left', enums.PwrFilterType),
			ArgStruct.scalar_enum('Relative_Left', enums.Relative),
			ArgStruct.scalar_enum('Dwidth_Right', enums.PwrFilterType),
			ArgStruct.scalar_enum('Relative_Right', enums.Relative)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Dwidth_Left: enums.PwrFilterType = None
			self.Relative_Left: enums.Relative = None
			self.Dwidth_Right: enums.PwrFilterType = None
			self.Relative_Right: enums.Relative = None

	# noinspection PyTypeChecker
	def get_dwidth(self) -> DwidthStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DEModulation:FILTer:DWIDth \n
		Snippet: value: DwidthStruct = driver.configure.afRf.measurement.demodulation.filterPy.get_dwidth() \n
		Configures the bandwidth of the distortion filter in the RF input path. For FM stereo, the settings configure the left
		and the right audio channel. For other modulation types, only the <...Left> settings are relevant. The <...
		Right> settings have no effect. \n
			:return: structure: for return value, see the help for DwidthStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:AFRF:MEASurement<Instance>:DEModulation:FILTer:DWIDth?', self.__class__.DwidthStruct())

	def set_dwidth(self, value: DwidthStruct) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DEModulation:FILTer:DWIDth \n
		Snippet: driver.configure.afRf.measurement.demodulation.filterPy.set_dwidth(value = DwidthStruct()) \n
		Configures the bandwidth of the distortion filter in the RF input path. For FM stereo, the settings configure the left
		and the right audio channel. For other modulation types, only the <...Left> settings are relevant. The <...
		Right> settings have no effect. \n
			:param value: see the help for DwidthStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:AFRF:MEASurement<Instance>:DEModulation:FILTer:DWIDth', value)

	# noinspection PyTypeChecker
	class DfrequencyStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Distor_Freq_Left: float: Range: 0 Hz to 10.5 kHz, Unit: Hz
			- Distor_Freq_Right: float: Range: 0 Hz to 10.5 kHz, Unit: Hz"""
		__meta_args_list = [
			ArgStruct.scalar_float('Distor_Freq_Left'),
			ArgStruct.scalar_float('Distor_Freq_Right')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Distor_Freq_Left: float = None
			self.Distor_Freq_Right: float = None

	def get_dfrequency(self) -> DfrequencyStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DEModulation:FILTer:DFRequency \n
		Snippet: value: DfrequencyStruct = driver.configure.afRf.measurement.demodulation.filterPy.get_dfrequency() \n
		Configures the reference frequency for single-tone measurements via the RF input path. For FM stereo, the settings
		configure the left and the right audio channel. For other modulation types, only <DistorFreqLeft> is relevant.
		<DistorFreqRight> has no effect. \n
			:return: structure: for return value, see the help for DfrequencyStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:AFRF:MEASurement<Instance>:DEModulation:FILTer:DFRequency?', self.__class__.DfrequencyStruct())

	def set_dfrequency(self, value: DfrequencyStruct) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DEModulation:FILTer:DFRequency \n
		Snippet: driver.configure.afRf.measurement.demodulation.filterPy.set_dfrequency(value = DfrequencyStruct()) \n
		Configures the reference frequency for single-tone measurements via the RF input path. For FM stereo, the settings
		configure the left and the right audio channel. For other modulation types, only <DistorFreqLeft> is relevant.
		<DistorFreqRight> has no effect. \n
			:param value: see the help for DfrequencyStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:AFRF:MEASurement<Instance>:DEModulation:FILTer:DFRequency', value)

	def get_enable(self) -> bool:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DEModulation:FILTer:ENABle \n
		Snippet: value: bool = driver.configure.afRf.measurement.demodulation.filterPy.get_enable() \n
		Selects whether the demodulation results are measured before or after the filters in the RF input path. For FM stereo,
		the demodulation results are always measured before the filters. \n
			:return: disable: No help available
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:DEModulation:FILTer:ENABle?')
		return Conversions.str_to_bool(response)

	def set_enable(self, disable: bool) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DEModulation:FILTer:ENABle \n
		Snippet: driver.configure.afRf.measurement.demodulation.filterPy.set_enable(disable = False) \n
		Selects whether the demodulation results are measured before or after the filters in the RF input path. For FM stereo,
		the demodulation results are always measured before the filters. \n
			:param disable: OFF | ON OFF Measure before filters ON Measure after filters
		"""
		param = Conversions.bool_to_str(disable)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:DEModulation:FILTer:ENABle {param}')

	# noinspection PyTypeChecker
	def get_weighting(self) -> enums.WeightingFilter:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DEModulation:FILTer:WEIGhting \n
		Snippet: value: enums.WeightingFilter = driver.configure.afRf.measurement.demodulation.filterPy.get_weighting() \n
		Selects the weighting filter in the RF input path. \n
			:return: weighting: OFF | AWEighting | CCITt | CMESsage OFF Filter disabled AWEighting A-weighting filter CCITt CCITT weighting filter CMESsage C-message weighting filter
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:DEModulation:FILTer:WEIGhting?')
		return Conversions.str_to_scalar_enum(response, enums.WeightingFilter)

	def set_weighting(self, weighting: enums.WeightingFilter) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DEModulation:FILTer:WEIGhting \n
		Snippet: driver.configure.afRf.measurement.demodulation.filterPy.set_weighting(weighting = enums.WeightingFilter.AWEighting) \n
		Selects the weighting filter in the RF input path. \n
			:param weighting: OFF | AWEighting | CCITt | CMESsage OFF Filter disabled AWEighting A-weighting filter CCITt CCITT weighting filter CMESsage C-message weighting filter
		"""
		param = Conversions.enum_scalar_to_str(weighting, enums.WeightingFilter)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:DEModulation:FILTer:WEIGhting {param}')

	# noinspection PyTypeChecker
	def get_deemphasis(self) -> enums.PreDeEmphasis:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DEModulation:FILTer:DEEMphasis \n
		Snippet: value: enums.PreDeEmphasis = driver.configure.afRf.measurement.demodulation.filterPy.get_deemphasis() \n
		Configures the de-emphasis filter in the RF input path. \n
			:return: deemphasis: OFF | T50 | T75 | T750 OFF Filter disabled T50, T75, T750 Time constant 50 µs / 75 µs / 750 µs
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:DEModulation:FILTer:DEEMphasis?')
		return Conversions.str_to_scalar_enum(response, enums.PreDeEmphasis)

	def set_deemphasis(self, deemphasis: enums.PreDeEmphasis) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DEModulation:FILTer:DEEMphasis \n
		Snippet: driver.configure.afRf.measurement.demodulation.filterPy.set_deemphasis(deemphasis = enums.PreDeEmphasis.OFF) \n
		Configures the de-emphasis filter in the RF input path. \n
			:param deemphasis: OFF | T50 | T75 | T750 OFF Filter disabled T50, T75, T750 Time constant 50 µs / 75 µs / 750 µs
		"""
		param = Conversions.enum_scalar_to_str(deemphasis, enums.PreDeEmphasis)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:DEModulation:FILTer:DEEMphasis {param}')

	def get_robust_auto(self) -> bool:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DEModulation:FILTer:ROBustauto \n
		Snippet: value: bool = driver.configure.afRf.measurement.demodulation.filterPy.get_robust_auto() \n
		Enables or disables robust automatic mode for distortion signal filtering in the RF input path. \n
			:return: automatic_mode: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:DEModulation:FILTer:ROBustauto?')
		return Conversions.str_to_bool(response)

	def set_robust_auto(self, automatic_mode: bool) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DEModulation:FILTer:ROBustauto \n
		Snippet: driver.configure.afRf.measurement.demodulation.filterPy.set_robust_auto(automatic_mode = False) \n
		Enables or disables robust automatic mode for distortion signal filtering in the RF input path. \n
			:param automatic_mode: OFF | ON
		"""
		param = Conversions.bool_to_str(automatic_mode)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:DEModulation:FILTer:ROBustauto {param}')

	def clone(self) -> 'FilterPy':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = FilterPy(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
