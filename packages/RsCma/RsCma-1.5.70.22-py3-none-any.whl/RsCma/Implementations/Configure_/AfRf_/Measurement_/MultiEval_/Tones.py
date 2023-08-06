from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Tones:
	"""Tones commands group definition. 34 total commands, 11 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("tones", core, parent)

	@property
	def voip(self):
		"""voip commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_voip'):
			from .Tones_.Voip import Voip
			self._voip = Voip(self._core, self._base)
		return self._voip

	@property
	def spdifRight(self):
		"""spdifRight commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_spdifRight'):
			from .Tones_.SpdifRight import SpdifRight
			self._spdifRight = SpdifRight(self._core, self._base)
		return self._spdifRight

	@property
	def spdifLeft(self):
		"""spdifLeft commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_spdifLeft'):
			from .Tones_.SpdifLeft import SpdifLeft
			self._spdifLeft = SpdifLeft(self._core, self._base)
		return self._spdifLeft

	@property
	def audioInput(self):
		"""audioInput commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_audioInput'):
			from .Tones_.AudioInput import AudioInput
			self._audioInput = AudioInput(self._core, self._base)
		return self._audioInput

	@property
	def demodulation(self):
		"""demodulation commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_demodulation'):
			from .Tones_.Demodulation import Demodulation
			self._demodulation = Demodulation(self._core, self._base)
		return self._demodulation

	@property
	def dcs(self):
		"""dcs commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_dcs'):
			from .Tones_.Dcs import Dcs
			self._dcs = Dcs(self._core, self._base)
		return self._dcs

	@property
	def dialing(self):
		"""dialing commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_dialing'):
			from .Tones_.Dialing import Dialing
			self._dialing = Dialing(self._core, self._base)
		return self._dialing

	@property
	def selCall(self):
		"""selCall commands group. 2 Sub-classes, 4 commands."""
		if not hasattr(self, '_selCall'):
			from .Tones_.SelCall import SelCall
			self._selCall = SelCall(self._core, self._base)
		return self._selCall

	@property
	def fdialing(self):
		"""fdialing commands group. 1 Sub-classes, 5 commands."""
		if not hasattr(self, '_fdialing'):
			from .Tones_.Fdialing import Fdialing
			self._fdialing = Fdialing(self._core, self._base)
		return self._fdialing

	@property
	def dtmf(self):
		"""dtmf commands group. 2 Sub-classes, 2 commands."""
		if not hasattr(self, '_dtmf'):
			from .Tones_.Dtmf import Dtmf
			self._dtmf = Dtmf(self._core, self._base)
		return self._dtmf

	@property
	def scal(self):
		"""scal commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_scal'):
			from .Tones_.Scal import Scal
			self._scal = Scal(self._core, self._base)
		return self._scal

	def clone(self) -> 'Tones':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Tones(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
