from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.StructBase import StructBase
from ........Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Deviation:
	"""Deviation commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("deviation", core, parent)

	# noinspection PyTypeChecker
	class ResultData(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: No parameter help available
			- Level_Peak: float: No parameter help available
			- Level_Rms: float: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float('Level_Peak'),
			ArgStruct.scalar_float('Level_Rms')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Level_Peak: float = None
			self.Level_Rms: float = None

	def fetch(self) -> ResultData:
		"""SCPI: FETCh:AFRF:MEASurement<Instance>:MEValuation:SINRight:LEVel:DELTa:DEViation \n
		Snippet: value: ResultData = driver.afRf.measurement.multiEval.spdifRight.level.delta.deviation.fetch() \n
		No command help available \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'FETCh:AFRF:MEASurement<Instance>:MEValuation:SINRight:LEVel:DELTa:DEViation?', self.__class__.ResultData())

	def read(self) -> ResultData:
		"""SCPI: READ:AFRF:MEASurement<Instance>:MEValuation:SINRight:LEVel:DELTa:DEViation \n
		Snippet: value: ResultData = driver.afRf.measurement.multiEval.spdifRight.level.delta.deviation.read() \n
		No command help available \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'READ:AFRF:MEASurement<Instance>:MEValuation:SINRight:LEVel:DELTa:DEViation?', self.__class__.ResultData())
