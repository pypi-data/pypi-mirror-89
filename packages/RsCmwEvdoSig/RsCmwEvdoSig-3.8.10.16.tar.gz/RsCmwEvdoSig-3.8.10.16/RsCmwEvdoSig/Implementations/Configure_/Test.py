from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Test:
	"""Test commands group definition. 2 total commands, 1 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("test", core, parent)

	@property
	def cstatus(self):
		"""cstatus commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_cstatus'):
			from .Test_.Cstatus import Cstatus
			self._cstatus = Cstatus(self._core, self._base)
		return self._cstatus

	def clone(self) -> 'Test':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Test(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
