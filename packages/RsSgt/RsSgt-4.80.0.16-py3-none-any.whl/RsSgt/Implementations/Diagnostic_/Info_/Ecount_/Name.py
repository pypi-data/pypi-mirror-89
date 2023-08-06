from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.Utilities import trim_str_response
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Name:
	"""Name commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("name", core, parent)

	def get(self, channel=repcap.Channel.Default) -> str:
		"""SCPI: DIAGnostic:INFO:ECOunt<CH>:NAME \n
		Snippet: value: str = driver.diagnostic.info.ecount.name.get(channel = repcap.Channel.Default) \n
		No command help available \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ecount')
			:return: ecount: No help available"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'DIAGnostic:INFO:ECOunt{channel_cmd_val}:NAME?')
		return trim_str_response(response)
