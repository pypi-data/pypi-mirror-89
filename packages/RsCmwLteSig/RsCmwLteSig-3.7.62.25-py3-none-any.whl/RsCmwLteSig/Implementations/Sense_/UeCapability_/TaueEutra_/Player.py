from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Player:
	"""Player commands group definition. 9 total commands, 0 Sub-groups, 9 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("player", core, parent)

	def get_uta_supported(self) -> bool:
		"""SCPI: SENSe:LTE:SIGNaling<instance>:UECapability:TAUeeutra:PLAYer:UTASupported \n
		Snippet: value: bool = driver.sense.ueCapability.taueEutra.player.get_uta_supported() \n
		Returns whether the UE supports transmit antenna selection or not. \n
			:return: ue_tx_ant_sel_supp: OFF | ON
		"""
		response = self._core.io.query_str('SENSe:LTE:SIGNaling<Instance>:UECapability:TAUeeutra:PLAYer:UTASupported?')
		return Conversions.str_to_bool(response)

	def get_usrs_support(self) -> bool:
		"""SCPI: SENSe:LTE:SIGNaling<instance>:UECapability:TAUeeutra:PLAYer:USRSsupport \n
		Snippet: value: bool = driver.sense.ueCapability.taueEutra.player.get_usrs_support() \n
		Returns whether the UE supports PDSCH transmission mode 7 for FDD or not. \n
			:return: ue_sp_ref_sigs_supp: OFF | ON
		"""
		response = self._core.io.query_str('SENSe:LTE:SIGNaling<Instance>:UECapability:TAUeeutra:PLAYer:USRSsupport?')
		return Conversions.str_to_bool(response)

	def get_tapp_support(self) -> bool:
		"""SCPI: SENSe:LTE:SIGNaling<instance>:UECapability:TAUeeutra:PLAYer:TAPPsupport \n
		Snippet: value: bool = driver.sense.ueCapability.taueEutra.player.get_tapp_support() \n
		Returns whether the UE supports transmit diversity for specific PUCCH formats. \n
			:return: supported: OFF | ON
		"""
		response = self._core.io.query_str('SENSe:LTE:SIGNaling<Instance>:UECapability:TAUeeutra:PLAYer:TAPPsupport?')
		return Conversions.str_to_bool(response)

	def get_twef_support(self) -> bool:
		"""SCPI: SENSe:LTE:SIGNaling<instance>:UECapability:TAUeeutra:PLAYer:TWEFsupport \n
		Snippet: value: bool = driver.sense.ueCapability.taueEutra.player.get_twef_support() \n
		Returns whether the UE supports PDSCH TM 9 with 8 CSI reference signal ports for FDD. \n
			:return: supported: OFF | ON
		"""
		response = self._core.io.query_str('SENSe:LTE:SIGNaling<Instance>:UECapability:TAUeeutra:PLAYer:TWEFsupport?')
		return Conversions.str_to_bool(response)

	def get_pd_support(self) -> bool:
		"""SCPI: SENSe:LTE:SIGNaling<instance>:UECapability:TAUeeutra:PLAYer:PDSupport \n
		Snippet: value: bool = driver.sense.ueCapability.taueEutra.player.get_pd_support() \n
		Returns whether the UE supports PMI disabling. \n
			:return: supported: OFF | ON
		"""
		response = self._core.io.query_str('SENSe:LTE:SIGNaling<Instance>:UECapability:TAUeeutra:PLAYer:PDSupport?')
		return Conversions.str_to_bool(response)

	def get_ccs_support(self) -> bool:
		"""SCPI: SENSe:LTE:SIGNaling<instance>:UECapability:TAUeeutra:PLAYer:CCSSupport \n
		Snippet: value: bool = driver.sense.ueCapability.taueEutra.player.get_ccs_support() \n
		Returns whether the UE supports cross-carrier scheduling for CA. \n
			:return: supported: OFF | ON
		"""
		response = self._core.io.query_str('SENSe:LTE:SIGNaling<Instance>:UECapability:TAUeeutra:PLAYer:CCSSupport?')
		return Conversions.str_to_bool(response)

	def get_spp_support(self) -> bool:
		"""SCPI: SENSe:LTE:SIGNaling<instance>:UECapability:TAUeeutra:PLAYer:SPPSupport \n
		Snippet: value: bool = driver.sense.ueCapability.taueEutra.player.get_spp_support() \n
		Returns whether the UE supports the simultaneous transmission of PUCCH and PUSCH. \n
			:return: supported: OFF | ON
		"""
		response = self._core.io.query_str('SENSe:LTE:SIGNaling<Instance>:UECapability:TAUeeutra:PLAYer:SPPSupport?')
		return Conversions.str_to_bool(response)

	def get_mcpc_support(self) -> bool:
		"""SCPI: SENSe:LTE:SIGNaling<instance>:UECapability:TAUeeutra:PLAYer:MCPCsupport \n
		Snippet: value: bool = driver.sense.ueCapability.taueEutra.player.get_mcpc_support() \n
		Returns whether the UE supports multi-cluster PUSCH transmission within a CC. \n
			:return: supported: OFF | ON
		"""
		response = self._core.io.query_str('SENSe:LTE:SIGNaling<Instance>:UECapability:TAUeeutra:PLAYer:MCPCsupport?')
		return Conversions.str_to_bool(response)

	def get_nurc_list(self) -> List[bool]:
		"""SCPI: SENSe:LTE:SIGNaling<instance>:UECapability:TAUeeutra:PLAYer:NURClist \n
		Snippet: value: List[bool] = driver.sense.ueCapability.taueEutra.player.get_nurc_list() \n
		Returns a list of values, indicating whether the UE supports non-contiguous UL resource allocations within a CC for the
		individual E-UTRA operating bands. \n
			:return: supported_band: OFF | ON 256 values: user-defined band, band 1 to band 255
		"""
		response = self._core.io.query_str('SENSe:LTE:SIGNaling<Instance>:UECapability:TAUeeutra:PLAYer:NURClist?')
		return Conversions.str_to_bool_list(response)
