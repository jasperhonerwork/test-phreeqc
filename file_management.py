import os.path
import ctypes
import sys

class Input_file:
    """This wil create the input file needed for phreeqc to run"""
    def __init__(self, model_id):
        self.file_to_read = "input/Start_sheet.in"
        self.file_to_write = "input/phreeqc_de_punt_input.in"
        self.model = model_id
        self.using_file = ''
        self.db_data = ''

    def open_input_file(self):
        """Making the actual file"""
        file = open(self.file_to_write, "a")
        return file

    def start_input_file(self):
        """Putting in the text to start file"""
        if self.model == 1:
            file = open(self.file_to_read, "r")
            data = file.read()
            file.close()

            with open(self.file_to_write, "a") as file:
                file.write(data)
        else:
            ctypes.windll.user32.MessageBoxW(0, "No data available for this mode", "No data found", 1)

    def writing_to_input_file(self):
        """Writing al the values to the input file"""
        file = open(self.file_to_write, "a")
        if self.db_data != '':
            data = self.db_data
            if data == 'None':
                file.write('')
            else:
                file.write(f"{self.db_data}")
        else:
            file.write('')

    def close_input_file(self):
        """deleting the file after it ran"""
        open(self.file_to_write, 'w').close()