from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Setc:
	"""Setc commands group definition. 8 total commands, 1 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("setc", core, parent)

	@property
	def apPower(self):
		"""apPower commands group. 5 Sub-classes, 3 commands."""
		if not hasattr(self, '_apPower'):
			from .Setc_.ApPower import ApPower
			self._apPower = ApPower(self._core, self._base)
		return self._apPower

	def clone(self) -> 'Setc':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Setc(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
