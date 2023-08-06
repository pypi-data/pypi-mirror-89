from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FreqSweep:
	"""FreqSweep commands group definition. 6 total commands, 3 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("freqSweep", core, parent)

	@property
	def rbw(self):
		"""rbw commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_rbw'):
			from .FreqSweep_.Rbw import Rbw
			self._rbw = Rbw(self._core, self._base)
		return self._rbw

	@property
	def vbw(self):
		"""vbw commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_vbw'):
			from .FreqSweep_.Vbw import Vbw
			self._vbw = Vbw(self._core, self._base)
		return self._vbw

	@property
	def swt(self):
		"""swt commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_swt'):
			from .FreqSweep_.Swt import Swt
			self._swt = Swt(self._core, self._base)
		return self._swt

	def clone(self) -> 'FreqSweep':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = FreqSweep(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
