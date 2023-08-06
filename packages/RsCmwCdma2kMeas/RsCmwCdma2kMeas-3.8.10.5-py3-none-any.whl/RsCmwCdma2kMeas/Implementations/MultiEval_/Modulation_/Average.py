from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.StructBase import StructBase
from ....Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Average:
	"""Average commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("average", core, parent)

	# noinspection PyTypeChecker
	class ReadStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: decimal 'Reliability Indicator'
			- Evm_Rms: float: float Error vector magnitude RMS value Range: 0 % to 100 %, Unit: %
			- Evm_Peak: float: float Error vector magnitude peak value Range: 0 % to 100 %, Unit: %
			- Merr_Rms: float: float Magnitude error RMS value Range: 0 % to 100 %, Unit: %
			- Merr_Peak: float: float Magnitude error peak value Range: -100 % to 100 % (AVERage: 0% to 100 %, SDEViation: 0 % to 50 %) , Unit: %
			- Perr_Rms: float: float Phase error RMS value Range: 0 deg to 180 deg, Unit: deg
			- Perr_Peak: float: float Phase error peak value Range: -180 deg to 180 deg (AVERage: 0 deg to 180 deg, SDEViation: 0 deg to 90 deg) , Unit: deg
			- Iq_Offset: float: float I/Q origin offset Range: -100 dB to 0 dB, Unit: dB
			- Iq_Imbalance: float: float I/Q imbalance Range: -100 dB to 0 dB, Unit: dB
			- Cfreq_Error: float: float Carrier frequency error Range: -5000 Hz to 5000 Hz, Unit: Hz
			- Trans_Time_Err: float: float Transmit time error Range: -100 µs to 100 µs, Unit: µs
			- Msp_Ower_1_M_23: float: No parameter help available
			- Ms_Power_Wideband: float: No parameter help available
			- Wav_Quality: float: float Waveform quality Range: 0 to 1
			- Wav_Qual_Max_Pow: float: No parameter help available
			- Wav_Qual_Min_Pow: float: No parameter help available
			- Out_Of_Tol_Count: float: float Out of tolerance result, i.e. percentage of measurement intervals of the statistic count ([CMDLINK: CONFigure:CDMA:MEASi:MEValuation:SCOunt:MODulation CMDLINK]) exceeding the specified limits, see 'Limits (Power and Modulation) '. Range: 0 % to 100 %, Unit: %"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float('Evm_Rms'),
			ArgStruct.scalar_float('Evm_Peak'),
			ArgStruct.scalar_float('Merr_Rms'),
			ArgStruct.scalar_float('Merr_Peak'),
			ArgStruct.scalar_float('Perr_Rms'),
			ArgStruct.scalar_float('Perr_Peak'),
			ArgStruct.scalar_float('Iq_Offset'),
			ArgStruct.scalar_float('Iq_Imbalance'),
			ArgStruct.scalar_float('Cfreq_Error'),
			ArgStruct.scalar_float('Trans_Time_Err'),
			ArgStruct.scalar_float('Msp_Ower_1_M_23'),
			ArgStruct.scalar_float('Ms_Power_Wideband'),
			ArgStruct.scalar_float('Wav_Quality'),
			ArgStruct.scalar_float('Wav_Qual_Max_Pow'),
			ArgStruct.scalar_float('Wav_Qual_Min_Pow'),
			ArgStruct.scalar_float('Out_Of_Tol_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Evm_Rms: float = None
			self.Evm_Peak: float = None
			self.Merr_Rms: float = None
			self.Merr_Peak: float = None
			self.Perr_Rms: float = None
			self.Perr_Peak: float = None
			self.Iq_Offset: float = None
			self.Iq_Imbalance: float = None
			self.Cfreq_Error: float = None
			self.Trans_Time_Err: float = None
			self.Msp_Ower_1_M_23: float = None
			self.Ms_Power_Wideband: float = None
			self.Wav_Quality: float = None
			self.Wav_Qual_Max_Pow: float = None
			self.Wav_Qual_Min_Pow: float = None
			self.Out_Of_Tol_Count: float = None

	def read(self) -> ReadStruct:
		"""SCPI: READ:CDMA:MEASurement<Instance>:MEValuation:MODulation:AVERage \n
		Snippet: value: ReadStruct = driver.multiEval.modulation.average.read() \n
		Return the current, average, minimum, maximum and standard deviation modulation single value results.
		The values described below are returned by FETCh and READ commands. CALCulate commands return limit check results instead,
		one value for each result listed below. The ranges indicated below apply to all results except standard deviation results.
		The minimum for standard deviation results equals 0. The maximum equals the width of the indicated range divided by two.
		Exceptions are explicitly stated. The number to the left of each result parameter is provided for easy identification of
		the parameter position within the result array. \n
			:return: structure: for return value, see the help for ReadStruct structure arguments."""
		return self._core.io.query_struct(f'READ:CDMA:MEASurement<Instance>:MEValuation:MODulation:AVERage?', self.__class__.ReadStruct())

	# noinspection PyTypeChecker
	class FetchStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: decimal 'Reliability Indicator'
			- Evm_Rms: float: float Error vector magnitude RMS value Range: 0 % to 100 %, Unit: %
			- Evm_Peak: float: float Error vector magnitude peak value Range: 0 % to 100 %, Unit: %
			- Merr_Rms: float: float Magnitude error RMS value Range: 0 % to 100 %, Unit: %
			- Merr_Peak: float: float Magnitude error peak value Range: -100 % to 100 % (AVERage: 0% to 100 %, SDEViation: 0 % to 50 %) , Unit: %
			- Perr_Rms: float: float Phase error RMS value Range: 0 deg to 180 deg, Unit: deg
			- Perr_Peak: float: float Phase error peak value Range: -180 deg to 180 deg (AVERage: 0 deg to 180 deg, SDEViation: 0 deg to 90 deg) , Unit: deg
			- Iq_Offset: float: float I/Q origin offset Range: -100 dB to 0 dB, Unit: dB
			- Iq_Imbalance: int: float I/Q imbalance Range: -100 dB to 0 dB, Unit: dB
			- Cfreq_Error: float: float Carrier frequency error Range: -5000 Hz to 5000 Hz, Unit: Hz
			- Trans_Time_Err: float: float Transmit time error Range: -100 µs to 100 µs, Unit: µs
			- Msp_Ower_1_M_23: float: No parameter help available
			- Ms_Power_Wideband: float: No parameter help available
			- Wav_Quality: float: float Waveform quality Range: 0 to 1
			- Wav_Qual_Max_Pow: float: No parameter help available
			- Wav_Qual_Min_Power: float: No parameter help available
			- Out_Of_Tol_Count: float: float Out of tolerance result, i.e. percentage of measurement intervals of the statistic count ([CMDLINK: CONFigure:CDMA:MEASi:MEValuation:SCOunt:MODulation CMDLINK]) exceeding the specified limits, see 'Limits (Power and Modulation) '. Range: 0 % to 100 %, Unit: %"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float('Evm_Rms'),
			ArgStruct.scalar_float('Evm_Peak'),
			ArgStruct.scalar_float('Merr_Rms'),
			ArgStruct.scalar_float('Merr_Peak'),
			ArgStruct.scalar_float('Perr_Rms'),
			ArgStruct.scalar_float('Perr_Peak'),
			ArgStruct.scalar_float('Iq_Offset'),
			ArgStruct.scalar_int('Iq_Imbalance'),
			ArgStruct.scalar_float('Cfreq_Error'),
			ArgStruct.scalar_float('Trans_Time_Err'),
			ArgStruct.scalar_float('Msp_Ower_1_M_23'),
			ArgStruct.scalar_float('Ms_Power_Wideband'),
			ArgStruct.scalar_float('Wav_Quality'),
			ArgStruct.scalar_float('Wav_Qual_Max_Pow'),
			ArgStruct.scalar_float('Wav_Qual_Min_Power'),
			ArgStruct.scalar_float('Out_Of_Tol_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Evm_Rms: float = None
			self.Evm_Peak: float = None
			self.Merr_Rms: float = None
			self.Merr_Peak: float = None
			self.Perr_Rms: float = None
			self.Perr_Peak: float = None
			self.Iq_Offset: float = None
			self.Iq_Imbalance: int = None
			self.Cfreq_Error: float = None
			self.Trans_Time_Err: float = None
			self.Msp_Ower_1_M_23: float = None
			self.Ms_Power_Wideband: float = None
			self.Wav_Quality: float = None
			self.Wav_Qual_Max_Pow: float = None
			self.Wav_Qual_Min_Power: float = None
			self.Out_Of_Tol_Count: float = None

	def fetch(self) -> FetchStruct:
		"""SCPI: FETCh:CDMA:MEASurement<Instance>:MEValuation:MODulation:AVERage \n
		Snippet: value: FetchStruct = driver.multiEval.modulation.average.fetch() \n
		Return the current, average, minimum, maximum and standard deviation modulation single value results.
		The values described below are returned by FETCh and READ commands. CALCulate commands return limit check results instead,
		one value for each result listed below. The ranges indicated below apply to all results except standard deviation results.
		The minimum for standard deviation results equals 0. The maximum equals the width of the indicated range divided by two.
		Exceptions are explicitly stated. The number to the left of each result parameter is provided for easy identification of
		the parameter position within the result array. \n
			:return: structure: for return value, see the help for FetchStruct structure arguments."""
		return self._core.io.query_struct(f'FETCh:CDMA:MEASurement<Instance>:MEValuation:MODulation:AVERage?', self.__class__.FetchStruct())

	# noinspection PyTypeChecker
	class CalculateStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: decimal 'Reliability Indicator'
			- Evm_Rms: float: float Error vector magnitude RMS value Range: 0 % to 100 %, Unit: %
			- Evm_Peak: float: float Error vector magnitude peak value Range: 0 % to 100 %, Unit: %
			- Merr_Rms: float: float Magnitude error RMS value Range: 0 % to 100 %, Unit: %
			- Merr_Peak: float: float Magnitude error peak value Range: -100 % to 100 % (AVERage: 0% to 100 %, SDEViation: 0 % to 50 %) , Unit: %
			- Perr_Rms: float: float Phase error RMS value Range: 0 deg to 180 deg, Unit: deg
			- Perr_Peak: float: float Phase error peak value Range: -180 deg to 180 deg (AVERage: 0 deg to 180 deg, SDEViation: 0 deg to 90 deg) , Unit: deg
			- Iq_Offset: float: float I/Q origin offset Range: -100 dB to 0 dB, Unit: dB
			- Iq_Imbalance: float: float I/Q imbalance Range: -100 dB to 0 dB, Unit: dB
			- Cfreq_Error: float: float Carrier frequency error Range: -5000 Hz to 5000 Hz, Unit: Hz
			- Trans_Time_Err: float: float Transmit time error Range: -100 µs to 100 µs, Unit: µs
			- Msp_Ower_1_M_23: float: No parameter help available
			- Ms_Power_Wideband: float: No parameter help available
			- Wav_Quality: float: float Waveform quality Range: 0 to 1
			- Wav_Qual_Max_Pow: float: No parameter help available
			- Wav_Qual_Min_Power: float: No parameter help available
			- Out_Of_Tol_Count: float: float Out of tolerance result, i.e. percentage of measurement intervals of the statistic count ([CMDLINK: CONFigure:CDMA:MEASi:MEValuation:SCOunt:MODulation CMDLINK]) exceeding the specified limits, see 'Limits (Power and Modulation) '. Range: 0 % to 100 %, Unit: %"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float('Evm_Rms'),
			ArgStruct.scalar_float('Evm_Peak'),
			ArgStruct.scalar_float('Merr_Rms'),
			ArgStruct.scalar_float('Merr_Peak'),
			ArgStruct.scalar_float('Perr_Rms'),
			ArgStruct.scalar_float('Perr_Peak'),
			ArgStruct.scalar_float('Iq_Offset'),
			ArgStruct.scalar_float('Iq_Imbalance'),
			ArgStruct.scalar_float('Cfreq_Error'),
			ArgStruct.scalar_float('Trans_Time_Err'),
			ArgStruct.scalar_float('Msp_Ower_1_M_23'),
			ArgStruct.scalar_float('Ms_Power_Wideband'),
			ArgStruct.scalar_float('Wav_Quality'),
			ArgStruct.scalar_float('Wav_Qual_Max_Pow'),
			ArgStruct.scalar_float('Wav_Qual_Min_Power'),
			ArgStruct.scalar_float('Out_Of_Tol_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Evm_Rms: float = None
			self.Evm_Peak: float = None
			self.Merr_Rms: float = None
			self.Merr_Peak: float = None
			self.Perr_Rms: float = None
			self.Perr_Peak: float = None
			self.Iq_Offset: float = None
			self.Iq_Imbalance: float = None
			self.Cfreq_Error: float = None
			self.Trans_Time_Err: float = None
			self.Msp_Ower_1_M_23: float = None
			self.Ms_Power_Wideband: float = None
			self.Wav_Quality: float = None
			self.Wav_Qual_Max_Pow: float = None
			self.Wav_Qual_Min_Power: float = None
			self.Out_Of_Tol_Count: float = None

	def calculate(self) -> CalculateStruct:
		"""SCPI: CALCulate:CDMA:MEASurement<Instance>:MEValuation:MODulation:AVERage \n
		Snippet: value: CalculateStruct = driver.multiEval.modulation.average.calculate() \n
		Return the current, average, minimum, maximum and standard deviation modulation single value results.
		The values described below are returned by FETCh and READ commands. CALCulate commands return limit check results instead,
		one value for each result listed below. The ranges indicated below apply to all results except standard deviation results.
		The minimum for standard deviation results equals 0. The maximum equals the width of the indicated range divided by two.
		Exceptions are explicitly stated. The number to the left of each result parameter is provided for easy identification of
		the parameter position within the result array. \n
			:return: structure: for return value, see the help for CalculateStruct structure arguments."""
		return self._core.io.query_struct(f'CALCulate:CDMA:MEASurement<Instance>:MEValuation:MODulation:AVERage?', self.__class__.CalculateStruct())
