from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mode:
	"""Mode commands group definition. 8 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mode", core, parent)

	@property
	def display(self):
		"""display commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_display'):
			from .Mode_.Display import Display
			self._display = Display(self._core, self._base)
		return self._display

	@property
	def file(self):
		"""file commands group. 7 Sub-classes, 0 commands."""
		if not hasattr(self, '_file'):
			from .Mode_.File import File
			self._file = File(self._core, self._base)
		return self._file

	def clone(self) -> 'Mode':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Mode(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
