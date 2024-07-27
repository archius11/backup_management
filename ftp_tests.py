import os
import uuid
from ftplib import error_perm

import ftp as ftp_manager
from config import FTP_WRITER, FTP_READER, FTP_FULL_READER


uuid_string = str(uuid.uuid4())
ftp_test_file_name = f'/test/{uuid_string}.txt'   # unique filename in the session
local_test_file_name = f'files/{uuid_string}.txt'


def test_read_list(ftp, must_have_permissions):
    try:
        dirs = ftp.get_list('/')
        dirs = sorted(list(dirs.keys()))
    except Exception as e:
        exception = e
        dirs = []
    else:
        exception = None

    if must_have_permissions:
        assert exception is None and dirs == ['alfa6', 'o2', 'test', 'zup31']
    else:
        assert type(exception) is error_perm


def test_read_file(ftp, must_have_permissions):
    try:
        ftp.read_file(ftp_test_file_name, 'files')
        with open(local_test_file_name, 'r') as file:
            file_string = file.readline()
    except Exception as e:
        exception = e
        file_string = ''
    else:
        exception = None

    if must_have_permissions:
        assert exception is None and file_string == 'test string\n'
    else:
        assert type(exception) is error_perm


def test_write_file(ftp, must_have_permissions):

    try:
        ftp.write_file('files/test.txt', ftp_test_file_name)
    except Exception as e:
        exception = e
    else:
        exception = None

    if must_have_permissions:
        assert exception is None
    else:
        assert type(exception) is error_perm


def test_writer():
    ftp = ftp_manager.FTPOperator(FTP_WRITER)
    test_write_file(ftp, must_have_permissions=True)
    test_write_file(ftp, must_have_permissions=False)   # test overwrite file
    test_read_list(ftp, must_have_permissions=False)
    test_read_file(ftp, must_have_permissions=False)


def test_all_reader():
    ftp = ftp_manager.FTPOperator(FTP_FULL_READER)
    test_read_list(ftp, must_have_permissions=True)
    test_write_file(ftp, must_have_permissions=False)
    test_read_file(ftp, must_have_permissions=True)


def test_file_reader():
    ftp = ftp_manager.FTPOperator(FTP_READER)
    test_read_list(ftp, must_have_permissions=False)
    test_write_file(ftp, must_have_permissions=False)
    test_read_file(ftp, must_have_permissions=True)


if __name__ == '__main__':
    test_writer()
    test_all_reader()
    test_file_reader()

    os.remove(local_test_file_name)

    print('successful')
