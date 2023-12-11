import pytest
from nextpy.utils.logger import Logger , Log
import logging
import time

class TestLogger:
    def test_initialization(self):
        logger = Logger(save_logs=False, verbose=False)
        assert not logger.verbose
        assert not logger.save_logs

    def test_logging(self):
        logger = Logger(save_logs=False, verbose=False)
        logger.log("Test message", level=logging.INFO)
        assert len(logger.logs) == 1
        assert logger.logs[0].msg == "Test message"

    def test_time_calculation(self):
        logger = Logger(save_logs=False, verbose=False)
        time.sleep(1)
        logger.log("Test message", level=logging.INFO)
        assert logger.logs[0].time >= 0

    def test_verbose_property(self):
        logger = Logger(save_logs=False, verbose=False)
        assert not logger.verbose
        logger.verbose = True
        assert logger.verbose

    def test_save_logs_property(self):
        logger = Logger(save_logs=False, verbose=False)
        assert not logger.save_logs
        logger.save_logs = True
        assert logger.save_logs

    def test_logs_retrieval(self):
        logger = Logger(save_logs=False, verbose=False)
        logger._logs.clear()  # Clear logs before test
        logger.log("Test message", level=logging.INFO)
        logs = logger.logs
        assert len(logs) == 1 

    def test_log_format(self):
        logger = Logger(save_logs=False, verbose=False)
        logger.log("Test message", level=logging.INFO)
        log_entry = logger.logs[0]
        assert isinstance(log_entry, Log)  
        assert log_entry.msg == "Test message"
        assert isinstance(log_entry.time, float)
        assert isinstance(log_entry.level, str)


    def test_info_level_logging(self):
        logger = Logger(save_logs=False, verbose=False)
        logger.log("Info message", level=logging.INFO)
        assert logger.logs[-1].msg == "Info message"
        assert logger.logs[-1].level == "INFO"

    def test_warning_level_logging(self):
        logger = Logger(save_logs=False, verbose=False)
        logger.log("Warning message", level=logging.WARNING)
        assert logger.logs[-1].msg == "Warning message"
        assert logger.logs[-1].level == "WARNING"

    def test_error_level_logging(self):
        logger = Logger(save_logs=False, verbose=False)
        logger.log("Error message", level=logging.ERROR)
        assert logger.logs[-1].msg == "Error message"
        assert logger.logs[-1].level == "ERROR"

    def test_debug_level_logging(self):
        logger = Logger(save_logs=False, verbose=False)
        logger.log("Debug message", level=logging.DEBUG)
        assert logger.logs[-1].msg == "Debug message"
        assert logger.logs[-1].level == "DEBUG"