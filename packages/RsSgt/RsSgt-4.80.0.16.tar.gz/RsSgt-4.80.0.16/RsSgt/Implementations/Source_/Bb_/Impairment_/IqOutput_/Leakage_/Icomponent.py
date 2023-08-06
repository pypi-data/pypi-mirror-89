from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Icomponent:
	"""Icomponent commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("icomponent", core, parent)

	def set(self, ipart: float, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce]:BB:IMPairment:IQOutput<CH>:LEAKage:I \n
		Snippet: driver.source.bb.impairment.iqOutput.leakage.icomponent.set(ipart = 1.0, channel = repcap.Channel.Default) \n
		Determines the leakage amplitude of the I or Q-signal component of the corresponding stream.
			INTRO_CMD_HELP: The suffix <ch> has the following values: \n
			- <ch>= 0: I/Q Analog Outputs
			- <ch>= 1: I/Q Modulator Digital Impairments \n
			:param ipart: float Range: -10 to 10
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'IqOutput')"""
		param = Conversions.decimal_value_to_str(ipart)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce:BB:IMPairment:IQOutput{channel_cmd_val}:LEAKage:I {param}')

	def get(self, channel=repcap.Channel.Default) -> float:
		"""SCPI: [SOURce]:BB:IMPairment:IQOutput<CH>:LEAKage:I \n
		Snippet: value: float = driver.source.bb.impairment.iqOutput.leakage.icomponent.get(channel = repcap.Channel.Default) \n
		Determines the leakage amplitude of the I or Q-signal component of the corresponding stream.
			INTRO_CMD_HELP: The suffix <ch> has the following values: \n
			- <ch>= 0: I/Q Analog Outputs
			- <ch>= 1: I/Q Modulator Digital Impairments \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'IqOutput')
			:return: ipart: No help available"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce:BB:IMPairment:IQOutput{channel_cmd_val}:LEAKage:I?')
		return Conversions.str_to_float(response)
