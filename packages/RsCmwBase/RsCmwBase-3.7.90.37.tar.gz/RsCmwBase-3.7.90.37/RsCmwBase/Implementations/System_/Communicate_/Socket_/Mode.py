from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mode:
	"""Mode commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mode", core, parent)

	def set(self, protocolmode: enums.SocketProtocol, socketInstance=repcap.SocketInstance.Default) -> None:
		"""SCPI: SYSTem:COMMunicate:SOCKet<inst>:MODE \n
		Snippet: driver.system.communicate.socket.mode.set(protocolmode = enums.SocketProtocol.AGILent, socketInstance = repcap.SocketInstance.Default) \n
		Sets the protocol operation mode for direct socket communication. \n
			:param protocolmode: No help available
			:param socketInstance: optional repeated capability selector. Default value: Inst1 (settable in the interface 'Socket')"""
		param = Conversions.enum_scalar_to_str(protocolmode, enums.SocketProtocol)
		socketInstance_cmd_val = self._base.get_repcap_cmd_value(socketInstance, repcap.SocketInstance)
		self._core.io.write(f'SYSTem:COMMunicate:SOCKet{socketInstance_cmd_val}:MODE {param}')

	# noinspection PyTypeChecker
	def get(self, socketInstance=repcap.SocketInstance.Default) -> enums.SocketProtocol:
		"""SCPI: SYSTem:COMMunicate:SOCKet<inst>:MODE \n
		Snippet: value: enums.SocketProtocol = driver.system.communicate.socket.mode.get(socketInstance = repcap.SocketInstance.Default) \n
		Sets the protocol operation mode for direct socket communication. \n
			:param socketInstance: optional repeated capability selector. Default value: Inst1 (settable in the interface 'Socket')
			:return: protocolmode: No help available"""
		socketInstance_cmd_val = self._base.get_repcap_cmd_value(socketInstance, repcap.SocketInstance)
		response = self._core.io.query_str(f'SYSTem:COMMunicate:SOCKet{socketInstance_cmd_val}:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.SocketProtocol)
