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

	def read(self) -> List[float]:
		"""SCPI: READ:NRSub:MEASurement<Instance>:PRACh:TRACe:PERRor:CURRent \n
		Snippet: value: List[float] = driver.nrSubMeas.prach.trace.perror.current.read() \n
		Return the values of the phase error traces. Each value is averaged over the samples in one preamble subcarrier.
		The results of the current, average and maximum traces can be retrieved. See also 'Squares EVM, Magnitude Error, Phase
		Error'. \n
		Suppressed linked return values: reliability \n
			:return: results: Comma-separated list of phase error values, one value per subcarrier."""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'READ:NRSub:MEASurement<Instance>:PRACh:TRACe:PERRor:CURRent?', suppressed)
		return response

	def fetch(self) -> List[float]:
		"""SCPI: FETCh:NRSub:MEASurement<Instance>:PRACh:TRACe:PERRor:CURRent \n
		Snippet: value: List[float] = driver.nrSubMeas.prach.trace.perror.current.fetch() \n
		Return the values of the phase error traces. Each value is averaged over the samples in one preamble subcarrier.
		The results of the current, average and maximum traces can be retrieved. See also 'Squares EVM, Magnitude Error, Phase
		Error'. \n
		Suppressed linked return values: reliability \n
			:return: results: Comma-separated list of phase error values, one value per subcarrier."""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:NRSub:MEASurement<Instance>:PRACh:TRACe:PERRor:CURRent?', suppressed)
		return response
