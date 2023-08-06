from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.Utilities import trim_str_response
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sip:
	"""Sip commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sip", core, parent)

	def get_response(self) -> str:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:VOIP:SIP:RESPonse \n
		Snippet: value: str = driver.source.afRf.generator.voip.sip.get_response() \n
		Queries the text of the last received SIP response. \n
			:return: sip_response: Response string, for example 'OK'
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:VOIP:SIP:RESPonse?')
		return trim_str_response(response)

	# noinspection PyTypeChecker
	def get_state(self) -> enums.SipState:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:VOIP:SIP:STATe \n
		Snippet: value: enums.SipState = driver.source.afRf.generator.voip.sip.get_state() \n
		Queries the state of the VoIP connection to the DUT. \n
			:return: sip_state: TERMinated | ESTablished | ERRor
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:VOIP:SIP:STATe?')
		return Conversions.str_to_scalar_enum(response, enums.SipState)

	def get_code(self) -> int:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:VOIP:SIP:CODE \n
		Snippet: value: int = driver.source.afRf.generator.voip.sip.get_code() \n
		Queries the code number of the last received SIP response. \n
			:return: sip_code: Decimal number, for example 200
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:VOIP:SIP:CODE?')
		return Conversions.str_to_int(response)
