from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.RepeatedCapability import RepeatedCapability
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sensor:
	"""Sensor commands group definition. 1 total commands, 1 Sub-groups, 0 group commands
	Repeated Capability: Channel, default value after init: Channel.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sensor", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_channel_get', 'repcap_channel_set', repcap.Channel.Nr1)

	def repcap_channel_set(self, enum_value: repcap.Channel) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Channel.Default
		Default value after init: Channel.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_channel_get(self) -> repcap.Channel:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def power(self):
		"""power commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_power'):
			from .Sensor_.Power import Power
			self._power = Power(self._core, self._base)
		return self._power

	def clone(self) -> 'Sensor':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Sensor(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
