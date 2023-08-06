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
	class CalculateStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: decimal 'Reliability Indicator'
			- Out_Of_Tolerance: int: decimal Percentage of measurement intervals / bursts of the statistic count ([CMDLINK: CONFigure:GSM:MEASi:MEValuation:SCOunt:MODulation CMDLINK]) exceeding the specified modulation limits. Range: 0 % to 100 %, Unit: %
			- Evm_Rms: float: float Error vector magnitude RMS and peak value Range: 0 % to 100 %, Unit: %
			- Evmpeak: float: float Error vector magnitude RMS and peak value Range: 0 % to 100 %, Unit: %
			- Mag_Error_Rms: float: float Magnitude error RMS and peak value Range: 0 % to 100 %, Unit: %
			- Mag_Error_Peak: float: float Magnitude error RMS and peak value Range: 0 % to 100 %, Unit: %
			- Phase_Error_Rms: float: float Phase error RMS and peak value Range: 0 deg to 180 deg, Unit: deg
			- Phase_Error_Peak: float: float Phase error RMS and peak value Range: 0 deg to 180 deg, Unit: deg
			- Iq_Offset: float: float I/Q origin offset Range: -100 dB to 0 dB, Unit: dB
			- Iq_Imbalance: float: float I/Q imbalance Range: -100 dB to 0 dB, Unit: dB
			- Frequency_Error: float: float Carrier frequency error Range: -56000 Hz to 56000 Hz, Unit: Hz
			- Timing_Error: float: float Transmit time error Range: -100 Sym to 100 Sym, Unit: Symbol
			- Burst_Power: float: float Burst power Range: -100 dBm to 55 dBm, Unit: dBm
			- Am_Pmdelay: float: float AMPM delay (determined for 8PSK and 16-QAM modulation only - for GMSK zeros are returned) Range: -0.9225E-6 s to 0.9225E-6 s, Unit: s"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_int('Out_Of_Tolerance'),
			ArgStruct.scalar_float('Evm_Rms'),
			ArgStruct.scalar_float('Evmpeak'),
			ArgStruct.scalar_float('Mag_Error_Rms'),
			ArgStruct.scalar_float('Mag_Error_Peak'),
			ArgStruct.scalar_float('Phase_Error_Rms'),
			ArgStruct.scalar_float('Phase_Error_Peak'),
			ArgStruct.scalar_float('Iq_Offset'),
			ArgStruct.scalar_float('Iq_Imbalance'),
			ArgStruct.scalar_float('Frequency_Error'),
			ArgStruct.scalar_float('Timing_Error'),
			ArgStruct.scalar_float('Burst_Power'),
			ArgStruct.scalar_float('Am_Pmdelay')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Out_Of_Tolerance: int = None
			self.Evm_Rms: float = None
			self.Evmpeak: float = None
			self.Mag_Error_Rms: float = None
			self.Mag_Error_Peak: float = None
			self.Phase_Error_Rms: float = None
			self.Phase_Error_Peak: float = None
			self.Iq_Offset: float = None
			self.Iq_Imbalance: float = None
			self.Frequency_Error: float = None
			self.Timing_Error: float = None
			self.Burst_Power: float = None
			self.Am_Pmdelay: float = None

	def calculate(self) -> CalculateStruct:
		"""SCPI: CALCulate:GSM:MEASurement<Instance>:MEValuation:MODulation:AVERage \n
		Snippet: value: CalculateStruct = driver.multiEval.modulation.average.calculate() \n
		Returns the average single slot modulation results of the multi-evaluation measurement. The values described below are
		returned by FETCh and READ commands. CALCulate commands return limit check results instead, one value for each result
		listed below. \n
			:return: structure: for return value, see the help for CalculateStruct structure arguments."""
		return self._core.io.query_struct(f'CALCulate:GSM:MEASurement<Instance>:MEValuation:MODulation:AVERage?', self.__class__.CalculateStruct())

	# noinspection PyTypeChecker
	class ResultData(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: decimal 'Reliability Indicator'
			- Out_Of_Tolerance: int: decimal Percentage of measurement intervals / bursts of the statistic count ([CMDLINK: CONFigure:GSM:MEASi:MEValuation:SCOunt:MODulation CMDLINK]) exceeding the specified modulation limits. Range: 0 % to 100 %, Unit: %
			- Evm_Rms: float: float Error vector magnitude RMS and peak value Range: 0 % to 100 %, Unit: %
			- Evmpeak: float: float Error vector magnitude RMS and peak value Range: 0 % to 100 %, Unit: %
			- Mag_Error_Rms: float: float Magnitude error RMS and peak value Range: 0 % to 100 %, Unit: %
			- Mag_Error_Peak: float: float Magnitude error RMS and peak value Range: 0 % to 100 %, Unit: %
			- Phase_Error_Rms: float: float Phase error RMS and peak value Range: 0 deg to 180 deg, Unit: deg
			- Phase_Error_Peak: float: float Phase error RMS and peak value Range: 0 deg to 180 deg, Unit: deg
			- Iq_Offset: float: float I/Q origin offset Range: -100 dB to 0 dB, Unit: dB
			- Iq_Imbalance: float: float I/Q imbalance Range: -100 dB to 0 dB, Unit: dB
			- Frequency_Error: float: float Carrier frequency error Range: -56000 Hz to 56000 Hz, Unit: Hz
			- Timing_Error: float: float Transmit time error Range: -100 Sym to 100 Sym, Unit: Symbol
			- Burst_Power: float: float Burst power Range: -100 dBm to 55 dBm, Unit: dBm
			- Am_Pmdelay: float: float AMPM delay (determined for 8PSK and 16-QAM modulation only - for GMSK zeros are returned) Range: -0.9225E-6 s to 0.9225E-6 s, Unit: s"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_int('Out_Of_Tolerance'),
			ArgStruct.scalar_float('Evm_Rms'),
			ArgStruct.scalar_float('Evmpeak'),
			ArgStruct.scalar_float('Mag_Error_Rms'),
			ArgStruct.scalar_float('Mag_Error_Peak'),
			ArgStruct.scalar_float('Phase_Error_Rms'),
			ArgStruct.scalar_float('Phase_Error_Peak'),
			ArgStruct.scalar_float('Iq_Offset'),
			ArgStruct.scalar_float('Iq_Imbalance'),
			ArgStruct.scalar_float('Frequency_Error'),
			ArgStruct.scalar_float('Timing_Error'),
			ArgStruct.scalar_float('Burst_Power'),
			ArgStruct.scalar_float('Am_Pmdelay')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Out_Of_Tolerance: int = None
			self.Evm_Rms: float = None
			self.Evmpeak: float = None
			self.Mag_Error_Rms: float = None
			self.Mag_Error_Peak: float = None
			self.Phase_Error_Rms: float = None
			self.Phase_Error_Peak: float = None
			self.Iq_Offset: float = None
			self.Iq_Imbalance: float = None
			self.Frequency_Error: float = None
			self.Timing_Error: float = None
			self.Burst_Power: float = None
			self.Am_Pmdelay: float = None

	def fetch(self) -> ResultData:
		"""SCPI: FETCh:GSM:MEASurement<Instance>:MEValuation:MODulation:AVERage \n
		Snippet: value: ResultData = driver.multiEval.modulation.average.fetch() \n
		Returns the average single slot modulation results of the multi-evaluation measurement. The values described below are
		returned by FETCh and READ commands. CALCulate commands return limit check results instead, one value for each result
		listed below. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'FETCh:GSM:MEASurement<Instance>:MEValuation:MODulation:AVERage?', self.__class__.ResultData())

	def read(self) -> ResultData:
		"""SCPI: READ:GSM:MEASurement<Instance>:MEValuation:MODulation:AVERage \n
		Snippet: value: ResultData = driver.multiEval.modulation.average.read() \n
		Returns the average single slot modulation results of the multi-evaluation measurement. The values described below are
		returned by FETCh and READ commands. CALCulate commands return limit check results instead, one value for each result
		listed below. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'READ:GSM:MEASurement<Instance>:MEValuation:MODulation:AVERage?', self.__class__.ResultData())
