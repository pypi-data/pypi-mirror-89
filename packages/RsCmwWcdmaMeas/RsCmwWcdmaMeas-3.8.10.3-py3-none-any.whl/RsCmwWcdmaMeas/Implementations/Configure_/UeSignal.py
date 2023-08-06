from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class UeSignal:
	"""UeSignal commands group definition. 5 total commands, 1 Sub-groups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ueSignal", core, parent)

	@property
	def carrier(self):
		"""carrier commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_carrier'):
			from .UeSignal_.Carrier import Carrier
			self._carrier = Carrier(self._core, self._base)
		return self._carrier

	def get_dpdch(self) -> bool:
		"""SCPI: CONFigure:WCDMa:MEASurement<instance>:UESignal:DPDCh \n
		Snippet: value: bool = driver.configure.ueSignal.get_dpdch() \n
		Defines whether the UL DPCH contains a DPDCH. For the combined signal path scenario,
		use CONFigure:WCDMa:SIGN<i>:DL:LEVel:DPCH. \n
			:return: dpdch: OFF | ON OFF: DPCCH only ON: DPCCH plus DPDCH
		"""
		response = self._core.io.query_str('CONFigure:WCDMa:MEASurement<Instance>:UESignal:DPDCh?')
		return Conversions.str_to_bool(response)

	def set_dpdch(self, dpdch: bool) -> None:
		"""SCPI: CONFigure:WCDMa:MEASurement<instance>:UESignal:DPDCh \n
		Snippet: driver.configure.ueSignal.set_dpdch(dpdch = False) \n
		Defines whether the UL DPCH contains a DPDCH. For the combined signal path scenario,
		use CONFigure:WCDMa:SIGN<i>:DL:LEVel:DPCH. \n
			:param dpdch: OFF | ON OFF: DPCCH only ON: DPCCH plus DPDCH
		"""
		param = Conversions.bool_to_str(dpdch)
		self._core.io.write(f'CONFigure:WCDMa:MEASurement<Instance>:UESignal:DPDCh {param}')

	# noinspection PyTypeChecker
	def get_ul_config(self) -> enums.UlConfiguration:
		"""SCPI: CONFigure:WCDMa:MEASurement<instance>:UESignal:ULConfig \n
		Snippet: value: enums.UlConfiguration = driver.configure.ueSignal.get_ul_config() \n
		Selects the uplink signal configuration. \n
			:return: ul_configuration: QPSK | WCDMa | HSDPa | HSUPa | HSPA | HSPLus | DCHS | HDUPlus | DDUPlus | DHDU | 3CHS | 3DUPlus | 3HDU | 4CHS | 4DUPlus | 4HDU QPSK: QPSK signal WCDMa: WCDMA R99 signal HSDPa: signal with HSDPA-related channels HSUPa: signal with HSUPA channels HSPA: HSDPA related and HSUPA channels HSPLus: HSDPA+ related channels HDUPlus: HSDPA+ related and HSUPA channels DHDU: dual carrier HSDPA+ and dual carrier HSUPA active The following values cannot be set, but can be returned while the combined signal path scenario is active: DCHS: dual carrier HSDPA+ active DDUPlus: dual carrier HSDPA+ and HSUPA active 3CHS: three carrier HSDPA+ active 3DUPlus: three carrier HSDPA+ and HSUPA active 3HDU: three carrier HSDPA+ and dual carrier HSUPA active 4CHS: four carrier HSDPA+ active 4DUPlus: four carrier HSDPA+ and HSUPA active 4HDU: four carrier HSDPA+ and dual carrier HSUPA active
		"""
		response = self._core.io.query_str('CONFigure:WCDMa:MEASurement<Instance>:UESignal:ULConfig?')
		return Conversions.str_to_scalar_enum(response, enums.UlConfiguration)

	def set_ul_config(self, ul_configuration: enums.UlConfiguration) -> None:
		"""SCPI: CONFigure:WCDMa:MEASurement<instance>:UESignal:ULConfig \n
		Snippet: driver.configure.ueSignal.set_ul_config(ul_configuration = enums.UlConfiguration._3CHS) \n
		Selects the uplink signal configuration. \n
			:param ul_configuration: QPSK | WCDMa | HSDPa | HSUPa | HSPA | HSPLus | DCHS | HDUPlus | DDUPlus | DHDU | 3CHS | 3DUPlus | 3HDU | 4CHS | 4DUPlus | 4HDU QPSK: QPSK signal WCDMa: WCDMA R99 signal HSDPa: signal with HSDPA-related channels HSUPa: signal with HSUPA channels HSPA: HSDPA related and HSUPA channels HSPLus: HSDPA+ related channels HDUPlus: HSDPA+ related and HSUPA channels DHDU: dual carrier HSDPA+ and dual carrier HSUPA active The following values cannot be set, but can be returned while the combined signal path scenario is active: DCHS: dual carrier HSDPA+ active DDUPlus: dual carrier HSDPA+ and HSUPA active 3CHS: three carrier HSDPA+ active 3DUPlus: three carrier HSDPA+ and HSUPA active 3HDU: three carrier HSDPA+ and dual carrier HSUPA active 4CHS: four carrier HSDPA+ active 4DUPlus: four carrier HSDPA+ and HSUPA active 4HDU: four carrier HSDPA+ and dual carrier HSUPA active
		"""
		param = Conversions.enum_scalar_to_str(ul_configuration, enums.UlConfiguration)
		self._core.io.write(f'CONFigure:WCDMa:MEASurement<Instance>:UESignal:ULConfig {param}')

	def get_sformat(self) -> int:
		"""SCPI: CONFigure:WCDMa:MEASurement<instance>:UESignal:SFORmat \n
		Snippet: value: int = driver.configure.ueSignal.get_sformat() \n
		Selects the slot format for the UL DPCCH. \n
			:return: slot_format: decimal Range: 0 to 5
		"""
		response = self._core.io.query_str('CONFigure:WCDMa:MEASurement<Instance>:UESignal:SFORmat?')
		return Conversions.str_to_int(response)

	def set_sformat(self, slot_format: int) -> None:
		"""SCPI: CONFigure:WCDMa:MEASurement<instance>:UESignal:SFORmat \n
		Snippet: driver.configure.ueSignal.set_sformat(slot_format = 1) \n
		Selects the slot format for the UL DPCCH. \n
			:param slot_format: decimal Range: 0 to 5
		"""
		param = Conversions.decimal_value_to_str(slot_format)
		self._core.io.write(f'CONFigure:WCDMa:MEASurement<Instance>:UESignal:SFORmat {param}')

	# noinspection PyTypeChecker
	def get_cm_pattern(self) -> enums.PatternType:
		"""SCPI: CONFigure:WCDMa:MEASurement<instance>:UESignal:CMPattern \n
		Snippet: value: enums.PatternType = driver.configure.ueSignal.get_cm_pattern() \n
		Selects the expected TPC pattern for UL compressed mode.
			INTRO_CMD_HELP: For the combined signal path scenario, use: \n
			- CONFigure:WCDMa:SIGN<i>:CMODe:ULCM:TYPE
			- CONFigure:WCDMa:SIGN<i>:CMODe:ULCM:ACTivation \n
			:return: pattern_type: AR | AF | B AR: pattern A (rising TPC) defined in 3GPP TS 34.121, table 5.7.6 AF: pattern A (falling TPC) defined in 3GPP TS 34.121, table 5.7.7 B: pattern B defined in 3GPP TS 34.121, table 5.7.8
		"""
		response = self._core.io.query_str('CONFigure:WCDMa:MEASurement<Instance>:UESignal:CMPattern?')
		return Conversions.str_to_scalar_enum(response, enums.PatternType)

	def set_cm_pattern(self, pattern_type: enums.PatternType) -> None:
		"""SCPI: CONFigure:WCDMa:MEASurement<instance>:UESignal:CMPattern \n
		Snippet: driver.configure.ueSignal.set_cm_pattern(pattern_type = enums.PatternType.AF) \n
		Selects the expected TPC pattern for UL compressed mode.
			INTRO_CMD_HELP: For the combined signal path scenario, use: \n
			- CONFigure:WCDMa:SIGN<i>:CMODe:ULCM:TYPE
			- CONFigure:WCDMa:SIGN<i>:CMODe:ULCM:ACTivation \n
			:param pattern_type: AR | AF | B AR: pattern A (rising TPC) defined in 3GPP TS 34.121, table 5.7.6 AF: pattern A (falling TPC) defined in 3GPP TS 34.121, table 5.7.7 B: pattern B defined in 3GPP TS 34.121, table 5.7.8
		"""
		param = Conversions.enum_scalar_to_str(pattern_type, enums.PatternType)
		self._core.io.write(f'CONFigure:WCDMa:MEASurement<Instance>:UESignal:CMPattern {param}')

	def clone(self) -> 'UeSignal':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = UeSignal(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
