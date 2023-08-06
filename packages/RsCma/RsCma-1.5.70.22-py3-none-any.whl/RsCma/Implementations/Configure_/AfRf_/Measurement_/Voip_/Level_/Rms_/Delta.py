from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Delta:
	"""Delta commands group definition. 4 total commands, 1 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("delta", core, parent)

	@property
	def update(self):
		"""update commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_update'):
			from .Delta_.Update import Update
			self._update = Update(self._core, self._base)
		return self._update

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.DeltaMode:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:VOIP:LEVel:RMS:DELTa:MODE \n
		Snippet: value: enums.DeltaMode = driver.configure.afRf.measurement.voip.level.rms.delta.get_mode() \n
		No command help available \n
			:return: mode: No help available
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:VOIP:LEVel:RMS:DELTa:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.DeltaMode)

	def set_mode(self, mode: enums.DeltaMode) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:VOIP:LEVel:RMS:DELTa:MODE \n
		Snippet: driver.configure.afRf.measurement.voip.level.rms.delta.set_mode(mode = enums.DeltaMode.MEAS) \n
		No command help available \n
			:param mode: No help available
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.DeltaMode)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:VOIP:LEVel:RMS:DELTa:MODE {param}')

	def get_user(self) -> float:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:VOIP:LEVel:RMS:DELTa:USER \n
		Snippet: value: float = driver.configure.afRf.measurement.voip.level.rms.delta.get_user() \n
		No command help available \n
			:return: user_val: No help available
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:VOIP:LEVel:RMS:DELTa:USER?')
		return Conversions.str_to_float(response)

	def set_user(self, user_val: float) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:VOIP:LEVel:RMS:DELTa:USER \n
		Snippet: driver.configure.afRf.measurement.voip.level.rms.delta.set_user(user_val = 1.0) \n
		No command help available \n
			:param user_val: No help available
		"""
		param = Conversions.decimal_value_to_str(user_val)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:VOIP:LEVel:RMS:DELTa:USER {param}')

	def get_measured(self) -> float:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:VOIP:LEVel:RMS:DELTa:MEASured \n
		Snippet: value: float = driver.configure.afRf.measurement.voip.level.rms.delta.get_measured() \n
		No command help available \n
			:return: meas_val: No help available
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:VOIP:LEVel:RMS:DELTa:MEASured?')
		return Conversions.str_to_float(response)

	def clone(self) -> 'Delta':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Delta(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
