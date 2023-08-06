from ..Internal.Core import Core
from ..Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Configure:
	"""Configure commands group definition. 480 total commands, 5 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("configure", core, parent)

	@property
	def afRf(self):
		"""afRf commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_afRf'):
			from .Configure_.AfRf import AfRf
			self._afRf = AfRf(self._core, self._base)
		return self._afRf

	@property
	def base(self):
		"""base commands group. 11 Sub-classes, 2 commands."""
		if not hasattr(self, '_base'):
			from .Configure_.Base import Base
			self._base = Base(self._core, self._base)
		return self._base

	@property
	def sequencer(self):
		"""sequencer commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_sequencer'):
			from .Configure_.Sequencer import Sequencer
			self._sequencer = Sequencer(self._core, self._base)
		return self._sequencer

	@property
	def gprfMeasurement(self):
		"""gprfMeasurement commands group. 8 Sub-classes, 1 commands."""
		if not hasattr(self, '_gprfMeasurement'):
			from .Configure_.GprfMeasurement import GprfMeasurement
			self._gprfMeasurement = GprfMeasurement(self._core, self._base)
		return self._gprfMeasurement

	@property
	def display(self):
		"""display commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_display'):
			from .Configure_.Display import Display
			self._display = Display(self._core, self._base)
		return self._display

	def clone(self) -> 'Configure':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Configure(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
