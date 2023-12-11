"""Logger class.

This class is used to log messages to the console and/or a file. It provides functionalities to log messages with different severity levels, and can also save these logs to a file if desired. The logs are stored internally and can be retrieved for inspection.

Example:
    ```python
    from nextpy.utils.logger import Logger 

    logger = Logger()
    logger.log("Hello, world!")
    # Output: 2021-08-01 12:00:00 [INFO] Hello, world!

    logger.logs
    # Returns: [Log(msg='Hello, world!', level='INFO', time=0.0, source='your_source')]
    ```

Attributes:
    _logs (List[Log]): A list of Log objects representing the log history.
    _logger (logging.Logger): The underlying logger instance.
    _verbose (bool): Flag to control verbosity (console logging).
    _last_time (float): Timestamp of the last logged message.

Methods:
    log: Logs a message at the specified level.
    verbose: Property to get/set verbosity of the logger.
    save_logs: Property to check if logs are being saved to a file and to enable/disable this feature.
    _calculate_time_diff: Calculates the time difference since the last log.
    _invoked_from: Identifies the source that invoked the logger.
"""

import inspect
import logging
import sys
import time
from typing import List, NamedTuple


class Log(NamedTuple):
    """Represents a log entry.
    

    Attributes:
        msg (str): The log message.
        level (str): The log level as a string.
        time (float): Time difference since the last log message.
        source (str): The source of the log message.
    """

    msg: str
    level: str
    time: float
    source: str

class Logger:
    """A Logger class for logging messages to the console and/or a file.

    Attributes:
        _logs (List[Log]): List of Log objects representing the log history.
        _logger (logging.Logger): The underlying logger instance.
        _verbose (bool): Flag to control verbosity (console logging).
        _last_time (float): Timestamp of the last logged message.
    """

    _logs: List[Log] = []
    _logger: logging.Logger = logging.getLogger(__name__)

    def __init__(self, save_logs: bool = True, verbose: bool = False):
        """Initializes the Logger instance.

        Args:
            save_logs (bool): If True, logs will be saved to a file. Default is True.
            verbose (bool): If True, logs will also be printed to the console. Default is False.
        """
        self._verbose = verbose
        self._last_time = time.time()
        self._configure_logger(save_logs, verbose)

    def _configure_logger(self, save_logs: bool, verbose: bool):
        """Configures the underlying logger with appropriate handlers.

        Args:
            save_logs (bool): If True, adds a FileHandler.
            verbose (bool): If True, adds a StreamHandler for console output.
        """
        handlers = []

        if save_logs:
            try:
                filename = "nextpy.log"
                handlers.append(logging.FileHandler(filename))
            except Exception as e:
                sys.stderr.write(f"Error configuring file logging: {e}\n")

        if verbose:
            handlers.append(logging.StreamHandler(sys.stdout))

        for handler in handlers:
            self._logger.addHandler(handler)

        self._logger.setLevel(logging.INFO)
        self._logger.propagate = False

    def log(self, message: str, level: int = logging.INFO):
        """Logs a message at the specified level.

        Args:
            message (str): The message to log.
            level (int): The logging level, e.g., logging.INFO, logging.ERROR. Default is logging.INFO.
        """
        level_name = logging.getLevelName(level)
        self._logger.log(level, message)

        log_entry = Log(
            msg=message,
            level=level_name,
            time=self._calculate_time_diff(),
            source=self._invoked_from()
        )
        self._logs.append(log_entry)

    def _invoked_from(self) -> str:
        """Identifies the source (class or function name) that invoked the logger.

        Returns:
            str: The name of the class or function that invoked the logger.
        """
        frames = inspect.stack()
        # Start from 1 to skip the current _invoked_from call
        for frame_info in frames[1:]:
            frame = frame_info.frame
            code = frame.f_code
            calling_function = code.co_name

            # Check if it's called from a class method
            if 'self' in frame.f_locals:
                calling_class = frame.f_locals['self'].__class__.__name__
                return f"{calling_class}.{calling_function}"

            # Alternatively, check for the class name in the method resolution order of the object (if any)
            elif 'cls' in frame.f_locals:
                calling_class = frame.f_locals['cls'].__name__
                return f"{calling_class}.{calling_function}"

            # If neither, return the function name
            return calling_function

        return "Unknown"

    def _calculate_time_diff(self) -> float:
        """Calculates the time difference since the last logged message.

        Returns:
            float: Time difference in seconds.
        """
        time_diff = time.time() - self._last_time
        self._last_time = time.time()
        return time_diff

    @property
    def logs(self) -> List[Log]:
        """Returns the list of logged messages."""
        return self._logs

    @property
    def verbose(self) -> bool:
        """Returns the verbosity setting of the logger."""
        return self._verbose

    @verbose.setter
    def verbose(self, verbose: bool):
        """Sets the verbosity of the logger.

        Args:
            verbose (bool): If True, enables console logging.
        """
        self._verbose = verbose
        if verbose:
            self._add_stream_handler()
        else:
            self._remove_handler_by_type(logging.StreamHandler)

    @property
    def save_logs(self) -> bool:
        """Checks if logs are being saved to a file."""
        return any(isinstance(handler, logging.FileHandler) for handler in self._logger.handlers)

    @save_logs.setter
    def save_logs(self, save_logs: bool):
        """Enables or disables saving logs to a file.

        Args:
            save_logs (bool): If True, logs will be saved to a file.
        """
        if save_logs:
            filename = "nextpy.log"
            self._logger.addHandler(logging.FileHandler(filename))
        else:
            self._remove_handler_by_type(logging.FileHandler)

    def _add_stream_handler(self):
        """Adds a StreamHandler to the logger for console output."""
        if not any(isinstance(handler, logging.StreamHandler) for handler in self._logger.handlers):
            self._logger.addHandler(logging.StreamHandler(sys.stdout))

    def _remove_handler_by_type(self, handler_type):
        """Removes a specific type of handler from the logger.

        Args:
            handler_type (type): The type of handler to remove.
        """
        for handler in self._logger.handlers[:]:
            if isinstance(handler, handler_type):
                self._logger.removeHandler(handler)

#TODO: Remove this and adjust the audio model
def get_logger(logger_name):
    """Configures and returns a custom logger with the given name.

    Args:
        logger_name (str): The name of the logger.

    Returns:
        Logger: Configured custom logger object.
    """
    # Create a new instance of your custom Logger

    custom_logger = Logger()

    return custom_logger
