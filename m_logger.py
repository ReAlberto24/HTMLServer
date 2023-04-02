import builtins
import os
import queue
import re
import threading
from datetime import datetime
from inspect import getframeinfo, stack

from configuration import ForegroundColors, BackgroundColors, SpecialColors


def create_dir(directory: str = '') -> None:
    directories = directory.split('/')
    if len(directories) == 1:
        directories = directory.split('\\')

    if len(directories) == 1:
        return

    drive = re.compile(r'[a-zA-Z]:')
    if not drive.match(directories[0]):
        directories.insert(0, '.')
    else:
        directories[0] = directories[0] + '\\'

    del directories[-1]
    for i, x in enumerate(directories):
        try:
            os.mkdir(os.path.join(*directories[0:i], x))
        except WindowsError:
            pass
        except Exception as e:
            print(e)


class LogTypes:
    PRINT = 'PRINT'
    PRINT_COLOR = ForegroundColors.DARK_CYAN

    REQUEST = 'REQUEST'
    REQUEST_COLOR = ForegroundColors.DARK_MAGENTA

    WARNING = 'WARNING'
    WARNING_COLOR = ForegroundColors.LIGHT_YELLOW

    IMPORTANTWARNING = 'WARNING'
    IMPORTANTWARNING_COLOR = ForegroundColors.LIGHT_RED

    ERROR = 'ERROR'
    ERROR_COLOR = ForegroundColors.LIGHT_RED

    FATALERROR = 'FATAL_ERROR'
    FATALERROR_COLOR = ForegroundColors.DARK_RED


log_queue = queue.Queue()


class Log:
    def __init__(
            self,
            format_string: str = f'[$(call.type) $(datetime)] '
                                 f'({ForegroundColors.LIGHT_RED}$(call.base_filename){SpecialColors.RESET}:'
                                 f'{ForegroundColors.LIGHT_CYAN}$(call.lineno){SpecialColors.RESET}) $(message)',
            date_format_string: str = '%H:%M:%S',
            filename: str = 'main.log'
    ) -> None:
        # os.system('')

        self.format_string = format_string
        self.date_format_string = date_format_string
        self.enabled = True

        create_dir(filename)
        self.file = open(filename, 'w')
        self.ansi_escape = re.compile(r'(?:\x1B[@-_]|[\x80-\x9F])[0-?]*[ -/]*[@-~]')

        # self.file.write('SCHEMA: "' + self.ansi_escape.sub('', format_string) + '"\n')

        self.queue_print = threading.Thread(
            target=self.log_queue_print_thread,
            daemon=True
        )
        self.queue_print.start()

    def default_text_log(
            self,
            msg,
            datetime_now,
            caller,
            join,
            end,
            force_flush,
            log_color,
            log_type
    ) -> None:
        text = self.format_string.replace(
            '$(message)', join.join(msg)
        ).replace(
            '$(datetime)', datetime_now.strftime(self.date_format_string)
            # '$(datetime)', datetime.utcnow().strftime(self.date_format_string)
        ).replace(
            '$(call.filename)', caller.filename
        ).replace(
            '$(call.base_filename)', os.path.basename(caller.filename)
        ).replace(
            '$(call.lineno)', str(caller.lineno)
        ).replace(
            '$(call.type)', log_color + log_type + SpecialColors.RESET
        )

        if not self.enabled:
            self.file.write(self.ansi_escape.sub('', text) + '\n')
            self.file.flush()
            return

        builtins.print(
            text,
            end=end,
            flush=force_flush
        )

        self.file.write(self.ansi_escape.sub('', text) + '\n')
        self.file.flush()

    def log_queue_print_thread(self) -> None:
        global log_queue
        while True:
            try:
                # log = log_queue.get(block=False)
                log = log_queue.get()

                self.default_text_log(
                    *log
                )
            except queue.Empty:
                continue
            except KeyboardInterrupt:
                break
                # pass

    def nprint(self, *msg: list[str], join: str = ' ', end: str = '\n', force_flush: bool = False) -> None:
        global log_queue
        caller = getframeinfo(stack()[1][0])
        log_queue.put(
            (
                msg,
                datetime.now(),
                caller,
                join,
                end,
                force_flush,
                LogTypes.PRINT_COLOR,
                LogTypes.PRINT
            )
        )

    def request(self, *msg: list[str], join: str = ' ', end: str = '\n', force_flush: bool = False) -> None:
        caller = getframeinfo(stack()[1][0])
        log_queue.put(
            (
                msg,
                datetime.now(),
                caller,
                join,
                end,
                force_flush,
                LogTypes.REQUEST_COLOR,
                LogTypes.REQUEST
            )
        )

    def warning(self, *msg: list[str], join: str = ' ', end: str = '\n', force_flush: bool = False) -> None:
        caller = getframeinfo(stack()[1][0])
        log_queue.put(
            (
                msg,
                datetime.now(),
                caller,
                join,
                end,
                force_flush,
                LogTypes.WARNING_COLOR,
                LogTypes.WARNING
            )
        )

    def important_warning(self, *msg: list[str], join: str = ' ', end: str = '\n', force_flush: bool = False) -> None:
        caller = getframeinfo(stack()[1][0])
        log_queue.put(
            (
                msg,
                datetime.now(),
                caller,
                join,
                end,
                force_flush,
                LogTypes.IMPORTANTWARNING_COLOR,
                LogTypes.IMPORTANTWARNING
            )
        )

    def error(self, *msg: list[str], join: str = ' ', end: str = '\n', force_flush: bool = False) -> None:
        caller = getframeinfo(stack()[1][0])
        log_queue.put(
            (
                msg,
                datetime.now(),
                caller,
                join,
                end,
                force_flush,
                LogTypes.ERROR_COLOR,
                LogTypes.ERROR
            )
        )

    def fatal_error(self, *msg: list[str], join: str = ' ', end: str = '\n', force_flush: bool = False) -> None:
        caller = getframeinfo(stack()[1][0])
        log_queue.put(
            (
                msg,
                datetime.now(),
                caller,
                join,
                end,
                force_flush,
                LogTypes.FATALERROR_COLOR,
                LogTypes.FATALERROR
            )
        )

    def wait_until_queue_empty(self) -> None:
        global log_queue
        while log_queue.qsize() > 0:
            pass
