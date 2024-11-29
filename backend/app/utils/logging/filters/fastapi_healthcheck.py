"""Filter out healthcheck endpoints"""
import logging
class FastAPIHealthCheckFilter(logging.Filter):
    """
    Filter out healthcheck endpoints
    """
    def filter(self, record: logging.LogRecord) -> bool:
        return record.args and len(record.args) >= 3 and record.args[2] != "/healthcheck"
