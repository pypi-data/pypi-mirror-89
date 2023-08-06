from typing import List

from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........Internal.ArgSingleSuppressed import ArgSingleSuppressed
from ........Internal.Types import DataType
from ........ import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Average:
	"""Average commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("average", core, parent)

	def fetch(self) -> List[float]:
		"""SCPI: FETCh:NRSub:MEASurement<Instance>:MEValuation:LIST:ACLR:NR:POSitiv:AVERage \n
		Snippet: value: List[float] = driver.nrSubMeas.multiEval.listPy.aclr.nr.positiv.average.fetch() \n
		Return the ACLR for the first adjacent NR channel above (POSitiv) or below (NEGativ) the carrier frequency for all
		measured list mode segments. The values described below are returned by FETCh commands. CALCulate commands return limit
		check results instead, one value for each result listed below. \n
		Suppressed linked return values: reliability \n
			:return: nr_positiv: Comma-separated list of values, one per measured segment"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:NRSub:MEASurement<Instance>:MEValuation:LIST:ACLR:NR:POSitiv:AVERage?', suppressed)
		return response

	# noinspection PyTypeChecker
	def calculate(self) -> List[enums.ResultStatus2]:
		"""SCPI: CALCulate:NRSub:MEASurement<Instance>:MEValuation:LIST:ACLR:NR:POSitiv:AVERage \n
		Snippet: value: List[enums.ResultStatus2] = driver.nrSubMeas.multiEval.listPy.aclr.nr.positiv.average.calculate() \n
		Return the ACLR for the first adjacent NR channel above (POSitiv) or below (NEGativ) the carrier frequency for all
		measured list mode segments. The values described below are returned by FETCh commands. CALCulate commands return limit
		check results instead, one value for each result listed below. \n
		Suppressed linked return values: reliability \n
			:return: nr_positiv: Comma-separated list of values, one per measured segment"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'CALCulate:NRSub:MEASurement<Instance>:MEValuation:LIST:ACLR:NR:POSitiv:AVERage?', suppressed)
		return Conversions.str_to_list_enum(response, enums.ResultStatus2)
