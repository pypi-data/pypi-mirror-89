from typing import List

from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.Types import DataType
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sequence:
	"""Sequence commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sequence", core, parent)

	# noinspection PyTypeChecker
	class ResultData(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: See 'Reliability indicator values'
			- Length: int: Length of the tone sequence (number of digits)
			- Sequence: List[str]: Comma-separated list of 42 strings Each string indicates a dialed digit."""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_int('Length'),
			ArgStruct('Sequence', DataType.StringList, None, False, True, 1)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Length: int = None
			self.Sequence: List[str] = None

	def fetch(self) -> ResultData:
		"""SCPI: FETCh:AFRF:MEASurement<Instance>:MEValuation:TONes:SINRight:SEQuence \n
		Snippet: value: ResultData = driver.afRf.measurement.multiEval.tones.spdifRight.sequence.fetch() \n
		Queries the digit results of a tone sequence analysis. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'FETCh:AFRF:MEASurement<Instance>:MEValuation:TONes:SINRight:SEQuence?', self.__class__.ResultData())

	def read(self) -> ResultData:
		"""SCPI: READ:AFRF:MEASurement<Instance>:MEValuation:TONes:SINRight:SEQuence \n
		Snippet: value: ResultData = driver.afRf.measurement.multiEval.tones.spdifRight.sequence.read() \n
		Queries the digit results of a tone sequence analysis. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'READ:AFRF:MEASurement<Instance>:MEValuation:TONes:SINRight:SEQuence?', self.__class__.ResultData())
