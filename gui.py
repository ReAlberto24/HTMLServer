import os
import sys

import webview

from configuration import ForegroundColors, SpecialColors
from m_logger import Log

path = os.path.dirname(os.path.abspath(__file__))
ForeC = ForegroundColors
SpeC = SpecialColors
logger = Log(
    format_string=f'[$(call.type) $(datetime)] ({ForeC.LIGHT_RED}$(call.base_filename){SpeC.RESET}:{ForeC.LIGHT_CYAN}$(call.lineno){SpeC.RESET}) $(message)',
    date_format_string='%H:%M:%S',
    filename=f'logs/{os.path.basename(__file__)}.log'
)

if __name__ == '__main__':
    try:
        title = sys.argv[2]
        url = sys.argv[1]
    except IndexError:
        logger.fatal_error('Error while loading the URL and the TITLE')
        exit(1)

    logger.nprint('Starting the GUI')

    window_size = (1000, 600)
    window = webview.create_window(
        title,
        url,
        width=window_size[0],
        height=window_size[1],
        min_size=window_size,
        text_select=False
    )

    webview.start(
        gui=window,
        private_mode=False,
        storage_path=f'{path}\\gui'
    )

    logger.warning('GUI closed')
