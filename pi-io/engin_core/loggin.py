import os
from os import path
import errno

def log_text(file_path, text):
    with open('{}/log.txt'.format(file_path), "a") as file:
        file.writelines([text, ])
        file.close()
    return


def push_log(file_path, file_name, text):
    current_path = "{}/push_log".format(path.dirname(file_path))
    if not path.exists(current_path):
        try:
            os.makedirs(current_path)
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    _file = '{}/{}.txt'.format(file_path, file_name)
    with open(_file, "a+") as file:
        file.writelines([text, "\n"])
        file.close()
    return
