from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Fch:
	"""Fch commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("fch", core, parent)

	def get_freq_offset(self) -> int:
		"""SCPI: CONFigure:CDMA:SIGNaling<Instance>:LAYer:FCH:FOFFset \n
		Snippet: value: int = driver.configure.layer.fch.get_freq_offset() \n
		Sets the frame offset in the forward fundamental channel. Changing the frame offset immediately changes the traffic
		channel timing. \n
			:return: frame_offset: Range: 0 to 15
		"""
		response = self._core.io.query_str('CONFigure:CDMA:SIGNaling<Instance>:LAYer:FCH:FOFFset?')
		return Conversions.str_to_int(response)

	def set_freq_offset(self, frame_offset: int) -> None:
		"""SCPI: CONFigure:CDMA:SIGNaling<Instance>:LAYer:FCH:FOFFset \n
		Snippet: driver.configure.layer.fch.set_freq_offset(frame_offset = 1) \n
		Sets the frame offset in the forward fundamental channel. Changing the frame offset immediately changes the traffic
		channel timing. \n
			:param frame_offset: Range: 0 to 15
		"""
		param = Conversions.decimal_value_to_str(frame_offset)
		self._core.io.write(f'CONFigure:CDMA:SIGNaling<Instance>:LAYer:FCH:FOFFset {param}')
