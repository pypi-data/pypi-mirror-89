from typing import List

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.ArgSingleSuppressed import ArgSingleSuppressed
from ......Internal.Types import DataType


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Average:
	"""Average commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("average", core, parent)

	def fetch(self) -> List[float]:
		"""SCPI: FETCh:WCDMa:MEASurement<instance>:MEValuation:TRACe:PERRor:CHIP:AVERage \n
		Snippet: value: List[float] = driver.multiEval.trace.perror.chip.average.fetch() \n
		Returns the values of the RMS phase error vs. chip traces, measured in the preselected slot (see method RsCmwWcdmaMeas.
		Configure.MultiEval.pslot) . One value per chip is returned. The results of the current, average and maximum traces can
		be retrieved. See also 'Detailed Views: Modulation, CDP and CDE' \n
		Use RsCmwWcdmaMeas.reliability.last_value to read the updated reliability indicator. \n
			:return: phase_error_chip: float Range: -180 deg to 180 deg, Unit: deg"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:WCDMa:MEASurement<Instance>:MEValuation:TRACe:PERRor:CHIP:AVERage?', suppressed)
		return response

	def read(self) -> List[float]:
		"""SCPI: READ:WCDMa:MEASurement<instance>:MEValuation:TRACe:PERRor:CHIP:AVERage \n
		Snippet: value: List[float] = driver.multiEval.trace.perror.chip.average.read() \n
		Returns the values of the RMS phase error vs. chip traces, measured in the preselected slot (see method RsCmwWcdmaMeas.
		Configure.MultiEval.pslot) . One value per chip is returned. The results of the current, average and maximum traces can
		be retrieved. See also 'Detailed Views: Modulation, CDP and CDE' \n
		Use RsCmwWcdmaMeas.reliability.last_value to read the updated reliability indicator. \n
			:return: phase_error_chip: float Range: -180 deg to 180 deg, Unit: deg"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'READ:WCDMa:MEASurement<Instance>:MEValuation:TRACe:PERRor:CHIP:AVERage?', suppressed)
		return response
