from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal.Utilities import trim_str_response
from ...Internal.StructBase import StructBase
from ...Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ExtPwrSensor:
	"""ExtPwrSensor commands group definition. 8 total commands, 1 Sub-groups, 6 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("extPwrSensor", core, parent)

	@property
	def state(self):
		"""state commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .ExtPwrSensor_.State import State
			self._state = State(self._core, self._base)
		return self._state

	def initiate(self) -> None:
		"""SCPI: INITiate:GPRF:MEASurement<Instance>:EPSensor \n
		Snippet: driver.gprfMeasurement.extPwrSensor.initiate() \n
		Starts or continues the EPS measurement. \n
		"""
		self._core.io.write(f'INITiate:GPRF:MEASurement<Instance>:EPSensor')

	def initiate_with_opc(self) -> None:
		"""SCPI: INITiate:GPRF:MEASurement<Instance>:EPSensor \n
		Snippet: driver.gprfMeasurement.extPwrSensor.initiate_with_opc() \n
		Starts or continues the EPS measurement. \n
		Same as initiate, but waits for the operation to complete before continuing further. Use the RsCma.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'INITiate:GPRF:MEASurement<Instance>:EPSensor')

	def stop(self) -> None:
		"""SCPI: STOP:GPRF:MEASurement<Instance>:EPSensor \n
		Snippet: driver.gprfMeasurement.extPwrSensor.stop() \n
		Pauses the EPS measurement. \n
		"""
		self._core.io.write(f'STOP:GPRF:MEASurement<Instance>:EPSensor')

	def stop_with_opc(self) -> None:
		"""SCPI: STOP:GPRF:MEASurement<Instance>:EPSensor \n
		Snippet: driver.gprfMeasurement.extPwrSensor.stop_with_opc() \n
		Pauses the EPS measurement. \n
		Same as stop, but waits for the operation to complete before continuing further. Use the RsCma.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'STOP:GPRF:MEASurement<Instance>:EPSensor')

	def abort(self) -> None:
		"""SCPI: ABORt:GPRF:MEASurement<Instance>:EPSensor \n
		Snippet: driver.gprfMeasurement.extPwrSensor.abort() \n
		Stops the EPS measurement. \n
		"""
		self._core.io.write(f'ABORt:GPRF:MEASurement<Instance>:EPSensor')

	def abort_with_opc(self) -> None:
		"""SCPI: ABORt:GPRF:MEASurement<Instance>:EPSensor \n
		Snippet: driver.gprfMeasurement.extPwrSensor.abort_with_opc() \n
		Stops the EPS measurement. \n
		Same as abort, but waits for the operation to complete before continuing further. Use the RsCma.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'ABORt:GPRF:MEASurement<Instance>:EPSensor')

	def get_idn(self) -> str:
		"""SCPI: FETCh:GPRF:MEASurement<Instance>:EPSensor:IDN \n
		Snippet: value: str = driver.gprfMeasurement.extPwrSensor.get_idn() \n
		Queries the identification string of the connected external power sensor. \n
			:return: idn: String parameter
		"""
		response = self._core.io.query_str('FETCh:GPRF:MEASurement<Instance>:EPSensor:IDN?')
		return trim_str_response(response)

	# noinspection PyTypeChecker
	class ResultData(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: See 'Reliability indicator values'
			- Current_Power: float: Sensor power in the last measurement interval Unit: dBm
			- Average_Power: float: Average of all CurrentPower values within the last measurement cycle Unit: dBm
			- Minimum_Power: float: Minimum CurrentPower value since the start of the measurement Unit: dBm
			- Maximum_Power: float: Maximum CurrentPower value since the start of the measurement Unit: dBm
			- Elapsed_Stat: int: Elapsed statistic count (progress bar) Range: 0 to configured statistic count"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float('Current_Power'),
			ArgStruct.scalar_float('Average_Power'),
			ArgStruct.scalar_float('Minimum_Power'),
			ArgStruct.scalar_float('Maximum_Power'),
			ArgStruct.scalar_int('Elapsed_Stat')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Current_Power: float = None
			self.Average_Power: float = None
			self.Minimum_Power: float = None
			self.Maximum_Power: float = None
			self.Elapsed_Stat: int = None

	def fetch(self) -> ResultData:
		"""SCPI: FETCh:GPRF:MEASurement<Instance>:EPSensor \n
		Snippet: value: ResultData = driver.gprfMeasurement.extPwrSensor.fetch() \n
		Return all EPS measurement results. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'FETCh:GPRF:MEASurement<Instance>:EPSensor?', self.__class__.ResultData())

	def read(self) -> ResultData:
		"""SCPI: READ:GPRF:MEASurement<Instance>:EPSensor \n
		Snippet: value: ResultData = driver.gprfMeasurement.extPwrSensor.read() \n
		Return all EPS measurement results. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'READ:GPRF:MEASurement<Instance>:EPSensor?', self.__class__.ResultData())

	def clone(self) -> 'ExtPwrSensor':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ExtPwrSensor(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
