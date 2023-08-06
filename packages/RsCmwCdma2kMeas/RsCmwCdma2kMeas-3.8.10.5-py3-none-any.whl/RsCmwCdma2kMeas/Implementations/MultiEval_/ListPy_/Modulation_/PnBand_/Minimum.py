from typing import List

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.ArgSingleSuppressed import ArgSingleSuppressed
from ......Internal.Types import DataType


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Minimum:
	"""Minimum commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("minimum", core, parent)

	def fetch(self) -> List[float]:
		"""SCPI: FETCh:CDMA:MEASurement<Instance>:MEValuation:LIST:MODulation:PNBand:MINimum \n
		Snippet: value: List[float] = driver.multiEval.listPy.modulation.pnBand.minimum.fetch() \n
		Returns MS narrowband and wideband power (statistical) values for all active list mode segments. The narrowband filter is
		1.23 MHz, the wideband filter is 8 MHz wide. The values described below are returned by FETCh commands.
		CALCulate commands return limit check results instead, one value for each result listed below. \n
		Use RsCmwCdma2kMeas.reliability.last_value to read the updated reliability indicator. \n
			:return: msp_ower_1_m_23: float Comma-separated list of values, one per active segment. Range: -100 dBm to 50 dBm , Unit: dBm"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:CDMA:MEASurement<Instance>:MEValuation:LIST:MODulation:PNBand:MINimum?', suppressed)
		return response

	def calculate(self) -> List[float]:
		"""SCPI: CALCulate:CDMA:MEASurement<Instance>:MEValuation:LIST:MODulation:PNBand:MINimum \n
		Snippet: value: List[float] = driver.multiEval.listPy.modulation.pnBand.minimum.calculate() \n
		Returns MS narrowband and wideband power (statistical) values for all active list mode segments. The narrowband filter is
		1.23 MHz, the wideband filter is 8 MHz wide. The values described below are returned by FETCh commands.
		CALCulate commands return limit check results instead, one value for each result listed below. \n
		Use RsCmwCdma2kMeas.reliability.last_value to read the updated reliability indicator. \n
			:return: msp_ower_1_m_23: float Comma-separated list of values, one per active segment. Range: -100 dBm to 50 dBm , Unit: dBm"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'CALCulate:CDMA:MEASurement<Instance>:MEValuation:LIST:MODulation:PNBand:MINimum?', suppressed)
		return response
