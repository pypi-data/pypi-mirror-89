from typing import List

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.ArgSingleSuppressed import ArgSingleSuppressed
from ......Internal.Types import DataType


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Current:
	"""Current commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("current", core, parent)

	def fetch(self) -> List[float]:
		"""SCPI: FETCh:GSM:MEASurement<Instance>:MEValuation:LIST:MODulation:APDelay:CURRent \n
		Snippet: value: List[float] = driver.multiEval.listPy.modulation.apDelay.current.fetch() \n
		Return AM-PM delay results for all measured list mode segments. The values described below are returned by FETCh commands.
		CALCulate commands return limit check results instead, one value for each result listed below. \n
		Use RsCmwGsmMeas.reliability.last_value to read the updated reliability indicator. \n
			:return: am_pmdelay: float Comma-separated list of values, one per measured segment Range: -0.9225E-6 s to 0.9225E-6 s, Unit: s"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:GSM:MEASurement<Instance>:MEValuation:LIST:MODulation:APDelay:CURRent?', suppressed)
		return response

	def calculate(self) -> List[float]:
		"""SCPI: CALCulate:GSM:MEASurement<Instance>:MEValuation:LIST:MODulation:APDelay:CURRent \n
		Snippet: value: List[float] = driver.multiEval.listPy.modulation.apDelay.current.calculate() \n
		Return AM-PM delay results for all measured list mode segments. The values described below are returned by FETCh commands.
		CALCulate commands return limit check results instead, one value for each result listed below. \n
		Use RsCmwGsmMeas.reliability.last_value to read the updated reliability indicator. \n
			:return: am_pmdelay: float Comma-separated list of values, one per measured segment Range: -0.9225E-6 s to 0.9225E-6 s, Unit: s"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'CALCulate:GSM:MEASurement<Instance>:MEValuation:LIST:MODulation:APDelay:CURRent?', suppressed)
		return response
