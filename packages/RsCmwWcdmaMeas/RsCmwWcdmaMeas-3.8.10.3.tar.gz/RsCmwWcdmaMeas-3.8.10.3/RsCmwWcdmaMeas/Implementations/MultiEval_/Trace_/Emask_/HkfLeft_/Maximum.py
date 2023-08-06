from typing import List

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.ArgSingleSuppressed import ArgSingleSuppressed
from ......Internal.Types import DataType


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Maximum:
	"""Maximum commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("maximum", core, parent)

	def read(self) -> List[float]:
		"""SCPI: READ:WCDMa:MEASurement<instance>:MEValuation:TRACe:EMASk:HKFLeft:MAXimum \n
		Snippet: value: List[float] = driver.multiEval.trace.emask.hkfLeft.maximum.read() \n
		Returns the values of the spectrum emission 100 kHz traces. The left section and the right section of each trace are
		retrieved by separate commands (distinguished by the terms HKFLeft and HKFRight) . The results of the current, average
		and maximum traces can be retrieved. The covered frequency range depends on the limit line H mode (see method
		RsCmwWcdmaMeas.Configure.MultiEval.Limit.Emask.absolute) . See also 'Detailed Views: Spectrum Emission Mask' \n
		Use RsCmwWcdmaMeas.reliability.last_value to read the updated reliability indicator. \n
			:return: emask_100_kleft: float These values correspond to test points that are separated by 30 kHz. The covered frequency ranges are: Left section, line H mode B/C: -12450 kHz to -3570 kHz/-2670 kHz from the carrier Right section, line H mode B/C: 3570 kHz/2670 kHz to 12450 kHz from the carrier Line H mode A is not used for 100 kHz traces (NCAPs returned) Range: -100 dB to 0 dB, Unit: dB"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'READ:WCDMa:MEASurement<Instance>:MEValuation:TRACe:EMASk:HKFLeft:MAXimum?', suppressed)
		return response

	def fetch(self) -> List[float]:
		"""SCPI: FETCh:WCDMa:MEASurement<instance>:MEValuation:TRACe:EMASk:HKFLeft:MAXimum \n
		Snippet: value: List[float] = driver.multiEval.trace.emask.hkfLeft.maximum.fetch() \n
		Returns the values of the spectrum emission 100 kHz traces. The left section and the right section of each trace are
		retrieved by separate commands (distinguished by the terms HKFLeft and HKFRight) . The results of the current, average
		and maximum traces can be retrieved. The covered frequency range depends on the limit line H mode (see method
		RsCmwWcdmaMeas.Configure.MultiEval.Limit.Emask.absolute) . See also 'Detailed Views: Spectrum Emission Mask' \n
		Use RsCmwWcdmaMeas.reliability.last_value to read the updated reliability indicator. \n
			:return: emask_100_kleft: float These values correspond to test points that are separated by 30 kHz. The covered frequency ranges are: Left section, line H mode B/C: -12450 kHz to -3570 kHz/-2670 kHz from the carrier Right section, line H mode B/C: 3570 kHz/2670 kHz to 12450 kHz from the carrier Line H mode A is not used for 100 kHz traces (NCAPs returned) Range: -100 dB to 0 dB, Unit: dB"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:WCDMa:MEASurement<Instance>:MEValuation:TRACe:EMASk:HKFLeft:MAXimum?', suppressed)
		return response
