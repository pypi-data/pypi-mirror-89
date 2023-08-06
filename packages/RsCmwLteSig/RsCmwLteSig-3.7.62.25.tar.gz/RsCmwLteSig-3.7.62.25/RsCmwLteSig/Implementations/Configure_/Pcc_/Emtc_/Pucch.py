from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pucch:
	"""Pucch commands group definition. 2 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pucch", core, parent)

	@property
	def b(self):
		"""b commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_b'):
			from .Pucch_.B import B
			self._b = B(self._core, self._base)
		return self._b

	@property
	def a(self):
		"""a commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_a'):
			from .Pucch_.A import A
			self._a = A(self._core, self._base)
		return self._a

	def clone(self) -> 'Pucch':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Pucch(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
