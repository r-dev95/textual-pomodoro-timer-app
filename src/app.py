"""This is the module that defines the main app.
"""

import argparse
from logging import getLogger
from pathlib import Path
from typing import TYPE_CHECKING, Any, ClassVar, override

import plyer
from textual import on
from textual.app import App, ComposeResult
from textual.binding import Binding, BindingType
from textual.color import Color
from textual.containers import Horizontal
from textual.widgets import Button, Digits, Footer, Header, Input, Static

from lib.common.decorator import process_time, save_params_log
from lib.common.file import load_yaml
from lib.common.log import SetLogging
from lib.common.process import sec_to_hms
from lib.common.types import ParamKey as K
from lib.common.types import SessionType
from lib.settings import ParamLog

if TYPE_CHECKING:
    from textual.timer import Timer

PARAM_LOG = ParamLog()
LOGGER = getLogger(PARAM_LOG.NAME)


ICON_PATH = 'lib/ui/icons/icon.ico'


class MainApp(App):
    """Defines the main app.
    """
    #: str: The title to display in the :class:`Header`.
    TITLE = '🍅 Pomodoro Timer'
    #: str: The `tcss` file path.
    CSS_PATH = 'lib/ui/layout.tcss'
    #: list[BindingType]: The key bindings.
    BINDINGS: ClassVar[list[BindingType]] = [
        Binding(key='ctrl+c', action='quit', description='Quit', priority=True),
    ]

    def __init__(self) -> None:
        super().__init__()

        self.timer: Timer = None
        self.session: SessionType = SessionType.WAIT
        self.pre_session: SessionType = None
        self.work_time: int = None
        self.break_time: int = None
        self.session_time: int = None
        self.status_text = {
            SessionType.WAIT: 'Waiting',
            SessionType.WORK: 'In Progress',
            SessionType.BREAK: 'On Break',
            SessionType.PAUSE: 'Paused',
        }
        self.status_border = {
            SessionType.WAIT: ('heavy', Color(255, 255, 255)),
            SessionType.WORK: ('heavy', Color(0, 255, 0)),
            SessionType.BREAK: ('heavy', Color(0, 0, 255)),
            SessionType.PAUSE: ('heavy', Color(255, 255, 0)),
        }

        # For syntax highlighting.
        self.note: plyer.facades.Notification = plyer.notification

    @override
    def compose(self) -> ComposeResult:
        """Yield child widgets for a container.

        Yields:
            Iterator[ComposeResult]: The child widgets.
        """
        yield Header(show_clock=True)
        yield Horizontal(
            Input(
                value='25',
                placeholder='Work Time [m]',
                type='integer',
                id='work_time',
            ),
            Input(
                value='5',
                placeholder='Rest Time [m]',
                type='integer',
                id='break_time',
            ),
            id='input_group',
        )
        yield Horizontal(
            Button('Start', variant='success', id='start'),
            Button('Pause', variant='warning', id='pause'),
            Button('Reset', variant='primary', id='reset'),
            id='button_group',
        )
        yield Static(content=self.status_text[SessionType.WAIT], id='status')
        yield Digits(value='00:00:00', id='session_time')
        yield Footer()

    @on(message_type=Button.Pressed, selector='#start')
    def start_timer(self) -> None:
        """Start the timer.
        """
        LOGGER.debug(f'{self.timer=}, {self.session=}')
        if self.session == SessionType.WAIT:
            try:
                self.work_time = int(self.query_one(
                    selector='#work_time',
                    expect_type=Input,
                ).value) * 60 # minutes -> seconds
                self.break_time = int(self.query_one(
                    selector='#break_time',
                    expect_type=Input,
                ).value) * 60 # minutes -> seconds
                self.session_time = self.work_time
                self.session = SessionType.WORK
                self.timer = self.set_interval(interval=1, callback=self.update_timer)
            except ValueError:
                LOGGER.exception(f'Found an error.')
        elif self.session == SessionType.PAUSE:
            self.session = self.pre_session
            self.timer.resume()

    @on(message_type=Button.Pressed, selector='#pause')
    def pause_timer(self) -> None:
        """Pause the timer.
        """
        LOGGER.debug(f'{self.timer=}, {self.session=}')
        if self.timer and self.session != SessionType.PAUSE:
            self.pre_session = self.session
            self.session = SessionType.PAUSE
            self.timer.pause()
            self.update_ui()

    @on(message_type=Button.Pressed, selector='#reset')
    def reset_timer(self) -> None:
        """Reset the timer.
        """
        LOGGER.debug(f'{self.timer=}, {self.session=}')
        if self.timer:
            self.session = SessionType.WAIT
            self.timer.stop()
            self.timer = None
            self.work_time = None
            self.break_time = None
            self.session_time = None
            self.update_ui()

    def update_timer(self) -> None:
        """Update the timer.

        *   This method is a callback for :class:`self.timer`.
        """
        if self.session_time > 0:
            self.session_time -= 1
        else:
            self.update_session()
        self.update_ui()

    def update_session(self) -> None:
        """Update the session (Work session / Break session).
        """
        LOGGER.debug(f'{self.timer=}, {self.session=}')
        match self.session:
            case SessionType.WORK:
                self.session = SessionType.BREAK
                self.session_time = self.break_time
                self.plyer_nortify()
            case SessionType.BREAK:
                self.reset_timer()
                self.plyer_nortify()
            case _:
                LOGGER.error(f'{self.session=} does not define.')

    def update_ui(self) -> None:
        """Update the UI.
        """
        status = self.query_one(selector='#status', expect_type=Static)
        status.update(content=f'{self.status_text[self.session]}')
        status.styles.border = self.status_border[self.session]
        if self.session_time:
            hh, mm, ss, _ = sec_to_hms(time=self.session_time)
        else:
            hh, mm, ss = 0, 0, 0
        digits = self.query_one(selector='#session_time', expect_type=Digits)
        digits.update(value=f'{hh:02}:{mm:02}:{ss:02}')
        digits.styles.border = self.status_border[self.session]

    def plyer_nortify(self) -> None:
        """Use `plyer` to send OS notifications.
        """
        match self.session:
            case SessionType.WORK:
                msg = (
                    'Your working time is over. \n'
                    'Please take a break!'
                )
            case SessionType.BREAK:
                msg = (
                    'Your break time is over. \n'
                    'Get started!'
                )
            case _:
                msg = None

        if msg:
            self.note.notify(
                app_name=self.TITLE,
                app_icon=ICON_PATH,
                title='Notification',
                message=msg,
            )


@save_params_log(fname=f'log_params_{Path(__file__).stem}.yaml')
@process_time(print_func=LOGGER.info)
def main(params: dict[str, Any]) -> dict[str, Any]:
    """Main.

    This function is decorated by ``@save_params_log`` and ``@process_time``.

    Args:
        params (dict[str, Any]): parameters.

    Returns:
        dict[str, Any]: parameters.
    """
    app = MainApp()
    app.run()
    return params


def set_params() -> dict[str, Any]:
    """Sets the command line arguments and file parameters.

    *   Set only common parameters as command line arguments.
    *   Other necessary parameters are set in the file parameters.
    *   Use a yaml file. (:func:`lib.common.file.load_yaml`)

    Returns:
        dict[str, Any]: parameters.

    .. attention::

        Command line arguments are overridden by file parameters.
        This means that if you want to set everything using file parameters,
        you don't necessarily need to use command line arguments.
    """
    # set the command line arguments.
    parser = argparse.ArgumentParser()
    # log handler (idx=0: stream handler, idx=1: file handler)
    # (True: set handler, False: not set handler)
    parser.add_argument('--handler', default=[True, True], type=bool, nargs=2)
    # log level (idx=0: stream handler, idx=1: file handler)
    # (DEBUG: 10, INFO: 20, WARNING: 30, ERROR: 40, CRITICAL: 50)
    choices = [10, 20, 30, 40, 50]
    parser.add_argument('--level', default=[20, 20], type=int, nargs=2, choices=choices)
    # file path (parameters)
    parser.add_argument('--param', default='param/param.yaml', type=str)
    # directory path (data save)
    parser.add_argument('--result', default='result', type=str)

    params = vars(parser.parse_args())

    # set the file parameters.
    fpath = Path(params[K.PARAM])
    if K.PARAM in params and fpath.is_file():
        params.update(load_yaml(fpath=fpath))

    return params


if __name__ == '__main__':
    # set the parameters.
    params = set_params()
    # set the logging configuration.
    PARAM_LOG.HANDLER[PARAM_LOG.SH] = params[K.HANDLER][0]
    PARAM_LOG.HANDLER[PARAM_LOG.FH] = params[K.HANDLER][1]
    PARAM_LOG.LEVEL[PARAM_LOG.SH] = params[K.LEVEL][0]
    PARAM_LOG.LEVEL[PARAM_LOG.FH] = params[K.LEVEL][1]
    SetLogging(logger=LOGGER, param=PARAM_LOG)

    if params.get(K.RESULT):
        Path(params[K.RESULT]).mkdir(parents=True, exist_ok=True)

    main(params=params)
