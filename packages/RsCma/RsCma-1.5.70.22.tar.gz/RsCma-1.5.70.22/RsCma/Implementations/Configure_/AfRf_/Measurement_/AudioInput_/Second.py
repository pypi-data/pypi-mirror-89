from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Second:
	"""Second commands group definition. 3 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("second", core, parent)

	@property
	def level(self):
		"""level commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_level'):
			from .Second_.Level import Level
			self._level = Level(self._core, self._base)
		return self._level

	def get_mlevel(self) -> float:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:AIN:SECond:MLEVel \n
		Snippet: value: float = driver.configure.afRf.measurement.audioInput.second.get_mlevel() \n
		Specifies the maximum expected level for the AF2 IN connector. This setting is only relevant, if auto ranging is disabled.
		Use this command, if you want to set different level units, e.g. dBm (Table 'Units relevant for remote commands') , or
		set the level for both connectors independently. \n
			:return: max_level: Range: 10E-6 V to 43 V, Unit: V
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:AIN:SECond:MLEVel?')
		return Conversions.str_to_float(response)

	def set_mlevel(self, max_level: float) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:AIN:SECond:MLEVel \n
		Snippet: driver.configure.afRf.measurement.audioInput.second.set_mlevel(max_level = 1.0) \n
		Specifies the maximum expected level for the AF2 IN connector. This setting is only relevant, if auto ranging is disabled.
		Use this command, if you want to set different level units, e.g. dBm (Table 'Units relevant for remote commands') , or
		set the level for both connectors independently. \n
			:param max_level: Range: 10E-6 V to 43 V, Unit: V
		"""
		param = Conversions.decimal_value_to_str(max_level)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:AIN:SECond:MLEVel {param}')

	def clone(self) -> 'Second':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Second(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
