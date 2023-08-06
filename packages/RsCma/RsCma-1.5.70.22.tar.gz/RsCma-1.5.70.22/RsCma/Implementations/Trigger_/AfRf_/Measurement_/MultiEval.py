from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MultiEval:
	"""MultiEval commands group definition. 35 total commands, 1 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("multiEval", core, parent)

	@property
	def oscilloscope(self):
		"""oscilloscope commands group. 4 Sub-classes, 1 commands."""
		if not hasattr(self, '_oscilloscope'):
			from .MultiEval_.Oscilloscope import Oscilloscope
			self._oscilloscope = Oscilloscope(self._core, self._base)
		return self._oscilloscope

	def clone(self) -> 'MultiEval':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = MultiEval(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
