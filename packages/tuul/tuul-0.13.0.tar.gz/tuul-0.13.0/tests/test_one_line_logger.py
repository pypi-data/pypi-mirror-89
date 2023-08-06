#!/usr/bin/env python

"""Tests for `tuul` package."""
import logging
import unittest
from unittest.mock import patch

import tuul


class TestOneLineLogger(unittest.TestCase):
    def test_print_only_one_line(self):
        with self.assertLogs(level="DEBUG") as cm:
            logger = tuul.one_line_logger.get_logger()
            logger.debug("d1\nd2\n")
            logger.info("i1\ni2\n")
            logger.error("e1\ne2\n")
            try:
                1 / 0
            except ZeroDivisionError:
                logger.exception("x1\nx2\n")
        self.assertEqual(len(cm.output), 4, cm.output)
        self.assertEqual(len(cm.output[0].splitlines()), 1, cm.output[0])
        self.assertEqual(len(cm.output[1].splitlines()), 1, cm.output[0])
        self.assertEqual(len(cm.output[2].splitlines()), 1, cm.output[0])

    def test_control_logging_level(self):
        with self.assertLogs(level="ERROR") as cm:
            logger = tuul.one_line_logger.get_logger(logging_level=logging.ERROR)
            logger.debug("d1\nd2\n")
            logger.info("i1\ni2\n")
            logger.error("e1\ne2\n")
            try:
                1 / 0
            except ZeroDivisionError:
                logger.exception("x1\nx2\n")
        self.assertEqual(len(cm.output), 2, cm.output)

    def test_set_aws_logger_level(self):
        for name in ["boto", "urllib3", "s3transfer", "boto3", "botocore", "nose"]:
            with self.assertLogs(level="DEBUG") as cm:
                logger = tuul.one_line_logger.get_logger()
                logger.debug("print me")

                l1 = logging.getLogger(name)
                l1.debug("I should not be printed")
                l1.info("I should not be printed")
                l1.critical("I should be printed")
            self.assertEqual(2, len(cm.output), cm.output)

        for name in ["boto", "urllib3", "s3transfer", "boto3", "botocore", "nose"]:
            with self.assertLogs(level="DEBUG") as cm:
                logger = tuul.one_line_logger.get_logger(aws_logging_level=logging.INFO)
                logger.debug("print me")
                l1 = logging.getLogger(name)
                l1.debug("I should not be printed")
                l1.info("I should be printed")
                l1.critical("I should be printed")
            self.assertEqual(3, len(cm.output), cm.output)

    @staticmethod
    def foo_raises(record):
        raise RuntimeError("boom")

    @patch.object(
        tuul.one_line_logger.OneLineFormatter,
        "_handle_non_exists_aws_request_id",
        foo_raises,
    )
    def test_error_raised_in_formatter(self):
        with self.assertLogs(level="INFO") as cm:
            logger = tuul.one_line_logger.get_logger(logging_level=logging.DEBUG)
            logger.info("i1\ni2\n")
        self.assertEqual(len(cm.output), 1, cm.output)
        self.assertTrue("MONITOR_THIS " in cm.output[0], cm.output[0])
