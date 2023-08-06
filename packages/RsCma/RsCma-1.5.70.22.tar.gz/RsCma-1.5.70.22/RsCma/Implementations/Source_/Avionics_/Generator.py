from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Generator:
	"""Generator commands group definition. 74 total commands, 4 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("generator", core, parent)

	@property
	def rfSettings(self):
		"""rfSettings commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_rfSettings'):
			from .Generator_.RfSettings import RfSettings
			self._rfSettings = RfSettings(self._core, self._base)
		return self._rfSettings

	@property
	def vor(self):
		"""vor commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_vor'):
			from .Generator_.Vor import Vor
			self._vor = Vor(self._core, self._base)
		return self._vor

	@property
	def ils(self):
		"""ils commands group. 3 Sub-classes, 2 commands."""
		if not hasattr(self, '_ils'):
			from .Generator_.Ils import Ils
			self._ils = Ils(self._core, self._base)
		return self._ils

	@property
	def markerBeacon(self):
		"""markerBeacon commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_markerBeacon'):
			from .Generator_.MarkerBeacon import MarkerBeacon
			self._markerBeacon = MarkerBeacon(self._core, self._base)
		return self._markerBeacon

	def clone(self) -> 'Generator':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Generator(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
