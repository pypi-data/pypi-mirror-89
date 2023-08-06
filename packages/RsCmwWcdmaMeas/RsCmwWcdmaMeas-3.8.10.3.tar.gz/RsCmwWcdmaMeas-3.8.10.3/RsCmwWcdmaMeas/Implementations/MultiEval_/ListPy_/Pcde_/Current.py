from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.Types import DataType
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Current:
	"""Current commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("current", core, parent)

	# noinspection PyTypeChecker
	class FetchStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: decimal 'Reliability Indicator' In list mode, a zero reliability indicator indicates that the results in all measured segments are valid. A non-zero value indicates that an error occurred in at least one of the measured segments.
			- Return_Code: List[int]: decimal Reliability indicator for the segment. The meaning of the returned values is the same as for the common reliability indicator, see previous parameter.
			- Pcd_Error: List[float]: float Peak code domain error Range: -100 dB to 0 dB, Unit: dB
			- Pcd_Error_Phase: List[enums.PcdErrorPhase]: No parameter help available
			- Pcd_Error_Code_Nr: List[int]: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct('Return_Code', DataType.IntegerList, None, False, True, 1),
			ArgStruct('Pcd_Error', DataType.FloatList, None, False, True, 1),
			ArgStruct('Pcd_Error_Phase', DataType.EnumList, enums.PcdErrorPhase, False, True, 1),
			ArgStruct('Pcd_Error_Code_Nr', DataType.IntegerList, None, False, True, 1)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Return_Code: List[int] = None
			self.Pcd_Error: List[float] = None
			self.Pcd_Error_Phase: List[enums.PcdErrorPhase] = None
			self.Pcd_Error_Code_Nr: List[int] = None

	def fetch(self) -> FetchStruct:
		"""SCPI: FETCh:WCDMa:MEASurement<instance>:MEValuation:LIST:PCDE:CURRent \n
		Snippet: value: FetchStruct = driver.multiEval.listPy.pcde.current.fetch() \n
		Return the peak code domain error (PCDE) results in list mode. The values listed below in curly brackets {} are returned
		for the segments {...}seg 1, {...}seg 2, ..., {...}seg n, with n determined by method RsCmwWcdmaMeas.Configure.MultiEval.
		ListPy.count. \n
			:return: structure: for return value, see the help for FetchStruct structure arguments."""
		return self._core.io.query_struct(f'FETCh:WCDMa:MEASurement<Instance>:MEValuation:LIST:PCDE:CURRent?', self.__class__.FetchStruct())
