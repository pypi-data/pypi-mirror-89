from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Current:
	"""Current commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("current", core, parent)

	# noinspection PyTypeChecker
	class FetchStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: 'Reliability Indicator'
			- Seg_Reliability: int: Reliability indicator for the segment
			- Statist_Expired: int: Reached statistical length in slots
			- Out_Of_Tolerance: int: Percentage of measured subframes with failed limit check
			- Utra_2_Neg: float: ACLR for the second UTRA channel with lower frequency
			- Utra_1_Neg: float: ACLR for the first UTRA channel with lower frequency
			- Nr_Neg: float: ACLR for the first NR channel with lower frequency
			- Carrier: float: Power in the allocated NR channel
			- Nr_Pos: float: ACLR for the first NR channel with higher frequency
			- Utra_1_Pos: float: ACLR for the first UTRA channel with higher frequency
			- Utra_2_Pos: float: ACLR for the second UTRA channel with higher frequency"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_int('Seg_Reliability'),
			ArgStruct.scalar_int('Statist_Expired'),
			ArgStruct.scalar_int('Out_Of_Tolerance'),
			ArgStruct.scalar_float('Utra_2_Neg'),
			ArgStruct.scalar_float('Utra_1_Neg'),
			ArgStruct.scalar_float('Nr_Neg'),
			ArgStruct.scalar_float('Carrier'),
			ArgStruct.scalar_float('Nr_Pos'),
			ArgStruct.scalar_float('Utra_1_Pos'),
			ArgStruct.scalar_float('Utra_2_Pos')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Seg_Reliability: int = None
			self.Statist_Expired: int = None
			self.Out_Of_Tolerance: int = None
			self.Utra_2_Neg: float = None
			self.Utra_1_Neg: float = None
			self.Nr_Neg: float = None
			self.Carrier: float = None
			self.Nr_Pos: float = None
			self.Utra_1_Pos: float = None
			self.Utra_2_Pos: float = None

	def fetch(self, sEGMent=repcap.SEGMent.Default) -> FetchStruct:
		"""SCPI: FETCh:NRSub:MEASurement<Instance>:MEValuation:LIST:SEGMent<nr6g>:ACLR:CURRent \n
		Snippet: value: FetchStruct = driver.nrSubMeas.multiEval.listPy.segment.aclr.current.fetch(sEGMent = repcap.SEGMent.Default) \n
		Return ACLR single value results for segment <no> in list mode. The values described below are returned by FETCh commands.
		The first four values (reliability to out-of-tolerance result) are also returned by CALCulate commands. The remaining
		values returned by CALCulate commands are limit check results, one value for each result listed below. \n
			:param sEGMent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')
			:return: structure: for return value, see the help for FetchStruct structure arguments."""
		sEGMent_cmd_val = self._base.get_repcap_cmd_value(sEGMent, repcap.SEGMent)
		return self._core.io.query_struct(f'FETCh:NRSub:MEASurement<Instance>:MEValuation:LIST:SEGMent{sEGMent_cmd_val}:ACLR:CURRent?', self.__class__.FetchStruct())

	# noinspection PyTypeChecker
	class CalculateStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: 'Reliability Indicator'
			- Seg_Reliability: int: Reliability indicator for the segment
			- Statist_Expired: int: Reached statistical length in slots
			- Out_Of_Tolerance: int: Percentage of measured subframes with failed limit check
			- Utra_2_Neg: enums.ResultStatus2: ACLR for the second UTRA channel with lower frequency
			- Utra_1_Neg: enums.ResultStatus2: ACLR for the first UTRA channel with lower frequency
			- Nr_Neg: enums.ResultStatus2: ACLR for the first NR channel with lower frequency
			- Carrier: enums.ResultStatus2: Power in the allocated NR channel
			- Nr_Pos: enums.ResultStatus2: ACLR for the first NR channel with higher frequency
			- Utra_1_Pos: enums.ResultStatus2: ACLR for the first UTRA channel with higher frequency
			- Utra_2_Pos: enums.ResultStatus2: ACLR for the second UTRA channel with higher frequency"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_int('Seg_Reliability'),
			ArgStruct.scalar_int('Statist_Expired'),
			ArgStruct.scalar_int('Out_Of_Tolerance'),
			ArgStruct.scalar_enum('Utra_2_Neg', enums.ResultStatus2),
			ArgStruct.scalar_enum('Utra_1_Neg', enums.ResultStatus2),
			ArgStruct.scalar_enum('Nr_Neg', enums.ResultStatus2),
			ArgStruct.scalar_enum('Carrier', enums.ResultStatus2),
			ArgStruct.scalar_enum('Nr_Pos', enums.ResultStatus2),
			ArgStruct.scalar_enum('Utra_1_Pos', enums.ResultStatus2),
			ArgStruct.scalar_enum('Utra_2_Pos', enums.ResultStatus2)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Seg_Reliability: int = None
			self.Statist_Expired: int = None
			self.Out_Of_Tolerance: int = None
			self.Utra_2_Neg: enums.ResultStatus2 = None
			self.Utra_1_Neg: enums.ResultStatus2 = None
			self.Nr_Neg: enums.ResultStatus2 = None
			self.Carrier: enums.ResultStatus2 = None
			self.Nr_Pos: enums.ResultStatus2 = None
			self.Utra_1_Pos: enums.ResultStatus2 = None
			self.Utra_2_Pos: enums.ResultStatus2 = None

	def calculate(self, sEGMent=repcap.SEGMent.Default) -> CalculateStruct:
		"""SCPI: CALCulate:NRSub:MEASurement<Instance>:MEValuation:LIST:SEGMent<nr6g>:ACLR:CURRent \n
		Snippet: value: CalculateStruct = driver.nrSubMeas.multiEval.listPy.segment.aclr.current.calculate(sEGMent = repcap.SEGMent.Default) \n
		Return ACLR single value results for segment <no> in list mode. The values described below are returned by FETCh commands.
		The first four values (reliability to out-of-tolerance result) are also returned by CALCulate commands. The remaining
		values returned by CALCulate commands are limit check results, one value for each result listed below. \n
			:param sEGMent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')
			:return: structure: for return value, see the help for CalculateStruct structure arguments."""
		sEGMent_cmd_val = self._base.get_repcap_cmd_value(sEGMent, repcap.SEGMent)
		return self._core.io.query_struct(f'CALCulate:NRSub:MEASurement<Instance>:MEValuation:LIST:SEGMent{sEGMent_cmd_val}:ACLR:CURRent?', self.__class__.CalculateStruct())
