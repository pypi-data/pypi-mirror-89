from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CdThreshold:
	"""CdThreshold commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("cdThreshold", core, parent)

	def get_modulation(self) -> float:
		"""SCPI: CONFigure:WCDMa:MEASurement<instance>:MEValuation:CDTHreshold:MODulation \n
		Snippet: value: float = driver.configure.multiEval.cdThreshold.get_modulation() \n
		Defines the minimum relative signal strength of the (E-) DPDCH in the WCDMA signal (if present) to be detected and
		evaluated. \n
			:return: threshold: numeric Range: -25 dB to 10 dB, Unit: dB
		"""
		response = self._core.io.query_str('CONFigure:WCDMa:MEASurement<Instance>:MEValuation:CDTHreshold:MODulation?')
		return Conversions.str_to_float(response)

	def set_modulation(self, threshold: float) -> None:
		"""SCPI: CONFigure:WCDMa:MEASurement<instance>:MEValuation:CDTHreshold:MODulation \n
		Snippet: driver.configure.multiEval.cdThreshold.set_modulation(threshold = 1.0) \n
		Defines the minimum relative signal strength of the (E-) DPDCH in the WCDMA signal (if present) to be detected and
		evaluated. \n
			:param threshold: numeric Range: -25 dB to 10 dB, Unit: dB
		"""
		param = Conversions.decimal_value_to_str(threshold)
		self._core.io.write(f'CONFigure:WCDMa:MEASurement<Instance>:MEValuation:CDTHreshold:MODulation {param}')
