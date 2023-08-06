# Tull - python toolkit

Working, well tested utilities to be shared, and duplicated over and over again.

## One line logger

Print each call on a single line, \
useful for monitoring and aggregation. \
Supporting AWS Lambda logging.

100% coverage

General usage:
```
import tuul
_logger = tuul.one_line_logger.get_logger()
_logger.debug("this would be printed")
_logger = tuul.one_line_logger.get_logger()

import logging
_logger = tuul.one_line_logger.get_logger(logging_level=logging.INFO)
_logger.debug("no print would be made")
_logger.info("this would be printed")
```

Specific AWS loggers:
```
import tuul
_logger = tuul.one_line_logger.get_logger()

import logging
logging.getLogger("boto3").debug("no print would be made")

_logger = tuul.one_line_logger.get_logger(aws_logging_level=logging.DEBUG)
logging.getLogger("boto3").debug("this would be printed")

```




# Credits

This package was created with Cookiecutter and the `audreyr/cookiecutter-pypackage` project template.

Cookiecutter: https://github.com/audreyr/cookiecutter

`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
