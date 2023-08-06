from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Rmin:
	"""Rmin commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rmin", core, parent)

	def get_index(self) -> int:
		"""SCPI: CONFigure:EVDO:SIGNaling<instance>:LAYer:APPLication:RTAP:RMIN:INDex \n
		Snippet: value: int = driver.configure.layer.application.rtap.rmin.get_index() \n
		Selects the minimum data rate index for RTAP packets. Use method RsCmwEvdoSig.Configure.Layer.Application.Rtap.Rmin.rate
		to query the corresponding data rate. \n
			:return: rm_in_index: Range: 0 to 5
		"""
		response = self._core.io.query_str('CONFigure:EVDO:SIGNaling<Instance>:LAYer:APPLication:RTAP:RMIN:INDex?')
		return Conversions.str_to_int(response)

	def set_index(self, rm_in_index: int) -> None:
		"""SCPI: CONFigure:EVDO:SIGNaling<instance>:LAYer:APPLication:RTAP:RMIN:INDex \n
		Snippet: driver.configure.layer.application.rtap.rmin.set_index(rm_in_index = 1) \n
		Selects the minimum data rate index for RTAP packets. Use method RsCmwEvdoSig.Configure.Layer.Application.Rtap.Rmin.rate
		to query the corresponding data rate. \n
			:param rm_in_index: Range: 0 to 5
		"""
		param = Conversions.decimal_value_to_str(rm_in_index)
		self._core.io.write(f'CONFigure:EVDO:SIGNaling<Instance>:LAYer:APPLication:RTAP:RMIN:INDex {param}')

	def get_rate(self) -> float:
		"""SCPI: CONFigure:EVDO:SIGNaling<instance>:LAYer:APPLication:RTAP:RMIN:RATE \n
		Snippet: value: float = driver.configure.layer.application.rtap.rmin.get_rate() \n
		Queries the data rate for the selected minimum data rate index (method RsCmwEvdoSig.Configure.Layer.Application.Rtap.Rmin.
		index) . \n
			:return: rm_in_rate: Range: 0 kbit/s to 153.6 kbit/s
		"""
		response = self._core.io.query_str('CONFigure:EVDO:SIGNaling<Instance>:LAYer:APPLication:RTAP:RMIN:RATE?')
		return Conversions.str_to_float(response)
