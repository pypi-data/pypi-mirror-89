from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PeakSearch:
	"""PeakSearch commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("peakSearch", core, parent)

	def get_noa_markers(self) -> int:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:FFTSanalyzer:PSEarch:NOAMarkers \n
		Snippet: value: int = driver.configure.gprfMeasurement.fftSpecAn.peakSearch.get_noa_markers() \n
		Specifies the number of active peak search markers. \n
			:return: no_active_markers: Range: 0 to 5
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:FFTSanalyzer:PSEarch:NOAMarkers?')
		return Conversions.str_to_int(response)

	def set_noa_markers(self, no_active_markers: int) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:FFTSanalyzer:PSEarch:NOAMarkers \n
		Snippet: driver.configure.gprfMeasurement.fftSpecAn.peakSearch.set_noa_markers(no_active_markers = 1) \n
		Specifies the number of active peak search markers. \n
			:param no_active_markers: Range: 0 to 5
		"""
		param = Conversions.decimal_value_to_str(no_active_markers)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:FFTSanalyzer:PSEarch:NOAMarkers {param}')

	# noinspection PyTypeChecker
	class ValueStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Full_Span_Enable_0: bool: OFF | ON Configures marker 0 OFF Search from PeakRangeFrom0 to PeakRangeTo0 ON Search the full frequency span
			- Peak_Range_From_0: float: Start of peak search range for FullSpanEnable0 = OFF Range: - span / 2 to span / 2, Unit: Hz
			- Peak_Range_To_0: float: End of peak search range for FullSpanEnable0 = OFF Range: - span / 2 to span / 2, Unit: Hz
			- Full_Span_Enable_1: bool: Configures marker 1
			- Peak_Range_From_1: float: No parameter help available
			- Peak_Range_To_1: float: No parameter help available
			- Full_Span_Enable_2: bool: Configures marker 2
			- Peak_Range_From_2: float: No parameter help available
			- Peak_Range_To_2: float: No parameter help available
			- Full_Span_Enable_3: bool: Configures marker 3
			- Peak_Range_From_3: float: No parameter help available
			- Peak_Range_To_3: float: No parameter help available
			- Full_Span_Enable_4: bool: Configures marker 4
			- Peak_Range_From_4: float: No parameter help available
			- Peak_Range_To_4: float: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Full_Span_Enable_0'),
			ArgStruct.scalar_float('Peak_Range_From_0'),
			ArgStruct.scalar_float('Peak_Range_To_0'),
			ArgStruct.scalar_bool('Full_Span_Enable_1'),
			ArgStruct.scalar_float('Peak_Range_From_1'),
			ArgStruct.scalar_float('Peak_Range_To_1'),
			ArgStruct.scalar_bool('Full_Span_Enable_2'),
			ArgStruct.scalar_float('Peak_Range_From_2'),
			ArgStruct.scalar_float('Peak_Range_To_2'),
			ArgStruct.scalar_bool('Full_Span_Enable_3'),
			ArgStruct.scalar_float('Peak_Range_From_3'),
			ArgStruct.scalar_float('Peak_Range_To_3'),
			ArgStruct.scalar_bool('Full_Span_Enable_4'),
			ArgStruct.scalar_float('Peak_Range_From_4'),
			ArgStruct.scalar_float('Peak_Range_To_4')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Full_Span_Enable_0: bool = None
			self.Peak_Range_From_0: float = None
			self.Peak_Range_To_0: float = None
			self.Full_Span_Enable_1: bool = None
			self.Peak_Range_From_1: float = None
			self.Peak_Range_To_1: float = None
			self.Full_Span_Enable_2: bool = None
			self.Peak_Range_From_2: float = None
			self.Peak_Range_To_2: float = None
			self.Full_Span_Enable_3: bool = None
			self.Peak_Range_From_3: float = None
			self.Peak_Range_To_3: float = None
			self.Full_Span_Enable_4: bool = None
			self.Peak_Range_From_4: float = None
			self.Peak_Range_To_4: float = None

	def get_value(self) -> ValueStruct:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:FFTSanalyzer:PSEarch \n
		Snippet: value: ValueStruct = driver.configure.gprfMeasurement.fftSpecAn.peakSearch.get_value() \n
		Defines the peak search ranges for the five markers. In this command, the markers are labeled 0 to 4. At the graphical
		user interface, they are labeled 1 to 5. The allowed ranges, reset values and default units are identical for all markers.
		The ranges depend on the configured span, see method RsCma.Configure.GprfMeasurement.FftSpecAn.fspan. \n
			:return: structure: for return value, see the help for ValueStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:GPRF:MEASurement<Instance>:FFTSanalyzer:PSEarch?', self.__class__.ValueStruct())

	def set_value(self, value: ValueStruct) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:FFTSanalyzer:PSEarch \n
		Snippet: driver.configure.gprfMeasurement.fftSpecAn.peakSearch.set_value(value = ValueStruct()) \n
		Defines the peak search ranges for the five markers. In this command, the markers are labeled 0 to 4. At the graphical
		user interface, they are labeled 1 to 5. The allowed ranges, reset values and default units are identical for all markers.
		The ranges depend on the configured span, see method RsCma.Configure.GprfMeasurement.FftSpecAn.fspan. \n
			:param value: see the help for ValueStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:GPRF:MEASurement<Instance>:FFTSanalyzer:PSEarch', value)
