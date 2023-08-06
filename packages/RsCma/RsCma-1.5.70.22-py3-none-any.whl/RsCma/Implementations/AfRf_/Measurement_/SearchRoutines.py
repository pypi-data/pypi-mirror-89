from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SearchRoutines:
	"""SearchRoutines commands group definition. 33 total commands, 5 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("searchRoutines", core, parent)

	@property
	def state(self):
		"""state commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .SearchRoutines_.State import State
			self._state = State(self._core, self._base)
		return self._state

	@property
	def rsensitivity(self):
		"""rsensitivity commands group. 3 Sub-classes, 2 commands."""
		if not hasattr(self, '_rsensitivity'):
			from .SearchRoutines_.Rsensitivity import Rsensitivity
			self._rsensitivity = Rsensitivity(self._core, self._base)
		return self._rsensitivity

	@property
	def rifBandwidth(self):
		"""rifBandwidth commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_rifBandwidth'):
			from .SearchRoutines_.RifBandwidth import RifBandwidth
			self._rifBandwidth = RifBandwidth(self._core, self._base)
		return self._rifBandwidth

	@property
	def rsquelch(self):
		"""rsquelch commands group. 8 Sub-classes, 0 commands."""
		if not hasattr(self, '_rsquelch'):
			from .SearchRoutines_.Rsquelch import Rsquelch
			self._rsquelch = Rsquelch(self._core, self._base)
		return self._rsquelch

	@property
	def ssnr(self):
		"""ssnr commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_ssnr'):
			from .SearchRoutines_.Ssnr import Ssnr
			self._ssnr = Ssnr(self._core, self._base)
		return self._ssnr

	def initiate(self) -> None:
		"""SCPI: INITiate:AFRF:MEASurement<Instance>:SROutines \n
		Snippet: driver.afRf.measurement.searchRoutines.initiate() \n
		Starts or continues the search routine. \n
		"""
		self._core.io.write(f'INITiate:AFRF:MEASurement<Instance>:SROutines')

	def initiate_with_opc(self) -> None:
		"""SCPI: INITiate:AFRF:MEASurement<Instance>:SROutines \n
		Snippet: driver.afRf.measurement.searchRoutines.initiate_with_opc() \n
		Starts or continues the search routine. \n
		Same as initiate, but waits for the operation to complete before continuing further. Use the RsCma.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'INITiate:AFRF:MEASurement<Instance>:SROutines')

	def stop(self) -> None:
		"""SCPI: STOP:AFRF:MEASurement<Instance>:SROutines \n
		Snippet: driver.afRf.measurement.searchRoutines.stop() \n
		Pauses the search routine. \n
		"""
		self._core.io.write(f'STOP:AFRF:MEASurement<Instance>:SROutines')

	def stop_with_opc(self) -> None:
		"""SCPI: STOP:AFRF:MEASurement<Instance>:SROutines \n
		Snippet: driver.afRf.measurement.searchRoutines.stop_with_opc() \n
		Pauses the search routine. \n
		Same as stop, but waits for the operation to complete before continuing further. Use the RsCma.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'STOP:AFRF:MEASurement<Instance>:SROutines')

	def abort(self) -> None:
		"""SCPI: ABORt:AFRF:MEASurement<Instance>:SROutines \n
		Snippet: driver.afRf.measurement.searchRoutines.abort() \n
		Stops the search routine. \n
		"""
		self._core.io.write(f'ABORt:AFRF:MEASurement<Instance>:SROutines')

	def abort_with_opc(self) -> None:
		"""SCPI: ABORt:AFRF:MEASurement<Instance>:SROutines \n
		Snippet: driver.afRf.measurement.searchRoutines.abort_with_opc() \n
		Stops the search routine. \n
		Same as abort, but waits for the operation to complete before continuing further. Use the RsCma.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'ABORt:AFRF:MEASurement<Instance>:SROutines')

	def clone(self) -> 'SearchRoutines':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SearchRoutines(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
