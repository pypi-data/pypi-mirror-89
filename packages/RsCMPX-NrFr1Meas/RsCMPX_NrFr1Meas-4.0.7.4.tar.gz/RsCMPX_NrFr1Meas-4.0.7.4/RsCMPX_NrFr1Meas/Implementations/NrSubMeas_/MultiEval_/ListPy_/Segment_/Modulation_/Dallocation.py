from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dallocation:
	"""Dallocation commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dallocation", core, parent)

	# noinspection PyTypeChecker
	class FetchStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: 'Reliability Indicator'
			- Seg_Reliability: int: Reliability indicator for the segment
			- Nr_Res_Blocks: int: Number of allocated resource blocks
			- Offset_Res_Blocks: int: Offset of the first allocated resource block from the edge of the allocated UL transmission bandwidth"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_int('Seg_Reliability'),
			ArgStruct.scalar_int('Nr_Res_Blocks'),
			ArgStruct.scalar_int('Offset_Res_Blocks')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Seg_Reliability: int = None
			self.Nr_Res_Blocks: int = None
			self.Offset_Res_Blocks: int = None

	def fetch(self, sEGMent=repcap.SEGMent.Default) -> FetchStruct:
		"""SCPI: FETCh:NRSub:MEASurement<Instance>:MEValuation:LIST:SEGMent<nr>:MODulation:DALLocation \n
		Snippet: value: FetchStruct = driver.nrSubMeas.multiEval.listPy.segment.modulation.dallocation.fetch(sEGMent = repcap.SEGMent.Default) \n
		Return the detected allocation for segment <no> in list mode. The result is determined from the last measured slot of the
		statistical length. The individual measurements provide identical detected allocation results when measuring the same
		slot. However, different statistical lengths can be defined for the measurements so that the measured slots and returned
		results can differ. \n
			:param sEGMent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')
			:return: structure: for return value, see the help for FetchStruct structure arguments."""
		sEGMent_cmd_val = self._base.get_repcap_cmd_value(sEGMent, repcap.SEGMent)
		return self._core.io.query_struct(f'FETCh:NRSub:MEASurement<Instance>:MEValuation:LIST:SEGMent{sEGMent_cmd_val}:MODulation:DALLocation?', self.__class__.FetchStruct())
