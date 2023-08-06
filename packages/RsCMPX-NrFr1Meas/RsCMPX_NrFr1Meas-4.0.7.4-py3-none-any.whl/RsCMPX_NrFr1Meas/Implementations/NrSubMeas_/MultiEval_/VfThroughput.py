from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.ArgSingleSuppressed import ArgSingleSuppressed
from ....Internal.Types import DataType


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class VfThroughput:
	"""VfThroughput commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("vfThroughput", core, parent)

	def fetch(self) -> float:
		"""SCPI: FETCh:NRSub:MEASurement<Instance>:MEValuation:VFTHroughput \n
		Snippet: value: float = driver.nrSubMeas.multiEval.vfThroughput.fetch() \n
		Queries the View Filter Throughput. \n
		Suppressed linked return values: reliability \n
			:return: vf_throughput: No help available"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'FETCh:NRSub:MEASurement<Instance>:MEValuation:VFTHroughput?', suppressed)
		return Conversions.str_to_float(response)
