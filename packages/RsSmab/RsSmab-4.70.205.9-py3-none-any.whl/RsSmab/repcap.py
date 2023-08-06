from enum import Enum
from .Internal.RepeatedCapability import VALUE_DEFAULT
from .Internal.RepeatedCapability import VALUE_EMPTY


# noinspection SpellCheckingInspection
class HwInstance(Enum):
	"""Global Repeated capability HwInstance"""
	Empty = VALUE_EMPTY
	Default = VALUE_DEFAULT
	Inst0 = 0
	InstA = 1
	InstB = 2
	InstC = 3
	InstD = 4


# noinspection SpellCheckingInspection
class BitNumber(Enum):
	"""Repeated capability BitNumber"""
	Empty = VALUE_EMPTY
	Default = VALUE_DEFAULT
	Nr0 = 0
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


# noinspection SpellCheckingInspection
class Channel(Enum):
	"""Repeated capability Channel"""
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
