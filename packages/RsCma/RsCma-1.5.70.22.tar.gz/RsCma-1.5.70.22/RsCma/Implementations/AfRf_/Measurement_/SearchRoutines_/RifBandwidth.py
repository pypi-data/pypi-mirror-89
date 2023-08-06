from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RifBandwidth:
	"""RifBandwidth commands group definition. 8 total commands, 6 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rifBandwidth", core, parent)

	@property
	def frequency(self):
		"""frequency commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_frequency'):
			from .RifBandwidth_.Frequency import Frequency
			self._frequency = Frequency(self._core, self._base)
		return self._frequency

	@property
	def slevel(self):
		"""slevel commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_slevel'):
			from .RifBandwidth_.Slevel import Slevel
			self._slevel = Slevel(self._core, self._base)
		return self._slevel

	@property
	def nlevel(self):
		"""nlevel commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_nlevel'):
			from .RifBandwidth_.Nlevel import Nlevel
			self._nlevel = Nlevel(self._core, self._base)
		return self._nlevel

	@property
	def bandwidth(self):
		"""bandwidth commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bandwidth'):
			from .RifBandwidth_.Bandwidth import Bandwidth
			self._bandwidth = Bandwidth(self._core, self._base)
		return self._bandwidth

	@property
	def coffset(self):
		"""coffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_coffset'):
			from .RifBandwidth_.Coffset import Coffset
			self._coffset = Coffset(self._core, self._base)
		return self._coffset

	@property
	def signalQuality(self):
		"""signalQuality commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_signalQuality'):
			from .RifBandwidth_.SignalQuality import SignalQuality
			self._signalQuality = SignalQuality(self._core, self._base)
		return self._signalQuality

	def clone(self) -> 'RifBandwidth':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = RifBandwidth(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
