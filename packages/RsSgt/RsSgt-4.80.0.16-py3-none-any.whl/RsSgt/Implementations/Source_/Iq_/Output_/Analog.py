from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Analog:
	"""Analog commands group definition. 60 total commands, 4 Sub-groups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("analog", core, parent)

	@property
	def bias(self):
		"""bias commands group. 1 Sub-classes, 2 commands."""
		if not hasattr(self, '_bias'):
			from .Analog_.Bias import Bias
			self._bias = Bias(self._core, self._base)
		return self._bias

	@property
	def envelope(self):
		"""envelope commands group. 7 Sub-classes, 12 commands."""
		if not hasattr(self, '_envelope'):
			from .Analog_.Envelope import Envelope
			self._envelope = Envelope(self._core, self._base)
		return self._envelope

	@property
	def offset(self):
		"""offset commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_offset'):
			from .Analog_.Offset import Offset
			self._offset = Offset(self._core, self._base)
		return self._offset

	@property
	def setting(self):
		"""setting commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_setting'):
			from .Analog_.Setting import Setting
			self._setting = Setting(self._core, self._base)
		return self._setting

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:IQ:OUTPut:ANALog:STATe \n
		Snippet: value: bool = driver.source.iq.output.analog.get_state() \n
		Activates the specified analog I/Q output. \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:OUTPut:ANALog:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:IQ:OUTPut:ANALog:STATe \n
		Snippet: driver.source.iq.output.analog.set_state(state = False) \n
		Activates the specified analog I/Q output. \n
			:param state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:IQ:OUTPut:ANALog:STATe {param}')

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.IqOutMode:
		"""SCPI: [SOURce<HW>]:IQ:OUTPut:[ANALog]:MODE \n
		Snippet: value: enums.IqOutMode = driver.source.iq.output.analog.get_mode() \n
		Determines the mode for setting the output parameters. \n
			:return: mode: FIXed| VARiable FIXed Locks the I/Q output settings VARiable Unlocks the settings
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:OUTPut:ANALog:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.IqOutMode)

	def set_mode(self, mode: enums.IqOutMode) -> None:
		"""SCPI: [SOURce<HW>]:IQ:OUTPut:[ANALog]:MODE \n
		Snippet: driver.source.iq.output.analog.set_mode(mode = enums.IqOutMode.FIXed) \n
		Determines the mode for setting the output parameters. \n
			:param mode: FIXed| VARiable FIXed Locks the I/Q output settings VARiable Unlocks the settings
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.IqOutMode)
		self._core.io.write(f'SOURce<HwInstance>:IQ:OUTPut:ANALog:MODE {param}')

	def preset(self) -> None:
		"""SCPI: [SOURce<HW>]:IQ:OUTPut:[ANALog]:PRESet \n
		Snippet: driver.source.iq.output.analog.preset() \n
		Sets the default settings (*RST values specified for the commands) .
			INTRO_CMD_HELP: Not affected are: \n
			- The state set with the command method RsSgt.Source.Iq.Output.Analog.state.
			- If SCONfiguration:EXTernal:PBEHaviour 1, the I/Q ouptput type set with the command IQ:TYPE. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:IQ:OUTPut:ANALog:PRESet')

	def preset_with_opc(self) -> None:
		"""SCPI: [SOURce<HW>]:IQ:OUTPut:[ANALog]:PRESet \n
		Snippet: driver.source.iq.output.analog.preset_with_opc() \n
		Sets the default settings (*RST values specified for the commands) .
			INTRO_CMD_HELP: Not affected are: \n
			- The state set with the command method RsSgt.Source.Iq.Output.Analog.state.
			- If SCONfiguration:EXTernal:PBEHaviour 1, the I/Q ouptput type set with the command IQ:TYPE. \n
		Same as preset, but waits for the operation to complete before continuing further. Use the RsSgt.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:IQ:OUTPut:ANALog:PRESet')

	# noinspection PyTypeChecker
	def get_type_py(self) -> enums.IqOutType:
		"""SCPI: [SOURce<HW>]:IQ:OUTPut:[ANALog]:TYPE \n
		Snippet: value: enums.IqOutType = driver.source.iq.output.analog.get_type_py() \n
		Sets the type of the analog signal. \n
			:return: type_py: SINGle| DIFFerential
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:OUTPut:ANALog:TYPE?')
		return Conversions.str_to_scalar_enum(response, enums.IqOutType)

	def set_type_py(self, type_py: enums.IqOutType) -> None:
		"""SCPI: [SOURce<HW>]:IQ:OUTPut:[ANALog]:TYPE \n
		Snippet: driver.source.iq.output.analog.set_type_py(type_py = enums.IqOutType.DIFFerential) \n
		Sets the type of the analog signal. \n
			:param type_py: SINGle| DIFFerential
		"""
		param = Conversions.enum_scalar_to_str(type_py, enums.IqOutType)
		self._core.io.write(f'SOURce<HwInstance>:IQ:OUTPut:ANALog:TYPE {param}')

	def clone(self) -> 'Analog':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Analog(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
