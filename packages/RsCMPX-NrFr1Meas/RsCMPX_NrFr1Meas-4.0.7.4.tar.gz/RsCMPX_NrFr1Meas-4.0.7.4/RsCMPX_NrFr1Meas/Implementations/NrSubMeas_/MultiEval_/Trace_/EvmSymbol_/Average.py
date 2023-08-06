from typing import List

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.ArgSingleSuppressed import ArgSingleSuppressed
from ......Internal.Types import DataType


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Average:
	"""Average commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("average", core, parent)

	def read(self) -> List[float]:
		"""SCPI: READ:NRSub:MEASurement<Instance>:MEValuation:TRACe:EVMSymbol:AVERage \n
		Snippet: value: List[float] = driver.nrSubMeas.multiEval.trace.evmSymbol.average.read() \n
		Returns the values of the EVM vs modulation symbol trace. See also 'Square EVM'. \n
		Suppressed linked return values: reliability \n
			:return: ratio: Comma-separated list of EVM values, one value per modulation symbol"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'READ:NRSub:MEASurement<Instance>:MEValuation:TRACe:EVMSymbol:AVERage?', suppressed)
		return response

	def fetch(self) -> List[float]:
		"""SCPI: FETCh:NRSub:MEASurement<Instance>:MEValuation:TRACe:EVMSymbol:AVERage \n
		Snippet: value: List[float] = driver.nrSubMeas.multiEval.trace.evmSymbol.average.fetch() \n
		Returns the values of the EVM vs modulation symbol trace. See also 'Square EVM'. \n
		Suppressed linked return values: reliability \n
			:return: ratio: Comma-separated list of EVM values, one value per modulation symbol"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:NRSub:MEASurement<Instance>:MEValuation:TRACe:EVMSymbol:AVERage?', suppressed)
		return response
