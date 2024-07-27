from ftplib import FTP

from config import FTP_IP


class FTPBackupManager:
    pass


class FTPOperator:
    def __init__(self, user):
        self.ftp_server = None
        self.ftp_user = user

    def write_file(self, file_path, save_path):
        self.ftp_server = FTP(FTP_IP)
        self.ftp_server.login(user=self.ftp_user['login'], passwd=self.ftp_user['password'])

        with open(file_path, 'rb') as file:
            self.ftp_server.storbinary(f'STOR {save_path}', file)

        self.ftp_server.quit()
        self.ftp_server = None
