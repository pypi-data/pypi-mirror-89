from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sequencer:
	"""Sequencer commands group definition. 4 total commands, 1 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sequencer", core, parent)

	@property
	def tplan(self):
		"""tplan commands group. 2 Sub-classes, 2 commands."""
		if not hasattr(self, '_tplan'):
			from .Sequencer_.Tplan import Tplan
			self._tplan = Tplan(self._core, self._base)
		return self._tplan

	def clone(self) -> 'Sequencer':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Sequencer(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
