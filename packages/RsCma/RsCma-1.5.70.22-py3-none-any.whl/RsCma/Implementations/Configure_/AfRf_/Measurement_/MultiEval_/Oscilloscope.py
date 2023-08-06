from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Oscilloscope:
	"""Oscilloscope commands group definition. 8 total commands, 4 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("oscilloscope", core, parent)

	@property
	def demodulation(self):
		"""demodulation commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_demodulation'):
			from .Oscilloscope_.Demodulation import Demodulation
			self._demodulation = Demodulation(self._core, self._base)
		return self._demodulation

	@property
	def audioInput(self):
		"""audioInput commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_audioInput'):
			from .Oscilloscope_.AudioInput import AudioInput
			self._audioInput = AudioInput(self._core, self._base)
		return self._audioInput

	@property
	def spdif(self):
		"""spdif commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_spdif'):
			from .Oscilloscope_.Spdif import Spdif
			self._spdif = Spdif(self._core, self._base)
		return self._spdif

	@property
	def voip(self):
		"""voip commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_voip'):
			from .Oscilloscope_.Voip import Voip
			self._voip = Voip(self._core, self._base)
		return self._voip

	def clone(self) -> 'Oscilloscope':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Oscilloscope(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
