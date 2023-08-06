from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Spdif:
	"""Spdif commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("spdif", core, parent)

	# noinspection PyTypeChecker
	def get_xdivision(self) -> enums.Xdivision:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:SIN:XDIVision \n
		Snippet: value: enums.Xdivision = driver.configure.afRf.measurement.multiEval.oscilloscope.spdif.get_xdivision() \n
		No command help available \n
			:return: xdivision: No help available
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:SIN:XDIVision?')
		return Conversions.str_to_scalar_enum(response, enums.Xdivision)

	def set_xdivision(self, xdivision: enums.Xdivision) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:SIN:XDIVision \n
		Snippet: driver.configure.afRf.measurement.multiEval.oscilloscope.spdif.set_xdivision(xdivision = enums.Xdivision.M1) \n
		No command help available \n
			:param xdivision: No help available
		"""
		param = Conversions.enum_scalar_to_str(xdivision, enums.Xdivision)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:SIN:XDIVision {param}')

	def get_mtime(self) -> float:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:SIN:MTIMe \n
		Snippet: value: float = driver.configure.afRf.measurement.multiEval.oscilloscope.spdif.get_mtime() \n
		No command help available \n
			:return: meas_time: No help available
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:SIN:MTIMe?')
		return Conversions.str_to_float(response)

	def set_mtime(self, meas_time: float) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:SIN:MTIMe \n
		Snippet: driver.configure.afRf.measurement.multiEval.oscilloscope.spdif.set_mtime(meas_time = 1.0) \n
		No command help available \n
			:param meas_time: No help available
		"""
		param = Conversions.decimal_value_to_str(meas_time)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:SIN:MTIMe {param}')
