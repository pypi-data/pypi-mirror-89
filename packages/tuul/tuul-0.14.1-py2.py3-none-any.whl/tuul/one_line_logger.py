import logging
import traceback


# noinspection PyPep8Naming
class OneLineFormatter(logging.Formatter):
    def formatException(self, exc_info):
        """
        Format an exception so that it prints on a single line.
        """
        result = super(OneLineFormatter, self).formatException(exc_info)
        return repr(result)  # or format into one line however you want to

    def format(self, record):
        try:
            # noinspection PyTypeChecker
            self._handle_non_exists_aws_request_id(record)

            if record.exc_info:
                return (
                    super(OneLineFormatter, self).format(record).replace("\n", "    ")
                    + "\n"
                )

            record.message = record.getMessage()
            # noinspection PyUnresolvedReferences
            if self.usesTime():
                record.asctime = self.formatTime(record, self.datefmt)

            s = self.formatMessage(record).replace("\n", "  |  ") + "\n"
            return s
        except Exception:
            e_msg, r = self.get_error_context(record)
            return (
                f"MONITOR_THIS failed formatting record {r} {e_msg}".replace(
                    "\n", "  |  "
                )
                + "\n"
            )

    @staticmethod
    def get_error_context(record):
        try:
            r = f"{record}"
        except Exception:  # pragma: no cover
            r = "could not parse record to string"  # pragma: no cover
        try:
            e_msg = traceback.format_exc()
        except Exception:  # pragma: no cover
            e_msg = ""  # pragma: no cover
        return e_msg, r

    @staticmethod
    def _handle_non_exists_aws_request_id(record):
        try:
            record.aws_request_id
        except AttributeError:
            record.aws_request_id = " "


def get_logger(logging_level=logging.DEBUG, aws_logging_level=logging.WARNING):
    for name in ["boto", "urllib3", "s3transfer", "boto3", "botocore", "nose"]:
        logging.getLogger(name).setLevel(aws_logging_level)
    logging_level = logging_level
    logging.basicConfig(level=logging_level)
    logger = logging.getLogger()
    logger.setLevel(logging_level)

    f = OneLineFormatter(
        "[%(levelname)s]\t%(asctime)s.%(msecs)dZ\t%(aws_request_id)s\t%(message)s\n"
    )
    if logger.hasHandlers():
        if logger.handlers[0]:
            logger.handlers[0].setFormatter(f)
    logger.propagate = False
    return logger
