from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Action:
	"""Action commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("action", core, parent)

	def set(self) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:RFSettings:FARFrequency:ACTion \n
		Snippet: driver.configure.afRf.measurement.rfSettings.farFrequency.action.set() \n
		Sets the reference frequency of the channel definition to the current center frequency of the RF analyzer. \n
		"""
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:RFSettings:FARFrequency:ACTion')

	def set_with_opc(self) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:RFSettings:FARFrequency:ACTion \n
		Snippet: driver.configure.afRf.measurement.rfSettings.farFrequency.action.set_with_opc() \n
		Sets the reference frequency of the channel definition to the current center frequency of the RF analyzer. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsCma.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'CONFigure:AFRF:MEASurement<Instance>:RFSettings:FARFrequency:ACTion')
