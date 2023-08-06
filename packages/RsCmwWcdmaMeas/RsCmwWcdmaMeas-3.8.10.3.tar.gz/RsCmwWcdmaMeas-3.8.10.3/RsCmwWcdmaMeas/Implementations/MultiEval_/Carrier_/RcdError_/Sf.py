from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sf:
	"""Sf commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sf", core, parent)

	# noinspection PyTypeChecker
	class ResultData(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: decimal 'Reliability Indicator'
			- Dpcch: int: 2 | 4 | 8 | 16 | 32 | 64 | 128 | 256 Spreading factors for the indicated channels
			- Dpdch: int: 2 | 4 | 8 | 16 | 32 | 64 | 128 | 256 Spreading factors for the indicated channels
			- Hsd_Pcch: int: 2 | 4 | 8 | 16 | 32 | 64 | 128 | 256 Spreading factors for the indicated channels
			- Edpcch: int: 2 | 4 | 8 | 16 | 32 | 64 | 128 | 256 Spreading factors for the indicated channels
			- Edpd_Ch_1: int: 2 | 4 | 8 | 16 | 32 | 64 | 128 | 256 Spreading factors for the indicated channels
			- Edpd_Ch_2: int: 2 | 4 | 8 | 16 | 32 | 64 | 128 | 256 Spreading factors for the indicated channels
			- Edpd_Ch_3: int: 2 | 4 | 8 | 16 | 32 | 64 | 128 | 256 Spreading factors for the indicated channels
			- Edpd_Ch_4: int: 2 | 4 | 8 | 16 | 32 | 64 | 128 | 256 Spreading factors for the indicated channels"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_int('Dpcch'),
			ArgStruct.scalar_int('Dpdch'),
			ArgStruct.scalar_int('Hsd_Pcch'),
			ArgStruct.scalar_int('Edpcch'),
			ArgStruct.scalar_int('Edpd_Ch_1'),
			ArgStruct.scalar_int('Edpd_Ch_2'),
			ArgStruct.scalar_int('Edpd_Ch_3'),
			ArgStruct.scalar_int('Edpd_Ch_4')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Dpcch: int = None
			self.Dpdch: int = None
			self.Hsd_Pcch: int = None
			self.Edpcch: int = None
			self.Edpd_Ch_1: int = None
			self.Edpd_Ch_2: int = None
			self.Edpd_Ch_3: int = None
			self.Edpd_Ch_4: int = None

	def fetch(self, carrier=repcap.Carrier.Default) -> ResultData:
		"""SCPI: FETCh:WCDMa:MEASurement<instance>:MEValuation:CARRier<carrier>:RCDerror:SF \n
		Snippet: value: ResultData = driver.multiEval.carrier.rcdError.sf.fetch(carrier = repcap.Carrier.Default) \n
		Returns the spreading factors of the dedicated physical channels determined from a selected slot. The number to the left
		of each result parameter is provided for easy identification of the parameter position within the result array. \n
			:param carrier: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Carrier')
			:return: structure: for return value, see the help for ResultData structure arguments."""
		carrier_cmd_val = self._base.get_repcap_cmd_value(carrier, repcap.Carrier)
		return self._core.io.query_struct(f'FETCh:WCDMa:MEASurement<Instance>:MEValuation:CARRier{carrier_cmd_val}:RCDerror:SF?', self.__class__.ResultData())

	def read(self, carrier=repcap.Carrier.Default) -> ResultData:
		"""SCPI: READ:WCDMa:MEASurement<instance>:MEValuation:CARRier<carrier>:RCDerror:SF \n
		Snippet: value: ResultData = driver.multiEval.carrier.rcdError.sf.read(carrier = repcap.Carrier.Default) \n
		Returns the spreading factors of the dedicated physical channels determined from a selected slot. The number to the left
		of each result parameter is provided for easy identification of the parameter position within the result array. \n
			:param carrier: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Carrier')
			:return: structure: for return value, see the help for ResultData structure arguments."""
		carrier_cmd_val = self._base.get_repcap_cmd_value(carrier, repcap.Carrier)
		return self._core.io.query_struct(f'READ:WCDMa:MEASurement<Instance>:MEValuation:CARRier{carrier_cmd_val}:RCDerror:SF?', self.__class__.ResultData())
