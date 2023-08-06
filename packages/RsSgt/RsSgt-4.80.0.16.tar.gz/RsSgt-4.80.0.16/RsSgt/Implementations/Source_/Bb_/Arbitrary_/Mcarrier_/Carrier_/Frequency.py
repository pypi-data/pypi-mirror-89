from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Frequency:
	"""Frequency commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("frequency", core, parent)

	def set(self, frequency: int, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:ARBitrary:MCARrier:CARRier<CH>:FREQuency \n
		Snippet: driver.source.bb.arbitrary.mcarrier.carrier.frequency.set(frequency = 1, channel = repcap.Channel.Default) \n
		Sets or indicates the carrier frequency, depending on the selected carrier frequency mode. The carrier frequency can be
		set in 'Arbitrary Carrier frequency' mode. For 'Equidistant Carrier Spacing', the carrier spacing is determined
		automatically. \n
			:param frequency: float Value range depends on the max bandwidth, see data sheet Range: -40E6 to 40E6
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Carrier')"""
		param = Conversions.decimal_value_to_str(frequency)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:ARBitrary:MCARrier:CARRier{channel_cmd_val}:FREQuency {param}')

	def get(self, channel=repcap.Channel.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:ARBitrary:MCARrier:CARRier<CH>:FREQuency \n
		Snippet: value: int = driver.source.bb.arbitrary.mcarrier.carrier.frequency.get(channel = repcap.Channel.Default) \n
		Sets or indicates the carrier frequency, depending on the selected carrier frequency mode. The carrier frequency can be
		set in 'Arbitrary Carrier frequency' mode. For 'Equidistant Carrier Spacing', the carrier spacing is determined
		automatically. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Carrier')
			:return: frequency: float Value range depends on the max bandwidth, see data sheet Range: -40E6 to 40E6"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:ARBitrary:MCARrier:CARRier{channel_cmd_val}:FREQuency?')
		return Conversions.str_to_int(response)
