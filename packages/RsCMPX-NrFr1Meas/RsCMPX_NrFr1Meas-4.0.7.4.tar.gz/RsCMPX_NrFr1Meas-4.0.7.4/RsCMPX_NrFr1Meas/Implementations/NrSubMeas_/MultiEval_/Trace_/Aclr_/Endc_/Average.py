from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Average:
	"""Average commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("average", core, parent)

	# noinspection PyTypeChecker
	class ResultData(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: 'Reliability Indicator'
			- Endc_Neg: float: Power in the adjacent channel with lower frequency
			- Carrier: float: Power in the allocated channel (aggregated BW)
			- Endc_Pos: float: Power in the adjacent channel with higher frequency"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float('Endc_Neg'),
			ArgStruct.scalar_float('Carrier'),
			ArgStruct.scalar_float('Endc_Pos')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Endc_Neg: float = None
			self.Carrier: float = None
			self.Endc_Pos: float = None

	def read(self) -> ResultData:
		"""SCPI: READ:NRSub:MEASurement<Instance>:MEValuation:TRACe:ACLR:ENDC:AVERage \n
		Snippet: value: ResultData = driver.nrSubMeas.multiEval.trace.aclr.endc.average.read() \n
		Returns the absolute powers as displayed in the ACLR diagram for EN-DC. The current and average values can be retrieved.
		See also 'Square Spectrum ACLR'. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'READ:NRSub:MEASurement<Instance>:MEValuation:TRACe:ACLR:ENDC:AVERage?', self.__class__.ResultData())

	def fetch(self) -> ResultData:
		"""SCPI: FETCh:NRSub:MEASurement<Instance>:MEValuation:TRACe:ACLR:ENDC:AVERage \n
		Snippet: value: ResultData = driver.nrSubMeas.multiEval.trace.aclr.endc.average.fetch() \n
		Returns the absolute powers as displayed in the ACLR diagram for EN-DC. The current and average values can be retrieved.
		See also 'Square Spectrum ACLR'. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'FETCh:NRSub:MEASurement<Instance>:MEValuation:TRACe:ACLR:ENDC:AVERage?', self.__class__.ResultData())
