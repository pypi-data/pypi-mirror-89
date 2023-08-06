from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Qcomponent:
	"""Qcomponent commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("qcomponent", core, parent)

	def set(self, qpart: float, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce]:BB:IMPairment:IQOutput<CH>:LEAKage:Q \n
		Snippet: driver.source.bb.impairment.iqOutput.leakage.qcomponent.set(qpart = 1.0, channel = repcap.Channel.Default) \n
		Determines the leakage amplitude of the I or Q-signal component of the corresponding stream.
			INTRO_CMD_HELP: The suffix <ch> has the following values: \n
			- <ch>= 0: I/Q Analog Outputs
			- <ch>= 1: I/Q Modulator Digital Impairments \n
			:param qpart: float Range: -10 to 10
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'IqOutput')"""
		param = Conversions.decimal_value_to_str(qpart)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce:BB:IMPairment:IQOutput{channel_cmd_val}:LEAKage:Q {param}')

	def get(self, channel=repcap.Channel.Default) -> float:
		"""SCPI: [SOURce]:BB:IMPairment:IQOutput<CH>:LEAKage:Q \n
		Snippet: value: float = driver.source.bb.impairment.iqOutput.leakage.qcomponent.get(channel = repcap.Channel.Default) \n
		Determines the leakage amplitude of the I or Q-signal component of the corresponding stream.
			INTRO_CMD_HELP: The suffix <ch> has the following values: \n
			- <ch>= 0: I/Q Analog Outputs
			- <ch>= 1: I/Q Modulator Digital Impairments \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'IqOutput')
			:return: qpart: No help available"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce:BB:IMPairment:IQOutput{channel_cmd_val}:LEAKage:Q?')
		return Conversions.str_to_float(response)
