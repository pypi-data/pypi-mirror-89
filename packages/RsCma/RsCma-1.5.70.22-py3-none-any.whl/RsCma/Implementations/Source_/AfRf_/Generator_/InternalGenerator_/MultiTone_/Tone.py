from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.RepeatedCapability import RepeatedCapability
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Tone:
	"""Tone commands group definition. 2 total commands, 2 Sub-groups, 0 group commands
	Repeated Capability: ToneNumber, default value after init: ToneNumber.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("tone", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_toneNumber_get', 'repcap_toneNumber_set', repcap.ToneNumber.Nr1)

	def repcap_toneNumber_set(self, enum_value: repcap.ToneNumber) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to ToneNumber.Default
		Default value after init: ToneNumber.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_toneNumber_get(self) -> repcap.ToneNumber:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def enable(self):
		"""enable commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_enable'):
			from .Tone_.Enable import Enable
			self._enable = Enable(self._core, self._base)
		return self._enable

	@property
	def all(self):
		"""all commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_all'):
			from .Tone_.All import All
			self._all = All(self._core, self._base)
		return self._all

	def clone(self) -> 'Tone':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Tone(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
