from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal.RepeatedCapability import RepeatedCapability
from ... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ncell:
	"""Ncell commands group definition. 20 total commands, 7 Sub-groups, 0 group commands
	Repeated Capability: CellNo, default value after init: CellNo.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ncell", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_cellNo_get', 'repcap_cellNo_set', repcap.CellNo.Nr1)

	def repcap_cellNo_set(self, enum_value: repcap.CellNo) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to CellNo.Default
		Default value after init: CellNo.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_cellNo_get(self) -> repcap.CellNo:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def all(self):
		"""all commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_all'):
			from .Ncell_.All import All
			self._all = All(self._core, self._base)
		return self._all

	@property
	def lte(self):
		"""lte commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_lte'):
			from .Ncell_.Lte import Lte
			self._lte = Lte(self._core, self._base)
		return self._lte

	@property
	def gsm(self):
		"""gsm commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_gsm'):
			from .Ncell_.Gsm import Gsm
			self._gsm = Gsm(self._core, self._base)
		return self._gsm

	@property
	def wcdma(self):
		"""wcdma commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_wcdma'):
			from .Ncell_.Wcdma import Wcdma
			self._wcdma = Wcdma(self._core, self._base)
		return self._wcdma

	@property
	def cdma(self):
		"""cdma commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_cdma'):
			from .Ncell_.Cdma import Cdma
			self._cdma = Cdma(self._core, self._base)
		return self._cdma

	@property
	def evdo(self):
		"""evdo commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_evdo'):
			from .Ncell_.Evdo import Evdo
			self._evdo = Evdo(self._core, self._base)
		return self._evdo

	@property
	def tdscdma(self):
		"""tdscdma commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_tdscdma'):
			from .Ncell_.Tdscdma import Tdscdma
			self._tdscdma = Tdscdma(self._core, self._base)
		return self._tdscdma

	def clone(self) -> 'Ncell':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Ncell(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
