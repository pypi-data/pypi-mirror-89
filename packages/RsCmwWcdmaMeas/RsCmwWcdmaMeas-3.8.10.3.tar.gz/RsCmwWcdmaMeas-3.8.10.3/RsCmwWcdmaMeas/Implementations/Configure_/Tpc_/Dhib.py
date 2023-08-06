from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dhib:
	"""Dhib commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dhib", core, parent)

	def get_mlength(self) -> int:
		"""SCPI: CONFigure:WCDMa:MEASurement<instance>:TPC:DHIB:MLENgth \n
		Snippet: value: int = driver.configure.tpc.dhib.get_mlength() \n
		Defines the number of slots to be measured in 'DC HSDPA In-Band Emission' mode. \n
			:return: meas_length: numeric Range: 1 to 20, Unit: slots
		"""
		response = self._core.io.query_str('CONFigure:WCDMa:MEASurement<Instance>:TPC:DHIB:MLENgth?')
		return Conversions.str_to_int(response)

	def set_mlength(self, meas_length: int) -> None:
		"""SCPI: CONFigure:WCDMa:MEASurement<instance>:TPC:DHIB:MLENgth \n
		Snippet: driver.configure.tpc.dhib.set_mlength(meas_length = 1) \n
		Defines the number of slots to be measured in 'DC HSDPA In-Band Emission' mode. \n
			:param meas_length: numeric Range: 1 to 20, Unit: slots
		"""
		param = Conversions.decimal_value_to_str(meas_length)
		self._core.io.write(f'CONFigure:WCDMa:MEASurement<Instance>:TPC:DHIB:MLENgth {param}')

	def get_pattern(self) -> float:
		"""SCPI: CONFigure:WCDMa:MEASurement<instance>:TPC:DHIB:PATTern \n
		Snippet: value: float = driver.configure.tpc.dhib.get_pattern() \n
		Specifies the pattern and in the same time also the carrier to be tested. Select the pattern 00... for the tested carrier
		and 11... for the other carrier. \n
			:return: pattern: numeric | UD | DU UD: C1: 11... C2: 00... DU: C1: 00... C2: 11...
		"""
		response = self._core.io.query_str('CONFigure:WCDMa:MEASurement<Instance>:TPC:DHIB:PATTern?')
		return Conversions.str_to_float(response)

	def set_pattern(self, pattern: float) -> None:
		"""SCPI: CONFigure:WCDMa:MEASurement<instance>:TPC:DHIB:PATTern \n
		Snippet: driver.configure.tpc.dhib.set_pattern(pattern = 1.0) \n
		Specifies the pattern and in the same time also the carrier to be tested. Select the pattern 00... for the tested carrier
		and 11... for the other carrier. \n
			:param pattern: numeric | UD | DU UD: C1: 11... C2: 00... DU: C1: 00... C2: 11...
		"""
		param = Conversions.decimal_value_to_str(pattern)
		self._core.io.write(f'CONFigure:WCDMa:MEASurement<Instance>:TPC:DHIB:PATTern {param}')

	def get_aexecution(self) -> bool:
		"""SCPI: CONFigure:WCDMa:MEASurement<instance>:TPC:DHIB:AEXecution \n
		Snippet: value: bool = driver.configure.tpc.dhib.get_aexecution() \n
		Enables or disables automatic execution of the TPC setup for combined signal path measurements in 'In-band Emission' mode. \n
			:return: enable: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:WCDMa:MEASurement<Instance>:TPC:DHIB:AEXecution?')
		return Conversions.str_to_bool(response)

	def set_aexecution(self, enable: bool) -> None:
		"""SCPI: CONFigure:WCDMa:MEASurement<instance>:TPC:DHIB:AEXecution \n
		Snippet: driver.configure.tpc.dhib.set_aexecution(enable = False) \n
		Enables or disables automatic execution of the TPC setup for combined signal path measurements in 'In-band Emission' mode. \n
			:param enable: OFF | ON
		"""
		param = Conversions.bool_to_str(enable)
		self._core.io.write(f'CONFigure:WCDMa:MEASurement<Instance>:TPC:DHIB:AEXecution {param}')
