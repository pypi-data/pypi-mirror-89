from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SpdifLeft:
	"""SpdifLeft commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("spdifLeft", core, parent)

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.DigitalToneMode:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:SINLeft:MODE \n
		Snippet: value: enums.DigitalToneMode = driver.configure.afRf.measurement.multiEval.tones.spdifLeft.get_mode() \n
		Selects a dialing tone mode for the left SPDIF channel. \n
			:return: tone_mode: NONE | SELCall | DTMF | FDIA | SCAL None, SelCall, DTMF, free dialing, SELCAL
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:SINLeft:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.DigitalToneMode)

	def set_mode(self, tone_mode: enums.DigitalToneMode) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:SINLeft:MODE \n
		Snippet: driver.configure.afRf.measurement.multiEval.tones.spdifLeft.set_mode(tone_mode = enums.DigitalToneMode.DCS) \n
		Selects a dialing tone mode for the left SPDIF channel. \n
			:param tone_mode: NONE | SELCall | DTMF | FDIA | SCAL None, SelCall, DTMF, free dialing, SELCAL
		"""
		param = Conversions.enum_scalar_to_str(tone_mode, enums.DigitalToneMode)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:SINLeft:MODE {param}')
