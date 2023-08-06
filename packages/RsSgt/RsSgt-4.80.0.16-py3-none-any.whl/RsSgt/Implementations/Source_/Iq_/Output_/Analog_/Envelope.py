from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Envelope:
	"""Envelope commands group definition. 47 total commands, 7 Sub-groups, 12 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("envelope", core, parent)

	@property
	def emf(self):
		"""emf commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_emf'):
			from .Envelope_.Emf import Emf
			self._emf = Emf(self._core, self._base)
		return self._emf

	@property
	def pin(self):
		"""pin commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_pin'):
			from .Envelope_.Pin import Pin
			self._pin = Pin(self._core, self._base)
		return self._pin

	@property
	def power(self):
		"""power commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_power'):
			from .Envelope_.Power import Power
			self._power = Power(self._core, self._base)
		return self._power

	@property
	def shaping(self):
		"""shaping commands group. 6 Sub-classes, 3 commands."""
		if not hasattr(self, '_shaping'):
			from .Envelope_.Shaping import Shaping
			self._shaping = Shaping(self._core, self._base)
		return self._shaping

	@property
	def vcc(self):
		"""vcc commands group. 1 Sub-classes, 3 commands."""
		if not hasattr(self, '_vcc'):
			from .Envelope_.Vcc import Vcc
			self._vcc = Vcc(self._core, self._base)
		return self._vcc

	@property
	def vout(self):
		"""vout commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_vout'):
			from .Envelope_.Vout import Vout
			self._vout = Vout(self._core, self._base)
		return self._vout

	@property
	def vpp(self):
		"""vpp commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_vpp'):
			from .Envelope_.Vpp import Vpp
			self._vpp = Vpp(self._core, self._base)
		return self._vpp

	# noinspection PyTypeChecker
	def get_adaption(self) -> enums.IqOutEnvAdaption:
		"""SCPI: [SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:ADAPtion \n
		Snippet: value: enums.IqOutEnvAdaption = driver.source.iq.output.analog.envelope.get_adaption() \n
		Defines the envelope voltage adaption mode. \n
			:return: adaption_mode: AUTO| MANual| POWer AUTO = Auto Normalized, POWer = Auto Power, MANual = Manual
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:ADAPtion?')
		return Conversions.str_to_scalar_enum(response, enums.IqOutEnvAdaption)

	def set_adaption(self, adaption_mode: enums.IqOutEnvAdaption) -> None:
		"""SCPI: [SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:ADAPtion \n
		Snippet: driver.source.iq.output.analog.envelope.set_adaption(adaption_mode = enums.IqOutEnvAdaption.AUTO) \n
		Defines the envelope voltage adaption mode. \n
			:param adaption_mode: AUTO| MANual| POWer AUTO = Auto Normalized, POWer = Auto Power, MANual = Manual
		"""
		param = Conversions.enum_scalar_to_str(adaption_mode, enums.IqOutEnvAdaption)
		self._core.io.write(f'SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:ADAPtion {param}')

	def get_bias(self) -> float:
		"""SCPI: [SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:BIAS \n
		Snippet: value: float = driver.source.iq.output.analog.envelope.get_bias() \n
		Sets a bias. \n
			:return: bias: float Range: -3.6V to 3.6V , Unit: V
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:BIAS?')
		return Conversions.str_to_float(response)

	def set_bias(self, bias: float) -> None:
		"""SCPI: [SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:BIAS \n
		Snippet: driver.source.iq.output.analog.envelope.set_bias(bias = 1.0) \n
		Sets a bias. \n
			:param bias: float Range: -3.6V to 3.6V , Unit: V
		"""
		param = Conversions.decimal_value_to_str(bias)
		self._core.io.write(f'SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:BIAS {param}')

	def get_binput(self) -> bool:
		"""SCPI: [SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:BINPut \n
		Snippet: value: bool = driver.source.iq.output.analog.envelope.get_binput() \n
		Enables the generation of a bipolar signal. \n
			:return: bipolar_input: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:BINPut?')
		return Conversions.str_to_bool(response)

	def set_binput(self, bipolar_input: bool) -> None:
		"""SCPI: [SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:BINPut \n
		Snippet: driver.source.iq.output.analog.envelope.set_binput(bipolar_input = False) \n
		Enables the generation of a bipolar signal. \n
			:param bipolar_input: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(bipolar_input)
		self._core.io.write(f'SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:BINPut {param}')

	def get_delay(self) -> float:
		"""SCPI: [SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:DELay \n
		Snippet: value: float = driver.source.iq.output.analog.envelope.get_delay() \n
		Enables a time delay of the generated envelope signal relative to the corresponding RF signal. \n
			:return: delay: float Range: -500E-9 to 500E-9
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:DELay?')
		return Conversions.str_to_float(response)

	def set_delay(self, delay: float) -> None:
		"""SCPI: [SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:DELay \n
		Snippet: driver.source.iq.output.analog.envelope.set_delay(delay = 1.0) \n
		Enables a time delay of the generated envelope signal relative to the corresponding RF signal. \n
			:param delay: float Range: -500E-9 to 500E-9
		"""
		param = Conversions.decimal_value_to_str(delay)
		self._core.io.write(f'SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:DELay {param}')

	# noinspection PyTypeChecker
	def get_etrak(self) -> enums.IqOutEnvEtRak:
		"""SCPI: [SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:ETRak \n
		Snippet: value: enums.IqOutEnvEtRak = driver.source.iq.output.analog.envelope.get_etrak() \n
		Selects one of the predefined interface types or allows user-defined settings. See Table 'Default parameters per eTrak®
		Interface Type'. \n
			:return: etrak_ifc_type: USER| ET1V2| ET1V5| ET2V0
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:ETRak?')
		return Conversions.str_to_scalar_enum(response, enums.IqOutEnvEtRak)

	def set_etrak(self, etrak_ifc_type: enums.IqOutEnvEtRak) -> None:
		"""SCPI: [SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:ETRak \n
		Snippet: driver.source.iq.output.analog.envelope.set_etrak(etrak_ifc_type = enums.IqOutEnvEtRak.ET1V2) \n
		Selects one of the predefined interface types or allows user-defined settings. See Table 'Default parameters per eTrak®
		Interface Type'. \n
			:param etrak_ifc_type: USER| ET1V2| ET1V5| ET2V0
		"""
		param = Conversions.enum_scalar_to_str(etrak_ifc_type, enums.IqOutEnvEtRak)
		self._core.io.write(f'SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:ETRak {param}')

	def get_fdpd(self) -> bool:
		"""SCPI: [SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:FDPD \n
		Snippet: value: bool = driver.source.iq.output.analog.envelope.get_fdpd() \n
		Enables calculation of the envelope from predistorted signal. \n
			:return: calc_from_dpd_stat: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:FDPD?')
		return Conversions.str_to_bool(response)

	def set_fdpd(self, calc_from_dpd_stat: bool) -> None:
		"""SCPI: [SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:FDPD \n
		Snippet: driver.source.iq.output.analog.envelope.set_fdpd(calc_from_dpd_stat = False) \n
		Enables calculation of the envelope from predistorted signal. \n
			:param calc_from_dpd_stat: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(calc_from_dpd_stat)
		self._core.io.write(f'SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:FDPD {param}')

	def get_gain(self) -> float:
		"""SCPI: [SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:GAIN \n
		Snippet: value: float = driver.source.iq.output.analog.envelope.get_gain() \n
		Sets the gain of the used external DC modulator. \n
			:return: gain: float Range: -50 to 50
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:GAIN?')
		return Conversions.str_to_float(response)

	def set_gain(self, gain: float) -> None:
		"""SCPI: [SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:GAIN \n
		Snippet: driver.source.iq.output.analog.envelope.set_gain(gain = 1.0) \n
		Sets the gain of the used external DC modulator. \n
			:param gain: float Range: -50 to 50
		"""
		param = Conversions.decimal_value_to_str(gain)
		self._core.io.write(f'SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:GAIN {param}')

	def get_offset(self) -> float:
		"""SCPI: [SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:OFFSet \n
		Snippet: value: float = driver.source.iq.output.analog.envelope.get_offset() \n
		Sets an offset between the envelope and the inverted envelope signal. \n
			:return: offset: float Range: -8V to 8V , Unit: V
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:OFFSet?')
		return Conversions.str_to_float(response)

	def set_offset(self, offset: float) -> None:
		"""SCPI: [SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:OFFSet \n
		Snippet: driver.source.iq.output.analog.envelope.set_offset(offset = 1.0) \n
		Sets an offset between the envelope and the inverted envelope signal. \n
			:param offset: float Range: -8V to 8V , Unit: V
		"""
		param = Conversions.decimal_value_to_str(offset)
		self._core.io.write(f'SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:OFFSet {param}')

	def get_rin(self) -> float:
		"""SCPI: [SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:RIN \n
		Snippet: value: float = driver.source.iq.output.analog.envelope.get_rin() \n
		Sets the input impedance Rin of the used external DC modulator. \n
			:return: ipartnput_resistance: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:RIN?')
		return Conversions.str_to_float(response)

	def set_rin(self, ipartnput_resistance: float) -> None:
		"""SCPI: [SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:RIN \n
		Snippet: driver.source.iq.output.analog.envelope.set_rin(ipartnput_resistance = 1.0) \n
		Sets the input impedance Rin of the used external DC modulator. \n
			:param ipartnput_resistance: float Range: 50|100 to 1E6
		"""
		param = Conversions.decimal_value_to_str(ipartnput_resistance)
		self._core.io.write(f'SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:RIN {param}')

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:STATe \n
		Snippet: value: bool = driver.source.iq.output.analog.envelope.get_state() \n
		Enables the output of a control signal that follows the RF envelope. \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:STATe \n
		Snippet: driver.source.iq.output.analog.envelope.set_state(state = False) \n
		Enables the output of a control signal that follows the RF envelope. \n
			:param state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:STATe {param}')

	# noinspection PyTypeChecker
	def get_termination(self) -> enums.IqOutEnvTerm:
		"""SCPI: [SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:TERMination \n
		Snippet: value: enums.IqOutEnvTerm = driver.source.iq.output.analog.envelope.get_termination() \n
		Sets how the inputs of the DC modulator are terminated. \n
			:return: termination: GROund| WIRE
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:TERMination?')
		return Conversions.str_to_scalar_enum(response, enums.IqOutEnvTerm)

	def set_termination(self, termination: enums.IqOutEnvTerm) -> None:
		"""SCPI: [SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:TERMination \n
		Snippet: driver.source.iq.output.analog.envelope.set_termination(termination = enums.IqOutEnvTerm.GROund) \n
		Sets how the inputs of the DC modulator are terminated. \n
			:param termination: GROund| WIRE
		"""
		param = Conversions.enum_scalar_to_str(termination, enums.IqOutEnvTerm)
		self._core.io.write(f'SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:TERMination {param}')

	# noinspection PyTypeChecker
	def get_vref(self) -> enums.IqOutEnvVrEf:
		"""SCPI: [SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:VREF \n
		Snippet: value: enums.IqOutEnvVrEf = driver.source.iq.output.analog.envelope.get_vref() \n
		Defines whether the envelope voltage Vout is set directly or it is estimated from the selected supply voltage Vcc. \n
			:return: voltage_referenc: VCC| VOUT
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:VREF?')
		return Conversions.str_to_scalar_enum(response, enums.IqOutEnvVrEf)

	def set_vref(self, voltage_referenc: enums.IqOutEnvVrEf) -> None:
		"""SCPI: [SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:VREF \n
		Snippet: driver.source.iq.output.analog.envelope.set_vref(voltage_referenc = enums.IqOutEnvVrEf.VCC) \n
		Defines whether the envelope voltage Vout is set directly or it is estimated from the selected supply voltage Vcc. \n
			:param voltage_referenc: VCC| VOUT
		"""
		param = Conversions.enum_scalar_to_str(voltage_referenc, enums.IqOutEnvVrEf)
		self._core.io.write(f'SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:VREF {param}')

	def clone(self) -> 'Envelope':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Envelope(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
