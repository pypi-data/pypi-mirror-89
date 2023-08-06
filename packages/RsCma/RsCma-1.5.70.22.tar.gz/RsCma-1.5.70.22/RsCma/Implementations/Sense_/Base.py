from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Base:
	"""Base commands group definition. 11 total commands, 4 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("base", core, parent)

	@property
	def power(self):
		"""power commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_power'):
			from .Base_.Power import Power
			self._power = Power(self._core, self._base)
		return self._power

	@property
	def battery(self):
		"""battery commands group. 1 Sub-classes, 4 commands."""
		if not hasattr(self, '_battery'):
			from .Base_.Battery import Battery
			self._battery = Battery(self._core, self._base)
		return self._battery

	@property
	def temperature(self):
		"""temperature commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_temperature'):
			from .Base_.Temperature import Temperature
			self._temperature = Temperature(self._core, self._base)
		return self._temperature

	@property
	def reference(self):
		"""reference commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_reference'):
			from .Base_.Reference import Reference
			self._reference = Reference(self._core, self._base)
		return self._reference

	def clone(self) -> 'Base':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Base(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
