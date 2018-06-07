import subprocess
import requests
import time
import os
import signal

from config import PORT, SERVER_START_TIMEOUT, PROCFILE_PATH


def with_active_server(func):
    def wrapper():
        _start_server_process()
        try:
            func()
        except Exception:
            _kill_server_processes()
            raise
    return wrapper


def await_server_response(path):
    timeout = time.time() + SERVER_START_TIMEOUT
    while time.time() < timeout:
        try:
            return requests.get(f'http://localhost:{PORT}{path}')
        except requests.exceptions.ConnectionError:
            time.sleep(1)
    else:
        raise Exception(
            f'Could not connect to server within {SERVER_START_TIMEOUT} seconds, try re-running the tests?')


def _start_server_process():
    try:
        # check for a currently existing server, and kill it if so
        requests.get(f'http://localhost:{PORT}')
        _kill_server_processes()
    except requests.exceptions.ConnectionError:
        # start up our new server
        subprocess.Popen(f'heroku local -p {PORT}', shell=True)


def _kill_server_processes():
    with open(PROCFILE_PATH, 'r') as procfile:
        server_start_command = procfile.read().split('web: ')[1].strip()
    pids = [
        process.split(' ')[0]
        for process in subprocess.run('ps', stdout=subprocess.PIPE).stdout.decode('utf-8').split('\n')
        if server_start_command in process
    ]
    for pid in pids:
        try:
            os.kill(int(pid), signal.SIGTERM)
        except ProcessLookupError:
            pass
