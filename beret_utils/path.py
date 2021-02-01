import os


def get_path():

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def __path(file_name):
        file_name = os.path.expandvars(file_name)
        if file_name[0] != '/':
            return os.path.join(BASE_DIR, file_name)
        return file_name

    return __path
