from typing import List

from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........Internal.RepeatedCapability import RepeatedCapability
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Frequency:
	"""Frequency commands group definition. 2 total commands, 1 Sub-groups, 1 group commands
	Repeated Capability: FrequencyLobe, default value after init: FrequencyLobe.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("frequency", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_frequencyLobe_get', 'repcap_frequencyLobe_set', repcap.FrequencyLobe.Nr1)

	def repcap_frequencyLobe_set(self, enum_value: repcap.FrequencyLobe) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to FrequencyLobe.Default
		Default value after init: FrequencyLobe.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_frequencyLobe_get(self) -> repcap.FrequencyLobe:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def dtone(self):
		"""dtone commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dtone'):
			from .Frequency_.Dtone import Dtone
			self._dtone = Dtone(self._core, self._base)
		return self._dtone

	def get_stone(self) -> List[float]:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:FDIaling:FREQuency:STONe \n
		Snippet: value: List[float] = driver.configure.afRf.measurement.multiEval.tones.fdialing.frequency.get_stone() \n
		Assigns single-tone frequencies to digits, for analysis of free-dialing tone sequences. \n
			:return: tones_frequency: Comma-separated list of 16 frequencies, assigned to the digits 0, 1, ..., 9, A, ..., F Specifying fewer frequencies leaves the remaining digits unchanged. Range: 60 Hz to 4000 Hz, Unit: Hz
		"""
		response = self._core.io.query_bin_or_ascii_float_list('CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:FDIaling:FREQuency:STONe?')
		return response

	def set_stone(self, tones_frequency: List[float]) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:FDIaling:FREQuency:STONe \n
		Snippet: driver.configure.afRf.measurement.multiEval.tones.fdialing.frequency.set_stone(tones_frequency = [1.1, 2.2, 3.3]) \n
		Assigns single-tone frequencies to digits, for analysis of free-dialing tone sequences. \n
			:param tones_frequency: Comma-separated list of 16 frequencies, assigned to the digits 0, 1, ..., 9, A, ..., F Specifying fewer frequencies leaves the remaining digits unchanged. Range: 60 Hz to 4000 Hz, Unit: Hz
		"""
		param = Conversions.list_to_csv_str(tones_frequency)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:FDIaling:FREQuency:STONe {param}')

	def clone(self) -> 'Frequency':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Frequency(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
