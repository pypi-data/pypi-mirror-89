from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Modulation:
	"""Modulation commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("modulation", core, parent)

	# noinspection PyTypeChecker
	class ModulationStruct(StructBase):
		"""Structure for setting input parameters. Fields: \n
			- Mod_Statistics: int: Statistical length in slots
			- Mod_Enable: bool: Enable or disable the measurement of modulation results ON: Modulation results are measured according to the other enable flags in this command. Modulation results for which there is no explicit enable flag are also measured (e.g. I/Q offset, frequency error and timing error) . OFF: No modulation results at all are measured. The other enable flags in this command are ignored.
			- Evmenable: bool: Enable or disable measurement of EVM
			- Mag_Error_Enable: bool: Enable or disable measurement of magnitude error
			- Phase_Err_Enable: bool: Enable or disable measurement of phase error
			- Ib_Eenable: bool: Enable or disable measurement of inband emissions
			- Eq_Sp_Flat_Enable: bool: Enable or disable measurement of equalizer spectrum flatness results"""
		__meta_args_list = [
			ArgStruct.scalar_int('Mod_Statistics'),
			ArgStruct.scalar_bool('Mod_Enable'),
			ArgStruct.scalar_bool('Evmenable'),
			ArgStruct.scalar_bool('Mag_Error_Enable'),
			ArgStruct.scalar_bool('Phase_Err_Enable'),
			ArgStruct.scalar_bool('Ib_Eenable'),
			ArgStruct.scalar_bool('Eq_Sp_Flat_Enable')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Mod_Statistics: int = None
			self.Mod_Enable: bool = None
			self.Evmenable: bool = None
			self.Mag_Error_Enable: bool = None
			self.Phase_Err_Enable: bool = None
			self.Ib_Eenable: bool = None
			self.Eq_Sp_Flat_Enable: bool = None

	def set(self, structure: ModulationStruct, sEGMent=repcap.SEGMent.Default) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIST:SEGMent<no>:MODulation \n
		Snippet: driver.configure.nrSubMeas.multiEval.listPy.segment.modulation.set(value = [PROPERTY_STRUCT_NAME](), sEGMent = repcap.SEGMent.Default) \n
		Defines settings for modulation measurements in list mode for segment <no>. \n
			:param structure: for set value, see the help for ModulationStruct structure arguments.
			:param sEGMent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')"""
		sEGMent_cmd_val = self._base.get_repcap_cmd_value(sEGMent, repcap.SEGMent)
		self._core.io.write_struct(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIST:SEGMent{sEGMent_cmd_val}:MODulation', structure)

	def get(self, sEGMent=repcap.SEGMent.Default) -> ModulationStruct:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIST:SEGMent<no>:MODulation \n
		Snippet: value: ModulationStruct = driver.configure.nrSubMeas.multiEval.listPy.segment.modulation.get(sEGMent = repcap.SEGMent.Default) \n
		Defines settings for modulation measurements in list mode for segment <no>. \n
			:param sEGMent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')
			:return: structure: for return value, see the help for ModulationStruct structure arguments."""
		sEGMent_cmd_val = self._base.get_repcap_cmd_value(sEGMent, repcap.SEGMent)
		return self._core.io.query_struct(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIST:SEGMent{sEGMent_cmd_val}:MODulation?', self.__class__.ModulationStruct())
