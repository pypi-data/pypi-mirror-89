from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MultiTone:
	"""MultiTone commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("multiTone", core, parent)

	def get_scount(self) -> int:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:MTONe:SCOunt \n
		Snippet: value: int = driver.configure.afRf.measurement.multiEval.multiTone.get_scount() \n
		Specifies the number of measurement intervals per measurement cycle for multitone results. One measurement interval
		delivers a single 'Current' value for each test tone. \n
			:return: statistic_count: Range: 1 to 1000
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:MEValuation:MTONe:SCOunt?')
		return Conversions.str_to_int(response)

	def set_scount(self, statistic_count: int) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:MTONe:SCOunt \n
		Snippet: driver.configure.afRf.measurement.multiEval.multiTone.set_scount(statistic_count = 1) \n
		Specifies the number of measurement intervals per measurement cycle for multitone results. One measurement interval
		delivers a single 'Current' value for each test tone. \n
			:param statistic_count: Range: 1 to 1000
		"""
		param = Conversions.decimal_value_to_str(statistic_count)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:MEValuation:MTONe:SCOunt {param}')
