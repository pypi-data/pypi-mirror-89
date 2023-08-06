from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Amam:
	"""Amam commands group definition. 4 total commands, 1 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("amam", core, parent)

	@property
	def file(self):
		"""file commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_file'):
			from .Amam_.File import File
			self._file = File(self._core, self._base)
		return self._file

	def clone(self) -> 'Amam':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Amam(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
