from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.RepeatedCapability import RepeatedCapability
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Utdd:
	"""Utdd commands group definition. 2 total commands, 2 Sub-groups, 0 group commands
	Repeated Capability: UTddFreq, default value after init: UTddFreq.Freq128"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("utdd", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_uTddFreq_get', 'repcap_uTddFreq_set', repcap.UTddFreq.Freq128)

	def repcap_uTddFreq_set(self, enum_value: repcap.UTddFreq) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to UTddFreq.Default
		Default value after init: UTddFreq.Freq128"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_uTddFreq_get(self) -> repcap.UTddFreq:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def supported(self):
		"""supported commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_supported'):
			from .Utdd_.Supported import Supported
			self._supported = Supported(self._core, self._base)
		return self._supported

	@property
	def ereDirection(self):
		"""ereDirection commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_ereDirection'):
			from .Utdd_.EreDirection import EreDirection
			self._ereDirection = EreDirection(self._core, self._base)
		return self._ereDirection

	def clone(self) -> 'Utdd':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Utdd(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
