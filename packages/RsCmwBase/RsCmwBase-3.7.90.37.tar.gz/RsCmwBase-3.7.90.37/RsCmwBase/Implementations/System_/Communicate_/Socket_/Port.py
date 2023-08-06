from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Port:
	"""Port commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("port", core, parent)

	def set(self, portnumber: int, socketInstance=repcap.SocketInstance.Default) -> None:
		"""SCPI: SYSTem:COMMunicate:SOCKet<inst>:PORT \n
		Snippet: driver.system.communicate.socket.port.set(portnumber = 1, socketInstance = repcap.SocketInstance.Default) \n
		Sets the data port number for direct socket communication. \n
			:param portnumber: No help available
			:param socketInstance: optional repeated capability selector. Default value: Inst1 (settable in the interface 'Socket')"""
		param = Conversions.decimal_value_to_str(portnumber)
		socketInstance_cmd_val = self._base.get_repcap_cmd_value(socketInstance, repcap.SocketInstance)
		self._core.io.write(f'SYSTem:COMMunicate:SOCKet{socketInstance_cmd_val}:PORT {param}')

	def get(self, socketInstance=repcap.SocketInstance.Default) -> int:
		"""SCPI: SYSTem:COMMunicate:SOCKet<inst>:PORT \n
		Snippet: value: int = driver.system.communicate.socket.port.get(socketInstance = repcap.SocketInstance.Default) \n
		Sets the data port number for direct socket communication. \n
			:param socketInstance: optional repeated capability selector. Default value: Inst1 (settable in the interface 'Socket')
			:return: portnumber: No help available"""
		socketInstance_cmd_val = self._base.get_repcap_cmd_value(socketInstance, repcap.SocketInstance)
		response = self._core.io.query_str(f'SYSTem:COMMunicate:SOCKet{socketInstance_cmd_val}:PORT?')
		return Conversions.str_to_int(response)
