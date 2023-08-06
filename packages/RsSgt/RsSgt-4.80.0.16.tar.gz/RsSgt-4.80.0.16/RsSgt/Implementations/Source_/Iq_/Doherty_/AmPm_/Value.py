from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.Types import DataType
from ......Internal.ArgSingleList import ArgSingleList
from ......Internal.ArgSingle import ArgSingle
from ...... import enums
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Value:
	"""Value commands group definition. 3 total commands, 2 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("value", core, parent)

	@property
	def level(self):
		"""level commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_level'):
			from .Value_.Level import Level
			self._level = Level(self._core, self._base)
		return self._level

	@property
	def pep(self):
		"""pep commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pep'):
			from .Value_.Pep import Pep
			self._pep = Pep(self._core, self._base)
		return self._pep

	def get(self, xvalue: float, xunit: enums.Unknown, stream=repcap.Stream.Default) -> float:
		"""SCPI: [SOURce<HW>]:IQ:DOHerty<ST>:AMPM:VALue \n
		Snippet: value: float = driver.source.iq.doherty.amPm.value.get(xvalue = 1.0, xunit = enums.Unknown.DBM, stream = repcap.Stream.Default) \n
		No command help available \n
			:param xvalue: No help available
			:param xunit: No help available
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Doherty')
			:return: delta_phase: No help available"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('xvalue', xvalue, DataType.Float), ArgSingle('xunit', xunit, DataType.Enum))
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:IQ:DOHerty{stream_cmd_val}:AMPM:VALue? {param}'.rstrip())
		return Conversions.str_to_float(response)

	def clone(self) -> 'Value':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Value(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
