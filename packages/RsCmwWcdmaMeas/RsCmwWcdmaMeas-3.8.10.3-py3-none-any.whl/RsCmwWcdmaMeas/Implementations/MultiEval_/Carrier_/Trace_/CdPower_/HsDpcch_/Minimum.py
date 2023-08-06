from typing import List

from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.ArgSingleSuppressed import ArgSingleSuppressed
from .......Internal.Types import DataType
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Minimum:
	"""Minimum commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("minimum", core, parent)

	def read(self, carrier=repcap.Carrier.Default) -> List[float]:
		"""SCPI: READ:WCDMa:MEASurement<instance>:MEValuation:CARRier<carrier>:TRACe:CDPower:HSDPcch:MINimum \n
		Snippet: value: List[float] = driver.multiEval.carrier.trace.cdPower.hsDpcch.minimum.read(carrier = repcap.Carrier.Default) \n
		Returns the values of the RMS CDP vs. slot traces for the HS-DPCCH and the E-DPCCH. Each current value is averaged over a
		half-slot or a full-slot, depending on the measurement period (see method RsCmwWcdmaMeas.Configure.MultiEval.Mperiod.
		modulation) . The number of results depends on the measurement length (see method RsCmwWcdmaMeas.Configure.MultiEval.
		msCount) . The results of the current, average, minimum, maximum and standard deviation traces can be retrieved.
		The standard deviation traces cannot be displayed at the GUI. See also 'Detailed Views: Modulation, CDP and CDE' \n
		Use RsCmwWcdmaMeas.reliability.last_value to read the updated reliability indicator. \n
			:param carrier: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Carrier')
			:return: hsd_pcch: No help available"""
		carrier_cmd_val = self._base.get_repcap_cmd_value(carrier, repcap.Carrier)
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'READ:WCDMa:MEASurement<Instance>:MEValuation:CARRier{carrier_cmd_val}:TRACe:CDPower:HSDPcch:MINimum?', suppressed)
		return response

	def fetch(self, carrier=repcap.Carrier.Default) -> List[float]:
		"""SCPI: FETCh:WCDMa:MEASurement<instance>:MEValuation:CARRier<carrier>:TRACe:CDPower:HSDPcch:MINimum \n
		Snippet: value: List[float] = driver.multiEval.carrier.trace.cdPower.hsDpcch.minimum.fetch(carrier = repcap.Carrier.Default) \n
		Returns the values of the RMS CDP vs. slot traces for the HS-DPCCH and the E-DPCCH. Each current value is averaged over a
		half-slot or a full-slot, depending on the measurement period (see method RsCmwWcdmaMeas.Configure.MultiEval.Mperiod.
		modulation) . The number of results depends on the measurement length (see method RsCmwWcdmaMeas.Configure.MultiEval.
		msCount) . The results of the current, average, minimum, maximum and standard deviation traces can be retrieved.
		The standard deviation traces cannot be displayed at the GUI. See also 'Detailed Views: Modulation, CDP and CDE' \n
		Use RsCmwWcdmaMeas.reliability.last_value to read the updated reliability indicator. \n
			:param carrier: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Carrier')
			:return: hsd_pcch: No help available"""
		carrier_cmd_val = self._base.get_repcap_cmd_value(carrier, repcap.Carrier)
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:WCDMa:MEASurement<Instance>:MEValuation:CARRier{carrier_cmd_val}:TRACe:CDPower:HSDPcch:MINimum?', suppressed)
		return response
