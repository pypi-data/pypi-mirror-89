from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class IqOut:
	"""IqOut commands group definition. 2 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("iqOut", core, parent)

	@property
	def pcc(self):
		"""pcc commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_pcc'):
			from .IqOut_.Pcc import Pcc
			self._pcc = Pcc(self._core, self._base)
		return self._pcc

	@property
	def scc(self):
		"""scc commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_scc'):
			from .IqOut_.Scc import Scc
			self._scc = Scc(self._core, self._base)
		return self._scc

	def clone(self) -> 'IqOut':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = IqOut(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
