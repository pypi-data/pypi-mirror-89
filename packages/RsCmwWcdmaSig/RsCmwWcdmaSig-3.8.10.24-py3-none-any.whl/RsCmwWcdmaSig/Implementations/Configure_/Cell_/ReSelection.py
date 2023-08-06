from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.StructBase import StructBase
from ....Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ReSelection:
	"""ReSelection commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("reSelection", core, parent)

	# noinspection PyTypeChecker
	class SearchStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Sintrasearch: float: Range: -32 dB to 20 dB, Unit: dB
			- Sintersearch: float: Range: -32 dB to 20 dB, Unit: dB
			- Ssearchrat: float: Range: -32 dB to 20 dB, Unit: dB"""
		__meta_args_list = [
			ArgStruct.scalar_float('Sintrasearch'),
			ArgStruct.scalar_float('Sintersearch'),
			ArgStruct.scalar_float('Ssearchrat')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Sintrasearch: float = None
			self.Sintersearch: float = None
			self.Ssearchrat: float = None

	def get_search(self) -> SearchStruct:
		"""SCPI: CONFigure:WCDMa:SIGNaling<instance>:CELL:RESelection:SEARch \n
		Snippet: value: SearchStruct = driver.configure.cell.reSelection.get_search() \n
		Defines the thresholds Sintrasearch, Sintersearch and S searchRAT m = GSM required for cell reselection.
		They are transmitted to the UE in the system information. \n
			:return: structure: for return value, see the help for SearchStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:WCDMa:SIGNaling<Instance>:CELL:RESelection:SEARch?', self.__class__.SearchStruct())

	def set_search(self, value: SearchStruct) -> None:
		"""SCPI: CONFigure:WCDMa:SIGNaling<instance>:CELL:RESelection:SEARch \n
		Snippet: driver.configure.cell.reSelection.set_search(value = SearchStruct()) \n
		Defines the thresholds Sintrasearch, Sintersearch and S searchRAT m = GSM required for cell reselection.
		They are transmitted to the UE in the system information. \n
			:param value: see the help for SearchStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:WCDMa:SIGNaling<Instance>:CELL:RESelection:SEARch', value)

	# noinspection PyTypeChecker
	class QualityStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Qqualmin: float: Minimum required quality level in the reselection target cell. Range: -24 dB to 0 dB, Unit: dB
			- Qrxlevmin: float: Minimum RX level at a UE antenna required for reselection to the UMTS cell Range: -115 dBm to -25 dBm, Unit: dBm
			- Qrxlevmin_Eutra: float: Minimum RX level at a UE antenna required for access to the LTE cell Range: -140 dBm to -44 dBm, Unit: dBm
			- Qhyst_1_S: float: Hysteresis used for GSM, TDD and for FDD cells in case the quality measure for reselection is set to CPICH RSCP Range: 0 dB to 40 dB, Unit: dB
			- Qhyst_2_S: float: Hysteresis used for FDD cells if the quality measure for reselection is set to CPICH Ec/No Range: 0 dB to 40 dB, Unit: dB"""
		__meta_args_list = [
			ArgStruct.scalar_float('Qqualmin'),
			ArgStruct.scalar_float('Qrxlevmin'),
			ArgStruct.scalar_float('Qrxlevmin_Eutra'),
			ArgStruct.scalar_float('Qhyst_1_S'),
			ArgStruct.scalar_float('Qhyst_2_S')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Qqualmin: float = None
			self.Qrxlevmin: float = None
			self.Qrxlevmin_Eutra: float = None
			self.Qhyst_1_S: float = None
			self.Qhyst_2_S: float = None

	def get_quality(self) -> QualityStruct:
		"""SCPI: CONFigure:WCDMa:SIGNaling<instance>:CELL:RESelection:QUALity \n
		Snippet: value: QualityStruct = driver.configure.cell.reSelection.get_quality() \n
		Defines the power levels required for cell reselection. They are transmitted to the UE in the system information. \n
			:return: structure: for return value, see the help for QualityStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:WCDMa:SIGNaling<Instance>:CELL:RESelection:QUALity?', self.__class__.QualityStruct())

	def set_quality(self, value: QualityStruct) -> None:
		"""SCPI: CONFigure:WCDMa:SIGNaling<instance>:CELL:RESelection:QUALity \n
		Snippet: driver.configure.cell.reSelection.set_quality(value = QualityStruct()) \n
		Defines the power levels required for cell reselection. They are transmitted to the UE in the system information. \n
			:param value: see the help for QualityStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:WCDMa:SIGNaling<Instance>:CELL:RESelection:QUALity', value)

	def get_time(self) -> float:
		"""SCPI: CONFigure:WCDMa:SIGNaling<instance>:CELL:RESelection:TIME \n
		Snippet: value: float = driver.configure.cell.reSelection.get_time() \n
		Sets the time hysteresis for the cell reselection algorithm. \n
			:return: treselections: Range: 0 s to 31 s
		"""
		response = self._core.io.query_str('CONFigure:WCDMa:SIGNaling<Instance>:CELL:RESelection:TIME?')
		return Conversions.str_to_float(response)

	def set_time(self, treselections: float) -> None:
		"""SCPI: CONFigure:WCDMa:SIGNaling<instance>:CELL:RESelection:TIME \n
		Snippet: driver.configure.cell.reSelection.set_time(treselections = 1.0) \n
		Sets the time hysteresis for the cell reselection algorithm. \n
			:param treselections: Range: 0 s to 31 s
		"""
		param = Conversions.decimal_value_to_str(treselections)
		self._core.io.write(f'CONFigure:WCDMa:SIGNaling<Instance>:CELL:RESelection:TIME {param}')
