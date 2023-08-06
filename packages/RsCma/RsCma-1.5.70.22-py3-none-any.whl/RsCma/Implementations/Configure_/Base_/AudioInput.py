from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.RepeatedCapability import RepeatedCapability
from .... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AudioInput:
	"""AudioInput commands group definition. 4 total commands, 3 Sub-groups, 0 group commands
	Repeated Capability: AudioInput, default value after init: AudioInput.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("audioInput", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_audioInput_get', 'repcap_audioInput_set', repcap.AudioInput.Nr1)

	def repcap_audioInput_set(self, enum_value: repcap.AudioInput) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to AudioInput.Default
		Default value after init: AudioInput.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_audioInput_get(self) -> repcap.AudioInput:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def ecircuitry(self):
		"""ecircuitry commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ecircuitry'):
			from .AudioInput_.Ecircuitry import Ecircuitry
			self._ecircuitry = Ecircuitry(self._core, self._base)
		return self._ecircuitry

	@property
	def zbox(self):
		"""zbox commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_zbox'):
			from .AudioInput_.Zbox import Zbox
			self._zbox = Zbox(self._core, self._base)
		return self._zbox

	@property
	def limpedance(self):
		"""limpedance commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_limpedance'):
			from .AudioInput_.Limpedance import Limpedance
			self._limpedance = Limpedance(self._core, self._base)
		return self._limpedance

	def clone(self) -> 'AudioInput':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = AudioInput(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
