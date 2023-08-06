from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AmPoints:
	"""AmPoints commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("amPoints", core, parent)

	def get_enable(self) -> bool:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:AMPoints:ENABle \n
		Snippet: value: bool = driver.configure.afRf.measurement.searchRoutines.amPoints.get_enable() \n
		If enabled, the search granularity is decreased (smaller increments/decrements, more measurement steps) . \n
			:return: enable: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:SROutines:AMPoints:ENABle?')
		return Conversions.str_to_bool(response)

	def set_enable(self, enable: bool) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:AMPoints:ENABle \n
		Snippet: driver.configure.afRf.measurement.searchRoutines.amPoints.set_enable(enable = False) \n
		If enabled, the search granularity is decreased (smaller increments/decrements, more measurement steps) . \n
			:param enable: OFF | ON
		"""
		param = Conversions.bool_to_str(enable)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:SROutines:AMPoints:ENABle {param}')
