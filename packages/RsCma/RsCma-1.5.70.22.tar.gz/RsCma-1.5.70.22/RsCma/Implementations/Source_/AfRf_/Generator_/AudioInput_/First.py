from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class First:
	"""First commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("first", core, parent)

	def get_mlevel(self) -> float:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:AIN:FIRSt:MLEVel \n
		Snippet: value: float = driver.source.afRf.generator.audioInput.first.get_mlevel() \n
		Specifies the maximum expected level for the AF1 IN connector. This setting is only relevant, if auto ranging is disabled. \n
			:return: level: Maximum expected level Range: 10E-6 V to 43 V, Unit: V
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:AIN:FIRSt:MLEVel?')
		return Conversions.str_to_float(response)

	def set_mlevel(self, level: float) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:AIN:FIRSt:MLEVel \n
		Snippet: driver.source.afRf.generator.audioInput.first.set_mlevel(level = 1.0) \n
		Specifies the maximum expected level for the AF1 IN connector. This setting is only relevant, if auto ranging is disabled. \n
			:param level: Maximum expected level Range: 10E-6 V to 43 V, Unit: V
		"""
		param = Conversions.decimal_value_to_str(level)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:AIN:FIRSt:MLEVel {param}')
