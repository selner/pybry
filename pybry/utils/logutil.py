import functools
import logging
import time
from pprint import pformat

import loguru


class InterceptHandler(logging.Handler):
	def emit(self, record):
		# Get corresponding Loguru level if it exists
		try:
			level = logger.level(record.levelname).name
		except ValueError:
			level = record.levelno
		
		# Find caller from where originated the logged message
		frame, depth = logging.currentframe(), 2
		while frame.f_code.co_filename == logging.__file__:
			frame = frame.f_back
			depth += 1
		
		logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def catch_exception(*, logr=None):
	def wrapper(func):
		name = func.__name__
		logger_ = logr or loguru.logger
		
		@functools.wraps(func)
		def wrapped(*args, **kwargs):
			try:
				return func(*args, **kwargs)
			except Exception as ex:
				logger_.exception("Exception thrown in {} (except={}", name, ex)
				raise
		
		return wrapped
	
	return wrapper


def logger_wraps(*, entry=True, shouldexit=True, level="DEBUG"):
	def wrapper(func):
		name = func.__name__
		
		@functools.wraps(func)
		def wrapped(*args, **kwargs):
			logger_ = logger.opt(depth=1)
			if entry:
				logger_.log(level, "Entering '{}' (args={}, kwargs={})", name, args, kwargs)
			result = func(*args, **kwargs)
			if shouldexit:
				logger_.log(level, "Exiting '{}' (result={})", name, result)
			return result
		
		return wrapped
	
	return wrapper


def timeit(func):
	def wrapped(*args, **kwargs):
		start = time.time()
		result = func(*args, **kwargs)
		end = time.time()
		logger.debug("Function '{}' executed in {:f} s", func.__name__, end - start)
		return result
	
	return wrapped


from twisted.python import log
import sys

observer = log.PythonLoggingObserver()
observer.start()
# For scripts
# inthandler = InterceptHandler()

fmt = "<level>{message:<80} | {level:^5}</level> | <cyan>{name:^15} | {function:^10} | {line:^3}</cyan>"

config = {
	"handlers": [
		#        {"sink": sys.stdout, "format": "{time} - {message}", "enqueue": True},
		# {"sink":    sys.stdout,
		#  "format":  "{time:YYYYMMDD_HHmmss}  | {level: <5} | {message} | {name: ^15} | {function: ^15} | {line: >3} ",
		#  "enqueue": True},
		{"sink":    sys.stdout,
		 "format":  fmt,
		 "enqueue": True},
		{"sink":      "file.log", "format": fmt,
		 "serialize": True, "enqueue": True}
	],
	"extra":    {"user": "someone"}
}

loguru.logger.configure(**config)
loguru.logger.opt(exception=True)
loguru.logger.opt = functools.partial(loguru.logger.opt, exception=True)
# logger = logger.opt(colors=True)
# logger.opt = partial(logger.opt, colors=True)

# If Loguru fails to retrieve the proper "name" value, assign it manually
logger = loguru.logger.patch(lambda record: record.update(name=__name__))


def ppformat(obj):
    if obj:
        return pformat(obj, indent=0 )
    return ""

