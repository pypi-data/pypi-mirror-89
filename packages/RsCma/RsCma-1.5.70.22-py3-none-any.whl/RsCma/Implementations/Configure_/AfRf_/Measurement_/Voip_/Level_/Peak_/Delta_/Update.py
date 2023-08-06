from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Update:
	"""Update commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("update", core, parent)

	def set(self) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:VOIP:LEVel:PEAK:DELTa:UPDate \n
		Snippet: driver.configure.afRf.measurement.voip.level.peak.delta.update.set() \n
		No command help available \n
		"""
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:VOIP:LEVel:PEAK:DELTa:UPDate')

	def set_with_opc(self) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:VOIP:LEVel:PEAK:DELTa:UPDate \n
		Snippet: driver.configure.afRf.measurement.voip.level.peak.delta.update.set_with_opc() \n
		No command help available \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsCma.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'CONFigure:AFRF:MEASurement<Instance>:VOIP:LEVel:PEAK:DELTa:UPDate')
