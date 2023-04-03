import argparse
import json
import os
import random
import shlex
import signal
import socket
import subprocess
import sys
import threading
import time
from typing import NoReturn

import keyboard
import psutil
import requests
import waitress
from flask import Flask, request, redirect, make_response

import class_server
from configuration import *
from m_logger import Log

app = Flask(__name__, template_folder='html')
ForeC = ForegroundColors
SpeC = SpecialColors

logger = Log(
    format_string=f'[$(call.type) $(datetime)] ({ForeC.LIGHT_RED}$(call.base_filename){SpeC.RESET}:{ForeC.LIGHT_CYAN}$(call.lineno){SpeC.RESET}) $(message)',
    date_format_string='%H:%M:%S',
    filename=f'logs/{os.path.basename(__file__)}.log'
)

requests_file = open(
    'requests.bin',
    'wb'
)
# HTML: 0
# CSS: 1
# JAVASCRIPT: 2
# FILE: 3
# FILE_NAME_START: 5
# FILE_NAME_END: 6

start_time = str(int(time.time()))


@app.route('/', methods=['GET'])
def flask_index():
    global logger
    logger.request(
        f'[{ForegroundColors.LIGHT_MAGENTA}INDEX{SpecialColors.RESET}] Call'
        f'| Args: {list(request.args.items())}',
        join=' ',
        end='\n',
        force_flush=False
    )
    # return send_file('html/index.html')
    return redirect(location='/html/index.html', code=302)


@app.route('/js/<js_type>/<file>', methods=['GET'])
def flask_js(js_type, file):
    global logger
    logger.request(
        f'[{ForegroundColors.LIGHT_MAGENTA}JAVASCRIPT{SpecialColors.RESET}] Call (type: {js_type}, file: {file})'
        f'| Args: {list(request.args.items())}',
        join=' ',
        end='\n',
        force_flush=False
    )
    # 2: JAVASCRIPT; 5: FILE_NAME_START; {}: FILE_NAME; 6: FILE_NAME_START
    requests_file.write(bytes([2, len(file) + 1, 5]) + file.encode() + bytes([6]))
    requests_file.flush()
    return class_server.javascript(js_type, file)


@app.route('/file/<file_name>', methods=['GET'])
def flask_file(file_name):
    global logger
    directory = request.args.get('directory')
    logger.request(
        f'[{ForegroundColors.LIGHT_MAGENTA}FILE{SpecialColors.RESET}] Call (file: {file_name}) (dir: {directory})'
        f'| Args: {list(request.args.items())}',
        join=' ',
        end='\n',
        force_flush=False
    )
    # 3: FILE; 5: FILE_NAME_START; {}: FILE_NAME; 6: FILE_NAME_START
    requests_file.write(bytes([3, len(file_name) + 1, 5]) + file_name.encode() + bytes([6]))
    requests_file.flush()
    return class_server.file(file_name, directory)


@app.route('/css/<file_name>', methods=['GET'])
def flask_css(file_name):
    global logger
    logger.request(
        f'[{ForegroundColors.LIGHT_MAGENTA}CSS{SpecialColors.RESET}] Call (file: {file_name})'
        f'| Args: {list(request.args.items())}',
        join=' ',
        end='\n',
        force_flush=False
    )
    # 1: CSS; 5: FILE_NAME_START; {}: FILE_NAME; 6: FILE_NAME_START
    requests_file.write(bytes([1, len(file_name) + 1, 5]) + file_name.encode() + bytes([6]))
    requests_file.flush()
    return class_server.file(file_name, 'css')


@app.route('/html/<file_name>', methods=['GET'])
def flask_html(file_name):
    global logger
    logger.request(
        f'[{ForegroundColors.LIGHT_MAGENTA}HTML{SpecialColors.RESET}] Call (file: {file_name})'
        f'| Args: {list(request.args.items())}',
        join=' ',
        end='\n',
        force_flush=False
    )
    # 0: HTML; 5: FILE_NAME_START; {}: FILE_NAME; 6: FILE_NAME_START
    requests_file.write(bytes([0, len(file_name) + 1, 5]) + file_name.encode() + bytes([6]))
    requests_file.flush()
    return class_server.file(file_name, 'html')


@app.route('/admin/<file_name>', methods=['GET'])
def flask_admin(file_name: str):
    global logger
    global start_time
    global public_address
    global address

    logger.request(
        f'[{ForegroundColors.LIGHT_MAGENTA}ADMIN{SpecialColors.RESET}] Call (file: {file_name})'
        f'| Args: {list(request.args.items())}',
        join=' ',
        end='\n',
        force_flush=False
    )
    if file_name.rsplit('.', 1)[1] == 'html':
        resp = make_response(open(f'admin/{file_name}', 'r').read())
        resp.set_cookie('server_time', start_time)
        resp.set_cookie('server_public_address', public_address if public_address != '' else address)
        return resp

    elif file_name.rsplit('.', 1)[1] == 'py':
        python_process = subprocess.run(
            ['python', f'admin/{file_name}', *request.args],
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL
        )

        return python_process.stdout

    return class_server.file(file_name, 'admin')


def restart_program() -> NoReturn:
    try:
        p = psutil.Process(os.getpid())
        for handler in p.get_open_files() + p.connections():
            os.close(handler.fd)
    except Exception:
        pass

    python = sys.executable
    os.execl(python, python, *sys.argv)


def keyboard_shell() -> None:
    global logger
    while True:
        if keyboard.is_pressed('p'):
            logger.enabled = False
            print(f'Use the command {ForegroundColors.DARK_BLUE}quit{SpecialColors.RESET} to exit the shell')
            print(f'{ForegroundColors.LIGHT_RED}WARNING{SpecialColors.RESET}: '
                  f'Console logging wont be active while the shell is active')
            print(f'{ForegroundColors.LIGHT_RED}WARNING{SpecialColors.RESET}: '
                  f'Remember to use "quit" then CTRL+C to close the server securely')
            while True:
                text = shlex.split(input(f'{ForegroundColors.LIGHT_GREEN}shell{SpecialColors.RESET} > '))

                try:
                    command = text[0]
                    try:
                        c_args = text[1::]
                    except IndexError:
                        c_args = []

                    match command:
                        case 'exit':
                            if len(c_args) > 0:
                                if '-y' in c_args:
                                    os.kill(os.getpid(), signal.SIGINT)
                            elif input('Sure? [Y,n] ').strip().lower() == 'y':
                                os.kill(os.getpid(), signal.SIGINT)
                        case 'help':
                            print('  help: Show this command output\n'
                                  '  quit: Exit the shell mode\n'
                                  '  exit: Close the server\n'
                                  '    - args: {-y}\n'
                                  f'  restart: Restart the server ({ForegroundColors.LIGHT_RED}BUGGED{SpecialColors.RESET})\n'
                                  '    - args: {-y}\n'
                                  '  clear: Clear the console\n')
                        case 'quit':
                            print()
                            break
                        case 'restart':
                            if len(c_args) > 0:
                                if '-y' in c_args:
                                    restart_program()
                            elif input('Sure? [Y,n] ').strip().lower() == 'y':
                                restart_program()
                        case 'clear':
                            match os.name:
                                case 'nt':
                                    subprocess.run(['cls'], shell=True)
                                case 'posix':
                                    subprocess.run(['clear'], shell=True)
                        case _:
                            print(f'Unknown command: {command}')

                except IndexError:
                    pass
                except Exception as expt:
                    print(f'Unknown Exception while parsing command: {expt}')

            logger.enabled = True


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='details',
        usage='Use "%(prog)s --help" for more information',
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument('--server',
                        choices=['flask', 'wsgi'],
                        default='wsgi',
                        type=str,
                        help='1. Flask - Better for debugging - No Threads\n'
                             '2. Wsgi (waitress.serve) - Better performing - Default'
                        )

    parser.add_argument('--port',
                        type=int,
                        help='Specify the port to use (0 - 65535) - Default: 4000 - 8000',
                        default=None
                        )

    parser.add_argument('--public',
                        action='store_true',
                        help='Enable server access to the lan - Default to False',
                        default=False
                        )

    parser.add_argument('--threads',
                        help='Set how many threads the server can use (wsgi) - Default to 64',
                        default=64,
                        type=int
                        )

    parser.add_argument('--start_gui',
                        help='Start the gui automatically - Default to False',
                        action='store_true',
                        default=False
                        )

    # parser.set_defaults()
    args = parser.parse_args()

    if args.port and (0 <= args.port):
        port = args.port
    else:
        port = random.randint(4000, 8000)

    name = 'Server Manager'

    if args.public:
        sip = '0.0.0.0'
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(('8.8.8.8', 80))
            address = f'http://{s.getsockname()[0]}:{port}'
        public_address = 'http://' + requests.get('http://ipv4.icanhazip.com').content.decode().strip() + ':' + str(
            port)
        logger.important_warning('Admin GUI not enabled while in public mode')
    else:
        sip = '127.0.0.1'
        address = f'http://127.0.0.1:{port}'
        public_address = ''

        logger.nprint('Open GUI using: '
                      f'{ForegroundColors.LIGHT_RED}{sys.executable} gui.py "http://127.0.0.1:{port}/admin/index.html" "{name}"{SpecialColors.RESET}')
        logger.important_warning('Shell Mode will be disabled after opening the GUI for technical reasons')
        if args.start_gui:
            gui_process = subprocess.Popen(
                [
                    sys.executable,
                    'gui.py',
                    f'http://127.0.0.1:{port}/admin/index.html',
                    name
                ]
            )
        else:
            shell = threading.Thread(target=keyboard_shell, daemon=True)
            shell.start()

    logger.nprint(f'Running server on {ForegroundColors.LIGHT_BLUE}{sip}{SpecialColors.RESET}, '
                  f'port: {ForegroundColors.LIGHT_BLUE}{port}{SpecialColors.RESET} | '
                  f'{ForegroundColors.LIGHT_BLUE}{address}{SpecialColors.RESET} '
                  f'{"or" + ForegroundColors.LIGHT_BLUE + " http://" + public_address if public_address else ""}'
                  f'{SpecialColors.RESET}'
                  )

    logger.nprint(f'Additional info | args: {json.dumps(args.__dict__)}')

    logger.nprint(f'Open the {ForegroundColors.LIGHT_GREEN}shell{SpecialColors.RESET} by pressing "p"')
    logger.nprint(f'Use {ForegroundColors.DARK_GREEN}CTRL+C{SpecialColors.RESET} to stop the server')

    logger.warning('Starting server')

    try:
        match args.server:
            case 'flask':
                app.run(
                    host=sip,
                    port=port,
                    debug=False
                )

            case 'wsgi':
                waitress.serve(
                    app,
                    host=sip,
                    port=port,
                    threads=args.threads,
                    _quiet=True
                )
    except PermissionError:
        logger.fatal_error('Port or Address probably already in use')

    except Exception:
        logger.fatal_error('Unknown FATAL_ERROR while generating the server')

    logger.warning('Closing...')

    requests_file.close()

    logger.wait_until_queue_empty()
    logger.file.close()
