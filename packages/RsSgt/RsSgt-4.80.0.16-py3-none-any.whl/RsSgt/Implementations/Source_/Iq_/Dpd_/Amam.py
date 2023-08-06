from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Amam:
	"""Amam commands group definition. 4 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("amam", core, parent)

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Amam_.State import State
			self._state = State(self._core, self._base)
		return self._state

	@property
	def value(self):
		"""value commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_value'):
			from .Amam_.Value import Value
			self._value = Value(self._core, self._base)
		return self._value

	def clone(self) -> 'Amam':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Amam(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
