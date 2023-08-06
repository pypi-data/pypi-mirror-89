from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.Types import DataType
from ....Internal.ArgSingleList import ArgSingleList
from ....Internal.ArgSingle import ArgSingle
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ImportPy:
	"""ImportPy commands group definition. 4 total commands, 1 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("importPy", core, parent)

	@property
	def catalog(self):
		"""catalog commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_catalog'):
			from .ImportPy_.Catalog import Catalog
			self._catalog = Catalog(self._core, self._base)
		return self._catalog

	def delete(self, path_configuration_file_to_delete: str) -> None:
		"""SCPI: ROUTe:PATH:IMPort:DELete \n
		Snippet: driver.route.path.importPy.delete(path_configuration_file_to_delete = '1') \n
		Risk of losing settings: Removes the specified path configuration file from the switch unit’s compact flash memory. All
		path filenames have the extension '.path'. Do not enter the extension when specifying a filename. A filename query does
		not return the extension. For example, when you save the path file 'gen-pa_1', it is saved as 'gen-pa_1.path'. A query
		returns this filename as 'gen-pa_1', only. If the specified file does not exist, a SCPI error is generated. You can query
		the error with SYST:ERR?. The result can be, for example: -200,'Execution error;File does not exist.
		,ROUTe:PATH:IMPort:DELete ''Path5''' The command MMEMory:DELete is equivalent with method RsOsp.Route.Path.ImportPy.
		delete. \n
			:param path_configuration_file_to_delete: String parameter to specify the name of the file to be deleted.
		"""
		param = Conversions.value_to_quoted_str(path_configuration_file_to_delete)
		self._core.io.write(f'ROUTe:PATH:IMPort:DELete {param}')

	def delete_all(self, path_information: str = None) -> None:
		"""SCPI: ROUTe:PATH:IMPort:DELete:ALL \n
		Snippet: driver.route.path.importPy.delete_all(path_information = '1') \n
		Risk of losing settings: Removes all path configuration files from the switch unit’s compact flash memory. Before you
		delete all path configuration files, we recommend using the command method RsOsp.Route.Path.ImportPy.Catalog.
		get_ to query all currently defined path configuration files. \n
			:param path_information: No help available
		"""
		param = ''
		if path_information:
			param = Conversions.value_to_quoted_str(path_information)
		self._core.io.write(f'ROUTe:PATH:IMPort:DELete:ALL {param}'.strip())

	def set(self, import_filename: str, replace_or_keep: enums.ReplaceOrKeep = None) -> None:
		"""SCPI: ROUTe:PATH:IMPort \n
		Snippet: driver.route.path.importPy.set(import_filename = '1', replace_or_keep = enums.ReplaceOrKeep.KEEP) \n
		Loads a set of path configurations from a file on the compact flash memory into the switch unit’s internal volatile
		memory. All path filenames have the extension '.path'. Do not enter the extension when specifying a filename. A filename
		query does not return the extension. For example, when you save the path file 'gen-pa_1', it is saved as 'gen-pa_1.path'.
		A query returns this filename as 'gen-pa_1', only. If the specified file does not exist, a SCPI error is generated. You
		can query the error with SYST:ERR?. The result can be, for example: -200,'Execution error;Restoring device from file
		/opt/ospn/exportPath5.path failed,ROUTe:PATH:IMPort ''Path5''' The legacy command MMEM:LOAD:STATe is equivalent with
		method RsOsp.Route.Path.ImportPy.set. However, MMEM:LOAD:STATe does not support the parameter <import mode>, which is
		used with method RsOsp.Route.Path.ImportPy.set to specify keeping or replacing the path definitions (see below) . Risk of
		losing settings: Note that this command overwrites all current path definitions in the switch unit’s internal volatile
		memory with the path definitions in the loaded file. To avoid losing current path definitions, consider saving these
		definitions by method RsOsp.Route.Path.export, before you send the import command. \n
			:param import_filename: String parameter to specify the name of the file to be loaded.
			:param replace_or_keep: Optional parameter that decides about keeping or replacing the currently existing path definitions, see 'Import Paths'. If the parameter is missing, the import is performed in REPLace mode.
				- KEEP: Amends the current path definitions in the switch unit's internal memory with the imported path definitions. However, if you import paths that have the same names as existing paths in the memory, the imported paths overwrite the existing paths, even if you have specified to KEEP them.
				- REPLace: Discards the current path definitions in the switch unit's internal memory and replaces them with the imported path definitions."""
		param = ArgSingleList().compose_cmd_string(ArgSingle('import_filename', import_filename, DataType.String), ArgSingle('replace_or_keep', replace_or_keep, DataType.Enum, True))
		self._core.io.write(f'ROUTe:PATH:IMPort {param}'.rstrip())
