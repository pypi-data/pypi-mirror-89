from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class IpSec:
	"""IpSec commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ipSec", core, parent)

	# noinspection PyTypeChecker
	def get_ialgorithm(self) -> enums.IpSecIAlgorithm:
		"""SCPI: CONFigure:DATA:CONTrol:IMS:UAUThentic:IPSec:IALGorithm \n
		Snippet: value: enums.IpSecIAlgorithm = driver.configure.data.control.ims.uauthentication.ipSec.get_ialgorithm() \n
		No command help available \n
			:return: ip_seci_alg: No help available
		"""
		response = self._core.io.query_str('CONFigure:DATA:CONTrol:IMS:UAUThentic:IPSec:IALGorithm?')
		return Conversions.str_to_scalar_enum(response, enums.IpSecIAlgorithm)

	def set_ialgorithm(self, ip_seci_alg: enums.IpSecIAlgorithm) -> None:
		"""SCPI: CONFigure:DATA:CONTrol:IMS:UAUThentic:IPSec:IALGorithm \n
		Snippet: driver.configure.data.control.ims.uauthentication.ipSec.set_ialgorithm(ip_seci_alg = enums.IpSecIAlgorithm.AUTO) \n
		No command help available \n
			:param ip_seci_alg: No help available
		"""
		param = Conversions.enum_scalar_to_str(ip_seci_alg, enums.IpSecIAlgorithm)
		self._core.io.write(f'CONFigure:DATA:CONTrol:IMS:UAUThentic:IPSec:IALGorithm {param}')

	# noinspection PyTypeChecker
	def get_ealgorithm(self) -> enums.IpSecEAlgorithm:
		"""SCPI: CONFigure:DATA:CONTrol:IMS:UAUThentic:IPSec:EALGorithm \n
		Snippet: value: enums.IpSecEAlgorithm = driver.configure.data.control.ims.uauthentication.ipSec.get_ealgorithm() \n
		No command help available \n
			:return: ip_sece_alg: No help available
		"""
		response = self._core.io.query_str('CONFigure:DATA:CONTrol:IMS:UAUThentic:IPSec:EALGorithm?')
		return Conversions.str_to_scalar_enum(response, enums.IpSecEAlgorithm)

	def set_ealgorithm(self, ip_sece_alg: enums.IpSecEAlgorithm) -> None:
		"""SCPI: CONFigure:DATA:CONTrol:IMS:UAUThentic:IPSec:EALGorithm \n
		Snippet: driver.configure.data.control.ims.uauthentication.ipSec.set_ealgorithm(ip_sece_alg = enums.IpSecEAlgorithm.AES) \n
		No command help available \n
			:param ip_sece_alg: No help available
		"""
		param = Conversions.enum_scalar_to_str(ip_sece_alg, enums.IpSecEAlgorithm)
		self._core.io.write(f'CONFigure:DATA:CONTrol:IMS:UAUThentic:IPSec:EALGorithm {param}')

	def get_value(self) -> bool:
		"""SCPI: CONFigure:DATA:CONTrol:IMS:UAUThentic:IPSec \n
		Snippet: value: bool = driver.configure.data.control.ims.uauthentication.ipSec.get_value() \n
		No command help available \n
			:return: ip_sec: No help available
		"""
		response = self._core.io.query_str('CONFigure:DATA:CONTrol:IMS:UAUThentic:IPSec?')
		return Conversions.str_to_bool(response)

	def set_value(self, ip_sec: bool) -> None:
		"""SCPI: CONFigure:DATA:CONTrol:IMS:UAUThentic:IPSec \n
		Snippet: driver.configure.data.control.ims.uauthentication.ipSec.set_value(ip_sec = False) \n
		No command help available \n
			:param ip_sec: No help available
		"""
		param = Conversions.bool_to_str(ip_sec)
		self._core.io.write(f'CONFigure:DATA:CONTrol:IMS:UAUThentic:IPSec {param}')
