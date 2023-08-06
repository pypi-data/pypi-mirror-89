from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.Types import DataType
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct
from ......Internal.ArgSingleList import ArgSingleList
from ......Internal.ArgSingle import ArgSingle
from ...... import enums
from ...... import repcap


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
			- Return_Code: int: decimal Reliability indicator for the segment. The meaning of the returned values is the same as for the common reliability indicator, see previous parameter.
			- Carrier_Power: float: float Power at the nominal carrier UL frequency Range: -100 dBm to 55 dBm, Unit: dBm
			- Aclr_Minus_2: float: float Power of the adjacent channels (±1st adjacent channels at ±5 MHz from the UL frequency, ±2nd adjacent channels at ±10 MHz from the UL frequency) Range: -100 dBm to 55 dBm, Unit: dBm
			- Aclr_Minus_1: float: float Power of the adjacent channels (±1st adjacent channels at ±5 MHz from the UL frequency, ±2nd adjacent channels at ±10 MHz from the UL frequency) Range: -100 dBm to 55 dBm, Unit: dBm
			- Aclr_Plus_1: float: float Power of the adjacent channels (±1st adjacent channels at ±5 MHz from the UL frequency, ±2nd adjacent channels at ±10 MHz from the UL frequency) Range: -100 dBm to 55 dBm, Unit: dBm
			- Aclr_Plus_2: float: float Power of the adjacent channels (±1st adjacent channels at ±5 MHz from the UL frequency, ±2nd adjacent channels at ±10 MHz from the UL frequency) Range: -100 dBm to 55 dBm, Unit: dBm
			- Obw: float: float Occupied bandwidth Range: 0 MHz to 10 MHz, Unit: Hz
			- Emask_Margin_Ab: float: No parameter help available
			- Emask_Margin_Bc: float: No parameter help available
			- Emask_Margin_Cd: float: No parameter help available
			- Emask_Margin_Ef: float: No parameter help available
			- Emask_Margin_Fe: float: No parameter help available
			- Emask_Margin_Dc: float: No parameter help available
			- Emask_Margin_Cb: float: No parameter help available
			- Emask_Margin_Ba: float: No parameter help available
			- Ue_Power: float: float User equipment power Range: -100 dBm to 55 dBm, Unit: dBm
			- Emask_Margin_Had: float: No parameter help available
			- Emask_Margin_Hda: float: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_int('Return_Code'),
			ArgStruct.scalar_float('Carrier_Power'),
			ArgStruct.scalar_float('Aclr_Minus_2'),
			ArgStruct.scalar_float('Aclr_Minus_1'),
			ArgStruct.scalar_float('Aclr_Plus_1'),
			ArgStruct.scalar_float('Aclr_Plus_2'),
			ArgStruct.scalar_float('Obw'),
			ArgStruct.scalar_float('Emask_Margin_Ab'),
			ArgStruct.scalar_float('Emask_Margin_Bc'),
			ArgStruct.scalar_float('Emask_Margin_Cd'),
			ArgStruct.scalar_float('Emask_Margin_Ef'),
			ArgStruct.scalar_float('Emask_Margin_Fe'),
			ArgStruct.scalar_float('Emask_Margin_Dc'),
			ArgStruct.scalar_float('Emask_Margin_Cb'),
			ArgStruct.scalar_float('Emask_Margin_Ba'),
			ArgStruct.scalar_float('Ue_Power'),
			ArgStruct.scalar_float('Emask_Margin_Had'),
			ArgStruct.scalar_float('Emask_Margin_Hda')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Return_Code: int = None
			self.Carrier_Power: float = None
			self.Aclr_Minus_2: float = None
			self.Aclr_Minus_1: float = None
			self.Aclr_Plus_1: float = None
			self.Aclr_Plus_2: float = None
			self.Obw: float = None
			self.Emask_Margin_Ab: float = None
			self.Emask_Margin_Bc: float = None
			self.Emask_Margin_Cd: float = None
			self.Emask_Margin_Ef: float = None
			self.Emask_Margin_Fe: float = None
			self.Emask_Margin_Dc: float = None
			self.Emask_Margin_Cb: float = None
			self.Emask_Margin_Ba: float = None
			self.Ue_Power: float = None
			self.Emask_Margin_Had: float = None
			self.Emask_Margin_Hda: float = None

	def fetch(self, aclr_mode: enums.AclrMode = None, segment=repcap.Segment.Default) -> FetchStruct:
		"""SCPI: FETCh:WCDMa:MEASurement<instance>:MEValuation:LIST:SEGMent<nr>:SPECtrum:CURRent \n
		Snippet: value: FetchStruct = driver.multiEval.listPy.segment.spectrum.current.fetch(aclr_mode = enums.AclrMode.ABSolute, segment = repcap.Segment.Default) \n
		Returns the ACLR power and spectrum emission single value results for segment <no> in list mode. \n
			:param aclr_mode: ABSolute | RELative ABSolute: ACLR power displayed in dBm as absolute value RELative: ACLR power displayed in dB relative to carrier power
			:param segment: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')
			:return: structure: for return value, see the help for FetchStruct structure arguments."""
		param = ArgSingleList().compose_cmd_string(ArgSingle('aclr_mode', aclr_mode, DataType.Enum, True))
		segment_cmd_val = self._base.get_repcap_cmd_value(segment, repcap.Segment)
		return self._core.io.query_struct(f'FETCh:WCDMa:MEASurement<Instance>:MEValuation:LIST:SEGMent{segment_cmd_val}:SPECtrum:CURRent? {param}'.rstrip(), self.__class__.FetchStruct())
