from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Utilities import trim_str_response
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class IqRecorder:
	"""IqRecorder commands group definition. 26 total commands, 4 Sub-groups, 11 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("iqRecorder", core, parent)

	@property
	def iqSettings(self):
		"""iqSettings commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_iqSettings'):
			from .IqRecorder_.IqSettings import IqSettings
			self._iqSettings = IqSettings(self._core, self._base)
		return self._iqSettings

	@property
	def filterPy(self):
		"""filterPy commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_filterPy'):
			from .IqRecorder_.FilterPy import FilterPy
			self._filterPy = FilterPy(self._core, self._base)
		return self._filterPy

	@property
	def trigger(self):
		"""trigger commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_trigger'):
			from .IqRecorder_.Trigger import Trigger
			self._trigger = Trigger(self._core, self._base)
		return self._trigger

	@property
	def listPy(self):
		"""listPy commands group. 2 Sub-classes, 6 commands."""
		if not hasattr(self, '_listPy'):
			from .IqRecorder_.ListPy import ListPy
			self._listPy = ListPy(self._core, self._base)
		return self._listPy

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.MeasurementMode:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:IQRecorder:MODE \n
		Snippet: value: enums.MeasurementMode = driver.configure.gprf.measurement.iqRecorder.get_mode() \n
		No command help available \n
			:return: measurement_mode: No help available
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:IQRecorder:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.MeasurementMode)

	def set_mode(self, measurement_mode: enums.MeasurementMode) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:IQRecorder:MODE \n
		Snippet: driver.configure.gprf.measurement.iqRecorder.set_mode(measurement_mode = enums.MeasurementMode.NORMal) \n
		No command help available \n
			:param measurement_mode: No help available
		"""
		param = Conversions.enum_scalar_to_str(measurement_mode, enums.MeasurementMode)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:IQRecorder:MODE {param}')

	def get_timeout(self) -> float:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:IQRecorder:TOUT \n
		Snippet: value: float = driver.configure.gprf.measurement.iqRecorder.get_timeout() \n
		Defines a timeout for the measurement. The timer is started when the measurement is initiated via a READ or INIT command.
		It is not started if the measurement is initiated manually (ON | OFF key or RESTART | STOP key) . When the measurement
		has completed the first measurement cycle (first single shot) , the statistical depth is reached and the timer is reset.
		If the first measurement cycle has not been completed when the timer expires, the measurement is stopped. The measurement
		state changes to RDY. The reliability indicator is set to 1, indicating that a measurement timeout occurred.
		Still running READ, FETCh or CALCulate commands are completed, returning the available results. At least for some results,
		there are no values at all or the statistical depth has not been reached. A timeout of 0 s corresponds to an infinite
		measurement timeout. \n
			:return: tcd_time_out: No help available
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:IQRecorder:TOUT?')
		return Conversions.str_to_float(response)

	def set_timeout(self, tcd_time_out: float) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:IQRecorder:TOUT \n
		Snippet: driver.configure.gprf.measurement.iqRecorder.set_timeout(tcd_time_out = 1.0) \n
		Defines a timeout for the measurement. The timer is started when the measurement is initiated via a READ or INIT command.
		It is not started if the measurement is initiated manually (ON | OFF key or RESTART | STOP key) . When the measurement
		has completed the first measurement cycle (first single shot) , the statistical depth is reached and the timer is reset.
		If the first measurement cycle has not been completed when the timer expires, the measurement is stopped. The measurement
		state changes to RDY. The reliability indicator is set to 1, indicating that a measurement timeout occurred.
		Still running READ, FETCh or CALCulate commands are completed, returning the available results. At least for some results,
		there are no values at all or the statistical depth has not been reached. A timeout of 0 s corresponds to an infinite
		measurement timeout. \n
			:param tcd_time_out: No help available
		"""
		param = Conversions.decimal_value_to_str(tcd_time_out)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:IQRecorder:TOUT {param}')

	def get_ratio(self) -> float:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:IQRecorder:RATio \n
		Snippet: value: float = driver.configure.gprf.measurement.iqRecorder.get_ratio() \n
		Specifies a factor to reduce the sampling rate and to increase the measurement duration. The sampling rate resulting from
		the filter settings is multiplied with the specified ratio. \n
			:return: ratio: No help available
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:IQRecorder:RATio?')
		return Conversions.str_to_float(response)

	def set_ratio(self, ratio: float) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:IQRecorder:RATio \n
		Snippet: driver.configure.gprf.measurement.iqRecorder.set_ratio(ratio = 1.0) \n
		Specifies a factor to reduce the sampling rate and to increase the measurement duration. The sampling rate resulting from
		the filter settings is multiplied with the specified ratio. \n
			:param ratio: No help available
		"""
		param = Conversions.decimal_value_to_str(ratio)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:IQRecorder:RATio {param}')

	# noinspection PyTypeChecker
	def get_bypass(self) -> enums.IqRecBypass:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:IQRecorder:BYPass \n
		Snippet: value: enums.IqRecBypass = driver.configure.gprf.measurement.iqRecorder.get_bypass() \n
		No command help available \n
			:return: bypass: No help available
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:IQRecorder:BYPass?')
		return Conversions.str_to_scalar_enum(response, enums.IqRecBypass)

	def set_bypass(self, bypass: enums.IqRecBypass) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:IQRecorder:BYPass \n
		Snippet: driver.configure.gprf.measurement.iqRecorder.set_bypass(bypass = enums.IqRecBypass.BIT) \n
		No command help available \n
			:param bypass: No help available
		"""
		param = Conversions.enum_scalar_to_str(bypass, enums.IqRecBypass)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:IQRecorder:BYPass {param}')

	# noinspection PyTypeChecker
	def get_format_py(self) -> enums.IqFormat:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:IQRecorder:FORMat \n
		Snippet: value: enums.IqFormat = driver.configure.gprf.measurement.iqRecorder.get_format_py() \n
		Selects the coordinate system for the I/Q recorder results. \n
			:return: format_py: IQ: cartesian coordinates (I and Q axis) RPHI: polar coordinates (radius R and angle PHI)
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:IQRecorder:FORMat?')
		return Conversions.str_to_scalar_enum(response, enums.IqFormat)

	def set_format_py(self, format_py: enums.IqFormat) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:IQRecorder:FORMat \n
		Snippet: driver.configure.gprf.measurement.iqRecorder.set_format_py(format_py = enums.IqFormat.IQ) \n
		Selects the coordinate system for the I/Q recorder results. \n
			:param format_py: IQ: cartesian coordinates (I and Q axis) RPHI: polar coordinates (radius R and angle PHI)
		"""
		param = Conversions.enum_scalar_to_str(format_py, enums.IqFormat)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:IQRecorder:FORMat {param}')

	# noinspection PyTypeChecker
	def get_munit(self) -> enums.MagnitudeUnit:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:IQRecorder:MUNit \n
		Snippet: value: enums.MagnitudeUnit = driver.configure.gprf.measurement.iqRecorder.get_munit() \n
		Selects the magnitude unit for the measurement results. \n
			:return: magnitude_unit: Voltage units or raw I/Q data relative to full scale
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:IQRecorder:MUNit?')
		return Conversions.str_to_scalar_enum(response, enums.MagnitudeUnit)

	def set_munit(self, magnitude_unit: enums.MagnitudeUnit) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:IQRecorder:MUNit \n
		Snippet: driver.configure.gprf.measurement.iqRecorder.set_munit(magnitude_unit = enums.MagnitudeUnit.RAW) \n
		Selects the magnitude unit for the measurement results. \n
			:param magnitude_unit: Voltage units or raw I/Q data relative to full scale
		"""
		param = Conversions.enum_scalar_to_str(magnitude_unit, enums.MagnitudeUnit)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:IQRecorder:MUNit {param}')

	# noinspection PyTypeChecker
	def get_user(self) -> enums.UserDebugMode:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:IQRecorder:USER \n
		Snippet: value: enums.UserDebugMode = driver.configure.gprf.measurement.iqRecorder.get_user() \n
		No command help available \n
			:return: user_mode: No help available
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:IQRecorder:USER?')
		return Conversions.str_to_scalar_enum(response, enums.UserDebugMode)

	def set_user(self, user_mode: enums.UserDebugMode) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:IQRecorder:USER \n
		Snippet: driver.configure.gprf.measurement.iqRecorder.set_user(user_mode = enums.UserDebugMode.DEBug) \n
		No command help available \n
			:param user_mode: No help available
		"""
		param = Conversions.enum_scalar_to_str(user_mode, enums.UserDebugMode)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:IQRecorder:USER {param}')

	def get_iq_file(self) -> str:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:IQRecorder:IQFile \n
		Snippet: value: str = driver.configure.gprf.measurement.iqRecorder.get_iq_file() \n
		Selects a file for storage of the I/Q recorder results in binary format. \n
			:return: iq_save_file: Name and path of the file. The extension *.iqw is appended automatically.
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:IQRecorder:IQFile?')
		return trim_str_response(response)

	def set_iq_file(self, iq_save_file: str) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:IQRecorder:IQFile \n
		Snippet: driver.configure.gprf.measurement.iqRecorder.set_iq_file(iq_save_file = '1') \n
		Selects a file for storage of the I/Q recorder results in binary format. \n
			:param iq_save_file: Name and path of the file. The extension *.iqw is appended automatically.
		"""
		param = Conversions.value_to_quoted_str(iq_save_file)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:IQRecorder:IQFile {param}')

	# noinspection PyTypeChecker
	def get_wt_file(self) -> enums.FileSave:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:IQRecorder:WTFile \n
		Snippet: value: enums.FileSave = driver.configure.gprf.measurement.iqRecorder.get_wt_file() \n
		Selects whether the results are written to a file, to the memory or both. For file selection, see method RsCMPX_Gprf.
		Configure.Gprf.Measurement.IqRecorder.iqFile. \n
			:return: write_to_iq_file: OFF: The results are only stored in the memory. ON: The results are stored in the memory and in a file. ONLY: The results are only stored in a file.
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:IQRecorder:WTFile?')
		return Conversions.str_to_scalar_enum(response, enums.FileSave)

	def set_wt_file(self, write_to_iq_file: enums.FileSave) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:IQRecorder:WTFile \n
		Snippet: driver.configure.gprf.measurement.iqRecorder.set_wt_file(write_to_iq_file = enums.FileSave.OFF) \n
		Selects whether the results are written to a file, to the memory or both. For file selection, see method RsCMPX_Gprf.
		Configure.Gprf.Measurement.IqRecorder.iqFile. \n
			:param write_to_iq_file: OFF: The results are only stored in the memory. ON: The results are stored in the memory and in a file. ONLY: The results are only stored in a file.
		"""
		param = Conversions.enum_scalar_to_str(write_to_iq_file, enums.FileSave)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:IQRecorder:WTFile {param}')

	def get_ini_file(self) -> str:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:IQRecorder:INIFile \n
		Snippet: value: str = driver.configure.gprf.measurement.iqRecorder.get_ini_file() \n
		No command help available \n
			:return: ini_file: No help available
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:IQRecorder:INIFile?')
		return trim_str_response(response)

	def set_ini_file(self, ini_file: str) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:IQRecorder:INIFile \n
		Snippet: driver.configure.gprf.measurement.iqRecorder.set_ini_file(ini_file = '1') \n
		No command help available \n
			:param ini_file: No help available
		"""
		param = Conversions.value_to_quoted_str(ini_file)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:IQRecorder:INIFile {param}')

	# noinspection PyTypeChecker
	class CaptureStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Capt_Samp_Bef_Trig: int: Samples before trigger event
			- Capt_Samp_Aft_Trig: int: Samples after trigger event"""
		__meta_args_list = [
			ArgStruct.scalar_int('Capt_Samp_Bef_Trig'),
			ArgStruct.scalar_int('Capt_Samp_Aft_Trig')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Capt_Samp_Bef_Trig: int = None
			self.Capt_Samp_Aft_Trig: int = None

	def get_capture(self) -> CaptureStruct:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:IQRecorder:CAPTure \n
		Snippet: value: CaptureStruct = driver.configure.gprf.measurement.iqRecorder.get_capture() \n
		Selects the number of samples to be recorded before and after the trigger event. Configure the two settings so that their
		sum does not exceed the maximum number of samples. \n
			:return: structure: for return value, see the help for CaptureStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:GPRF:MEASurement<Instance>:IQRecorder:CAPTure?', self.__class__.CaptureStruct())

	def set_capture(self, value: CaptureStruct) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:IQRecorder:CAPTure \n
		Snippet: driver.configure.gprf.measurement.iqRecorder.set_capture(value = CaptureStruct()) \n
		Selects the number of samples to be recorded before and after the trigger event. Configure the two settings so that their
		sum does not exceed the maximum number of samples. \n
			:param value: see the help for CaptureStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:GPRF:MEASurement<Instance>:IQRecorder:CAPTure', value)

	def clone(self) -> 'IqRecorder':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = IqRecorder(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
