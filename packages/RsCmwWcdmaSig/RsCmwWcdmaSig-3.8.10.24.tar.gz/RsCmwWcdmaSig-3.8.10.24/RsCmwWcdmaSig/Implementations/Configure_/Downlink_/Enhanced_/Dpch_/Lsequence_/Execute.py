from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Execute:
	"""Execute commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("execute", core, parent)

	def set(self) -> None:
		"""SCPI: CONFigure:WCDMa:SIGNaling<instance>:DL:ENHanced:DPCH:LSEQuence:EXECute \n
		Snippet: driver.configure.downlink.enhanced.dpch.lsequence.execute.set() \n
		Initiates the DPCH level transitions in downlink according to out-of-sync power mask. The function is only available
		during a call. \n
		"""
		self._core.io.write(f'CONFigure:WCDMa:SIGNaling<Instance>:DL:ENHanced:DPCH:LSEQuence:EXECute')

	def set_with_opc(self) -> None:
		"""SCPI: CONFigure:WCDMa:SIGNaling<instance>:DL:ENHanced:DPCH:LSEQuence:EXECute \n
		Snippet: driver.configure.downlink.enhanced.dpch.lsequence.execute.set_with_opc() \n
		Initiates the DPCH level transitions in downlink according to out-of-sync power mask. The function is only available
		during a call. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsCmwWcdmaSig.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'CONFigure:WCDMa:SIGNaling<Instance>:DL:ENHanced:DPCH:LSEQuence:EXECute')
