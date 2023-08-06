from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MarkerBeacon:
	"""MarkerBeacon commands group definition. 14 total commands, 4 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("markerBeacon", core, parent)

	@property
	def afSettings(self):
		"""afSettings commands group. 1 Sub-classes, 4 commands."""
		if not hasattr(self, '_afSettings'):
			from .MarkerBeacon_.AfSettings import AfSettings
			self._afSettings = AfSettings(self._core, self._base)
		return self._afSettings

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_state'):
			from .MarkerBeacon_.State import State
			self._state = State(self._core, self._base)
		return self._state

	@property
	def rfSettings(self):
		"""rfSettings commands group. 1 Sub-classes, 2 commands."""
		if not hasattr(self, '_rfSettings'):
			from .MarkerBeacon_.RfSettings import RfSettings
			self._rfSettings = RfSettings(self._core, self._base)
		return self._rfSettings

	@property
	def idSignal(self):
		"""idSignal commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_idSignal'):
			from .MarkerBeacon_.IdSignal import IdSignal
			self._idSignal = IdSignal(self._core, self._base)
		return self._idSignal

	def clone(self) -> 'MarkerBeacon':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = MarkerBeacon(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
