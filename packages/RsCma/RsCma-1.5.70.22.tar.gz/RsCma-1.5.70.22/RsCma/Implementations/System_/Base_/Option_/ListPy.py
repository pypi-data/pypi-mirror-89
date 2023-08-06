from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.Types import DataType
from .....Internal.Utilities import trim_str_response
from .....Internal.ArgSingleList import ArgSingleList
from .....Internal.ArgSingle import ArgSingle
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ListPy:
	"""ListPy commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("listPy", core, parent)

	def get(self, producttype: enums.OptionsProductType = None, validity: enums.OptionValidity = None, scope: enums.OptionsScope = None, instrumentno: float = None) -> str:
		"""SCPI: SYSTem:BASE:OPTion:LIST \n
		Snippet: value: str = driver.system.base.option.listPy.get(producttype = enums.OptionsProductType.ALL, validity = enums.OptionValidity.ALL, scope = enums.OptionsScope.INSTrument, instrumentno = 1.0) \n
		Returns a list of installed software options (licenses) , hardware options, software packages and applications. The list
		can be filtered via parameters. If filtering results in an empty list, a '0' is returned. \n
			:param producttype: No help available
			:param validity: FUNCtional | VALid | ALL FUNCtional List only functional hardware options or applications. HWOPtion: Is functional if the hardware option and all its components can be used (no defect detected) . FWA: Is functional if the required hardware, software and license keys are available and functional. VALid List only valid software options. SWOPtion: Is valid if an active license key is available. ALL Disable filtering (default if parameter is omitted) .
			:param scope: No help available
			:param instrumentno: No help available
			:return: optionlist: No help available"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('producttype', producttype, DataType.Enum, True), ArgSingle('validity', validity, DataType.Enum, True), ArgSingle('scope', scope, DataType.Enum, True), ArgSingle('instrumentno', instrumentno, DataType.Float, True))
		response = self._core.io.query_str(f'SYSTem:BASE:OPTion:LIST? {param}'.rstrip())
		return trim_str_response(response)
