from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Frequency:
	"""Frequency commands group definition. 8 total commands, 2 Sub-groups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("frequency", core, parent)

	@property
	def span(self):
		"""span commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_span'):
			from .Frequency_.Span import Span
			self._span = Span(self._core, self._base)
		return self._span

	@property
	def marker(self):
		"""marker commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_marker'):
			from .Frequency_.Marker import Marker
			self._marker = Marker(self._core, self._base)
		return self._marker

	def get_center(self) -> float:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:SPECtrum:FREQuency:CENTer \n
		Snippet: value: float = driver.configure.gprfMeasurement.spectrum.frequency.get_center() \n
		Specifies the center frequency of the measurement. You can also configure this setting via method RsCma.Configure.
		GprfMeasurement.RfSettings.frequency. \n
			:return: center_frequency: Range: 100 kHz to 3 GHz, Unit: Hz
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:SPECtrum:FREQuency:CENTer?')
		return Conversions.str_to_float(response)

	def set_center(self, center_frequency: float) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:SPECtrum:FREQuency:CENTer \n
		Snippet: driver.configure.gprfMeasurement.spectrum.frequency.set_center(center_frequency = 1.0) \n
		Specifies the center frequency of the measurement. You can also configure this setting via method RsCma.Configure.
		GprfMeasurement.RfSettings.frequency. \n
			:param center_frequency: Range: 100 kHz to 3 GHz, Unit: Hz
		"""
		param = Conversions.decimal_value_to_str(center_frequency)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:SPECtrum:FREQuency:CENTer {param}')

	def get_start(self) -> float:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:SPECtrum:FREQuency:STARt \n
		Snippet: value: float = driver.configure.gprfMeasurement.spectrum.frequency.get_start() \n
		Specifies the start frequency of the measured span for the frequency sweep mode. \n
			:return: start_frequency: Range: 99500 Hz to 2.9999995 GHz, Unit: Hz
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:SPECtrum:FREQuency:STARt?')
		return Conversions.str_to_float(response)

	def set_start(self, start_frequency: float) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:SPECtrum:FREQuency:STARt \n
		Snippet: driver.configure.gprfMeasurement.spectrum.frequency.set_start(start_frequency = 1.0) \n
		Specifies the start frequency of the measured span for the frequency sweep mode. \n
			:param start_frequency: Range: 99500 Hz to 2.9999995 GHz, Unit: Hz
		"""
		param = Conversions.decimal_value_to_str(start_frequency)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:SPECtrum:FREQuency:STARt {param}')

	def get_stop(self) -> float:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:SPECtrum:FREQuency:STOP \n
		Snippet: value: float = driver.configure.gprfMeasurement.spectrum.frequency.get_stop() \n
		Specifies the stop frequency of the measured span for the frequency sweep mode. \n
			:return: stop_frequency: Range: 100500 Hz to 3.0000005 GHz, Unit: Hz
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:SPECtrum:FREQuency:STOP?')
		return Conversions.str_to_float(response)

	def set_stop(self, stop_frequency: float) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:SPECtrum:FREQuency:STOP \n
		Snippet: driver.configure.gprfMeasurement.spectrum.frequency.set_stop(stop_frequency = 1.0) \n
		Specifies the stop frequency of the measured span for the frequency sweep mode. \n
			:param stop_frequency: Range: 100500 Hz to 3.0000005 GHz, Unit: Hz
		"""
		param = Conversions.decimal_value_to_str(stop_frequency)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:SPECtrum:FREQuency:STOP {param}')

	def get_laspan(self) -> float:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:SPECtrum:FREQuency:LASPan \n
		Snippet: value: float = driver.configure.gprfMeasurement.spectrum.frequency.get_laspan() \n
		No command help available \n
			:return: last_span: No help available
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:SPECtrum:FREQuency:LASPan?')
		return Conversions.str_to_float(response)

	def set_laspan(self, last_span: float) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:SPECtrum:FREQuency:LASPan \n
		Snippet: driver.configure.gprfMeasurement.spectrum.frequency.set_laspan(last_span = 1.0) \n
		No command help available \n
			:param last_span: No help available
		"""
		param = Conversions.decimal_value_to_str(last_span)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:SPECtrum:FREQuency:LASPan {param}')

	def clone(self) -> 'Frequency':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Frequency(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
