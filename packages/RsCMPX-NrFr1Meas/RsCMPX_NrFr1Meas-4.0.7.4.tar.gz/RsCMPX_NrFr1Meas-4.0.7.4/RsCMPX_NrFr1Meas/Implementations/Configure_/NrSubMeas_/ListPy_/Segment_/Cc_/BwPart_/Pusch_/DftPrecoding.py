from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from .........Internal.Types import DataType
from .........Internal.ArgSingleList import ArgSingleList
from .........Internal.ArgSingle import ArgSingle
from ......... import enums
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DftPrecoding:
	"""DftPrecoding commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dftPrecoding", core, parent)

	def set(self, bwp: enums.BandwidthPart, dft_precodingcoding: bool, sEGMent=repcap.SEGMent.Default, carrierComponent=repcap.CarrierComponent.Default) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:LIST:SEGMent<no>[:CC<cc>]:BWPart:PUSCh:DFTPrecoding \n
		Snippet: driver.configure.nrSubMeas.listPy.segment.cc.bwPart.pusch.dftPrecoding.set(bwp = enums.BandwidthPart.BWP0, dft_precodingcoding = False, sEGMent = repcap.SEGMent.Default, carrierComponent = repcap.CarrierComponent.Default) \n
		Specifies whether the <BWP> on carrier <cc> in segment <no> uses a transform precoding function. \n
			:param bwp: No help available
			:param dft_precodingcoding: OFF: No transform precoding ON: With transform precoding
			:param sEGMent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cc')"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('bwp', bwp, DataType.Enum), ArgSingle('dft_precodingcoding', dft_precodingcoding, DataType.Boolean))
		sEGMent_cmd_val = self._base.get_repcap_cmd_value(sEGMent, repcap.SEGMent)
		carrierComponent_cmd_val = self._base.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:LIST:SEGMent{sEGMent_cmd_val}:CC{carrierComponent_cmd_val}:BWPart:PUSCh:DFTPrecoding {param}'.rstrip())

	def get(self, bwp: enums.BandwidthPart, sEGMent=repcap.SEGMent.Default, carrierComponent=repcap.CarrierComponent.Default) -> bool:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:LIST:SEGMent<no>[:CC<cc>]:BWPart:PUSCh:DFTPrecoding \n
		Snippet: value: bool = driver.configure.nrSubMeas.listPy.segment.cc.bwPart.pusch.dftPrecoding.get(bwp = enums.BandwidthPart.BWP0, sEGMent = repcap.SEGMent.Default, carrierComponent = repcap.CarrierComponent.Default) \n
		Specifies whether the <BWP> on carrier <cc> in segment <no> uses a transform precoding function. \n
			:param bwp: No help available
			:param sEGMent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cc')
			:return: dft_precodingcoding: OFF: No transform precoding ON: With transform precoding"""
		param = Conversions.enum_scalar_to_str(bwp, enums.BandwidthPart)
		sEGMent_cmd_val = self._base.get_repcap_cmd_value(sEGMent, repcap.SEGMent)
		carrierComponent_cmd_val = self._base.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		response = self._core.io.query_str(f'CONFigure:NRSub:MEASurement<Instance>:LIST:SEGMent{sEGMent_cmd_val}:CC{carrierComponent_cmd_val}:BWPart:PUSCh:DFTPrecoding? {param}')
		return Conversions.str_to_bool(response)
