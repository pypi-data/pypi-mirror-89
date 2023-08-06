from ..Internal.Core import Core
from ..Internal.CommandsGroup import CommandsGroup
from ..Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Configure:
	"""Configure commands group definition. 748 total commands, 23 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("configure", core, parent)

	@property
	def scc(self):
		"""scc commands group. 5 Sub-classes, 1 commands."""
		if not hasattr(self, '_scc'):
			from .Configure_.Scc import Scc
			self._scc = Scc(self._core, self._base)
		return self._scc

	@property
	def pcc(self):
		"""pcc commands group. 2 Sub-classes, 2 commands."""
		if not hasattr(self, '_pcc'):
			from .Configure_.Pcc import Pcc
			self._pcc = Pcc(self._core, self._base)
		return self._pcc

	@property
	def rfSettings(self):
		"""rfSettings commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_rfSettings'):
			from .Configure_.RfSettings import RfSettings
			self._rfSettings = RfSettings(self._core, self._base)
		return self._rfSettings

	@property
	def iqIn(self):
		"""iqIn commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_iqIn'):
			from .Configure_.IqIn import IqIn
			self._iqIn = IqIn(self._core, self._base)
		return self._iqIn

	@property
	def fading(self):
		"""fading commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_fading'):
			from .Configure_.Fading import Fading
			self._fading = Fading(self._core, self._base)
		return self._fading

	@property
	def caggregation(self):
		"""caggregation commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_caggregation'):
			from .Configure_.Caggregation import Caggregation
			self._caggregation = Caggregation(self._core, self._base)
		return self._caggregation

	@property
	def ncell(self):
		"""ncell commands group. 7 Sub-classes, 0 commands."""
		if not hasattr(self, '_ncell'):
			from .Configure_.Ncell import Ncell
			self._ncell = Ncell(self._core, self._base)
		return self._ncell

	@property
	def a(self):
		"""a commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_a'):
			from .Configure_.A import A
			self._a = A(self._core, self._base)
		return self._a

	@property
	def b(self):
		"""b commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_b'):
			from .Configure_.B import B
			self._b = B(self._core, self._base)
		return self._b

	@property
	def downlink(self):
		"""downlink commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_downlink'):
			from .Configure_.Downlink import Downlink
			self._downlink = Downlink(self._core, self._base)
		return self._downlink

	@property
	def uplink(self):
		"""uplink commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_uplink'):
			from .Configure_.Uplink import Uplink
			self._uplink = Uplink(self._core, self._base)
		return self._uplink

	@property
	def cell(self):
		"""cell commands group. 15 Sub-classes, 3 commands."""
		if not hasattr(self, '_cell'):
			from .Configure_.Cell import Cell
			self._cell = Cell(self._core, self._base)
		return self._cell

	@property
	def connection(self):
		"""connection commands group. 12 Sub-classes, 33 commands."""
		if not hasattr(self, '_connection'):
			from .Configure_.Connection import Connection
			self._connection = Connection(self._core, self._base)
		return self._connection

	@property
	def cqiReporting(self):
		"""cqiReporting commands group. 3 Sub-classes, 3 commands."""
		if not hasattr(self, '_cqiReporting'):
			from .Configure_.CqiReporting import CqiReporting
			self._cqiReporting = CqiReporting(self._core, self._base)
		return self._cqiReporting

	@property
	def ueReport(self):
		"""ueReport commands group. 2 Sub-classes, 7 commands."""
		if not hasattr(self, '_ueReport'):
			from .Configure_.UeReport import UeReport
			self._ueReport = UeReport(self._core, self._base)
		return self._ueReport

	@property
	def ueCapability(self):
		"""ueCapability commands group. 1 Sub-classes, 5 commands."""
		if not hasattr(self, '_ueCapability'):
			from .Configure_.UeCapability import UeCapability
			self._ueCapability = UeCapability(self._core, self._base)
		return self._ueCapability

	@property
	def sms(self):
		"""sms commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_sms'):
			from .Configure_.Sms import Sms
			self._sms = Sms(self._core, self._base)
		return self._sms

	@property
	def cbs(self):
		"""cbs commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_cbs'):
			from .Configure_.Cbs import Cbs
			self._cbs = Cbs(self._core, self._base)
		return self._cbs

	@property
	def eeLog(self):
		"""eeLog commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_eeLog'):
			from .Configure_.EeLog import EeLog
			self._eeLog = EeLog(self._core, self._base)
		return self._eeLog

	@property
	def extendedBler(self):
		"""extendedBler commands group. 1 Sub-classes, 5 commands."""
		if not hasattr(self, '_extendedBler'):
			from .Configure_.ExtendedBler import ExtendedBler
			self._extendedBler = ExtendedBler(self._core, self._base)
		return self._extendedBler

	@property
	def throughput(self):
		"""throughput commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_throughput'):
			from .Configure_.Throughput import Throughput
			self._throughput = Throughput(self._core, self._base)
		return self._throughput

	@property
	def mmonitor(self):
		"""mmonitor commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_mmonitor'):
			from .Configure_.Mmonitor import Mmonitor
			self._mmonitor = Mmonitor(self._core, self._base)
		return self._mmonitor

	@property
	def sib(self):
		"""sib commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_sib'):
			from .Configure_.Sib import Sib
			self._sib = Sib(self._core, self._base)
		return self._sib

	def get_etoe(self) -> bool:
		"""SCPI: CONFigure:LTE:SIGNaling<instance>:ETOE \n
		Snippet: value: bool = driver.configure.get_etoe() \n
		No command help available \n
			:return: end_to_end_enable: No help available
		"""
		response = self._core.io.query_str('CONFigure:LTE:SIGNaling<Instance>:ETOE?')
		return Conversions.str_to_bool(response)

	def set_etoe(self, end_to_end_enable: bool) -> None:
		"""SCPI: CONFigure:LTE:SIGNaling<instance>:ETOE \n
		Snippet: driver.configure.set_etoe(end_to_end_enable = False) \n
		No command help available \n
			:param end_to_end_enable: No help available
		"""
		param = Conversions.bool_to_str(end_to_end_enable)
		self._core.io.write(f'CONFigure:LTE:SIGNaling<Instance>:ETOE {param}')

	def clone(self) -> 'Configure':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Configure(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
