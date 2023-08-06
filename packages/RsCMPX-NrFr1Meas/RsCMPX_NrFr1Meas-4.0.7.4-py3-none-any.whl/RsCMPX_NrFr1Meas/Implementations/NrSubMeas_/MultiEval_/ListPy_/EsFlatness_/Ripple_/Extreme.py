from typing import List

from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.ArgSingleSuppressed import ArgSingleSuppressed
from .......Internal.Types import DataType
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Extreme:
	"""Extreme commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("extreme", core, parent)

	def fetch(self, ripple=repcap.Ripple.Default) -> List[float]:
		"""SCPI: FETCh:NRSub:MEASurement<Instance>:MEValuation:LIST:ESFLatness:RIPPle<nr6g>:EXTReme \n
		Snippet: value: List[float] = driver.nrSubMeas.multiEval.listPy.esFlatness.ripple.extreme.fetch(ripple = repcap.Ripple.Default) \n
		Return equalizer spectrum flatness single value results (ripple 1 or ripple 2) for all measured list mode segments. The
		values described below are returned by FETCh commands. CALCulate commands return limit check results instead, one value
		for each result listed below. \n
		Suppressed linked return values: reliability \n
			:param ripple: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ripple')
			:return: ripple: Comma-separated list of values, one per measured segment"""
		ripple_cmd_val = self._base.get_repcap_cmd_value(ripple, repcap.Ripple)
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:NRSub:MEASurement<Instance>:MEValuation:LIST:ESFLatness:RIPPle{ripple_cmd_val}:EXTReme?', suppressed)
		return response

	def calculate(self, ripple=repcap.Ripple.Default) -> List[float]:
		"""SCPI: CALCulate:NRSub:MEASurement<Instance>:MEValuation:LIST:ESFLatness:RIPPle<nr6g>:EXTReme \n
		Snippet: value: List[float] = driver.nrSubMeas.multiEval.listPy.esFlatness.ripple.extreme.calculate(ripple = repcap.Ripple.Default) \n
		Return equalizer spectrum flatness single value results (ripple 1 or ripple 2) for all measured list mode segments. The
		values described below are returned by FETCh commands. CALCulate commands return limit check results instead, one value
		for each result listed below. \n
		Suppressed linked return values: reliability \n
			:param ripple: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ripple')
			:return: ripple: Comma-separated list of values, one per measured segment"""
		ripple_cmd_val = self._base.get_repcap_cmd_value(ripple, repcap.Ripple)
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'CALCulate:NRSub:MEASurement<Instance>:MEValuation:LIST:ESFLatness:RIPPle{ripple_cmd_val}:EXTReme?', suppressed)
		return response
