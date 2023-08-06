from typing import List

from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.ArgSingleSuppressed import ArgSingleSuppressed
from .......Internal.Types import DataType


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Maximum:
	"""Maximum commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("maximum", core, parent)

	def read(self) -> List[int]:
		"""SCPI: READ:WCDMa:SIGNaling<instance>:HACK:TRACe:SUBFrame:CARRier<carrier>:TBLock:MAXimum \n
		Snippet: value: List[int] = driver.hack.trace.subframe.carrier.transportBlock.maximum.read() \n
		Returns the trace results per carrier with details on transport block size in subframes. Commands query minimum or
		maximum values. The number of results depends on the configured number of subframes N to be measured per measurement
		cycle, see method RsCmwWcdmaSig.Configure.Hack.msFrames. \n
		Use RsCmwWcdmaSig.reliability.last_value to read the updated reliability indicator. \n
		Global Repeated Capabilities: repcap.Carrier
			:return: block: Detected transport block size index Range: 0 to 7"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_int_list_suppressed(f'READ:WCDMa:SIGNaling<Instance>:HACK:TRACe:SUBFrame:CARRier<Carrier>:TBLock:MAXimum?', suppressed)
		return response

	def fetch(self) -> List[int]:
		"""SCPI: FETCh:WCDMa:SIGNaling<instance>:HACK:TRACe:SUBFrame:CARRier<carrier>:TBLock:MAXimum \n
		Snippet: value: List[int] = driver.hack.trace.subframe.carrier.transportBlock.maximum.fetch() \n
		Returns the trace results per carrier with details on transport block size in subframes. Commands query minimum or
		maximum values. The number of results depends on the configured number of subframes N to be measured per measurement
		cycle, see method RsCmwWcdmaSig.Configure.Hack.msFrames. \n
		Use RsCmwWcdmaSig.reliability.last_value to read the updated reliability indicator. \n
		Global Repeated Capabilities: repcap.Carrier
			:return: block: Detected transport block size index Range: 0 to 7"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_int_list_suppressed(f'FETCh:WCDMa:SIGNaling<Instance>:HACK:TRACe:SUBFrame:CARRier<Carrier>:TBLock:MAXimum?', suppressed)
		return response
