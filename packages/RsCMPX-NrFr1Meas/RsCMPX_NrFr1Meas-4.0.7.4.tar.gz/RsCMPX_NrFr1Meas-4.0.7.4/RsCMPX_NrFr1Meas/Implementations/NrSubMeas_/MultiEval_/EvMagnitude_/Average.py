from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.Types import DataType
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Average:
	"""Average commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("average", core, parent)

	# noinspection PyTypeChecker
	class ResultData(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: 'Reliability Indicator'
			- Low: List[float]: EVM value for low EVM window position.
			- High: List[float]: EVM value for high EVM window position."""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct('Low', DataType.FloatList, None, False, True, 1),
			ArgStruct('High', DataType.FloatList, None, False, True, 1)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Low: List[float] = None
			self.High: List[float] = None

	def read(self) -> ResultData:
		"""SCPI: READ:NRSub:MEASurement<Instance>:MEValuation:EVMagnitude:AVERage \n
		Snippet: value: ResultData = driver.nrSubMeas.multiEval.evMagnitude.average.read() \n
		Returns the values of the EVM RMS bar graphs for the OFDM symbols in the measured slot. The results of the current,
		average and maximum bar graphs can be retrieved. There is one pair of EVM values per OFDM symbol, returned in the
		following order: <Reliability>, {<Low>, <High>}symbol 0, {<Low>, <High>}symbol 1, ... See also 'Square EVM'. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'READ:NRSub:MEASurement<Instance>:MEValuation:EVMagnitude:AVERage?', self.__class__.ResultData())

	def fetch(self) -> ResultData:
		"""SCPI: FETCh:NRSub:MEASurement<Instance>:MEValuation:EVMagnitude:AVERage \n
		Snippet: value: ResultData = driver.nrSubMeas.multiEval.evMagnitude.average.fetch() \n
		Returns the values of the EVM RMS bar graphs for the OFDM symbols in the measured slot. The results of the current,
		average and maximum bar graphs can be retrieved. There is one pair of EVM values per OFDM symbol, returned in the
		following order: <Reliability>, {<Low>, <High>}symbol 0, {<Low>, <High>}symbol 1, ... See also 'Square EVM'. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'FETCh:NRSub:MEASurement<Instance>:MEValuation:EVMagnitude:AVERage?', self.__class__.ResultData())

	# noinspection PyTypeChecker
	class CalculateStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: No parameter help available
			- Low: List[enums.ResultStatus2]: No parameter help available
			- High: List[enums.ResultStatus2]: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct('Low', DataType.EnumList, enums.ResultStatus2, False, True, 1),
			ArgStruct('High', DataType.EnumList, enums.ResultStatus2, False, True, 1)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Low: List[enums.ResultStatus2] = None
			self.High: List[enums.ResultStatus2] = None

	def calculate(self) -> CalculateStruct:
		"""SCPI: CALCulate:NRSub:MEASurement<Instance>:MEValuation:EVMagnitude:AVERage \n
		Snippet: value: CalculateStruct = driver.nrSubMeas.multiEval.evMagnitude.average.calculate() \n
		No command help available \n
			:return: structure: for return value, see the help for CalculateStruct structure arguments."""
		return self._core.io.query_struct(f'CALCulate:NRSub:MEASurement<Instance>:MEValuation:EVMagnitude:AVERage?', self.__class__.CalculateStruct())
