from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.Utilities import trim_str_response
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Socket:
	"""Socket commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("socket", core, parent)

	def get_vresource(self) -> str:
		"""SCPI: SYSTem:COMMunicate:SOCKet:VRESource \n
		Snippet: value: str = driver.system.communicate.socket.get_vresource() \n
		Queries the VISA resource string of the socket resource (direct socket communication) . \n
			:return: visaresource: VISA resource string
		"""
		response = self._core.io.query_str('SYSTem:COMMunicate:SOCKet:VRESource?')
		return trim_str_response(response)

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.ProtocolMode:
		"""SCPI: SYSTem:COMMunicate:SOCKet:MODE \n
		Snippet: value: enums.ProtocolMode = driver.system.communicate.socket.get_mode() \n
		Sets the protocol operation mode for direct socket communication. \n
			:return: protocolmode: No help available
		"""
		response = self._core.io.query_str('SYSTem:COMMunicate:SOCKet:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.ProtocolMode)

	def set_mode(self, protocolmode: enums.ProtocolMode) -> None:
		"""SCPI: SYSTem:COMMunicate:SOCKet:MODE \n
		Snippet: driver.system.communicate.socket.set_mode(protocolmode = enums.ProtocolMode.AGILent) \n
		Sets the protocol operation mode for direct socket communication. \n
			:param protocolmode: RAW | AGILent | IEEE1174 RAW No support of control messages AGILent Emulation codes via control connection (control port) IEEE1174 Emulation codes via data connection (data port)
		"""
		param = Conversions.enum_scalar_to_str(protocolmode, enums.ProtocolMode)
		self._core.io.write(f'SYSTem:COMMunicate:SOCKet:MODE {param}')

	def get_port(self) -> int:
		"""SCPI: SYSTem:COMMunicate:SOCKet:PORT \n
		Snippet: value: int = driver.system.communicate.socket.get_port() \n
		Sets the data port number for direct socket communication. \n
			:return: portnumber: No help available
		"""
		response = self._core.io.query_str('SYSTem:COMMunicate:SOCKet:PORT?')
		return Conversions.str_to_int(response)

	def set_port(self, portnumber: int) -> None:
		"""SCPI: SYSTem:COMMunicate:SOCKet:PORT \n
		Snippet: driver.system.communicate.socket.set_port(portnumber = 1) \n
		Sets the data port number for direct socket communication. \n
			:param portnumber: To select a free port number, enter 0. To select a specific port number, use the following range. Range: 1024 to 32767
		"""
		param = Conversions.decimal_value_to_str(portnumber)
		self._core.io.write(f'SYSTem:COMMunicate:SOCKet:PORT {param}')
