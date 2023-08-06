from typing import List

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.ArgSingleSuppressed import ArgSingleSuppressed
from ......Internal.Types import DataType


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Rms:
	"""Rms commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rms", core, parent)

	def fetch(self) -> List[float]:
		"""SCPI: FETCh:NRSub:MEASurement<Instance>:MEValuation:LIST:PMONitor:RMS \n
		Snippet: value: List[float] = driver.nrSubMeas.multiEval.listPy.pmonitor.rms.fetch() \n
		Return the power monitor results for all measured segments in list mode. The commands return one power result per
		subframe for the measured carrier. The power values are RMS averaged over the subframe or represent the peak value within
		the subframe.
			INTRO_CMD_HELP: Commands for querying the result list structure: \n
			- method RsCMPX_NrFr1Meas.NrSubMeas.MultiEval.ListPy.Segment.Pmonitor.Array.Start.fetch
			- method RsCMPX_NrFr1Meas.NrSubMeas.MultiEval.ListPy.Segment.Pmonitor.Array.Length.fetch  \n
		Suppressed linked return values: reliability \n
			:return: step_rms_power: Comma-separated list of power values, one value per subframe, from first subframe of first measured segment to last subframe of last measured segment For an inactive segment, only one INV is returned, independent of the number of configured subframes."""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:NRSub:MEASurement<Instance>:MEValuation:LIST:PMONitor:RMS?', suppressed)
		return response
