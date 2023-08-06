from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Aranging:
	"""Aranging commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("aranging", core, parent)

	def set(self, enable: bool, audioInput=repcap.AudioInput.Default) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:AIN<nr>:ARANging \n
		Snippet: driver.configure.afRf.measurement.audioInput.aranging.set(enable = False, audioInput = repcap.AudioInput.Default) \n
		Enables or disables auto ranging for an AF IN connector. \n
			:param enable: OFF | ON Switches auto ranging off or on
			:param audioInput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioInput')"""
		param = Conversions.bool_to_str(enable)
		audioInput_cmd_val = self._base.get_repcap_cmd_value(audioInput, repcap.AudioInput)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:AIN{audioInput_cmd_val}:ARANging {param}')

	def get(self, audioInput=repcap.AudioInput.Default) -> bool:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:AIN<nr>:ARANging \n
		Snippet: value: bool = driver.configure.afRf.measurement.audioInput.aranging.get(audioInput = repcap.AudioInput.Default) \n
		Enables or disables auto ranging for an AF IN connector. \n
			:param audioInput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioInput')
			:return: enable: OFF | ON Switches auto ranging off or on"""
		audioInput_cmd_val = self._base.get_repcap_cmd_value(audioInput, repcap.AudioInput)
		response = self._core.io.query_str(f'CONFigure:AFRF:MEASurement<Instance>:AIN{audioInput_cmd_val}:ARANging?')
		return Conversions.str_to_bool(response)
