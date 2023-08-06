import base64
import fileinput
import hashlib
import json
import logging
import os
import platform
import shutil
import socket
import sys
import warnings
import zipfile
from collections import namedtuple
from datetime import datetime
from subprocess import Popen, PIPE, TimeoutExpired

import winrm
from requests.exceptions import ConnectionError
from winrm import Protocol
from winrm.exceptions import (InvalidCredentialsError,
                              WinRMError,
                              WinRMTransportError,
                              WinRMOperationTimeoutError)

__author__ = 'Andrey Komissarov'
__email__ = 'a.komisssarov@gmail.com'
__date__ = '12.2019'
__version__ = '1.0.7'

logger_name = 'WinOSClient'
logger = logging.getLogger(logger_name)
logger.setLevel(logging.INFO)
formatter = logging.Formatter(fmt='%(asctime)-15s | %(levelname)s | %(name)s | %(message)s',
                              datefmt='%Y-%m-%d %H:%M:%S')

# Console logger
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(formatter)
logger.addHandler(ch)


class ResponseParser:
    """Response parser"""

    def __init__(self, response):
        self.response = response

    def __repr__(self):
        return str(self.response)

    @staticmethod
    def _decoder(response):
        return response.decode('cp1252').strip()

    @property
    def stdout(self) -> str:
        try:
            stdout = self._decoder(self.response.std_out)
        except AttributeError:
            stdout = self._decoder(self.response[1])
        out = stdout if stdout else None
        logger.info(out)
        return out

    @property
    def stderr(self) -> str:
        try:
            stderr = self._decoder(self.response.std_err)
        except AttributeError:
            stderr = self._decoder(self.response[2])
        err = stderr if stderr else None
        if err:
            logger.error(err)
        return err

    @property
    def exited(self) -> int:
        try:
            exited = self.response.status_code
        except AttributeError:
            exited = self.response[0]
        logger.info(exited)
        return exited

    @property
    def ok(self) -> bool:
        try:
            return self.response.status_code == 0
        except AttributeError:
            return self.response[0] == 0

    def json(self):
        return json.loads(self.stdout)

    def decoded(self, encoding: str = 'utf8'):
        """Decode stdout response.

        :param encoding: utf8 by default
        :return:
        """

        return base64.b64decode(self.stdout).decode(encoding)


class WinOSClient:
    """The cross-platform tool to work with remote and local Windows OS.

    Returns response object with exit code, sent command, stdout/sdtderr.
    Check response methods.
    """

    _URL = 'https://pypi.org/project/pywinrm/'

    def __init__(
            self,
            host: str = '',
            username: str = '',
            password: str = '',
            logger_enabled: bool = True):

        self.host = host
        self.username = username
        self.password = password
        logger.disabled = not logger_enabled

    def __str__(self):
        return (
            f'Local host: {self.get_current_os_name()}\n'
            f'Remote IP: {self.host}\n'
            f'Username: {self.username}\n'
            f'Password: {self.password}'
        )

    @property
    def version(self):
        return __version__

    def list_all_methods(self):
        """Returns all available public methods"""

        methods = [
            method for method in self.__dir__()
            if not method.startswith('_')
        ]
        index = methods.index('list_all_methods') + 1
        return methods[index:]

    def __local(self):
        return not self.host or self.host == 'localhost' \
               or self.host == '127.0.0.1'

    def is_host_available(self, port: int = 5985, timeout: int = 5) -> bool:
        """Check remote host is available using specified port.

        Port 5985 used by default
        """

        if self.__local():
            return True

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            response = sock.connect_ex((self.host, port))
            result = False if response else True
            logger.info(f'{self.host} is available: {result}')
            return result

    # ---------- Remote section ----------
    @property
    def session(self):
        """Create WinRM session connection to a remote server"""

        session = winrm.Session(self.host, auth=(self.username, self.password))
        return session

    def _protocol(self, endpoint: str, transport: str):
        """Create Protocol using low-level API"""

        session = self.session

        protocol = Protocol(
            endpoint=endpoint,
            transport=transport,
            username=self.username,
            password=self.password,
            server_cert_validation='ignore',
            message_encryption='always')

        session.protocol = protocol
        return session

    def _client(
            self,
            command: str,
            ps: bool = False,
            cmd: bool = False,
            use_cred_ssp: bool = False,
            *args) -> ResponseParser:
        """The client to send PowerShell or command-line commands

        :param command: Command to execute
        :param ps: Specify if PowerShell is used
        :param cmd: Specify if command-line is used
        :param use_cred_ssp: Specify if CredSSP is used
        :param args: Arguments for command-line
        :return:
        """

        response = None

        try:
            logger.info(f'[{self.host}] ' + command)
            if ps:  # Use PowerShell
                endpoint = (f'https://{self.host}:5986/wsman'
                            if use_cred_ssp
                            else f'http://{self.host}:5985/wsman')
                transport = 'credssp' if use_cred_ssp else 'ntlm'
                client = self._protocol(endpoint, transport)
                response = client.run_ps(command)
            elif cmd:  # Use command-line
                client = self._protocol(
                    endpoint=f'http://{self.host}:5985/wsman',
                    transport='ntlm')
                response = client.run_cmd(command, [arg for arg in args])
            return ResponseParser(response)

        # Catch exceptions
        except InvalidCredentialsError as err:
            logger.error(f'Invalid credentials: {self.username}@{self.password}. {err}')
            raise InvalidCredentialsError
        except ConnectionError as err:
            logger.error('Connection error: ' + str(err))
            raise ConnectionError
        except (WinRMError,
                WinRMOperationTimeoutError,
                WinRMTransportError) as err:
            logger.error('WinRM error: ' + str(err))
            raise err
        except Exception as err:
            logger.error('Unhandled error: ' + str(err))
            logger.error('Try to use "run_cmd_local" method instead.')
            raise err

    def run_cmd(self, command: str, timeout: int = 60, *args) -> ResponseParser:
        """
        Allows to execute cmd command on a remote server.

        Executes command locally if host was not specified
        or host == "localhost/127.0.0.1"

        :param command: command
        :param args: additional command arguments
        :param timeout: timeout
        :return: Object with exit code, stdout and stderr
        """

        if self.__local():
            return self._run_local(command, timeout)
        return self._client(command, cmd=True, *args)

    def run_ps(self,
               command: str = None,
               use_cred_ssp: bool = False,
               script: str = None,
               timeout: int = 60,
               **params) -> ResponseParser:
        """Allows to execute PowerShell command or script using a remote shell and local server.

        :param command: Command
        :param use_cred_ssp: Use CredSSP.
        :param script: Powershell script full path.
        :param params: Named parameters to be invoked with the script specified.
        :param timeout: Timeout in sec.
        :return: Object with exit code, stdout and stderr
        """

        if self.__local():
            cmd = f'powershell.exe {command}'
            if script:
                params_ = ' '.join([f'-{key} {value}' for key, value in params.items()])
                cmd = f'powershell.exe -file {script} {params_}'

            with Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE) as process:
                logger.info('[LOCAL PS] ' + cmd)
                process.wait(timeout)
                stdout, stderr = process.communicate()
                exitcode = process.wait(timeout=timeout)
                response = exitcode, stdout, stderr
                return ResponseParser(response)

        return self._client(command, ps=True, use_cred_ssp=use_cred_ssp)

    # ---------- Local section ----------
    @staticmethod
    def _run_local(cmd: str, timeout: int = 60):
        """Main function to send commands using subprocess LOCALLY.

        Used command-line (cmd.exe or bash)

        :param cmd: string, command
        :param timeout: timeout for command
        :return: Decoded response

        """

        with Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE) as process:
            try:
                logger.info('[LOCAL CMD] ' + cmd)
                stdout, stderr = process.communicate(timeout=timeout)
                exitcode = process.wait(timeout=timeout)
                response = exitcode, stdout, stderr
                return ResponseParser(response)

            except TimeoutExpired as err:
                process.kill()
                logger.error('Timeout exception: ' + str(err))
                raise err

    @staticmethod
    def get_current_os_name():
        """Returns current OS name"""

        return platform.system()

    @property
    def is_windows(self):
        logger.info('sdf')
        return self.get_current_os_name() == 'Windows'

    @property
    def is_linux(self):
        return self.get_current_os_name() == 'Linux'

    @staticmethod
    def exists(path: str) -> bool:
        """Check file/directory exists

        :param path: Full path. Can be network path. Share must be attached!
        :return:
        """

        return os.path.exists(path)

    def get_content(self, path):
        return self.run_ps(f'Get-Content "{path}"')

    def get_json(self, path: str) -> dict:
        """Read JSON file as string and pretty print it into console """

        file = self.get_content(path)
        return file.json()

    @staticmethod
    def get_local_hostname_ip():
        """Get local IP and hostname

        :return: Object with "ip" and "hostname" properties
        """

        host_name = socket.gethostname()
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        return type(
            'HostnameIP', (),
            {
                'ip': s.getsockname()[0],
                'hostname': host_name
            }
        )

    @staticmethod
    def search(directory: str, ends: str = None, starts: str = None, filter_: str = None) -> list:
        """Search for file(s) in specified directory

        :param directory: Root directory to search
        :param ends: Ends with
        :param starts: Start with
        :param filter_: Search files by containing
        :return: list of files
        """

        result = []
        for file in os.listdir(directory):
            file_lower = file.lower()

            if ends:
                if file_lower.endswith(ends.lower()):
                    result.append(file)
            elif starts:
                if file_lower.startswith(starts.lower()):
                    result.append(file)
            elif filter_:
                if filter_.lower() in file_lower:
                    result.append(file)
        return result

    @staticmethod
    def list_dir(path: str, prefix: str = '', ends: str = ''):
        """Get dir list"""

        return [
            os.path.join(path, file) for file in os.listdir(path) if
            os.path.isfile(os.path.join(path, file)) and
            file.startswith(prefix) and file.endswith(ends)
        ]

    def sort_files(self, path: str, prefix: str = '', ends: str = '') -> list:
        """Sort files in a directory by ctime (modification time)

        :param path: Full path to the share (directory)
        :param prefix: Prefix
        :param ends: File end filter
        :return: List of sorted files name by ctime
        """

        files = self.list_dir(path, prefix, ends)
        files.sort(key=os.path.getctime, reverse=True)
        return files

    def get_last_file_name(self, path: str, prefix: str = '', ends: str = ''):
        """Get last file from specified directory

        :param path: Full path to the share (directory)
        :param prefix: Prefix
        :param ends: File end filter
        :return: Last file name by ctime
        """

        all_files = self.list_dir(path, prefix, ends)

        try:
            last_build = max(all_files, key=os.path.getctime)
            return os.path.basename(last_build)
        except ValueError as err:
            logger.error(f'{err}. Maybe file with specified criteria not found.')
            return 'File not found. Try another search parameters.'

    # noinspection PyUnresolvedReferences
    @staticmethod
    def get_file_version(path: str):
        """Get local windows file version from file property

        Windows only.

        pip install pywin32

        :param path: Full path to the file
        :return: 51.1052.0.0
        """

        exists = os.path.exists(path)
        if exists:
            try:
                from win32com.client import Dispatch
            except ModuleNotFoundError as err:
                warnings.warn('To use this method use "pip install pywin32". Windows only.')
                logger.warning('To use this method perform "pip install pywin32"')
                raise err

            ver_parser = Dispatch('Scripting.FileSystemObject')
            return ver_parser.GetFileVersion(path)
        else:
            return 'File not found'

    @staticmethod
    def get_file_size(path: str):
        """Get local windows file size

        :param path: Full path to the file
        :return:
        """

        try:
            return os.path.getsize(path)
        except FileNotFoundError as err:
            logger.error(f'File not found. {err}')
            raise err

    @staticmethod
    def replace_text(path: str, old_text: str, new_text: str, backup: str = '.bak'):
        """Replace all string mansion with a new string

        :param path: Full file path
        :param old_text: Text to replace
        :param new_text: Replacements text
        :param backup: Create backup file with specified extension in
        a current directory.
        Use blank string "" if you do
        """

        with fileinput.FileInput(path, inplace=True, backup=backup) as file:
            for line in file:
                print(line.replace(old_text, new_text), end='')

    @staticmethod
    def get_absolute_path(path):
        """Returns absolute file path"""

        return os.path.abspath(path)

    @staticmethod
    def get_md5(file: str):
        """
        Open file and calculate MD5

        :param file: Full file path
        :type file: str
        :return: File's MD5 hash
        """

        with open(file, 'rb') as f:
            m = hashlib.md5()
            while True:
                data = f.read(8192)
                if not data:
                    break
                m.update(data)
            return m.hexdigest()

    @staticmethod
    def clean_directory(path: str):
        """Clean (remove) all files from a windows directory

        :param path: Full file\\directory path
        """

        try:
            for the_file in os.listdir(path):
                file_path = os.path.join(path, the_file)
                basename = os.path.basename(file_path)

                if os.path.isfile(file_path):
                    if basename != 'pagefile.sys':
                        os.remove(file_path)
                elif os.path.isdir(file_path):
                    if basename != 'System Volume Information':
                        shutil.rmtree(file_path)
            return True
        except OSError as e:
            print(f'The user name or password to {path} is incorrect', e)
            raise e

    @staticmethod
    def remove(path: str) -> bool:
        """Remove file or directory recursively

        :param path: Full file\\directory path
        """

        try:
            if os.path.isfile(path):
                os.remove(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)
            return True
        except OSError as e:
            print(f'The user name or password to {path} is incorrect', e)
            return False

    def copy(self, source: str, destination: str, new_name=None):
        """Copy file to a remote windows directory.

        Creates destination directory if does not exist.

        :param source: Source file to copy
        :param destination: Destination directory.
        :param new_name: Copy file with a new name if specified.
        :return: Check copied file exists
        """

        # Get full destination path
        dst_full = (os.path.join(destination, new_name)
                    if new_name
                    else
                    destination)

        # Create directory
        dir_name = os.path.dirname(dst_full) if new_name else destination
        self.create_directory(dir_name)

        try:
            shutil.copy(source, dst_full)
        except FileNotFoundError as err:
            logger.error(f'ERROR occurred during file copy. {err}')
            raise err

        return self.exists(dst_full)

    @staticmethod
    def unzip(path_to_zip_file: str, target_directory=None):
        """
        Extract .zip archive to destination folder
        Creates destination folder if it does not exist
        """

        directory_to_extract_to = target_directory

        if not target_directory:
            directory_to_extract_to = os.path.dirname(path_to_zip_file)

        with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
            zip_ref.extractall(directory_to_extract_to)
        print('Unzipped to:', directory_to_extract_to)

        return target_directory

    def create_directory(self, path: str):
        """Create directory. No errors if it already exists."""

        os.makedirs(path, exist_ok=True)

        return self.exists(path)

    @staticmethod
    def timestamp(sec: bool = False):
        """Get time stamp"""

        if sec:
            return datetime.now().strftime('%Y%m%d_%H%M%S')
        return datetime.now().strftime('%Y%m%d_%H%M')

    def ping(self, host: str = '', packets_number: int = 4):
        """Ping remote host

        :param host: IP address to ping. Used host IP from init by default
        :param packets_number: Number of packets. 4 by default
        """

        counter = 'c'
        if self.get_current_os_name() == 'Windows':
            counter = 'n'

        ip_ = host if host else self.host

        command = f'ping -{counter} {packets_number} {ip_}'
        return self._run_local(cmd=command)

    # ---------- Service / process management ----------
    def get_service(self, name: str):
        """Check windows service"""

        return self.run_ps(f'Get-Service -Name {name}')

    def get_service_status(self, name: str):
        """Check windows service status"""

        return self.run_ps(f'(Get-Service -Name {name}).Status')

    def start_service(self, name: str):
        """Start service"""
        return self.run_ps(f'Start-Service -Name {name}')

    def restart_service(self, name: str):
        """Restart service"""
        return self.run_ps(f'Restart-Service -Name {name}')

    def stop_service(self, name: str):
        """Stop service"""
        return self.run_ps(f'Stop-Service -Name {name}')

    def get_process(self, name: str):
        """Check windows process status"""

        return self.run_ps(f'Get-Process -Name {name}')

    def kill_process(self, name: str):
        """Kill windows local service status. Remote and local"""

        return self.run_cmd(f'taskkill -im {name} /f')

    def wait_service_start(self, name: str, interval: int = 3):
        """while ((Get-Service -Name ALG).Status -ne "Running"){Start-Sleep 1}"""

        cmd = f'while ((Get-Service -Name {name}).Status -ne "Running"){{Start-Sleep {interval}}}'
        return self.run_ps(cmd)

    def get_service_file_version(self, name: str):
        """Get FileVersion from the process"""

        return self.run_ps(f'(Get-Process -Name {name}).FileVersion')

    def is_process_running(self, name: str) -> bool:
        """Check local windows process is running"""

        cmd = f'(Get-Service -Name {name}).Status -eq "running"'
        response = self.run_ps(cmd)
        if response.stdout == 'True':
            return True
        return False

    def _get_process_memory_info(self, name: str, full: bool = False) -> namedtuple:
        """Return a namedtuple with variable fields depending on the
        platform, representing memory information about the process.

        The "portable" fields available on all platforms are `rss` and `vms`.

        All numbers are expressed in bytes.
        """

        raise NotImplemented

    def _get_process_memory_percent(self, name: str, memtype='rss') -> float:
        """
        Compare process memory to total physical system memory and
        calculate process memory utilization as a percentage.

        :param name: process name
        :param memtype: what type of
        process memory you want to compare against (defaults to "rss").

        psutil.Process().memory_info()._fields
        ('rss', 'vms', 'shared', 'text', 'lib', 'data', 'dirty', 'uss', 'pss')
        """

        raise NotImplemented

    def _get_process_cpu_percent(self, name: str, interval=None) -> float:
        """
        Return a float representing the current process CPU
        utilization as a percentage.

        When *interval* is 0.0 or None (default) compares process times
        to system CPU times elapsed since last call, returning
        immediately (non-blocking). That means that the first time
        this is called it will return a meaningful 0.0 value.

        When *interval* is > 0.0 compares process times to system CPU
        times elapsed before and after the interval (blocking).

        In this case is recommended for accuracy that this function
        be called with at least 0.1 seconds between calls.

        A value > 100.0 can be returned in case of processes running
        multiple threads on different CPU cores.
        """

        raise NotImplemented

    def attach_share(self, share, username, password):
        """Attach network share"""

        command = f'net use {share} /u:{username} {password}'
        return self.run_cmd(command)

    def debug_info(self):
        logger.info('Linux client created')
        logger.info(f'Local host: {self.get_current_os_name()}')
        logger.info(f'Remote IP: {self.host}')
        logger.info(f'Username: {self.username}')
        logger.info(f'Password: {self.password}')
        logger.info(f'Available: {self.is_host_available()}')
        logger.info(sys.version)
