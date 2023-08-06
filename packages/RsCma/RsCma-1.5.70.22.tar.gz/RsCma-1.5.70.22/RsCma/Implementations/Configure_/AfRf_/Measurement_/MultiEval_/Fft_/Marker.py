from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.RepeatedCapability import RepeatedCapability
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Marker:
	"""Marker commands group definition. 2 total commands, 2 Sub-groups, 0 group commands
	Repeated Capability: MarkerOther, default value after init: MarkerOther.Nr2"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("marker", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_markerOther_get', 'repcap_markerOther_set', repcap.MarkerOther.Nr2)

	def repcap_markerOther_set(self, enum_value: repcap.MarkerOther) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to MarkerOther.Default
		Default value after init: MarkerOther.Nr2"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_markerOther_get(self) -> repcap.MarkerOther:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def enable(self):
		"""enable commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_enable'):
			from .Marker_.Enable import Enable
			self._enable = Enable(self._core, self._base)
		return self._enable

	@property
	def placement(self):
		"""placement commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_placement'):
			from .Marker_.Placement import Placement
			self._placement = Placement(self._core, self._base)
		return self._placement

	def clone(self) -> 'Marker':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Marker(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
