from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Frequency:
	"""Frequency commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("frequency", core, parent)

	def set(self, filter_frequency: float, notch=repcap.Notch.Default) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:VOIP:FILTer:NOTCh<Num>:FREQuency \n
		Snippet: driver.configure.afRf.measurement.voip.filterPy.notch.frequency.set(filter_frequency = 1.0, notch = repcap.Notch.Default) \n
		No command help available \n
			:param filter_frequency: No help available
			:param notch: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Notch')"""
		param = Conversions.decimal_value_to_str(filter_frequency)
		notch_cmd_val = self._base.get_repcap_cmd_value(notch, repcap.Notch)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:VOIP:FILTer:NOTCh{notch_cmd_val}:FREQuency {param}')

	def get(self, notch=repcap.Notch.Default) -> float:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:VOIP:FILTer:NOTCh<Num>:FREQuency \n
		Snippet: value: float = driver.configure.afRf.measurement.voip.filterPy.notch.frequency.get(notch = repcap.Notch.Default) \n
		No command help available \n
			:param notch: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Notch')
			:return: filter_frequency: No help available"""
		notch_cmd_val = self._base.get_repcap_cmd_value(notch, repcap.Notch)
		response = self._core.io.query_str(f'CONFigure:AFRF:MEASurement<Instance>:VOIP:FILTer:NOTCh{notch_cmd_val}:FREQuency?')
		return Conversions.str_to_float(response)
