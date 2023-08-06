from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Power:
	"""Power commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("power", core, parent)

	def get_step(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:ARBitrary:MCARrier:EDIT:CARRier:POWer:STEP \n
		Snippet: value: float = driver.source.bb.arbitrary.mcarrier.edit.carrier.power.get_step() \n
		The command sets the step width by which the starting power of the carriers in the defined carrier range will be
		incremented. \n
			:return: step: float Range: -80 to 80, Unit: dB
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ARBitrary:MCARrier:EDIT:CARRier:POWer:STEP?')
		return Conversions.str_to_float(response)

	def set_step(self, step: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:ARBitrary:MCARrier:EDIT:CARRier:POWer:STEP \n
		Snippet: driver.source.bb.arbitrary.mcarrier.edit.carrier.power.set_step(step = 1.0) \n
		The command sets the step width by which the starting power of the carriers in the defined carrier range will be
		incremented. \n
			:param step: float Range: -80 to 80, Unit: dB
		"""
		param = Conversions.decimal_value_to_str(step)
		self._core.io.write(f'SOURce<HwInstance>:BB:ARBitrary:MCARrier:EDIT:CARRier:POWer:STEP {param}')

	def get_start(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:ARBitrary:MCARrier:EDIT:CARRier:POWer:[STARt] \n
		Snippet: value: float = driver.source.bb.arbitrary.mcarrier.edit.carrier.power.get_start() \n
		The command sets the power for the individual carriers in the defined carrier range. If the command method RsSgt.Source.
		Bb.Arbitrary.Mcarrier.Edit.Carrier.Power.step is used to define a step width, the power entered here applies only to the
		starting carrier. The power of the remaining carriers is stepped up or down by the power specified in the method RsSgt.
		Source.Bb.Arbitrary.Mcarrier.Edit.Carrier.Power.step command. \n
			:return: start: float Range: -80 to 0, Unit: dB
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ARBitrary:MCARrier:EDIT:CARRier:POWer:STARt?')
		return Conversions.str_to_float(response)

	def set_start(self, start: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:ARBitrary:MCARrier:EDIT:CARRier:POWer:[STARt] \n
		Snippet: driver.source.bb.arbitrary.mcarrier.edit.carrier.power.set_start(start = 1.0) \n
		The command sets the power for the individual carriers in the defined carrier range. If the command method RsSgt.Source.
		Bb.Arbitrary.Mcarrier.Edit.Carrier.Power.step is used to define a step width, the power entered here applies only to the
		starting carrier. The power of the remaining carriers is stepped up or down by the power specified in the method RsSgt.
		Source.Bb.Arbitrary.Mcarrier.Edit.Carrier.Power.step command. \n
			:param start: float Range: -80 to 0, Unit: dB
		"""
		param = Conversions.decimal_value_to_str(start)
		self._core.io.write(f'SOURce<HwInstance>:BB:ARBitrary:MCARrier:EDIT:CARRier:POWer:STARt {param}')
