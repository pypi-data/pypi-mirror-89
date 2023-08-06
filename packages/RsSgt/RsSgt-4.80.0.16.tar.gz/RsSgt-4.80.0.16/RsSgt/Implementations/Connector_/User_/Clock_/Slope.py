from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Slope:
	"""Slope commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("slope", core, parent)

	def set(self, slope: enums.SlopeType, channel=repcap.Channel.Default) -> None:
		"""SCPI: CONNector:USER<CH>:CLOCk:SLOPe \n
		Snippet: driver.connector.user.clock.slope.set(slope = enums.SlopeType.NEGative, channel = repcap.Channel.Default) \n
		Sets the polarity of the active slope of an applied instrument trigger/clock. \n
			:param slope: NEGative| POSitive
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')"""
		param = Conversions.enum_scalar_to_str(slope, enums.SlopeType)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'CONNector:USER{channel_cmd_val}:CLOCk:SLOPe {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.SlopeType:
		"""SCPI: CONNector:USER<CH>:CLOCk:SLOPe \n
		Snippet: value: enums.SlopeType = driver.connector.user.clock.slope.get(channel = repcap.Channel.Default) \n
		Sets the polarity of the active slope of an applied instrument trigger/clock. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:return: slope: NEGative| POSitive"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'CONNector:USER{channel_cmd_val}:CLOCk:SLOPe?')
		return Conversions.str_to_scalar_enum(response, enums.SlopeType)
