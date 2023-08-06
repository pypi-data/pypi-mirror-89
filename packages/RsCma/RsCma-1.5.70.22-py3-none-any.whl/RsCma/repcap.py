from enum import Enum
from .Internal.RepeatedCapability import VALUE_DEFAULT
from .Internal.RepeatedCapability import VALUE_EMPTY


# noinspection SpellCheckingInspection
class Instance(Enum):
	"""Global Repeated capability Instance \n
	Selects the instrument"""
	Empty = VALUE_EMPTY
	Default = VALUE_DEFAULT
	Inst1 = 1
	Inst2 = 2
	Inst3 = 3
	Inst4 = 4
	Inst5 = 5
	Inst6 = 6
	Inst7 = 7
	Inst8 = 8
	Inst9 = 9
	Inst10 = 10
	Inst11 = 11
	Inst12 = 12
	Inst13 = 13
	Inst14 = 14
	Inst15 = 15
	Inst16 = 16
	Inst17 = 17
	Inst18 = 18
	Inst19 = 19
	Inst20 = 20
	Inst21 = 21
	Inst22 = 22
	Inst23 = 23
	Inst24 = 24
	Inst25 = 25
	Inst26 = 26
	Inst27 = 27
	Inst28 = 28
	Inst29 = 29
	Inst30 = 30
	Inst31 = 31
	Inst32 = 32


# noinspection SpellCheckingInspection
class AudioInput(Enum):
	"""Repeated capability AudioInput \n
	Selects the AF index"""
	Empty = VALUE_EMPTY
	Default = VALUE_DEFAULT
	Nr1 = 1
	Nr2 = 2


# noinspection SpellCheckingInspection
class AudioOutput(Enum):
	"""Repeated capability AudioOutput \n
	Selects the connector number"""
	Empty = VALUE_EMPTY
	Default = VALUE_DEFAULT
	Nr1 = 1
	Nr2 = 2


# noinspection SpellCheckingInspection
class Battery(Enum):
	"""Repeated capability Battery \n
	Index of battery"""
	Empty = VALUE_EMPTY
	Default = VALUE_DEFAULT
	Ix1 = 1
	Ix2 = 2


# noinspection SpellCheckingInspection
class Bit(Enum):
	"""Repeated capability Bit"""
	Empty = VALUE_EMPTY
	Default = VALUE_DEFAULT
	Nr8 = 8
	Nr9 = 9
	Nr10 = 10
	Nr11 = 11
	Nr12 = 12


# noinspection SpellCheckingInspection
class Channel(Enum):
	"""Repeated capability Channel \n
	Selects the path input"""
	Empty = VALUE_EMPTY
	Default = VALUE_DEFAULT
	Nr1 = 1
	Nr2 = 2


# noinspection SpellCheckingInspection
class Connector(Enum):
	"""Repeated capability Connector \n
	Selects the connector"""
	Empty = VALUE_EMPTY
	Default = VALUE_DEFAULT
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8


# noinspection SpellCheckingInspection
class FrequencyLobe(Enum):
	"""Repeated capability FrequencyLobe \n
	index"""
	Empty = VALUE_EMPTY
	Default = VALUE_DEFAULT
	Nr1 = 1
	Nr2 = 2


# noinspection SpellCheckingInspection
class Instrument(Enum):
	"""Repeated capability Instrument \n
	instrument"""
	Empty = VALUE_EMPTY
	Default = VALUE_DEFAULT
	Nr1 = 1
	Nr2 = 2


# noinspection SpellCheckingInspection
class InternalGen(Enum):
	"""Repeated capability InternalGen \n
	Number of DigitalGenerator"""
	Empty = VALUE_EMPTY
	Default = VALUE_DEFAULT
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4


# noinspection SpellCheckingInspection
class Marker(Enum):
	"""Repeated capability Marker \n
	Selects the marker"""
	Empty = VALUE_EMPTY
	Default = VALUE_DEFAULT
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5


# noinspection SpellCheckingInspection
class MarkerOther(Enum):
	"""Repeated capability MarkerOther \n
	Selects the Marker"""
	Empty = VALUE_EMPTY
	Default = VALUE_DEFAULT
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5


# noinspection SpellCheckingInspection
class Notch(Enum):
	"""Repeated capability Notch \n
	Select the Notch filter index"""
	Empty = VALUE_EMPTY
	Default = VALUE_DEFAULT
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3


# noinspection SpellCheckingInspection
class Relay(Enum):
	"""Repeated capability Relay \n
	Index of Relay"""
	Empty = VALUE_EMPTY
	Default = VALUE_DEFAULT
	Ix1 = 1
	Ix2 = 2


# noinspection SpellCheckingInspection
class ToneNumber(Enum):
	"""Repeated capability ToneNumber \n
	no"""
	Empty = VALUE_EMPTY
	Default = VALUE_DEFAULT
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8
	Nr9 = 9
	Nr10 = 10
	Nr11 = 11
	Nr12 = 12
	Nr13 = 13
	Nr14 = 14
	Nr15 = 15
	Nr16 = 16
	Nr17 = 17
	Nr18 = 18
	Nr19 = 19
	Nr20 = 20


# noinspection SpellCheckingInspection
class TTL(Enum):
	"""Repeated capability TTL \n
	Index of TTL Register"""
	Empty = VALUE_EMPTY
	Default = VALUE_DEFAULT
	Ix1 = 1
	Ix2 = 2


# noinspection SpellCheckingInspection
class Window(Enum):
	"""Repeated capability Window \n
	1-n"""
	Empty = VALUE_EMPTY
	Default = VALUE_DEFAULT
	Win1 = 1
	Win2 = 2
	Win3 = 3
	Win4 = 4
	Win5 = 5
	Win6 = 6
	Win7 = 7
	Win8 = 8
	Win9 = 9
	Win10 = 10
	Win11 = 11
	Win12 = 12
	Win13 = 13
	Win14 = 14
	Win15 = 15
	Win16 = 16
	Win17 = 17
	Win18 = 18
	Win19 = 19
	Win20 = 20
	Win21 = 21
	Win22 = 22
	Win23 = 23
	Win24 = 24
	Win25 = 25
	Win26 = 26
	Win27 = 27
	Win28 = 28
	Win29 = 29
	Win30 = 30
	Win31 = 31
	Win32 = 32
