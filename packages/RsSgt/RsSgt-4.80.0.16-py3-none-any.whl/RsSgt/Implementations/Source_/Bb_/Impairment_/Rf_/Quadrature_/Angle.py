from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Angle:
	"""Angle commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("angle", core, parent)

	def set(self, angle: float, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce]:BB:IMPairment:RF<CH>:QUADrature:[ANGLe] \n
		Snippet: driver.source.bb.impairment.rf.quadrature.angle.set(angle = 1.0, channel = repcap.Channel.Default) \n
		No command help available \n
			:param angle: No help available
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Rf')"""
		param = Conversions.decimal_value_to_str(angle)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce:BB:IMPairment:RF{channel_cmd_val}:QUADrature:ANGLe {param}')

	def get(self, channel=repcap.Channel.Default) -> float:
		"""SCPI: [SOURce]:BB:IMPairment:RF<CH>:QUADrature:[ANGLe] \n
		Snippet: value: float = driver.source.bb.impairment.rf.quadrature.angle.get(channel = repcap.Channel.Default) \n
		No command help available \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Rf')
			:return: angle: No help available"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce:BB:IMPairment:RF{channel_cmd_val}:QUADrature:ANGLe?')
		return Conversions.str_to_float(response)
