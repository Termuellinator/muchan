from enum import Enum

from .utils import MetaSingleton


class LevelEnum(Enum):
    """Enum defining the different log severities"""

    info = "INFO"
    critical = "CRITICAL"
    error = "ERROR"
    warning = "WARNING"


class Logging(metaclass=MetaSingleton):
    """Write events with different severities to a logfile

    Args:
        file_name (Path): A path object pointing to the desired log file.

    Methods
    """

    def __init__(self, file_name: str) -> None:
        self.file_name = file_name

    def _write_log(self, lvl: LevelEnum, msg: str) -> None:
        """Write to the log file

        Args:
            lvl (LevelEnum): severity level of the event
            msg (str): description of the event
        """
        with open(self.file_name, "a") as log_file:
            log_file.write(f"[{lvl.name}] {msg}\n")  # [CRITICAL] message goes here

    def info(self, msg: str) -> None:
        """Write an event with severity 'INFO'

        Args:
            msg (str): The log-message to be written after '[INFO]'
        """
        self._write_log(LevelEnum.info, msg)

    def critical(self, msg: str) -> None:
        """Write an event with severity 'CRITICAL'

        Args:
            msg (str): The log-message to be written after '[CRITICAL]'
        """
        self._write_log(LevelEnum.critical, msg)

    def error(self, msg: str) -> None:
        """Write an event with severity 'ERROR'

        Args:
            msg (str): The log-message to be written after '[ERROR]'
        """
        self._write_log(LevelEnum.error, msg)

    def warning(self, msg: str) -> None:
        """Write an event with severity 'WARNING'

        Args:
            msg (str): The log-message to be written after '[WARNING]'
        """
        self._write_log(LevelEnum.warning, msg)
