from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........Internal.ArgSingleSuppressed import ArgSingleSuppressed
from ........Internal.Types import DataType
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Length:
	"""Length commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("length", core, parent)

	def fetch(self, sEGMent=repcap.SEGMent.Default) -> int:
		"""SCPI: FETCh:NRSub:MEASurement<Instance>:MEValuation:LIST:SEGMent<nr6g>:PMONitor:ARRay:LENGth \n
		Snippet: value: int = driver.nrSubMeas.multiEval.listPy.segment.pmonitor.array.length.fetch(sEGMent = repcap.SEGMent.Default) \n
		Returns the number of power monitor results for segment <no> contained in a result list for all measured segments. Such a
		result list is, for example, returned by the command method RsCMPX_NrFr1Meas.NrSubMeas.MultiEval.ListPy.Pmonitor.Rms.
		fetch. \n
		Suppressed linked return values: reliability \n
			:param sEGMent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')
			:return: length: Number of power monitor results"""
		sEGMent_cmd_val = self._base.get_repcap_cmd_value(sEGMent, repcap.SEGMent)
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'FETCh:NRSub:MEASurement<Instance>:MEValuation:LIST:SEGMent{sEGMent_cmd_val}:PMONitor:ARRay:LENGth?', suppressed)
		return Conversions.str_to_int(response)
