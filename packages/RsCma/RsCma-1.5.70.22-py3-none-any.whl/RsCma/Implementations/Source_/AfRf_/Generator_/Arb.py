from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Arb:
	"""Arb commands group definition. 13 total commands, 3 Sub-groups, 6 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("arb", core, parent)

	@property
	def file(self):
		"""file commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_file'):
			from .Arb_.File import File
			self._file = File(self._core, self._base)
		return self._file

	@property
	def marker(self):
		"""marker commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_marker'):
			from .Arb_.Marker import Marker
			self._marker = Marker(self._core, self._base)
		return self._marker

	@property
	def samples(self):
		"""samples commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_samples'):
			from .Arb_.Samples import Samples
			self._samples = Samples(self._core, self._base)
		return self._samples

	def get_crate(self) -> float:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:ARB:CRATe \n
		Snippet: value: float = driver.source.afRf.generator.arb.get_crate() \n
		Queries the clock rate of the loaded ARB file. \n
			:return: clock_rate: Unit: Hz
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:ARB:CRATe?')
		return Conversions.str_to_float(response)

	# noinspection PyTypeChecker
	def get_crc_protect(self) -> enums.YesNoStatus:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:ARB:CRCProtect \n
		Snippet: value: enums.YesNoStatus = driver.source.afRf.generator.arb.get_crc_protect() \n
		Queries whether the loaded ARB file contains a CRC checksum. \n
			:return: crc_protection: NO | YES
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:ARB:CRCProtect?')
		return Conversions.str_to_scalar_enum(response, enums.YesNoStatus)

	def get_freq_offset(self) -> float:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:ARB:FOFFset \n
		Snippet: value: float = driver.source.afRf.generator.arb.get_freq_offset() \n
		Defines a frequency offset to be imposed at the baseband during ARB generation. \n
			:return: frequency_offset: Range: -10 MHz to 10 MHz, Unit: Hz
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:ARB:FOFFset?')
		return Conversions.str_to_float(response)

	def set_freq_offset(self, frequency_offset: float) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:ARB:FOFFset \n
		Snippet: driver.source.afRf.generator.arb.set_freq_offset(frequency_offset = 1.0) \n
		Defines a frequency offset to be imposed at the baseband during ARB generation. \n
			:param frequency_offset: Range: -10 MHz to 10 MHz, Unit: Hz
		"""
		param = Conversions.decimal_value_to_str(frequency_offset)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:ARB:FOFFset {param}')

	def get_loffset(self) -> float:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:ARB:LOFFset \n
		Snippet: value: float = driver.source.afRf.generator.arb.get_loffset() \n
		Queries the peak to average ratio (PAR) of the loaded ARB file. The PAR is also called level offset. \n
			:return: level_offset: Unit: dB
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:ARB:LOFFset?')
		return Conversions.str_to_float(response)

	def get_poffset(self) -> float:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:ARB:POFFset \n
		Snippet: value: float = driver.source.afRf.generator.arb.get_poffset() \n
		Queries the peak offset of the loaded ARB file. \n
			:return: peak_offset: Unit: dB
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:ARB:POFFset?')
		return Conversions.str_to_float(response)

	# noinspection PyTypeChecker
	def get_repetition(self) -> enums.RepeatMode:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:ARB:REPetition \n
		Snippet: value: enums.RepeatMode = driver.source.afRf.generator.arb.get_repetition() \n
		Defines how often the ARB file is processed. \n
			:return: repetition: CONTinuous | SINGle CONTinuous Cyclic continuous processing SINGle File is processed once
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:ARB:REPetition?')
		return Conversions.str_to_scalar_enum(response, enums.RepeatMode)

	def set_repetition(self, repetition: enums.RepeatMode) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:ARB:REPetition \n
		Snippet: driver.source.afRf.generator.arb.set_repetition(repetition = enums.RepeatMode.CONTinuous) \n
		Defines how often the ARB file is processed. \n
			:param repetition: CONTinuous | SINGle CONTinuous Cyclic continuous processing SINGle File is processed once
		"""
		param = Conversions.enum_scalar_to_str(repetition, enums.RepeatMode)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:ARB:REPetition {param}')

	def clone(self) -> 'Arb':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Arb(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
