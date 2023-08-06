from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Store:
	"""Store commands group definition. 2 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("store", core, parent)

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Store_.State import State
			self._state = State(self._core, self._base)
		return self._state

	@property
	def item(self):
		"""item commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_item'):
			from .Store_.Item import Item
			self._item = Item(self._core, self._base)
		return self._item

	def clone(self) -> 'Store':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Store(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
