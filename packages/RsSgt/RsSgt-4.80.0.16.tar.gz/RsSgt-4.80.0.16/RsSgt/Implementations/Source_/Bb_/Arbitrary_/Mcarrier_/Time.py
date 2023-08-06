from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Time:
	"""Time commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("time", core, parent)

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.ArbMultCarrSigDurMod:
		"""SCPI: [SOURce<HW>]:BB:ARBitrary:MCARrier:TIME:MODE \n
		Snippet: value: enums.ArbMultCarrSigDurMod = driver.source.bb.arbitrary.mcarrier.time.get_mode() \n
		Selects the mode for calculating the resulting signal period of the multi carrier waveform. The resulting period is
		always calculated for all carriers in the carrier table irrespective of their state (ON/OFF) . \n
			:return: mode: LONG| SHORt| LCM | USER LONG The resulting signal period is defined by the longest I/Q file in the carrier table. Shorter I/Q files are periodically repeated. SHORt The resulting signal period is defined by the shortest I/Q file in the carrier table. Only the first part of longer I/Q files is used. USER The signal period can be set with command method RsSgt.Source.Bb.Arbitrary.Mcarrier.Time.value. Shorter I/Q files are repeated periodically, and only the first part of longer I/Q files is used. LCM The output file duration is the least common multiple of all input file durations.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ARBitrary:MCARrier:TIME:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.ArbMultCarrSigDurMod)

	def set_mode(self, mode: enums.ArbMultCarrSigDurMod) -> None:
		"""SCPI: [SOURce<HW>]:BB:ARBitrary:MCARrier:TIME:MODE \n
		Snippet: driver.source.bb.arbitrary.mcarrier.time.set_mode(mode = enums.ArbMultCarrSigDurMod.LCM) \n
		Selects the mode for calculating the resulting signal period of the multi carrier waveform. The resulting period is
		always calculated for all carriers in the carrier table irrespective of their state (ON/OFF) . \n
			:param mode: LONG| SHORt| LCM | USER LONG The resulting signal period is defined by the longest I/Q file in the carrier table. Shorter I/Q files are periodically repeated. SHORt The resulting signal period is defined by the shortest I/Q file in the carrier table. Only the first part of longer I/Q files is used. USER The signal period can be set with command method RsSgt.Source.Bb.Arbitrary.Mcarrier.Time.value. Shorter I/Q files are repeated periodically, and only the first part of longer I/Q files is used. LCM The output file duration is the least common multiple of all input file durations.
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.ArbMultCarrSigDurMod)
		self._core.io.write(f'SOURce<HwInstance>:BB:ARBitrary:MCARrier:TIME:MODE {param}')

	def get_value(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:ARBitrary:MCARrier:TIME \n
		Snippet: value: float = driver.source.bb.arbitrary.mcarrier.time.get_value() \n
		Sets the user-defined signal period. This setting is only possible for Signal Period Mode User (BB:ARB:MCAR:TIME:MODE
		USER) . \n
			:return: time: float Range: 0 to 1E9, Unit: s
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ARBitrary:MCARrier:TIME?')
		return Conversions.str_to_float(response)

	def set_value(self, time: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:ARBitrary:MCARrier:TIME \n
		Snippet: driver.source.bb.arbitrary.mcarrier.time.set_value(time = 1.0) \n
		Sets the user-defined signal period. This setting is only possible for Signal Period Mode User (BB:ARB:MCAR:TIME:MODE
		USER) . \n
			:param time: float Range: 0 to 1E9, Unit: s
		"""
		param = Conversions.decimal_value_to_str(time)
		self._core.io.write(f'SOURce<HwInstance>:BB:ARBitrary:MCARrier:TIME {param}')
