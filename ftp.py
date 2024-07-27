from ftplib import FTP
import os

from config import FTP_IP


class FTPConnect:
    def __init__(self, ftp_user):
        self.ftp = FTP(FTP_IP)
        self.ftp_user = ftp_user

    def __enter__(self):
        self.ftp.login(user=self.ftp_user['login'], passwd=self.ftp_user['password'])
        return self

    def __exit__(self, exception_type, exception_value, exception_traceback):
        self.ftp.quit()


class FTPOperator:
    def __init__(self, user):
        self.ftp_user = user

    def write_file(self, file_path, save_path):
        with FTPConnect(self.ftp_user) as ftp_server:
            with open(file_path, 'rb') as file:
                ftp_server.ftp.storbinary(f'STOR {save_path}', file)

    def read_file(self, file_path, save_path):
        with FTPConnect(self.ftp_user) as ftp_server:
            dir_name = os.path.dirname(file_path)
            base_name = os.path.basename(file_path)

            ftp_server.ftp.cwd(dir_name)
            with open(os.path.join(save_path, base_name), 'wb') as file:
                ftp_server.ftp.retrbinary(f'RETR {base_name}', file.write)

    def get_list(self, dir_path):
        with FTPConnect(self.ftp_user) as ftp_server:
            ftp_server.ftp.cwd(dir_path)
            content = dict(ftp_server.ftp.mlsd())
            content.pop('.', None)
            content.pop('..', None)

        return content
