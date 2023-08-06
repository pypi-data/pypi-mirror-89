from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AfSettings:
	"""AfSettings commands group definition. 11 total commands, 3 Sub-groups, 6 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("afSettings", core, parent)

	@property
	def audioOutput(self):
		"""audioOutput commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_audioOutput'):
			from .AfSettings_.AudioOutput import AudioOutput
			self._audioOutput = AudioOutput(self._core, self._base)
		return self._audioOutput

	@property
	def frequency(self):
		"""frequency commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_frequency'):
			from .AfSettings_.Frequency import Frequency
			self._frequency = Frequency(self._core, self._base)
		return self._frequency

	@property
	def fmoddepth(self):
		"""fmoddepth commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fmoddepth'):
			from .AfSettings_.Fmoddepth import Fmoddepth
			self._fmoddepth = Fmoddepth(self._core, self._base)
		return self._fmoddepth

	# noinspection PyTypeChecker
	def get_connector(self) -> enums.AudioConnector:
		"""SCPI: SOURce:AVIonics:GENerator<Instance>:ILS:LOCalizer:AFSettings:CONNector \n
		Snippet: value: enums.AudioConnector = driver.source.avionics.generator.ils.localizer.afSettings.get_connector() \n
		Selects the output connector for the generated AF signal (AF1 OUT or AF2 OUT) . If you want to route both the localizer
		signal and the glide slope signal to an AF output, you must configure different connectors for the two signals. \n
			:return: connector: AF1O | AF2O
		"""
		response = self._core.io.query_str('SOURce:AVIonics:GENerator<Instance>:ILS:LOCalizer:AFSettings:CONNector?')
		return Conversions.str_to_scalar_enum(response, enums.AudioConnector)

	def set_connector(self, connector: enums.AudioConnector) -> None:
		"""SCPI: SOURce:AVIonics:GENerator<Instance>:ILS:LOCalizer:AFSettings:CONNector \n
		Snippet: driver.source.avionics.generator.ils.localizer.afSettings.set_connector(connector = enums.AudioConnector.AF1O) \n
		Selects the output connector for the generated AF signal (AF1 OUT or AF2 OUT) . If you want to route both the localizer
		signal and the glide slope signal to an AF output, you must configure different connectors for the two signals. \n
			:param connector: AF1O | AF2O
		"""
		param = Conversions.enum_scalar_to_str(connector, enums.AudioConnector)
		self._core.io.write(f'SOURce:AVIonics:GENerator<Instance>:ILS:LOCalizer:AFSettings:CONNector {param}')

	def get_enable(self) -> bool:
		"""SCPI: SOURce:AVIonics:GENerator<Instance>:ILS:LOCalizer:AFSettings:ENABle \n
		Snippet: value: bool = driver.source.avionics.generator.ils.localizer.afSettings.get_enable() \n
		Enables or disables the modulation of the RF carrier with the audio tones for the two lobes. \n
			:return: enable: OFF | ON
		"""
		response = self._core.io.query_str('SOURce:AVIonics:GENerator<Instance>:ILS:LOCalizer:AFSettings:ENABle?')
		return Conversions.str_to_bool(response)

	def set_enable(self, enable: bool) -> None:
		"""SCPI: SOURce:AVIonics:GENerator<Instance>:ILS:LOCalizer:AFSettings:ENABle \n
		Snippet: driver.source.avionics.generator.ils.localizer.afSettings.set_enable(enable = False) \n
		Enables or disables the modulation of the RF carrier with the audio tones for the two lobes. \n
			:param enable: OFF | ON
		"""
		param = Conversions.bool_to_str(enable)
		self._core.io.write(f'SOURce:AVIonics:GENerator<Instance>:ILS:LOCalizer:AFSettings:ENABle {param}')

	def get_sdm(self) -> float:
		"""SCPI: SOURce:AVIonics:GENerator<Instance>:ILS:LOCalizer:AFSettings:SDM \n
		Snippet: value: float = driver.source.avionics.generator.ils.localizer.afSettings.get_sdm() \n
		Sets the sum of depth of modulations (SDM) . \n
			:return: mod_depth: Range: 0 % to 100 %, Unit: %
		"""
		response = self._core.io.query_str('SOURce:AVIonics:GENerator<Instance>:ILS:LOCalizer:AFSettings:SDM?')
		return Conversions.str_to_float(response)

	def set_sdm(self, mod_depth: float) -> None:
		"""SCPI: SOURce:AVIonics:GENerator<Instance>:ILS:LOCalizer:AFSettings:SDM \n
		Snippet: driver.source.avionics.generator.ils.localizer.afSettings.set_sdm(mod_depth = 1.0) \n
		Sets the sum of depth of modulations (SDM) . \n
			:param mod_depth: Range: 0 % to 100 %, Unit: %
		"""
		param = Conversions.decimal_value_to_str(mod_depth)
		self._core.io.write(f'SOURce:AVIonics:GENerator<Instance>:ILS:LOCalizer:AFSettings:SDM {param}')

	def get_ddm(self) -> float:
		"""SCPI: SOURce:AVIonics:GENerator<Instance>:ILS:LOCalizer:AFSettings:DDM \n
		Snippet: value: float = driver.source.avionics.generator.ils.localizer.afSettings.get_ddm() \n
		Sets the difference in modulation depth between the two lobes. The maximum allowed absolute value is limited by the
		configured SDM value. \n
			:return: ddm: Range: -100 % to 100 %, Unit: %
		"""
		response = self._core.io.query_str('SOURce:AVIonics:GENerator<Instance>:ILS:LOCalizer:AFSettings:DDM?')
		return Conversions.str_to_float(response)

	def set_ddm(self, ddm: float) -> None:
		"""SCPI: SOURce:AVIonics:GENerator<Instance>:ILS:LOCalizer:AFSettings:DDM \n
		Snippet: driver.source.avionics.generator.ils.localizer.afSettings.set_ddm(ddm = 1.0) \n
		Sets the difference in modulation depth between the two lobes. The maximum allowed absolute value is limited by the
		configured SDM value. \n
			:param ddm: Range: -100 % to 100 %, Unit: %
		"""
		param = Conversions.decimal_value_to_str(ddm)
		self._core.io.write(f'SOURce:AVIonics:GENerator<Instance>:ILS:LOCalizer:AFSettings:DDM {param}')

	# noinspection PyTypeChecker
	def get_fly(self) -> enums.LeftRightDirection:
		"""SCPI: SOURce:AVIonics:GENerator<Instance>:ILS:LOCalizer:AFSettings:FLY \n
		Snippet: value: enums.LeftRightDirection = driver.source.avionics.generator.ils.localizer.afSettings.get_fly() \n
		Sets the direction towards the ideal line (fly left or fly right) and the sign of the configured DDM value. \n
			:return: direction: LEFT | RIGHt
		"""
		response = self._core.io.query_str('SOURce:AVIonics:GENerator<Instance>:ILS:LOCalizer:AFSettings:FLY?')
		return Conversions.str_to_scalar_enum(response, enums.LeftRightDirection)

	def set_fly(self, direction: enums.LeftRightDirection) -> None:
		"""SCPI: SOURce:AVIonics:GENerator<Instance>:ILS:LOCalizer:AFSettings:FLY \n
		Snippet: driver.source.avionics.generator.ils.localizer.afSettings.set_fly(direction = enums.LeftRightDirection.LEFT) \n
		Sets the direction towards the ideal line (fly left or fly right) and the sign of the configured DDM value. \n
			:param direction: LEFT | RIGHt
		"""
		param = Conversions.enum_scalar_to_str(direction, enums.LeftRightDirection)
		self._core.io.write(f'SOURce:AVIonics:GENerator<Instance>:ILS:LOCalizer:AFSettings:FLY {param}')

	def get_poffset(self) -> float:
		"""SCPI: SOURce:AVIonics:GENerator<Instance>:ILS:LOCalizer:AFSettings:POFFset \n
		Snippet: value: float = driver.source.avionics.generator.ils.localizer.afSettings.get_poffset() \n
		Sets the phase offset between the audio signals of the two lobes. \n
			:return: poffset: Range: -60 deg to 120 deg, Unit: deg
		"""
		response = self._core.io.query_str('SOURce:AVIonics:GENerator<Instance>:ILS:LOCalizer:AFSettings:POFFset?')
		return Conversions.str_to_float(response)

	def set_poffset(self, poffset: float) -> None:
		"""SCPI: SOURce:AVIonics:GENerator<Instance>:ILS:LOCalizer:AFSettings:POFFset \n
		Snippet: driver.source.avionics.generator.ils.localizer.afSettings.set_poffset(poffset = 1.0) \n
		Sets the phase offset between the audio signals of the two lobes. \n
			:param poffset: Range: -60 deg to 120 deg, Unit: deg
		"""
		param = Conversions.decimal_value_to_str(poffset)
		self._core.io.write(f'SOURce:AVIonics:GENerator<Instance>:ILS:LOCalizer:AFSettings:POFFset {param}')

	def clone(self) -> 'AfSettings':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = AfSettings(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
