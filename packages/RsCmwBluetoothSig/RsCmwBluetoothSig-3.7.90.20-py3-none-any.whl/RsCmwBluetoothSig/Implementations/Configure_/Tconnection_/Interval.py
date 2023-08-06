from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Interval:
	"""Interval commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("interval", core, parent)

	def get_le_signaling(self) -> int:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:TCONnection:INTerval:LESignaling \n
		Snippet: value: int = driver.configure.tconnection.interval.get_le_signaling() \n
		No command help available \n
			:return: connection_interval: No help available
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:TCONnection:INTerval:LESignaling?')
		return Conversions.str_to_int(response)

	def set_le_signaling(self, connection_interval: int) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:TCONnection:INTerval:LESignaling \n
		Snippet: driver.configure.tconnection.interval.set_le_signaling(connection_interval = 1) \n
		No command help available \n
			:param connection_interval: No help available
		"""
		param = Conversions.decimal_value_to_str(connection_interval)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:TCONnection:INTerval:LESignaling {param}')
