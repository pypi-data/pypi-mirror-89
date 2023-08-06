from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class State:
	"""State commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("state", core, parent)

	def set(self, control: bool) -> None:
		"""SCPI: SOURce:DATA:CONTrol:UDP:STATe \n
		Snippet: driver.source.data.control.udp.state.set(control = False) \n
		No command help available \n
			:param control: No help available
		"""
		param = Conversions.bool_to_str(control)
		self._core.io.write_with_opc(f'SOURce:DATA:CONTrol:UDP:STATe {param}')

	# noinspection PyTypeChecker
	def get(self) -> enums.DauState:
		"""SCPI: SOURce:DATA:CONTrol:UDP:STATe \n
		Snippet: value: enums.DauState = driver.source.data.control.udp.state.get() \n
		No command help available \n
			:return: state: No help available"""
		response = self._core.io.query_str_with_opc(f'SOURce:DATA:CONTrol:UDP:STATe?')
		return Conversions.str_to_scalar_enum(response, enums.DauState)
