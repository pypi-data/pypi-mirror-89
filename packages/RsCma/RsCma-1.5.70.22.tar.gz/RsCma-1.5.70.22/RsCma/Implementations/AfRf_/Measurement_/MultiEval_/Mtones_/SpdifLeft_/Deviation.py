from typing import List

from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.Types import DataType
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Deviation:
	"""Deviation commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("deviation", core, parent)

	# noinspection PyTypeChecker
	class ResultData(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: See 'Reliability indicator values'
			- Freq: List[float]: Tone frequency Unit: Hz
			- Level: List[float]: Audio level measured at the tone frequency Unit: dBFS"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct('Freq', DataType.FloatList, None, False, True, 1),
			ArgStruct('Level', DataType.FloatList, None, False, True, 1)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Freq: List[float] = None
			self.Level: List[float] = None

	def fetch(self) -> ResultData:
		"""SCPI: FETCh:AFRF:MEASurement<Instance>:MEValuation:MTONes:SINLeft:DEViation \n
		Snippet: value: ResultData = driver.afRf.measurement.multiEval.mtones.spdifLeft.deviation.fetch() \n
		Queries the multitone results for the left SPDIF channel. The results are returned in the following order: <Reliability>,
		{<Freq>, <Level>}Tone 1, ..., {<Freq>, <Level>}Tone 20 \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'FETCh:AFRF:MEASurement<Instance>:MEValuation:MTONes:SINLeft:DEViation?', self.__class__.ResultData())

	def read(self) -> ResultData:
		"""SCPI: READ:AFRF:MEASurement<Instance>:MEValuation:MTONes:SINLeft:DEViation \n
		Snippet: value: ResultData = driver.afRf.measurement.multiEval.mtones.spdifLeft.deviation.read() \n
		Queries the multitone results for the left SPDIF channel. The results are returned in the following order: <Reliability>,
		{<Freq>, <Level>}Tone 1, ..., {<Freq>, <Level>}Tone 20 \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'READ:AFRF:MEASurement<Instance>:MEValuation:MTONes:SINLeft:DEViation?', self.__class__.ResultData())
