from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Application:
	"""Application commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("application", core, parent)

	# noinspection PyTypeChecker
	def get_select(self) -> enums.SubTab:
		"""SCPI: DISPlay:AFRF:MEASurement<Instance>:APPLication:SELect \n
		Snippet: value: enums.SubTab = driver.display.afRf.measurement.application.get_select() \n
		No command help available \n
			:return: sub_tab: No help available
		"""
		response = self._core.io.query_str('DISPlay:AFRF:MEASurement<Instance>:APPLication:SELect?')
		return Conversions.str_to_scalar_enum(response, enums.SubTab)

	def set_select(self, sub_tab: enums.SubTab) -> None:
		"""SCPI: DISPlay:AFRF:MEASurement<Instance>:APPLication:SELect \n
		Snippet: driver.display.afRf.measurement.application.set_select(sub_tab = enums.SubTab.AFResults) \n
		No command help available \n
			:param sub_tab: No help available
		"""
		param = Conversions.enum_scalar_to_str(sub_tab, enums.SubTab)
		self._core.io.write(f'DISPlay:AFRF:MEASurement<Instance>:APPLication:SELect {param}')
