from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MultiTone:
	"""MultiTone commands group definition. 9 total commands, 7 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("multiTone", core, parent)

	@property
	def tone(self):
		"""tone commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_tone'):
			from .MultiTone_.Tone import Tone
			self._tone = Tone(self._core, self._base)
		return self._tone

	@property
	def enable(self):
		"""enable commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_enable'):
			from .MultiTone_.Enable import Enable
			self._enable = Enable(self._core, self._base)
		return self._enable

	@property
	def crest(self):
		"""crest commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_crest'):
			from .MultiTone_.Crest import Crest
			self._crest = Crest(self._core, self._base)
		return self._crest

	@property
	def frequency(self):
		"""frequency commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_frequency'):
			from .MultiTone_.Frequency import Frequency
			self._frequency = Frequency(self._core, self._base)
		return self._frequency

	@property
	def level(self):
		"""level commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_level'):
			from .MultiTone_.Level import Level
			self._level = Level(self._core, self._base)
		return self._level

	@property
	def ilevel(self):
		"""ilevel commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ilevel'):
			from .MultiTone_.Ilevel import Ilevel
			self._ilevel = Ilevel(self._core, self._base)
		return self._ilevel

	@property
	def tlevel(self):
		"""tlevel commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tlevel'):
			from .MultiTone_.Tlevel import Tlevel
			self._tlevel = Tlevel(self._core, self._base)
		return self._tlevel

	def clone(self) -> 'MultiTone':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = MultiTone(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
