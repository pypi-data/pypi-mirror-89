from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mtones:
	"""Mtones commands group definition. 24 total commands, 3 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mtones", core, parent)

	@property
	def audioInput(self):
		"""audioInput commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_audioInput'):
			from .Mtones_.AudioInput import AudioInput
			self._audioInput = AudioInput(self._core, self._base)
		return self._audioInput

	@property
	def spdifLeft(self):
		"""spdifLeft commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_spdifLeft'):
			from .Mtones_.SpdifLeft import SpdifLeft
			self._spdifLeft = SpdifLeft(self._core, self._base)
		return self._spdifLeft

	@property
	def spdifRight(self):
		"""spdifRight commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_spdifRight'):
			from .Mtones_.SpdifRight import SpdifRight
			self._spdifRight = SpdifRight(self._core, self._base)
		return self._spdifRight

	def clone(self) -> 'Mtones':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Mtones(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
