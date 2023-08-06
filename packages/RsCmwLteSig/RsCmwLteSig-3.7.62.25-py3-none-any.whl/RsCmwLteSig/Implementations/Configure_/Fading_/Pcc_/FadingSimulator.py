from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FadingSimulator:
	"""FadingSimulator commands group definition. 19 total commands, 8 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("fadingSimulator", core, parent)

	@property
	def globale(self):
		"""globale commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_globale'):
			from .FadingSimulator_.Globale import Globale
			self._globale = Globale(self._core, self._base)
		return self._globale

	@property
	def bypass(self):
		"""bypass commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bypass'):
			from .FadingSimulator_.Bypass import Bypass
			self._bypass = Bypass(self._core, self._base)
		return self._bypass

	@property
	def standard(self):
		"""standard commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_standard'):
			from .FadingSimulator_.Standard import Standard
			self._standard = Standard(self._core, self._base)
		return self._standard

	@property
	def restart(self):
		"""restart commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_restart'):
			from .FadingSimulator_.Restart import Restart
			self._restart = Restart(self._core, self._base)
		return self._restart

	@property
	def insertionLoss(self):
		"""insertionLoss commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_insertionLoss'):
			from .FadingSimulator_.InsertionLoss import InsertionLoss
			self._insertionLoss = InsertionLoss(self._core, self._base)
		return self._insertionLoss

	@property
	def dshift(self):
		"""dshift commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_dshift'):
			from .FadingSimulator_.Dshift import Dshift
			self._dshift = Dshift(self._core, self._base)
		return self._dshift

	@property
	def matrix(self):
		"""matrix commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_matrix'):
			from .FadingSimulator_.Matrix import Matrix
			self._matrix = Matrix(self._core, self._base)
		return self._matrix

	@property
	def hmat(self):
		"""hmat commands group. 2 Sub-classes, 2 commands."""
		if not hasattr(self, '_hmat'):
			from .FadingSimulator_.Hmat import Hmat
			self._hmat = Hmat(self._core, self._base)
		return self._hmat

	# noinspection PyTypeChecker
	def get_kconstant(self) -> enums.KeepConstant:
		"""SCPI: CONFigure:LTE:SIGNaling<instance>:FADing[:PCC]:FSIMulator:KCONstant \n
		Snippet: value: enums.KeepConstant = driver.configure.fading.pcc.fadingSimulator.get_kconstant() \n
		No command help available \n
			:return: keep_constant: No help available
		"""
		response = self._core.io.query_str('CONFigure:LTE:SIGNaling<Instance>:FADing:PCC:FSIMulator:KCONstant?')
		return Conversions.str_to_scalar_enum(response, enums.KeepConstant)

	def set_kconstant(self, keep_constant: enums.KeepConstant) -> None:
		"""SCPI: CONFigure:LTE:SIGNaling<instance>:FADing[:PCC]:FSIMulator:KCONstant \n
		Snippet: driver.configure.fading.pcc.fadingSimulator.set_kconstant(keep_constant = enums.KeepConstant.DSHift) \n
		No command help available \n
			:param keep_constant: No help available
		"""
		param = Conversions.enum_scalar_to_str(keep_constant, enums.KeepConstant)
		self._core.io.write(f'CONFigure:LTE:SIGNaling<Instance>:FADing:PCC:FSIMulator:KCONstant {param}')

	def get_enable(self) -> bool:
		"""SCPI: CONFigure:LTE:SIGNaling<instance>:FADing[:PCC]:FSIMulator:ENABle \n
		Snippet: value: bool = driver.configure.fading.pcc.fadingSimulator.get_enable() \n
		Enables/disables the fading simulator. \n
			:return: enable: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:LTE:SIGNaling<Instance>:FADing:PCC:FSIMulator:ENABle?')
		return Conversions.str_to_bool(response)

	def set_enable(self, enable: bool) -> None:
		"""SCPI: CONFigure:LTE:SIGNaling<instance>:FADing[:PCC]:FSIMulator:ENABle \n
		Snippet: driver.configure.fading.pcc.fadingSimulator.set_enable(enable = False) \n
		Enables/disables the fading simulator. \n
			:param enable: OFF | ON
		"""
		param = Conversions.bool_to_str(enable)
		self._core.io.write(f'CONFigure:LTE:SIGNaling<Instance>:FADing:PCC:FSIMulator:ENABle {param}')

	# noinspection PyTypeChecker
	def get_profile(self) -> enums.FadingProfile:
		"""SCPI: CONFigure:LTE:SIGNaling<instance>:FADing[:PCC]:FSIMulator:PROFile \n
		Snippet: value: enums.FadingProfile = driver.configure.fading.pcc.fadingSimulator.get_profile() \n
		Selects a propagation condition profile for fading. \n
			:return: profile: EP5Low | EP5Medium | EP5High | EV5Low | EV5Medium | EV5High | EV7Low | EV7Medium | EV7High | ET7Low | ET7Medium | ET7High | ET3Low | ET3Medium | ET3High | HSTRain | HST | CTESt | ETL30 | ETM30 | ETH30 | EVL200 | EVM200 | EVH200 | UMI3 | UMI30 | UMA3 | UMA30 EP5Low | EP5Medium | EP5High EPA, 5-Hz Doppler, low/medium/high correlation ETL30 | ETM30 | ETH30 ETU, 30-Hz Doppler, low/medium/high correlation ET7Low | ET7Medium | ET7High ETU, 70-Hz Doppler, low/medium/high correlation ET3Low | ET3Medium | ET3High ETU, 300-Hz Doppler, low/medium/high correlation EV5Low | EV5Medium | EV5High EVA, 5-Hz Doppler, low/medium/high correlation EV7Low | EV7Medium | EV7High EVA, 70-Hz Doppler, low/medium/high correlation EVL200 | EVM200 | EVH200 EVA, 200-Hz Doppler, low/medium/high correlation HSTRain | HST High-speed train scenario (both values have the same effect) CTESt Multi-path profile for CQI tests UMI3 | UMI30 SCME UMi, 3 km/h or 30 km/h UMA3 | UMA30 SCME UMa, 3 km/h or 30 km/h
		"""
		response = self._core.io.query_str('CONFigure:LTE:SIGNaling<Instance>:FADing:PCC:FSIMulator:PROFile?')
		return Conversions.str_to_scalar_enum(response, enums.FadingProfile)

	def set_profile(self, profile: enums.FadingProfile) -> None:
		"""SCPI: CONFigure:LTE:SIGNaling<instance>:FADing[:PCC]:FSIMulator:PROFile \n
		Snippet: driver.configure.fading.pcc.fadingSimulator.set_profile(profile = enums.FadingProfile.CTESt) \n
		Selects a propagation condition profile for fading. \n
			:param profile: EP5Low | EP5Medium | EP5High | EV5Low | EV5Medium | EV5High | EV7Low | EV7Medium | EV7High | ET7Low | ET7Medium | ET7High | ET3Low | ET3Medium | ET3High | HSTRain | HST | CTESt | ETL30 | ETM30 | ETH30 | EVL200 | EVM200 | EVH200 | UMI3 | UMI30 | UMA3 | UMA30 EP5Low | EP5Medium | EP5High EPA, 5-Hz Doppler, low/medium/high correlation ETL30 | ETM30 | ETH30 ETU, 30-Hz Doppler, low/medium/high correlation ET7Low | ET7Medium | ET7High ETU, 70-Hz Doppler, low/medium/high correlation ET3Low | ET3Medium | ET3High ETU, 300-Hz Doppler, low/medium/high correlation EV5Low | EV5Medium | EV5High EVA, 5-Hz Doppler, low/medium/high correlation EV7Low | EV7Medium | EV7High EVA, 70-Hz Doppler, low/medium/high correlation EVL200 | EVM200 | EVH200 EVA, 200-Hz Doppler, low/medium/high correlation HSTRain | HST High-speed train scenario (both values have the same effect) CTESt Multi-path profile for CQI tests UMI3 | UMI30 SCME UMi, 3 km/h or 30 km/h UMA3 | UMA30 SCME UMa, 3 km/h or 30 km/h
		"""
		param = Conversions.enum_scalar_to_str(profile, enums.FadingProfile)
		self._core.io.write(f'CONFigure:LTE:SIGNaling<Instance>:FADing:PCC:FSIMulator:PROFile {param}')

	def clone(self) -> 'FadingSimulator':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = FadingSimulator(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
