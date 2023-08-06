from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Magnitude:
	"""Magnitude commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("magnitude", core, parent)

	def set(self, ipartq_ratio: float, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce]:BB:IMPairment:RF<CH>:IQRatio:[MAGNitude] \n
		Snippet: driver.source.bb.impairment.rf.iqRatio.magnitude.set(ipartq_ratio = 1.0, channel = repcap.Channel.Default) \n
		No command help available \n
			:param ipartq_ratio: No help available
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Rf')"""
		param = Conversions.decimal_value_to_str(ipartq_ratio)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce:BB:IMPairment:RF{channel_cmd_val}:IQRatio:MAGNitude {param}')

	def get(self, channel=repcap.Channel.Default) -> float:
		"""SCPI: [SOURce]:BB:IMPairment:RF<CH>:IQRatio:[MAGNitude] \n
		Snippet: value: float = driver.source.bb.impairment.rf.iqRatio.magnitude.get(channel = repcap.Channel.Default) \n
		No command help available \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Rf')
			:return: ipartq_ratio: No help available"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce:BB:IMPairment:RF{channel_cmd_val}:IQRatio:MAGNitude?')
		return Conversions.str_to_float(response)
