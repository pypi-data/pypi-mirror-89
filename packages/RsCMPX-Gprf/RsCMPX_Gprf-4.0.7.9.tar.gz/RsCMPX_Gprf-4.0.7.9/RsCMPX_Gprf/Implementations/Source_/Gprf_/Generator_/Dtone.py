from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dtone:
	"""Dtone commands group definition. 3 total commands, 2 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dtone", core, parent)

	@property
	def ofrequency(self):
		"""ofrequency commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ofrequency'):
			from .Dtone_.Ofrequency import Ofrequency
			self._ofrequency = Ofrequency(self._core, self._base)
		return self._ofrequency

	@property
	def level(self):
		"""level commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_level'):
			from .Dtone_.Level import Level
			self._level = Level(self._core, self._base)
		return self._level

	def get_ratio(self) -> float:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:DTONe:RATio \n
		Snippet: value: float = driver.source.gprf.generator.dtone.get_ratio() \n
		Specifies the ratio in dB between the RMS levels of the two signals. \n
			:return: ratio: No help available
		"""
		response = self._core.io.query_str('SOURce:GPRF:GENerator<Instance>:DTONe:RATio?')
		return Conversions.str_to_float(response)

	def set_ratio(self, ratio: float) -> None:
		"""SCPI: SOURce:GPRF:GENerator<Instance>:DTONe:RATio \n
		Snippet: driver.source.gprf.generator.dtone.set_ratio(ratio = 1.0) \n
		Specifies the ratio in dB between the RMS levels of the two signals. \n
			:param ratio: No help available
		"""
		param = Conversions.decimal_value_to_str(ratio)
		self._core.io.write(f'SOURce:GPRF:GENerator<Instance>:DTONe:RATio {param}')

	def clone(self) -> 'Dtone':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Dtone(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
