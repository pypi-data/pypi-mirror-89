from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class InsertionLoss:
	"""InsertionLoss commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("insertionLoss", core, parent)

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.InsertLossMode:
		"""SCPI: CONFigure:EVDO:SIGNaling<instance>:FADing:FSIMulator:ILOSs:MODE \n
		Snippet: value: enums.InsertLossMode = driver.configure.fading.fsimulator.insertionLoss.get_mode() \n
		Sets the insertion loss mode. \n
			:return: insert_loss_mode: NORMal | USER NORMal: the insertion loss is determined by the fading profile USER: the insertion loss can be adjusted manually
		"""
		response = self._core.io.query_str('CONFigure:EVDO:SIGNaling<Instance>:FADing:FSIMulator:ILOSs:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.InsertLossMode)

	def set_mode(self, insert_loss_mode: enums.InsertLossMode) -> None:
		"""SCPI: CONFigure:EVDO:SIGNaling<instance>:FADing:FSIMulator:ILOSs:MODE \n
		Snippet: driver.configure.fading.fsimulator.insertionLoss.set_mode(insert_loss_mode = enums.InsertLossMode.NORMal) \n
		Sets the insertion loss mode. \n
			:param insert_loss_mode: NORMal | USER NORMal: the insertion loss is determined by the fading profile USER: the insertion loss can be adjusted manually
		"""
		param = Conversions.enum_scalar_to_str(insert_loss_mode, enums.InsertLossMode)
		self._core.io.write(f'CONFigure:EVDO:SIGNaling<Instance>:FADing:FSIMulator:ILOSs:MODE {param}')

	def get_loss(self) -> float:
		"""SCPI: CONFigure:EVDO:SIGNaling<instance>:FADing:FSIMulator:ILOSs:LOSS \n
		Snippet: value: float = driver.configure.fading.fsimulator.insertionLoss.get_loss() \n
		Sets the insertion loss for the fading simulator. A setting is only allowed in USER mode (see method RsCmwEvdoSig.
		Configure.Fading.Fsimulator.InsertionLoss.mode) . \n
			:return: insertion_loss: Range: 0 dB to 18 dB , Unit: dB
		"""
		response = self._core.io.query_str('CONFigure:EVDO:SIGNaling<Instance>:FADing:FSIMulator:ILOSs:LOSS?')
		return Conversions.str_to_float(response)

	def set_loss(self, insertion_loss: float) -> None:
		"""SCPI: CONFigure:EVDO:SIGNaling<instance>:FADing:FSIMulator:ILOSs:LOSS \n
		Snippet: driver.configure.fading.fsimulator.insertionLoss.set_loss(insertion_loss = 1.0) \n
		Sets the insertion loss for the fading simulator. A setting is only allowed in USER mode (see method RsCmwEvdoSig.
		Configure.Fading.Fsimulator.InsertionLoss.mode) . \n
			:param insertion_loss: Range: 0 dB to 18 dB , Unit: dB
		"""
		param = Conversions.decimal_value_to_str(insertion_loss)
		self._core.io.write(f'CONFigure:EVDO:SIGNaling<Instance>:FADing:FSIMulator:ILOSs:LOSS {param}')

	def get_csamples(self) -> float:
		"""SCPI: CONFigure:EVDO:SIGNaling<instance>:FADing:FSIMulator:ILOSs:CSAMples \n
		Snippet: value: float = driver.configure.fading.fsimulator.insertionLoss.get_csamples() \n
		No command help available \n
			:return: clipped_samples: No help available
		"""
		response = self._core.io.query_str('CONFigure:EVDO:SIGNaling<Instance>:FADing:FSIMulator:ILOSs:CSAMples?')
		return Conversions.str_to_float(response)
