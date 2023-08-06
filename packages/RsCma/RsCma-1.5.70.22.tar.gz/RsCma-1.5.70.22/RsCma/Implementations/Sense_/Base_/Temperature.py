from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Temperature:
	"""Temperature commands group definition. 3 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("temperature", core, parent)

	@property
	def exceeded(self):
		"""exceeded commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_exceeded'):
			from .Temperature_.Exceeded import Exceeded
			self._exceeded = Exceeded(self._core, self._base)
		return self._exceeded

	def get_environment(self) -> float:
		"""SCPI: SENSe:BASE:TEMPerature:ENVironment \n
		Snippet: value: float = driver.sense.base.temperature.get_environment() \n
		No command help available \n
			:return: temperature: No help available
		"""
		response = self._core.io.query_str('SENSe:BASE:TEMPerature:ENVironment?')
		return Conversions.str_to_float(response)

	def clone(self) -> 'Temperature':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Temperature(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
