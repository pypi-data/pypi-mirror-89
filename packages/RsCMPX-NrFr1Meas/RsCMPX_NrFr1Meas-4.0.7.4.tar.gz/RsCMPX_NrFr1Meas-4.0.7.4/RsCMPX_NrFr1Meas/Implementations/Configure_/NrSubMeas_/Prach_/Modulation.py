from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Modulation:
	"""Modulation commands group definition. 3 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("modulation", core, parent)

	@property
	def ewLength(self):
		"""ewLength commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_ewLength'):
			from .Modulation_.EwLength import EwLength
			self._ewLength = EwLength(self._core, self._base)
		return self._ewLength

	# noinspection PyTypeChecker
	def get_ew_position(self) -> enums.LowHigh:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:PRACh:MODulation:EWPosition \n
		Snippet: value: enums.LowHigh = driver.configure.nrSubMeas.prach.modulation.get_ew_position() \n
		Specifies the position of the EVM window used for calculation of the trace results. \n
			:return: evmwindow_pos: No help available
		"""
		response = self._core.io.query_str('CONFigure:NRSub:MEASurement<Instance>:PRACh:MODulation:EWPosition?')
		return Conversions.str_to_scalar_enum(response, enums.LowHigh)

	def set_ew_position(self, evmwindow_pos: enums.LowHigh) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:PRACh:MODulation:EWPosition \n
		Snippet: driver.configure.nrSubMeas.prach.modulation.set_ew_position(evmwindow_pos = enums.LowHigh.HIGH) \n
		Specifies the position of the EVM window used for calculation of the trace results. \n
			:param evmwindow_pos: No help available
		"""
		param = Conversions.enum_scalar_to_str(evmwindow_pos, enums.LowHigh)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:PRACh:MODulation:EWPosition {param}')

	def clone(self) -> 'Modulation':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Modulation(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
