from typing import List

from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Setting:
	"""Setting commands group definition. 4 total commands, 0 Sub-groups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("setting", core, parent)

	def get_catalog(self) -> List[str]:
		"""SCPI: [SOURce<HW>]:ILS:SETTing:CATalog \n
		Snippet: value: List[str] = driver.source.ils.setting.get_catalog() \n
		Queries the files with settings in the default directory. Listed are files with the file extension *.adf/*.ils/*.vor.
		Refer to 'Accessing Files in the Default or in a Specified Directory' for general information on file handling in the
		default and in a specific directory. \n
			:return: avionic_ils_cat_names: filename1,filename2,... Returns a string of filenames separated by commas.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:ILS:SETTing:CATalog?')
		return Conversions.str_to_str_list(response)

	def delete(self, filename: str) -> None:
		"""SCPI: [SOURce<HW>]:ILS:SETTing:DELete \n
		Snippet: driver.source.ils.setting.delete(filename = '1') \n
		Deletes the selected file from the default or the specified directory. Deleted are files with extension *.adf/*.ils/*.vor.
		Refer to 'Accessing Files in the Default or in a Specified Directory' for general information on file handling in the
		default and in a specific directory. \n
			:param filename: 'filename' Filename or complete file path; file extension can be omitted
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:ILS:SETTing:DELete {param}')

	def load(self, filename: str) -> None:
		"""SCPI: [SOURce<HW>]:ILS:SETTing:LOAD \n
		Snippet: driver.source.ils.setting.load(filename = '1') \n
		Loads the selected file from the default or the specified directory. Loaded are files with extension *.adf/*.ils/*.vor.
		Refer to 'Accessing Files in the Default or in a Specified Directory' for general information on file handling in the
		default and in a specific directory. \n
			:param filename: 'filename' Filename or complete file path; file extension can be omitted
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:ILS:SETTing:LOAD {param}')

	def set_store(self, filename: str) -> None:
		"""SCPI: [SOURce<HW>]:ILS:SETTing:STORe \n
		Snippet: driver.source.ils.setting.set_store(filename = '1') \n
		Saves the current settings into the selected file; the file extension (*.adf/*.ils/*.vor) is assigned automatically.
		Refer to 'Accessing Files in the Default or in a Specified Directory' for general information on file handling in the
		default and in a specific directory. \n
			:param filename: 'filename' Filename or complete file path
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:ILS:SETTing:STORe {param}')
