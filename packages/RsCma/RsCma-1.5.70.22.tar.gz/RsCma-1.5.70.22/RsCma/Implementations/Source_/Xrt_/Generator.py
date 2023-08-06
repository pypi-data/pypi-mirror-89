from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Generator:
	"""Generator commands group definition. 21 total commands, 4 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("generator", core, parent)

	@property
	def reliability(self):
		"""reliability commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_reliability'):
			from .Generator_.Reliability import Reliability
			self._reliability = Reliability(self._core, self._base)
		return self._reliability

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_state'):
			from .Generator_.State import State
			self._state = State(self._core, self._base)
		return self._state

	@property
	def rfSettings(self):
		"""rfSettings commands group. 1 Sub-classes, 2 commands."""
		if not hasattr(self, '_rfSettings'):
			from .Generator_.RfSettings import RfSettings
			self._rfSettings = RfSettings(self._core, self._base)
		return self._rfSettings

	@property
	def arb(self):
		"""arb commands group. 3 Sub-classes, 6 commands."""
		if not hasattr(self, '_arb'):
			from .Generator_.Arb import Arb
			self._arb = Arb(self._core, self._base)
		return self._arb

	# noinspection PyTypeChecker
	def get_dsource(self) -> enums.DigitalSource:
		"""SCPI: SOURce:XRT:GENerator<Instance>:DSOurce \n
		Snippet: value: enums.DigitalSource = driver.source.xrt.generator.get_dsource() \n
		No command help available \n
			:return: dsource: No help available
		"""
		response = self._core.io.query_str('SOURce:XRT:GENerator<Instance>:DSOurce?')
		return Conversions.str_to_scalar_enum(response, enums.DigitalSource)

	def set_dsource(self, dsource: enums.DigitalSource) -> None:
		"""SCPI: SOURce:XRT:GENerator<Instance>:DSOurce \n
		Snippet: driver.source.xrt.generator.set_dsource(dsource = enums.DigitalSource.ARB) \n
		No command help available \n
			:param dsource: No help available
		"""
		param = Conversions.enum_scalar_to_str(dsource, enums.DigitalSource)
		self._core.io.write(f'SOURce:XRT:GENerator<Instance>:DSOurce {param}')

	def clone(self) -> 'Generator':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Generator(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
