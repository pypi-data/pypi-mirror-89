from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SearchRoutines:
	"""SearchRoutines commands group definition. 27 total commands, 6 Sub-groups, 7 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("searchRoutines", core, parent)

	@property
	def dialing(self):
		"""dialing commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dialing'):
			from .SearchRoutines_.Dialing import Dialing
			self._dialing = Dialing(self._core, self._base)
		return self._dialing

	@property
	def amPoints(self):
		"""amPoints commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_amPoints'):
			from .SearchRoutines_.AmPoints import AmPoints
			self._amPoints = AmPoints(self._core, self._base)
		return self._amPoints

	@property
	def limit(self):
		"""limit commands group. 3 Sub-classes, 1 commands."""
		if not hasattr(self, '_limit'):
			from .SearchRoutines_.Limit import Limit
			self._limit = Limit(self._core, self._base)
		return self._limit

	@property
	def rifBandwidth(self):
		"""rifBandwidth commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_rifBandwidth'):
			from .SearchRoutines_.RifBandwidth import RifBandwidth
			self._rifBandwidth = RifBandwidth(self._core, self._base)
		return self._rifBandwidth

	@property
	def rsquelch(self):
		"""rsquelch commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_rsquelch'):
			from .SearchRoutines_.Rsquelch import Rsquelch
			self._rsquelch = Rsquelch(self._core, self._base)
		return self._rsquelch

	@property
	def ssnr(self):
		"""ssnr commands group. 1 Sub-classes, 7 commands."""
		if not hasattr(self, '_ssnr'):
			from .SearchRoutines_.Ssnr import Ssnr
			self._ssnr = Ssnr(self._core, self._base)
		return self._ssnr

	def get_mrf_level(self) -> float:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:MRFLevel \n
		Snippet: value: float = driver.configure.afRf.measurement.searchRoutines.get_mrf_level() \n
		Configures the maximum RF level for the signal generator. A too high value can damage your DUT. \n
			:return: max_level: Range: -130 dBm to -30 dBm, Unit: dBm
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:SROutines:MRFLevel?')
		return Conversions.str_to_float(response)

	def set_mrf_level(self, max_level: float) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:MRFLevel \n
		Snippet: driver.configure.afRf.measurement.searchRoutines.set_mrf_level(max_level = 1.0) \n
		Configures the maximum RF level for the signal generator. A too high value can damage your DUT. \n
			:param max_level: Range: -130 dBm to -30 dBm, Unit: dBm
		"""
		param = Conversions.decimal_value_to_str(max_level)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:SROutines:MRFLevel {param}')

	def get_sq_value(self) -> float:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:SQValue \n
		Snippet: value: float = driver.configure.afRf.measurement.searchRoutines.get_sq_value() \n
		Configures the target value for the audio signal quality. \n
			:return: target_par_val: Range: 1 dB to 46 dB, Unit: dB
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:SROutines:SQValue?')
		return Conversions.str_to_float(response)

	def set_sq_value(self, target_par_val: float) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:SQValue \n
		Snippet: driver.configure.afRf.measurement.searchRoutines.set_sq_value(target_par_val = 1.0) \n
		Configures the target value for the audio signal quality. \n
			:param target_par_val: Range: 1 dB to 46 dB, Unit: dB
		"""
		param = Conversions.decimal_value_to_str(target_par_val)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:SROutines:SQValue {param}')

	# noinspection PyTypeChecker
	def get_sq_type(self) -> enums.TargetParType:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:SQTYpe \n
		Snippet: value: enums.TargetParType = driver.configure.afRf.measurement.searchRoutines.get_sq_type() \n
		Selects the type of audio signal quality to be measured. \n
			:return: target_par_type: SINad | SNRatio | SNNRatio | SNDNratio
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:SROutines:SQTYpe?')
		return Conversions.str_to_scalar_enum(response, enums.TargetParType)

	def set_sq_type(self, target_par_type: enums.TargetParType) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:SQTYpe \n
		Snippet: driver.configure.afRf.measurement.searchRoutines.set_sq_type(target_par_type = enums.TargetParType.SINad) \n
		Selects the type of audio signal quality to be measured. \n
			:param target_par_type: SINad | SNRatio | SNNRatio | SNDNratio
		"""
		param = Conversions.enum_scalar_to_str(target_par_type, enums.TargetParType)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:SROutines:SQTYpe {param}')

	def get_stolerance(self) -> float:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:STOLerance \n
		Snippet: value: float = driver.configure.afRf.measurement.searchRoutines.get_stolerance() \n
		The maximum allowed deviation of the current signal quality from the average signal quality. \n
			:return: tolerance: Unit: dB
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:SROutines:STOLerance?')
		return Conversions.str_to_float(response)

	def set_stolerance(self, tolerance: float) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:STOLerance \n
		Snippet: driver.configure.afRf.measurement.searchRoutines.set_stolerance(tolerance = 1.0) \n
		The maximum allowed deviation of the current signal quality from the average signal quality. \n
			:param tolerance: Unit: dB
		"""
		param = Conversions.decimal_value_to_str(tolerance)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:SROutines:STOLerance {param}')

	def get_se_time(self) -> float:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:SETime \n
		Snippet: value: float = driver.configure.afRf.measurement.searchRoutines.get_se_time() \n
		Waiting time after a change of the signal properties before the measurement is started. \n
			:return: setting_time: Unit: s
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:SROutines:SETime?')
		return Conversions.str_to_float(response)

	def set_se_time(self, setting_time: float) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:SETime \n
		Snippet: driver.configure.afRf.measurement.searchRoutines.set_se_time(setting_time = 1.0) \n
		Waiting time after a change of the signal properties before the measurement is started. \n
			:param setting_time: Unit: s
		"""
		param = Conversions.decimal_value_to_str(setting_time)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:SROutines:SETime {param}')

	# noinspection PyTypeChecker
	def get_path(self) -> enums.SearchRoutinePath:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:PATH \n
		Snippet: value: enums.SearchRoutinePath = driver.configure.afRf.measurement.searchRoutines.get_path() \n
		Configures the path from where the test instrument receives the audio input by the connector or by 'VoIP'. \n
			:return: path: AFI1 | AFI2 | VOIP
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:SROutines:PATH?')
		return Conversions.str_to_scalar_enum(response, enums.SearchRoutinePath)

	def set_path(self, path: enums.SearchRoutinePath) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:PATH \n
		Snippet: driver.configure.afRf.measurement.searchRoutines.set_path(path = enums.SearchRoutinePath.AFI1) \n
		Configures the path from where the test instrument receives the audio input by the connector or by 'VoIP'. \n
			:param path: AFI1 | AFI2 | VOIP
		"""
		param = Conversions.enum_scalar_to_str(path, enums.SearchRoutinePath)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:SROutines:PATH {param}')

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.SearchRoutine:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:MODE \n
		Snippet: value: enums.SearchRoutine = driver.configure.afRf.measurement.searchRoutines.get_mode() \n
		No command help available \n
			:return: search_routine: No help available
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:SROutines:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.SearchRoutine)

	def set_mode(self, search_routine: enums.SearchRoutine) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:MODE \n
		Snippet: driver.configure.afRf.measurement.searchRoutines.set_mode(search_routine = enums.SearchRoutine.RIFBandwidth) \n
		No command help available \n
			:param search_routine: No help available
		"""
		param = Conversions.enum_scalar_to_str(search_routine, enums.SearchRoutine)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:SROutines:MODE {param}')

	def clone(self) -> 'SearchRoutines':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SearchRoutines(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
