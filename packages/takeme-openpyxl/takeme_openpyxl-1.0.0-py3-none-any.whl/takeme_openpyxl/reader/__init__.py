""" Excel Reader Module """

# 3rd Party Library
import openpyxl

class Reader:
    def __init__(self, filename: str, column_info: dict):
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
        self.__work_book = openpyxl.load_workbook(filename=filename)
        self.__work_sheet = self.__work_book.active
        self.__label_row = 1
        self.__current_row = 2
        self.__column_info = column_info

    def get_value(self, column_id: str, row_id: str=None) -> str:
        """
        Get the value of the specified column in the current row.

        [column_id]

        Starting from A, B, C, ...
        """
        if row_id is None:
            cell = '{}{}'.format(column_id, self.__current_row)
        else:
            cell = '{}{}'.format(column_id, row_id)
        value = self.__work_sheet[cell].value
        if value is None:
            return None
        return str(value).strip()

    def validate_labels(self) -> bool:
        """
        Gets the boolean value indicating whether the labels in the current Excel sheet is valid or not.
        """
        for key in self.__column_info:
            expected = self.__column_info[key]['label']
            actual = self.get_value(self.__column_info[key]['column'], self.__label_row)
            if actual is None or not actual.startswith(expected):
                print('Label: {} != {}'.format(expected, actual))
                return False
        return True

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

    @property
    def last_row(self) -> int:
        """
        Gets the last row index.
        """
        return self.__work_sheet.max_row

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
        Increments row index by 1.
        """
        self.__current_row += 1

    def close(self):
        """
        Close the current workbook.
        """
        self.__work_book.close()
