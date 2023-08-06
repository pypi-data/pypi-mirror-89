from typing import List

from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.RepeatedCapability import RepeatedCapability
from .... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ttl:
	"""Ttl commands group definition. 3 total commands, 2 Sub-groups, 1 group commands
	Repeated Capability: TTL, default value after init: TTL.Ix1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ttl", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_tTL_get', 'repcap_tTL_set', repcap.TTL.Ix1)

	def repcap_tTL_set(self, enum_value: repcap.TTL) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to TTL.Default
		Default value after init: TTL.Ix1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_tTL_get(self) -> repcap.TTL:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def update(self):
		"""update commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_update'):
			from .Ttl_.Update import Update
			self._update = Update(self._core, self._base)
		return self._update

	@property
	def direction(self):
		"""direction commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_direction'):
			from .Ttl_.Direction import Direction
			self._direction = Direction(self._core, self._base)
		return self._direction

	def set(self, pin_state: List[bool], tTL=repcap.TTL.Default) -> None:
		"""SCPI: CONFigure:BASE:TTL<Index> \n
		Snippet: driver.configure.base.ttl.set(pin_state = [True, False, True], tTL = repcap.TTL.Default) \n
		Sets or queries the individual bits of a TTL register of the CONTROL connector. A register with direction IN can only be
		queried. A register with direction OUT can be configured. Before querying the input register, update the values, see
		method RsCma.Configure.Base.Ttl.Update.set. \n
			:param pin_state: OFF | ON Comma-separated list of four values, one per bit of the register Register 1: Pin 1, 2, 3, 4 Register 2: Pin 14, 15, 16, 17 OFF = 0, ON = 1
			:param tTL: optional repeated capability selector. Default value: Ix1 (settable in the interface 'Ttl')"""
		param = Conversions.list_to_csv_str(pin_state)
		tTL_cmd_val = self._base.get_repcap_cmd_value(tTL, repcap.TTL)
		self._core.io.write(f'CONFigure:BASE:TTL{tTL_cmd_val} {param}')

	def get(self, tTL=repcap.TTL.Default) -> List[bool]:
		"""SCPI: CONFigure:BASE:TTL<Index> \n
		Snippet: value: List[bool] = driver.configure.base.ttl.get(tTL = repcap.TTL.Default) \n
		Sets or queries the individual bits of a TTL register of the CONTROL connector. A register with direction IN can only be
		queried. A register with direction OUT can be configured. Before querying the input register, update the values, see
		method RsCma.Configure.Base.Ttl.Update.set. \n
			:param tTL: optional repeated capability selector. Default value: Ix1 (settable in the interface 'Ttl')
			:return: pin_state: OFF | ON Comma-separated list of four values, one per bit of the register Register 1: Pin 1, 2, 3, 4 Register 2: Pin 14, 15, 16, 17 OFF = 0, ON = 1"""
		tTL_cmd_val = self._base.get_repcap_cmd_value(tTL, repcap.TTL)
		response = self._core.io.query_str(f'CONFigure:BASE:TTL{tTL_cmd_val}?')
		return Conversions.str_to_bool_list(response)

	def clone(self) -> 'Ttl':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Ttl(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
