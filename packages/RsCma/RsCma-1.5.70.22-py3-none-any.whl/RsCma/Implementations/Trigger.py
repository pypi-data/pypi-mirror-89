from ..Internal.Core import Core
from ..Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Trigger:
	"""Trigger commands group definition. 74 total commands, 3 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("trigger", core, parent)

	@property
	def afRf(self):
		"""afRf commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_afRf'):
			from .Trigger_.AfRf import AfRf
			self._afRf = AfRf(self._core, self._base)
		return self._afRf

	@property
	def base(self):
		"""base commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_base'):
			from .Trigger_.Base import Base
			self._base = Base(self._core, self._base)
		return self._base

	@property
	def gprfMeasurement(self):
		"""gprfMeasurement commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_gprfMeasurement'):
			from .Trigger_.GprfMeasurement import GprfMeasurement
			self._gprfMeasurement = GprfMeasurement(self._core, self._base)
		return self._gprfMeasurement

	def clone(self) -> 'Trigger':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Trigger(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
