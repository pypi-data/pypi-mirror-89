""" Excel Writer Module """

# 3rd Party Library
import openpyxl

class Writer:
    def __init__(self, column_info: dict):
        """
        Constructor

        [column_info]

        {
            'column1': {
                'label': 'Label 1',
                'column': 'A'
            },

            'column2': {
                'label': 'Label 2',
                'column': 'B'
            },
        }
        """
        self.__work_book = openpyxl.Workbook()
        self.__work_sheet = self.__work_book.active
        self.__label_row = 1
        self.__current_row = 2
        self.__column_info = column_info

    def __write_labels(self):
        """
        Writes labels in the first row.
        """
        for key in self.__column_info.keys():
            cell = '{column}{row}'.format(
                column=self.__column_info[key]['column'],
                row=self.__label_row
            )
            self.__work_sheet[cell] = self.__column_info[key]['label']

    @property
    def current_row(self) -> int:
        """
        Gets the current row index.
        """
        return self.__current_row

    @property
    def label_row(self) -> int:
        """
        Gets the label row index.
        """
        return self.__label_row

    @current_row.setter
    def current_row(self, row: int):
        """
        Set the start row.
        """
        self.__current_row = row

    @label_row.setter
    def label_row(self, row: int):
        """
        Set the label row.
        """
        self.__label_row = row

    def next_row(self):
        """
        Increment row index by 1.
        """
        self.__current_row += 1

    def write(self, key: str, value: str) -> bool:
        """
        Writes to the specified cell.
        """
        try:
            cell = '{column}{row}'.format(
                column=self.__column_info[key]['column'],
                row=self.__current_row
            )
            self.__work_sheet[cell] = value
            return True
        except openpyxl.utils.exceptions.IllegalCharacterError as e:
            print(str(e))
        return False

    def flush(self, filename: str):
        """
        Saves in memory sheet to the specified file.
        """
        self.__write_labels()
        self.__work_book.save(filename)
        self.__work_book.close()
