from typing import List

from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal.Types import DataType
from ...Internal.StructBase import StructBase
from ...Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ber:
	"""Ber commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ber", core, parent)

	# noinspection PyTypeChecker
	class ResultData(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: decimal 'Reliability Indicator'
			- Ber: float or bool: float % bit error rate Range: 0 % to 100 %, Unit: %
			- Berabsolute: List[float or bool]: float Total number of detected bit errors The BER measurement evaluates 114 data bits per GMSK-modulated normal burst, 306 data bits per 8PSK-modulated burst. Range: 0 to no. of measured bits
			- Bercount: List[float or bool]: float Total number of evaluated bits Range: 0 to no. of measured bits"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float_ext('Ber'),
			ArgStruct('Berabsolute', DataType.FloatList, None, False, False, 8),
			ArgStruct('Bercount', DataType.FloatList, None, False, False, 8)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Ber: float or bool = None
			self.Berabsolute: List[float or bool] = None
			self.Bercount: List[float or bool] = None

	def read(self) -> ResultData:
		"""SCPI: READ:GSM:MEASurement<Instance>:MEValuation:BER \n
		Snippet: value: ResultData = driver.multiEval.ber.read() \n
		Returns the measured bit error rate. The BER measurement must be enabled using method RsCmwGsmMeas.Configure.MultiEval.
		Result.ber. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'READ:GSM:MEASurement<Instance>:MEValuation:BER?', self.__class__.ResultData())

	def fetch(self) -> ResultData:
		"""SCPI: FETCh:GSM:MEASurement<Instance>:MEValuation:BER \n
		Snippet: value: ResultData = driver.multiEval.ber.fetch() \n
		Returns the measured bit error rate. The BER measurement must be enabled using method RsCmwGsmMeas.Configure.MultiEval.
		Result.ber. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'FETCh:GSM:MEASurement<Instance>:MEValuation:BER?', self.__class__.ResultData())
