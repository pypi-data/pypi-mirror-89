from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Result:
	"""Result commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("result", core, parent)

	def get_ts_mask(self) -> bool:
		"""SCPI: CONFigure:UWB:MEASurement<Instance>:MEValuation:RESult:TSMask \n
		Snippet: value: bool = driver.configure.uwbMeas.multiEval.result.get_ts_mask() \n
		Enables or disables the evaluation of results in the multi-evaluation measurement. \n
			:return: enable: OFF: Do not evaluate results ON: Evaluate results
		"""
		response = self._core.io.query_str('CONFigure:UWB:MEASurement<Instance>:MEValuation:RESult:TSMask?')
		return Conversions.str_to_bool(response)

	def set_ts_mask(self, enable: bool) -> None:
		"""SCPI: CONFigure:UWB:MEASurement<Instance>:MEValuation:RESult:TSMask \n
		Snippet: driver.configure.uwbMeas.multiEval.result.set_ts_mask(enable = False) \n
		Enables or disables the evaluation of results in the multi-evaluation measurement. \n
			:param enable: OFF: Do not evaluate results ON: Evaluate results
		"""
		param = Conversions.bool_to_str(enable)
		self._core.io.write(f'CONFigure:UWB:MEASurement<Instance>:MEValuation:RESult:TSMask {param}')

	def get_power_vs_time(self) -> bool:
		"""SCPI: CONFigure:UWB:MEASurement<Instance>:MEValuation:RESult:PVTime \n
		Snippet: value: bool = driver.configure.uwbMeas.multiEval.result.get_power_vs_time() \n
		Enables or disables the evaluation of results in the multi-evaluation measurement. \n
			:return: enable: OFF: Do not evaluate results ON: Evaluate results
		"""
		response = self._core.io.query_str('CONFigure:UWB:MEASurement<Instance>:MEValuation:RESult:PVTime?')
		return Conversions.str_to_bool(response)

	def set_power_vs_time(self, enable: bool) -> None:
		"""SCPI: CONFigure:UWB:MEASurement<Instance>:MEValuation:RESult:PVTime \n
		Snippet: driver.configure.uwbMeas.multiEval.result.set_power_vs_time(enable = False) \n
		Enables or disables the evaluation of results in the multi-evaluation measurement. \n
			:param enable: OFF: Do not evaluate results ON: Evaluate results
		"""
		param = Conversions.bool_to_str(enable)
		self._core.io.write(f'CONFigure:UWB:MEASurement<Instance>:MEValuation:RESult:PVTime {param}')

	def get_emodulation(self) -> bool:
		"""SCPI: CONFigure:UWB:MEASurement<Instance>:MEValuation:RESult:EMODulation \n
		Snippet: value: bool = driver.configure.uwbMeas.multiEval.result.get_emodulation() \n
		Enables or disables the evaluation of results in the multi-evaluation measurement. \n
			:return: enable: OFF: Do not evaluate results ON: Evaluate results
		"""
		response = self._core.io.query_str('CONFigure:UWB:MEASurement<Instance>:MEValuation:RESult:EMODulation?')
		return Conversions.str_to_bool(response)

	def set_emodulation(self, enable: bool) -> None:
		"""SCPI: CONFigure:UWB:MEASurement<Instance>:MEValuation:RESult:EMODulation \n
		Snippet: driver.configure.uwbMeas.multiEval.result.set_emodulation(enable = False) \n
		Enables or disables the evaluation of results in the multi-evaluation measurement. \n
			:param enable: OFF: Do not evaluate results ON: Evaluate results
		"""
		param = Conversions.bool_to_str(enable)
		self._core.io.write(f'CONFigure:UWB:MEASurement<Instance>:MEValuation:RESult:EMODulation {param}')
