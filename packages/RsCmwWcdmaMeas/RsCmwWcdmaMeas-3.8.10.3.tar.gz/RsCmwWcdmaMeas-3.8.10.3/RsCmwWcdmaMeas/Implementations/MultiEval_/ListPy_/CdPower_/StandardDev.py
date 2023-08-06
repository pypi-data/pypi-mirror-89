from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.Types import DataType
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StandardDev:
	"""StandardDev commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("standardDev", core, parent)

	# noinspection PyTypeChecker
	class FetchStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: decimal 'Reliability Indicator' In list mode, a zero reliability indicator indicates that the results in all measured segments are valid. A non-zero value indicates that an error occurred in at least one of the measured segments.
			- Return_Code: List[int]: decimal Reliability indicator for the segment. The meaning of the returned values is the same as for the common reliability indicator, see previous parameter.
			- Dpcch: List[float]: float RMS CDP values for the indicated channels Range: -100 dB to 0 dB (SDEViation 0 dB to 50 dB) , Unit: dB
			- Dpdch: List[float]: float RMS CDP values for the indicated channels Range: -100 dB to 0 dB (SDEViation 0 dB to 50 dB) , Unit: dB
			- Hsd_Pcch: List[float]: float RMS CDP values for the indicated channels Range: -100 dB to 0 dB (SDEViation 0 dB to 50 dB) , Unit: dB
			- Edpcch: List[float]: float RMS CDP values for the indicated channels Range: -100 dB to 0 dB (SDEViation 0 dB to 50 dB) , Unit: dB
			- Edpd_Ch_1: List[float]: float RMS CDP values for the indicated channels Range: -100 dB to 0 dB (SDEViation 0 dB to 50 dB) , Unit: dB
			- Edpd_Ch_2: List[float]: float RMS CDP values for the indicated channels Range: -100 dB to 0 dB (SDEViation 0 dB to 50 dB) , Unit: dB
			- Edpd_Ch_3: List[float]: float RMS CDP values for the indicated channels Range: -100 dB to 0 dB (SDEViation 0 dB to 50 dB) , Unit: dB
			- Edpd_Ch_4: List[float]: float RMS CDP values for the indicated channels Range: -100 dB to 0 dB (SDEViation 0 dB to 50 dB) , Unit: dB"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct('Return_Code', DataType.IntegerList, None, False, True, 1),
			ArgStruct('Dpcch', DataType.FloatList, None, False, True, 1),
			ArgStruct('Dpdch', DataType.FloatList, None, False, True, 1),
			ArgStruct('Hsd_Pcch', DataType.FloatList, None, False, True, 1),
			ArgStruct('Edpcch', DataType.FloatList, None, False, True, 1),
			ArgStruct('Edpd_Ch_1', DataType.FloatList, None, False, True, 1),
			ArgStruct('Edpd_Ch_2', DataType.FloatList, None, False, True, 1),
			ArgStruct('Edpd_Ch_3', DataType.FloatList, None, False, True, 1),
			ArgStruct('Edpd_Ch_4', DataType.FloatList, None, False, True, 1)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Return_Code: List[int] = None
			self.Dpcch: List[float] = None
			self.Dpdch: List[float] = None
			self.Hsd_Pcch: List[float] = None
			self.Edpcch: List[float] = None
			self.Edpd_Ch_1: List[float] = None
			self.Edpd_Ch_2: List[float] = None
			self.Edpd_Ch_3: List[float] = None
			self.Edpd_Ch_4: List[float] = None

	def fetch(self) -> FetchStruct:
		"""SCPI: FETCh:WCDMa:MEASurement<instance>:MEValuation:LIST:CDPower:SDEViation \n
		Snippet: value: FetchStruct = driver.multiEval.listPy.cdPower.standardDev.fetch() \n
		Return the RMS CDP vs. slot results in list mode. The values listed below in curly brackets {} are returned for the
		segments {...}seg 1, {...}seg 2, ..., {...}seg n, with n determined by method RsCmwWcdmaMeas.Configure.MultiEval.ListPy.
		count. \n
			:return: structure: for return value, see the help for FetchStruct structure arguments."""
		return self._core.io.query_struct(f'FETCh:WCDMa:MEASurement<Instance>:MEValuation:LIST:CDPower:SDEViation?', self.__class__.FetchStruct())
