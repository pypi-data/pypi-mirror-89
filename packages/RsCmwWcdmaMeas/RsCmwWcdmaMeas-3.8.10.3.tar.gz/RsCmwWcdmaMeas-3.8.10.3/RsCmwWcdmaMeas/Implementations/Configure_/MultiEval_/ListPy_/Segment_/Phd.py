from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Phd:
	"""Phd commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("phd", core, parent)

	def set(self, enable_ph_d: bool, segment=repcap.Segment.Default) -> None:
		"""SCPI: CONFigure:WCDMa:MEASurement<instance>:MEValuation:LIST:SEGMent<nr>:PHD \n
		Snippet: driver.configure.multiEval.listPy.segment.phd.set(enable_ph_d = False, segment = repcap.Segment.Default) \n
		Enables the calculation of the phase discontinuity vs. slot results in segment no. <no>; see 'Multi-Evaluation List Mode'. \n
			:param enable_ph_d: OFF | ON OFF: Disable measurement ON: Enable measurement of phase discontinuity
			:param segment: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')"""
		param = Conversions.bool_to_str(enable_ph_d)
		segment_cmd_val = self._base.get_repcap_cmd_value(segment, repcap.Segment)
		self._core.io.write(f'CONFigure:WCDMa:MEASurement<Instance>:MEValuation:LIST:SEGMent{segment_cmd_val}:PHD {param}')

	def get(self, segment=repcap.Segment.Default) -> bool:
		"""SCPI: CONFigure:WCDMa:MEASurement<instance>:MEValuation:LIST:SEGMent<nr>:PHD \n
		Snippet: value: bool = driver.configure.multiEval.listPy.segment.phd.get(segment = repcap.Segment.Default) \n
		Enables the calculation of the phase discontinuity vs. slot results in segment no. <no>; see 'Multi-Evaluation List Mode'. \n
			:param segment: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')
			:return: enable_ph_d: OFF | ON OFF: Disable measurement ON: Enable measurement of phase discontinuity"""
		segment_cmd_val = self._base.get_repcap_cmd_value(segment, repcap.Segment)
		response = self._core.io.query_str(f'CONFigure:WCDMa:MEASurement<Instance>:MEValuation:LIST:SEGMent{segment_cmd_val}:PHD?')
		return Conversions.str_to_bool(response)
