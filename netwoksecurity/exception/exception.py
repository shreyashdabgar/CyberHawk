import sys

def why_error(error, error_details):
    _, _, exc_tb = sys.exc_info()  # Get the traceback info
    file_name = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno
    return f"Error in file: {file_name} at line {line_number} - {str(error)}"

class CustomException(Exception):
    def __init__(self, error):  # Only pass `error`, no need for `error_details`
        super().__init__(error)
        self.error = why_error(error, sys.exc_info())  # Fetch traceback inside

    def __str__(self):
        return self.error
