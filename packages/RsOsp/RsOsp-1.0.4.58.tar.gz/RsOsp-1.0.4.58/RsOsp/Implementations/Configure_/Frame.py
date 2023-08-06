from typing import List

from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Frame:
	"""Frame commands group definition. 11 total commands, 3 Sub-groups, 5 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("frame", core, parent)

	@property
	def define(self):
		"""define commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_define'):
			from .Frame_.Define import Define
			self._define = Define(self._core, self._base)
		return self._define

	@property
	def insert(self):
		"""insert commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_insert'):
			from .Frame_.Insert import Insert
			self._insert = Insert(self._core, self._base)
		return self._insert

	@property
	def importPy(self):
		"""importPy commands group. 1 Sub-classes, 3 commands."""
		if not hasattr(self, '_importPy'):
			from .Frame_.ImportPy import ImportPy
			self._importPy = ImportPy(self._core, self._base)
		return self._importPy

	def get_catalog(self) -> List[str]:
		"""SCPI: CONFigure:FRAMe:CATalog \n
		Snippet: value: List[str] = driver.configure.frame.get_catalog() \n
		Returns a comma-separated configuration list of all 'frames' (switch units in single state or in a master-slaves setup)
		that are stored in the (master) switch unit's volatile memory. Use the command method RsOsp.Configure.Frame.export to
		save the configuration list to the switch unit's compact flash memory. The configuration is also saved automatically to
		the flash memory during the shutdown procedure and loaded at startup into the volatile memory. \n
			:return: frame_info_list: The information on each frame comprises the following information: Fxx|Address|Status|TransmittedHostname. In detail:
				- Fxx: Frame ID, where F01 is the master, F02 is the 1st slave, F03 is the 2nd slave, and so on.
				- Address: IP address or configured hostname, as specified by CONF:FRAM:DEF or in the user interface ('WebGUI') at 'Configuration' 'Master-Slave' 'Edit Slave' 'Address:'No address is defined for the master switch unit (F01) . For the master, the query returns an empty field in the response string.For master and slave switch units that are in 'Virtual Mode', the query returns Not available (virtual frame) in this field.
				- Status: For example, Single, Master, or in the slaves: Connected, Broken (slave not available) , Refused (when trying to configure another master as a slave) .
				- TransmittedHostname: Hostname, if available, or Not available (virtual frame) .If no address or hostname is defined for an existing frame, for example due to an incomplete definition in the user interface ('WebGUI') , the query returns an empty field. For example, the response can be 'F02||Invalid address|'."""
		response = self._core.io.query_str('CONFigure:FRAMe:CATalog?')
		return Conversions.str_to_str_list(response, clear_one_empty_item=True)

	def set_add(self, configured_address: str) -> None:
		"""SCPI: CONFigure:FRAMe:ADD \n
		Snippet: driver.configure.frame.set_add(configured_address = '1') \n
		Adds an entry for a slave switch unit at the end of the list of frame IDs in the switch unit’s internal volatile memory.
		The command assigns the next available frame ID to the new slave. \n
			:param configured_address: Specifies the IP address or the hostname of the slave switch unit that you want to add.
		"""
		param = Conversions.value_to_quoted_str(configured_address)
		self._core.io.write(f'CONFigure:FRAMe:ADD {param}')

	def delete(self, frame_id: str) -> None:
		"""SCPI: CONFigure:FRAMe:DELete \n
		Snippet: driver.configure.frame.delete(frame_id = r1) \n
		Deletes a selected slave-unit definition from the switch unit’s internal volatile memory. Use the command method RsOsp.
		Configure.Frame.catalog to query the existing slave definitions. When you delete a slave switch unit from an existing
		list of slaves, all following frame IDs of slaves listed after the deleted slave are automatically renumbered
		(decremented by 1) . For example, if you delete a slave with frame ID F03, the next remaining slave F04 becomes slave F03,
		the next remaining slave F05 becomes slave F04, etc. Note that the deletion of a slave can impact your path definitions,
		even if the deleted frame was not used for any path definitions. For example, consider a setup with 4 slave switch units
		(F02 to F05) . If you delete the 2nd slave (F03) , a path that includes modules in the previous 3rd slave (F04) now
		addresses the new 3rd slave, which previously was the 4th slave (F05) . This change can destroy the functionality of your
		path definitions - or it can be intentional. \n
			:param frame_id: Selects the frame ID Fxx of the slave switch unit you wish to delete, starting with F02 (note that the 1st slave is the 2nd frame) . Use the frame ID without quotation marks.
		"""
		param = Conversions.value_to_str(frame_id)
		self._core.io.write(f'CONFigure:FRAMe:DELete {param}')

	def delete_all(self) -> None:
		"""SCPI: CONFigure:FRAMe:DELete:ALL \n
		Snippet: driver.configure.frame.delete_all() \n
		Deletes all currently defined slave switch units from the master switch unit’s internal volatile memory.
		Before you delete all slave unit definitions, we recommend using the command method RsOsp.Configure.Frame.catalog to
		query all currently defined slave units. \n
		"""
		self._core.io.write(f'CONFigure:FRAMe:DELete:ALL')

	def delete_all_with_opc(self) -> None:
		"""SCPI: CONFigure:FRAMe:DELete:ALL \n
		Snippet: driver.configure.frame.delete_all_with_opc() \n
		Deletes all currently defined slave switch units from the master switch unit’s internal volatile memory.
		Before you delete all slave unit definitions, we recommend using the command method RsOsp.Configure.Frame.catalog to
		query all currently defined slave units. \n
		Same as delete_all, but waits for the operation to complete before continuing further. Use the RsOsp.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'CONFigure:FRAMe:DELete:ALL')

	def export(self, slave_configuration_file_name_to_export: str) -> None:
		"""SCPI: CONFigure:FRAMe:EXPort \n
		Snippet: driver.configure.frame.export(slave_configuration_file_name_to_export = '1') \n
		Stores the currently defined slaves configuration as a nonvolatile file in the compact flash memory of your master switch
		unit. For configuring slaves, see method RsOsp.Configure.Frame.Define.set. All slave configuration filenames have the
		extension '.slaves'. Do not enter the extension when specifying a filename. A filename query does not return the
		extension. For example, when you save the slave configuration file 'subunit1', it is saved as 'subunit1.slaves'. A query
		returns this filename as 'subunit1', only. \n
			:param slave_configuration_file_name_to_export: String parameter to specify the name of the file to be stored.
		"""
		param = Conversions.value_to_quoted_str(slave_configuration_file_name_to_export)
		self._core.io.write(f'CONFigure:FRAMe:EXPort {param}')
