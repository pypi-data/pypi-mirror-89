from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Step:
	"""Step commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("step", core, parent)

	def set_action(self, pcontrol: enums.PowerControl) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PCONtrol:STEP:ACTion \n
		Snippet: driver.configure.connection.powerControl.step.set_action(pcontrol = enums.PowerControl.DOWN) \n
		Sends a command to the EUT to increase/decrease power. \n
			:param pcontrol: UP | DOWN | MAX One step up, one step down, command to maximum EUT power
		"""
		param = Conversions.enum_scalar_to_str(pcontrol, enums.PowerControl)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PCONtrol:STEP:ACTion {param}')
