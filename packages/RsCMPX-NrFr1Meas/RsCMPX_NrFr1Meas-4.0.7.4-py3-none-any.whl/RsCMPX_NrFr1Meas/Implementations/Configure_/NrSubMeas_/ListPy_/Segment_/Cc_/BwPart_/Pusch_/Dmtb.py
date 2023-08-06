from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from .........Internal.Types import DataType
from .........Internal.StructBase import StructBase
from .........Internal.ArgStruct import ArgStruct
from .........Internal.ArgSingleList import ArgSingleList
from .........Internal.ArgSingle import ArgSingle
from ......... import enums
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dmtb:
	"""Dmtb commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dmtb", core, parent)

	def set(self, bwp: enums.BandwidthPart, config_type: int, add_position: int, max_length: int, sEGMent=repcap.SEGMent.Default, carrierComponent=repcap.CarrierComponent.Default) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:LIST:SEGMent<no>[:CC<cc>]:BWPart:PUSCh:DMTB \n
		Snippet: driver.configure.nrSubMeas.listPy.segment.cc.bwPart.pusch.dmtb.set(bwp = enums.BandwidthPart.BWP0, config_type = 1, add_position = 1, max_length = 1, sEGMent = repcap.SEGMent.Default, carrierComponent = repcap.CarrierComponent.Default) \n
		Configures the DM-RS for mapping type B. The settings apply to the <BWP> on carrier <cc> in segment <no>. \n
			:param bwp: No help available
			:param config_type: DM-RS setting 'dmrs-Type'.
			:param add_position: DM-RS setting 'dmrs-AdditionalPosition'.
			:param max_length: DM-RS setting 'maxLength'.
			:param sEGMent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cc')"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('bwp', bwp, DataType.Enum), ArgSingle('config_type', config_type, DataType.Integer), ArgSingle('add_position', add_position, DataType.Integer), ArgSingle('max_length', max_length, DataType.Integer))
		sEGMent_cmd_val = self._base.get_repcap_cmd_value(sEGMent, repcap.SEGMent)
		carrierComponent_cmd_val = self._base.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:LIST:SEGMent{sEGMent_cmd_val}:CC{carrierComponent_cmd_val}:BWPart:PUSCh:DMTB {param}'.rstrip())

	# noinspection PyTypeChecker
	class GetStruct(StructBase):
		"""Response structure. Fields: \n
			- Config_Type: int: DM-RS setting 'dmrs-Type'.
			- Add_Position: int: DM-RS setting 'dmrs-AdditionalPosition'.
			- Max_Length: int: DM-RS setting 'maxLength'."""
		__meta_args_list = [
			ArgStruct.scalar_int('Config_Type'),
			ArgStruct.scalar_int('Add_Position'),
			ArgStruct.scalar_int('Max_Length')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Config_Type: int = None
			self.Add_Position: int = None
			self.Max_Length: int = None

	def get(self, bwp: enums.BandwidthPart, sEGMent=repcap.SEGMent.Default, carrierComponent=repcap.CarrierComponent.Default) -> GetStruct:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:LIST:SEGMent<no>[:CC<cc>]:BWPart:PUSCh:DMTB \n
		Snippet: value: GetStruct = driver.configure.nrSubMeas.listPy.segment.cc.bwPart.pusch.dmtb.get(bwp = enums.BandwidthPart.BWP0, sEGMent = repcap.SEGMent.Default, carrierComponent = repcap.CarrierComponent.Default) \n
		Configures the DM-RS for mapping type B. The settings apply to the <BWP> on carrier <cc> in segment <no>. \n
			:param bwp: No help available
			:param sEGMent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cc')
			:return: structure: for return value, see the help for GetStruct structure arguments."""
		param = Conversions.enum_scalar_to_str(bwp, enums.BandwidthPart)
		sEGMent_cmd_val = self._base.get_repcap_cmd_value(sEGMent, repcap.SEGMent)
		carrierComponent_cmd_val = self._base.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		return self._core.io.query_struct(f'CONFigure:NRSub:MEASurement<Instance>:LIST:SEGMent{sEGMent_cmd_val}:CC{carrierComponent_cmd_val}:BWPart:PUSCh:DMTB? {param}', self.__class__.GetStruct())
