from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Digital:
	"""Digital commands group definition. 2 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("digital", core, parent)

	@property
	def rf(self):
		"""rf commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rf'):
			from .Digital_.Rf import Rf
			self._rf = Rf(self._core, self._base)
		return self._rf

	def get_file(self) -> str:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:DIGital:FILE \n
		Snippet: value: str = driver.source.afRf.generator.digital.get_file() \n
		No command help available \n
			:return: arb_file: No help available
		"""
		response = self._core.io.query_str_with_opc('SOURce:AFRF:GENerator<Instance>:DIGital:FILE?')
		return trim_str_response(response)

	def set_file(self, arb_file: str) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:DIGital:FILE \n
		Snippet: driver.source.afRf.generator.digital.set_file(arb_file = '1') \n
		No command help available \n
			:param arb_file: No help available
		"""
		param = Conversions.value_to_quoted_str(arb_file)
		self._core.io.write_with_opc(f'SOURce:AFRF:GENerator<Instance>:DIGital:FILE {param}')

	def clone(self) -> 'Digital':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Digital(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
