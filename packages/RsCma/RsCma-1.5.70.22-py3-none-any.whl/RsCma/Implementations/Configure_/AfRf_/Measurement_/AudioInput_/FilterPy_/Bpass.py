from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Bpass:
	"""Bpass commands group definition. 3 total commands, 3 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("bpass", core, parent)

	@property
	def enable(self):
		"""enable commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_enable'):
			from .Bpass_.Enable import Enable
			self._enable = Enable(self._core, self._base)
		return self._enable

	@property
	def cfrequency(self):
		"""cfrequency commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cfrequency'):
			from .Bpass_.Cfrequency import Cfrequency
			self._cfrequency = Cfrequency(self._core, self._base)
		return self._cfrequency

	@property
	def bandwidth(self):
		"""bandwidth commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bandwidth'):
			from .Bpass_.Bandwidth import Bandwidth
			self._bandwidth = Bandwidth(self._core, self._base)
		return self._bandwidth

	def clone(self) -> 'Bpass':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Bpass(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
