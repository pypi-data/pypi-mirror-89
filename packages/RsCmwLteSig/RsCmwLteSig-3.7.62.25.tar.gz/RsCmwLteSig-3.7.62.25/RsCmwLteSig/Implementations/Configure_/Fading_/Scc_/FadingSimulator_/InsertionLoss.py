from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class InsertionLoss:
	"""InsertionLoss commands group definition. 2 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("insertionLoss", core, parent)

	@property
	def mode(self):
		"""mode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mode'):
			from .InsertionLoss_.Mode import Mode
			self._mode = Mode(self._core, self._base)
		return self._mode

	@property
	def loss(self):
		"""loss commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_loss'):
			from .InsertionLoss_.Loss import Loss
			self._loss = Loss(self._core, self._base)
		return self._loss

	def clone(self) -> 'InsertionLoss':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = InsertionLoss(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
