from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Communicate:
	"""Communicate commands group definition. 17 total commands, 7 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("communicate", core, parent)

	@property
	def net(self):
		"""net commands group. 1 Sub-classes, 5 commands."""
		if not hasattr(self, '_net'):
			from .Communicate_.Net import Net
			self._net = Net(self._core, self._base)
		return self._net

	@property
	def gpib(self):
		"""gpib commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_gpib'):
			from .Communicate_.Gpib import Gpib
			self._gpib = Gpib(self._core, self._base)
		return self._gpib

	@property
	def usb(self):
		"""usb commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_usb'):
			from .Communicate_.Usb import Usb
			self._usb = Usb(self._core, self._base)
		return self._usb

	@property
	def rsib(self):
		"""rsib commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rsib'):
			from .Communicate_.Rsib import Rsib
			self._rsib = Rsib(self._core, self._base)
		return self._rsib

	@property
	def socket(self):
		"""socket commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_socket'):
			from .Communicate_.Socket import Socket
			self._socket = Socket(self._core, self._base)
		return self._socket

	@property
	def vxi(self):
		"""vxi commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_vxi'):
			from .Communicate_.Vxi import Vxi
			self._vxi = Vxi(self._core, self._base)
		return self._vxi

	@property
	def hislip(self):
		"""hislip commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_hislip'):
			from .Communicate_.Hislip import Hislip
			self._hislip = Hislip(self._core, self._base)
		return self._hislip

	def clone(self) -> 'Communicate':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Communicate(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
