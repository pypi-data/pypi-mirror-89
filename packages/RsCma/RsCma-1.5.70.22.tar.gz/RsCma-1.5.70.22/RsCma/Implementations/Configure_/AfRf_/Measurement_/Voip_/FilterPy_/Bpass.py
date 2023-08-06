from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Bpass:
	"""Bpass commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("bpass", core, parent)

	def get_enable(self) -> bool:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:VOIP:FILTer:BPASs:ENABle \n
		Snippet: value: bool = driver.configure.afRf.measurement.voip.filterPy.bpass.get_enable() \n
		Enables or disables the variable bandpass filter in the VoIP input path. \n
			:return: enable: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:VOIP:FILTer:BPASs:ENABle?')
		return Conversions.str_to_bool(response)

	def set_enable(self, enable: bool) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:VOIP:FILTer:BPASs:ENABle \n
		Snippet: driver.configure.afRf.measurement.voip.filterPy.bpass.set_enable(enable = False) \n
		Enables or disables the variable bandpass filter in the VoIP input path. \n
			:param enable: OFF | ON
		"""
		param = Conversions.bool_to_str(enable)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:VOIP:FILTer:BPASs:ENABle {param}')

	def get_cfrequency(self) -> float:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:VOIP:FILTer:BPASs:CFRequency \n
		Snippet: value: float = driver.configure.afRf.measurement.voip.filterPy.bpass.get_cfrequency() \n
		Configures the center frequency of the variable bandpass filter in the VoIP input path. \n
			:return: frequency: Range: 0 Hz to 21 kHz, Unit: Hz
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:VOIP:FILTer:BPASs:CFRequency?')
		return Conversions.str_to_float(response)

	def set_cfrequency(self, frequency: float) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:VOIP:FILTer:BPASs:CFRequency \n
		Snippet: driver.configure.afRf.measurement.voip.filterPy.bpass.set_cfrequency(frequency = 1.0) \n
		Configures the center frequency of the variable bandpass filter in the VoIP input path. \n
			:param frequency: Range: 0 Hz to 21 kHz, Unit: Hz
		"""
		param = Conversions.decimal_value_to_str(frequency)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:VOIP:FILTer:BPASs:CFRequency {param}')

	def get_bandwidth(self) -> float:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:VOIP:FILTer:BPASs:BWIDth \n
		Snippet: value: float = driver.configure.afRf.measurement.voip.filterPy.bpass.get_bandwidth() \n
		Configures the bandwidth of the variable bandpass filter in the VoIP input path. \n
			:return: bandwidth: Range: 20 Hz to 20 kHz, Unit: Hz
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:VOIP:FILTer:BPASs:BWIDth?')
		return Conversions.str_to_float(response)

	def set_bandwidth(self, bandwidth: float) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:VOIP:FILTer:BPASs:BWIDth \n
		Snippet: driver.configure.afRf.measurement.voip.filterPy.bpass.set_bandwidth(bandwidth = 1.0) \n
		Configures the bandwidth of the variable bandpass filter in the VoIP input path. \n
			:param bandwidth: Range: 20 Hz to 20 kHz, Unit: Hz
		"""
		param = Conversions.decimal_value_to_str(bandwidth)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:VOIP:FILTer:BPASs:BWIDth {param}')
