from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class State:
	"""State commands group definition. 2 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("state", core, parent)

	@property
	def all(self):
		"""all commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_all'):
			from .State_.All import All
			self._all = All(self._core, self._base)
		return self._all

	# noinspection PyTypeChecker
	def fetch(self) -> enums.ResourceState:
		"""SCPI: FETCh:GPRF:MEASurement<Instance>:ACP:STATe \n
		Snippet: value: enums.ResourceState = driver.gprfMeasurement.acp.state.fetch() \n
		Queries the main ACP measurement state. \n
			:return: meas_state: OFF | RDY | RUN OFF Measurement is off RDY Measurement has been paused or is finished RUN Measurement is running"""
		response = self._core.io.query_str(f'FETCh:GPRF:MEASurement<Instance>:ACP:STATe?')
		return Conversions.str_to_scalar_enum(response, enums.ResourceState)

	def clone(self) -> 'State':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = State(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
