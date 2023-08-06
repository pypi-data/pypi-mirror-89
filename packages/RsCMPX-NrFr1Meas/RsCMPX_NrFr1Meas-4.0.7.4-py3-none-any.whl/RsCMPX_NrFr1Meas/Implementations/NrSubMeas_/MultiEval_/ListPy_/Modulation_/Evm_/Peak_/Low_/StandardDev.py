from typing import List

from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal.ArgSingleSuppressed import ArgSingleSuppressed
from .........Internal.Types import DataType


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StandardDev:
	"""StandardDev commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("standardDev", core, parent)

	def fetch(self) -> List[float]:
		"""SCPI: FETCh:NRSub:MEASurement<Instance>:MEValuation:LIST:MODulation:EVM:PEAK:LOW:SDEViation \n
		Snippet: value: List[float] = driver.nrSubMeas.multiEval.listPy.modulation.evm.peak.low.standardDev.fetch() \n
		Return error vector magnitude peak values for low and high EVM window position, for all measured list mode segments. The
		values described below are returned by FETCh commands. CALCulate commands return limit check results instead, one value
		for each result listed below. \n
		Suppressed linked return values: reliability \n
			:return: evmpeak_low: Comma-separated list of values, one per measured segment"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:NRSub:MEASurement<Instance>:MEValuation:LIST:MODulation:EVM:PEAK:LOW:SDEViation?', suppressed)
		return response
