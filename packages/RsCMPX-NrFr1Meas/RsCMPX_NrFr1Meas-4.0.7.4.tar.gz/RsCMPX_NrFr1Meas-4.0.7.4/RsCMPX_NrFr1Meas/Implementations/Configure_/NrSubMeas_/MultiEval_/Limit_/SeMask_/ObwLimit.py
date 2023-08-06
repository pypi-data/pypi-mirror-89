from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ObwLimit:
	"""ObwLimit commands group definition. 2 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("obwLimit", core, parent)

	@property
	def cbandwidth(self):
		"""cbandwidth commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cbandwidth'):
			from .ObwLimit_.Cbandwidth import Cbandwidth
			self._cbandwidth = Cbandwidth(self._core, self._base)
		return self._cbandwidth

	def get_endc(self) -> float or bool:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:SEMask:OBWLimit:ENDC \n
		Snippet: value: float or bool = driver.configure.nrSubMeas.multiEval.limit.seMask.obwLimit.get_endc() \n
		Defines an upper limit for the occupied bandwidth, for EN-DC measurements. \n
			:return: obwlimit: No help available
		"""
		response = self._core.io.query_str('CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:SEMask:OBWLimit:ENDC?')
		return Conversions.str_to_float_or_bool(response)

	def set_endc(self, obwlimit: float or bool) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:SEMask:OBWLimit:ENDC \n
		Snippet: driver.configure.nrSubMeas.multiEval.limit.seMask.obwLimit.set_endc(obwlimit = 1.0) \n
		Defines an upper limit for the occupied bandwidth, for EN-DC measurements. \n
			:param obwlimit: No help available
		"""
		param = Conversions.decimal_or_bool_value_to_str(obwlimit)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:SEMask:OBWLimit:ENDC {param}')

	def clone(self) -> 'ObwLimit':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ObwLimit(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
