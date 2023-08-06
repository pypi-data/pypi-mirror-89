from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ack:
	"""Ack commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ack", core, parent)

	# noinspection PyTypeChecker
	def get_fmode(self) -> enums.FMode:
		"""SCPI: CONFigure:EVDO:SIGNaling<instance>:LAYer:APPLication:FMCTap:ACK:FMODe \n
		Snippet: value: enums.FMode = driver.configure.layer.application.fmctap.ack.get_fmode() \n
		Configures the ACK channel bit fixed mode (see 3GPP2 C.S0029) for a carrier. Preselect the related carrier using the
		method RsCmwEvdoSig.Configure.Carrier.setting command. \n
			:return: fm_ode: NUSed | AALWays | NAALways Not used, ACK always, NACK always
		"""
		response = self._core.io.query_str('CONFigure:EVDO:SIGNaling<Instance>:LAYer:APPLication:FMCTap:ACK:FMODe?')
		return Conversions.str_to_scalar_enum(response, enums.FMode)

	def set_fmode(self, fm_ode: enums.FMode) -> None:
		"""SCPI: CONFigure:EVDO:SIGNaling<instance>:LAYer:APPLication:FMCTap:ACK:FMODe \n
		Snippet: driver.configure.layer.application.fmctap.ack.set_fmode(fm_ode = enums.FMode.AALWays) \n
		Configures the ACK channel bit fixed mode (see 3GPP2 C.S0029) for a carrier. Preselect the related carrier using the
		method RsCmwEvdoSig.Configure.Carrier.setting command. \n
			:param fm_ode: NUSed | AALWays | NAALways Not used, ACK always, NACK always
		"""
		param = Conversions.enum_scalar_to_str(fm_ode, enums.FMode)
		self._core.io.write(f'CONFigure:EVDO:SIGNaling<Instance>:LAYer:APPLication:FMCTap:ACK:FMODe {param}')

	def get_mtype(self) -> bool:
		"""SCPI: CONFigure:EVDO:SIGNaling<instance>:LAYer:APPLication:FMCTap:ACK:MTYPe \n
		Snippet: value: bool = driver.configure.layer.application.fmctap.ack.get_mtype() \n
		Queries if the ACK channel modulation type fixed mode (see 3GPP2 C.S0029) is enabled for a carrier. Currently this mode
		is always switched off. Preselect the related carrier using the method RsCmwEvdoSig.Configure.Carrier.setting command. \n
			:return: mtype: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:EVDO:SIGNaling<Instance>:LAYer:APPLication:FMCTap:ACK:MTYPe?')
		return Conversions.str_to_bool(response)
