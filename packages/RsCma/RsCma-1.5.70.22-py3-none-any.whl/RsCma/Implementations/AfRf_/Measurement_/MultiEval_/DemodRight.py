from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DemodRight:
	"""DemodRight commands group definition. 16 total commands, 1 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("demodRight", core, parent)

	@property
	def afSignal(self):
		"""afSignal commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_afSignal'):
			from .DemodRight_.AfSignal import AfSignal
			self._afSignal = AfSignal(self._core, self._base)
		return self._afSignal

	def clone(self) -> 'DemodRight':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = DemodRight(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
