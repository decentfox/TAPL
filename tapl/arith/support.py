class FileInfo:
    def __repr__(self):
        return '<Unknown file and line>:'


class Info(FileInfo):
    """
    An element of the type info represents a "file position": a
    file name, line number, and character position within the line.
    Used for printing error messages.
    """

    def __init__(self, file_name, line_num, char_pos):
        self._file_name = file_name
        self._line_num = line_num
        self._char_pos = char_pos

    def __repr__(self):
        """
        In the text of the book, file positions in error messages are replaced
        with the string "Error:" *)
        """
        return f'{self._file_name}: {self._line_num}.{self._char_pos}:'


dummy_info = FileInfo()
