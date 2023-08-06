from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SpdifLeft:
	"""SpdifLeft commands group definition. 8 total commands, 1 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("spdifLeft", core, parent)

	@property
	def power(self):
		"""power commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_power'):
			from .SpdifLeft_.Power import Power
			self._power = Power(self._core, self._base)
		return self._power

	def clone(self) -> 'SpdifLeft':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SpdifLeft(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
