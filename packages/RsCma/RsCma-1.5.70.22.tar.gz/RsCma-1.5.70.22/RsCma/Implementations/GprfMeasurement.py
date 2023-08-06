from ..Internal.Core import Core
from ..Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class GprfMeasurement:
	"""GprfMeasurement commands group definition. 198 total commands, 7 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("gprfMeasurement", core, parent)

	@property
	def spectrum(self):
		"""spectrum commands group. 11 Sub-classes, 3 commands."""
		if not hasattr(self, '_spectrum'):
			from .GprfMeasurement_.Spectrum import Spectrum
			self._spectrum = Spectrum(self._core, self._base)
		return self._spectrum

	@property
	def extPwrSensor(self):
		"""extPwrSensor commands group. 1 Sub-classes, 6 commands."""
		if not hasattr(self, '_extPwrSensor'):
			from .GprfMeasurement_.ExtPwrSensor import ExtPwrSensor
			self._extPwrSensor = ExtPwrSensor(self._core, self._base)
		return self._extPwrSensor

	@property
	def nrt(self):
		"""nrt commands group. 3 Sub-classes, 4 commands."""
		if not hasattr(self, '_nrt'):
			from .GprfMeasurement_.Nrt import Nrt
			self._nrt = Nrt(self._core, self._base)
		return self._nrt

	@property
	def power(self):
		"""power commands group. 8 Sub-classes, 3 commands."""
		if not hasattr(self, '_power'):
			from .GprfMeasurement_.Power import Power
			self._power = Power(self._core, self._base)
		return self._power

	@property
	def fftSpecAn(self):
		"""fftSpecAn commands group. 7 Sub-classes, 3 commands."""
		if not hasattr(self, '_fftSpecAn'):
			from .GprfMeasurement_.FftSpecAn import FftSpecAn
			self._fftSpecAn = FftSpecAn(self._core, self._base)
		return self._fftSpecAn

	@property
	def acp(self):
		"""acp commands group. 4 Sub-classes, 3 commands."""
		if not hasattr(self, '_acp'):
			from .GprfMeasurement_.Acp import Acp
			self._acp = Acp(self._core, self._base)
		return self._acp

	@property
	def iqRecorder(self):
		"""iqRecorder commands group. 5 Sub-classes, 5 commands."""
		if not hasattr(self, '_iqRecorder'):
			from .GprfMeasurement_.IqRecorder import IqRecorder
			self._iqRecorder = IqRecorder(self._core, self._base)
		return self._iqRecorder

	def clone(self) -> 'GprfMeasurement':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = GprfMeasurement(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
