from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.ArgSingleSuppressed import ArgSingleSuppressed
from .....Internal.Types import DataType


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class EvPreamble:
	"""EvPreamble commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("evPreamble", core, parent)

	def read(self) -> List[float]:
		"""SCPI: READ:NRSub:MEASurement<Instance>:PRACh:TRACe:EVPReamble \n
		Snippet: value: List[float] = driver.nrSubMeas.prach.trace.evPreamble.read() \n
		Return the values of the EVM vs preamble traces. See also 'Squares EVM vs Preamble, Power vs Preamble'. \n
		Suppressed linked return values: reliability \n
			:return: results: Comma-separated list of EVM values, for preamble 1 to n of the measurement interval."""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'READ:NRSub:MEASurement<Instance>:PRACh:TRACe:EVPReamble?', suppressed)
		return response

	def fetch(self) -> List[float]:
		"""SCPI: FETCh:NRSub:MEASurement<Instance>:PRACh:TRACe:EVPReamble \n
		Snippet: value: List[float] = driver.nrSubMeas.prach.trace.evPreamble.fetch() \n
		Return the values of the EVM vs preamble traces. See also 'Squares EVM vs Preamble, Power vs Preamble'. \n
		Suppressed linked return values: reliability \n
			:return: results: Comma-separated list of EVM values, for preamble 1 to n of the measurement interval."""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:NRSub:MEASurement<Instance>:PRACh:TRACe:EVPReamble?', suppressed)
		return response
