from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Types import DataType
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Arb:
	"""Arb commands group definition. 28 total commands, 6 Sub-groups, 10 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("arb", core, parent)

	@property
	def samples(self):
		"""samples commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_samples'):
			from .Arb_.Samples import Samples
			self._samples = Samples(self._core, self._base)
		return self._samples

	@property
	def udMarker(self):
		"""udMarker commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_udMarker'):
			from .Arb_.UdMarker import UdMarker
			self._udMarker = UdMarker(self._core, self._base)
		return self._udMarker

	@property
	def file(self):
		"""file commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_file'):
			from .Arb_.File import File
			self._file = File(self._core, self._base)
		return self._file

	@property
	def msegment(self):
		"""msegment commands group. 0 Sub-classes, 7 commands."""
		if not hasattr(self, '_msegment'):
			from .Arb_.Msegment import Msegment
			self._msegment = Msegment(self._core, self._base)
		return self._msegment

	@property
	def marker(self):
		"""marker commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_marker'):
			from .Arb_.Marker import Marker
			self._marker = Marker(self._core, self._base)
		return self._marker

	@property
	def segments(self):
		"""segments commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_segments'):
			from .Arb_.Segments import Segments
			self._segments = Segments(self._core, self._base)
		return self._segments

	def get_freq_offset(self) -> float:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:ARB:FOFFset \n
		Snippet: value: float = driver.source.gprf.generator.arb.get_freq_offset() \n
		No command help available \n
			:return: frequency_offset: No help available
		"""
		response = self._core.io.query_str('SOURce:GPRF:GENerator<Instance>:ARB:FOFFset?')
		return Conversions.str_to_float(response)

	def set_freq_offset(self, frequency_offset: float) -> None:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:ARB:FOFFset \n
		Snippet: driver.source.gprf.generator.arb.set_freq_offset(frequency_offset = 1.0) \n
		No command help available \n
			:param frequency_offset: No help available
		"""
		param = Conversions.decimal_value_to_str(frequency_offset)
		self._core.io.write(f'SOURce:GPRF:GENerator<Instance>:ARB:FOFFset {param}')

	# noinspection PyTypeChecker
	class ScountStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Sample_Count_Time: float: No parameter help available
			- Sample_Count: List[int]: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_float('Sample_Count_Time'),
			ArgStruct('Sample_Count', DataType.IntegerList, None, False, True, 1)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Sample_Count_Time: float = None
			self.Sample_Count: List[int] = None

	def get_scount(self) -> ScountStruct:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:ARB:SCOunt \n
		Snippet: value: ScountStruct = driver.source.gprf.generator.arb.get_scount() \n
		No command help available \n
			:return: structure: for return value, see the help for ScountStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce:GPRF:GENerator<Instance>:ARB:SCOunt?', self.__class__.ScountStruct())

	def get_asamples(self) -> int:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:ARB:ASAMples \n
		Snippet: value: int = driver.source.gprf.generator.arb.get_asamples() \n
		No command help available \n
			:return: add_samples: No help available
		"""
		response = self._core.io.query_str('SOURce:GPRF:GENerator<Instance>:ARB:ASAMples?')
		return Conversions.str_to_int(response)

	def set_asamples(self, add_samples: int) -> None:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:ARB:ASAMples \n
		Snippet: driver.source.gprf.generator.arb.set_asamples(add_samples = 1) \n
		No command help available \n
			:param add_samples: No help available
		"""
		param = Conversions.decimal_value_to_str(add_samples)
		self._core.io.write(f'SOURce:GPRF:GENerator<Instance>:ARB:ASAMples {param}')

	# noinspection PyTypeChecker
	def get_repetition(self) -> enums.RepeatMode:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:ARB:REPetition \n
		Snippet: value: enums.RepeatMode = driver.source.gprf.generator.arb.get_repetition() \n
		No command help available \n
			:return: repetition: No help available
		"""
		response = self._core.io.query_str('SOURce:GPRF:GENerator<Instance>:ARB:REPetition?')
		return Conversions.str_to_scalar_enum(response, enums.RepeatMode)

	def set_repetition(self, repetition: enums.RepeatMode) -> None:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:ARB:REPetition \n
		Snippet: driver.source.gprf.generator.arb.set_repetition(repetition = enums.RepeatMode.CONTinuous) \n
		No command help available \n
			:param repetition: No help available
		"""
		param = Conversions.enum_scalar_to_str(repetition, enums.RepeatMode)
		self._core.io.write(f'SOURce:GPRF:GENerator<Instance>:ARB:REPetition {param}')

	def get_cycles(self) -> int:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:ARB:CYCLes \n
		Snippet: value: int = driver.source.gprf.generator.arb.get_cycles() \n
		No command help available \n
			:return: cycles: No help available
		"""
		response = self._core.io.query_str('SOURce:GPRF:GENerator<Instance>:ARB:CYCLes?')
		return Conversions.str_to_int(response)

	def set_cycles(self, cycles: int) -> None:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:ARB:CYCLes \n
		Snippet: driver.source.gprf.generator.arb.set_cycles(cycles = 1) \n
		No command help available \n
			:param cycles: No help available
		"""
		param = Conversions.decimal_value_to_str(cycles)
		self._core.io.write(f'SOURce:GPRF:GENerator<Instance>:ARB:CYCLes {param}')

	def get_poffset(self) -> float:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:ARB:POFFset \n
		Snippet: value: float = driver.source.gprf.generator.arb.get_poffset() \n
		Queries the peak offset of the loaded waveform file. \n
			:return: peak_offset: Offset value as specified in WinIQSIM2
		"""
		response = self._core.io.query_str('SOURce:GPRF:GENerator<Instance>:ARB:POFFset?')
		return Conversions.str_to_float(response)

	def get_crate(self) -> float:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:ARB:CRATe \n
		Snippet: value: float = driver.source.gprf.generator.arb.get_crate() \n
		Queries the clock rate of the loaded waveform file. The clock rates of waveform files created with R&S WinIQSIM2 are
		compatible with the R&S CMX500. \n
			:return: clock_rate: No help available
		"""
		response = self._core.io.query_str('SOURce:GPRF:GENerator<Instance>:ARB:CRATe?')
		return Conversions.str_to_float(response)

	def get_loffset(self) -> float:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:ARB:LOFFset \n
		Snippet: value: float = driver.source.gprf.generator.arb.get_loffset() \n
		Queries the level offset (peak to average ratio, PAR) of the loaded waveform file. The PAR is equal to the absolute value
		of the difference between the RMS Offset and the Peak Offset defined in WinIQSIM2 (crest factor) . \n
			:return: level_offset: No help available
		"""
		response = self._core.io.query_str('SOURce:GPRF:GENerator<Instance>:ARB:LOFFset?')
		return Conversions.str_to_float(response)

	# noinspection PyTypeChecker
	def get_crc_protect(self) -> enums.YesNoStatus:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:ARB:CRCProtect \n
		Snippet: value: enums.YesNoStatus = driver.source.gprf.generator.arb.get_crc_protect() \n
		Indicates whether the loaded ARB file contains a CRC checksum. To get a valid result, the related ARB file must be loaded
		into the memory. That means, the baseband mode must be ARB and the generator state must be ON. Otherwise, NAV is returned. \n
			:return: crc_protection: No help available
		"""
		response = self._core.io.query_str('SOURce:GPRF:GENerator<Instance>:ARB:CRCProtect?')
		return Conversions.str_to_scalar_enum(response, enums.YesNoStatus)

	def get_status(self) -> int:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:ARB:STATus \n
		Snippet: value: int = driver.source.gprf.generator.arb.get_status() \n
		No command help available \n
			:return: arb_segment_no: No help available
		"""
		response = self._core.io.query_str('SOURce:GPRF:GENerator<Instance>:ARB:STATus?')
		return Conversions.str_to_int(response)

	def clone(self) -> 'Arb':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Arb(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
