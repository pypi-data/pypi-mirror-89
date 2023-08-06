from typing import List

from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.ArgSingleSuppressed import ArgSingleSuppressed
from .......Internal.Types import DataType
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Average:
	"""Average commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("average", core, parent)

	def fetch(self, maxRange=repcap.MaxRange.Default) -> List[float]:
		"""SCPI: FETCh:NRSub:MEASurement<Instance>:MEValuation:LIST:ESFLatness:MAXR<nr6g>:AVERage \n
		Snippet: value: List[float] = driver.nrSubMeas.multiEval.listPy.esFlatness.maxr.average.fetch(maxRange = repcap.MaxRange.Default) \n
		Return equalizer spectrum flatness single value results (maximum within a range) for all measured list mode segments. The
		values described below are returned by FETCh commands. CALCulate commands return limit check results instead, one value
		for each result listed below. \n
		Suppressed linked return values: reliability \n
			:param maxRange: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Maxr')
			:return: max_r: Comma-separated list of values, one per measured segment"""
		maxRange_cmd_val = self._base.get_repcap_cmd_value(maxRange, repcap.MaxRange)
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:NRSub:MEASurement<Instance>:MEValuation:LIST:ESFLatness:MAXR{maxRange_cmd_val}:AVERage?', suppressed)
		return response

	def calculate(self, maxRange=repcap.MaxRange.Default) -> List[float]:
		"""SCPI: CALCulate:NRSub:MEASurement<Instance>:MEValuation:LIST:ESFLatness:MAXR<nr6g>:AVERage \n
		Snippet: value: List[float] = driver.nrSubMeas.multiEval.listPy.esFlatness.maxr.average.calculate(maxRange = repcap.MaxRange.Default) \n
		Return equalizer spectrum flatness single value results (maximum within a range) for all measured list mode segments. The
		values described below are returned by FETCh commands. CALCulate commands return limit check results instead, one value
		for each result listed below. \n
		Suppressed linked return values: reliability \n
			:param maxRange: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Maxr')
			:return: max_r: Comma-separated list of values, one per measured segment"""
		maxRange_cmd_val = self._base.get_repcap_cmd_value(maxRange, repcap.MaxRange)
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'CALCulate:NRSub:MEASurement<Instance>:MEValuation:LIST:ESFLatness:MAXR{maxRange_cmd_val}:AVERage?', suppressed)
		return response
