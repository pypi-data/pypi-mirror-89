from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FormatPy:
	"""FormatPy commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("formatPy", core, parent)

	def set(self, eformat: enums.Eformat, instrument=repcap.Instrument.Default) -> None:
		"""SCPI: TRACe:REMote:MODE:FILE<instrument>:FORMat \n
		Snippet: driver.trace.remote.mode.file.formatPy.set(eformat = enums.Eformat.ASCii, instrument = repcap.Instrument.Default) \n
		Specifies the target file format for tracing of the remote control interface. The trace can be stored as ASCII file or as
		XML file. \n
			:param eformat: ASCii | XML Default value: XML
			:param instrument: optional repeated capability selector. Default value: Nr1 (settable in the interface 'File')"""
		param = Conversions.enum_scalar_to_str(eformat, enums.Eformat)
		instrument_cmd_val = self._base.get_repcap_cmd_value(instrument, repcap.Instrument)
		self._core.io.write(f'TRACe:REMote:MODE:FILE{instrument_cmd_val}:FORMat {param}')

	# noinspection PyTypeChecker
	def get(self, instrument=repcap.Instrument.Default) -> enums.Eformat:
		"""SCPI: TRACe:REMote:MODE:FILE<instrument>:FORMat \n
		Snippet: value: enums.Eformat = driver.trace.remote.mode.file.formatPy.get(instrument = repcap.Instrument.Default) \n
		Specifies the target file format for tracing of the remote control interface. The trace can be stored as ASCII file or as
		XML file. \n
			:param instrument: optional repeated capability selector. Default value: Nr1 (settable in the interface 'File')
			:return: eformat: No help available"""
		instrument_cmd_val = self._base.get_repcap_cmd_value(instrument, repcap.Instrument)
		response = self._core.io.query_str(f'TRACe:REMote:MODE:FILE{instrument_cmd_val}:FORMat?')
		return Conversions.str_to_scalar_enum(response, enums.Eformat)
