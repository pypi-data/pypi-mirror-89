from typing import List

from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.Types import DataType
from ........Internal.StructBase import StructBase
from ........Internal.ArgStruct import ArgStruct
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Maximum:
	"""Maximum commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("maximum", core, parent)

	# noinspection PyTypeChecker
	class FetchStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: 'Reliability Indicator'
			- Rbw: enums.RbwB: Used resolution bandwidth (configured via limit settings) . K030: RBW 30 kHz K100: RBW 100 kHz M1: RBW 1 MHz PC1: RBW 1 % of channel BW PC2: RBW 2 % of channel BW
			- Power: List[float]: Comma-separated list of power results If the limit check is disabled for the area, INV is returned."""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_enum('Rbw', enums.RbwB),
			ArgStruct('Power', DataType.FloatList, None, False, True, 1)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Rbw: enums.RbwB = None
			self.Power: List[float] = None

	def fetch(self, area=repcap.Area.Default) -> FetchStruct:
		"""SCPI: FETCh:NRSub:MEASurement<Instance>:MEValuation:TRACe:SEMask:AREA<area>:NEGative:MAXimum \n
		Snippet: value: FetchStruct = driver.nrSubMeas.multiEval.trace.seMask.area.negative.maximum.fetch(area = repcap.Area.Default) \n
		Returns the measured power values for a single spectrum emission mask area with enabled limit check. The results of the
		current, average and maximum traces can be retrieved. The area is located below (NEGative) or above (POSitive) the
		carrier center frequency. See also 'Square Spectrum Emission Mask'. \n
			:param area: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Area')
			:return: structure: for return value, see the help for FetchStruct structure arguments."""
		area_cmd_val = self._base.get_repcap_cmd_value(area, repcap.Area)
		return self._core.io.query_struct(f'FETCh:NRSub:MEASurement<Instance>:MEValuation:TRACe:SEMask:AREA{area_cmd_val}:NEGative:MAXimum?', self.__class__.FetchStruct())
