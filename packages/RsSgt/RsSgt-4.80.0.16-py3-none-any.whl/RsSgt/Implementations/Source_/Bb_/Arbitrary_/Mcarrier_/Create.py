from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Create:
	"""Create commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("create", core, parent)

	def set(self) -> None:
		"""SCPI: [SOURce<HW>]:BB:ARBitrary:MCARrier:CREate \n
		Snippet: driver.source.bb.arbitrary.mcarrier.create.set() \n
		Creates a multi carrier waveform using the current settings of the carrier table. The multi carrier waveform is saved
		into the file defined with command method RsSgt.Source.Bb.Arbitrary.Mcarrier.ofile. The file extension is *.wv. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:BB:ARBitrary:MCARrier:CREate')

	def set_with_opc(self) -> None:
		"""SCPI: [SOURce<HW>]:BB:ARBitrary:MCARrier:CREate \n
		Snippet: driver.source.bb.arbitrary.mcarrier.create.set_with_opc() \n
		Creates a multi carrier waveform using the current settings of the carrier table. The multi carrier waveform is saved
		into the file defined with command method RsSgt.Source.Bb.Arbitrary.Mcarrier.ofile. The file extension is *.wv. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsSgt.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:ARBitrary:MCARrier:CREate')
