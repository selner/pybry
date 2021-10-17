import subprocess
import sys

from pybry.utils.logutil import logger


def do_shell_command(cmdline=None, cmdargs=None, logmsgkey="shell_execute", outputfile=None):
    outloc = None
    try:
        outloc = subprocess.PIPE if not outputfile else open(outputfile, "w")
        cmd = cmdargs if not cmdline else cmdline

        logger.warning(f'Running cmd: {cmd}...')
        p = subprocess.Popen(cmd, shell=True, stdout=outloc,
                             stderr=subprocess.STDOUT,
                             stdin=subprocess.PIPE)

        resp = p.communicate()[0]
        retcode = p.returncode

        if retcode < 0:
            logger.warning(f'{logmsgkey} was terminated by signal {-retcode}')
            logger.info(f'{logmsgkey} was terminated by signal {-retcode} (cmdline="{cmdline}")')
        elif retcode == 0:
            logger.info(f'{logmsgkey} completed.  RetCode=0; cmdline="{cmdline}')
        else:
            logger.info(f'{logmsgkey} call returned {-retcode} (cmdline="{cmdline}")')
            raise Exception(
                f'{logmsgkey} shell command ({cmdline}) returned a non-zero error code {-retcode}')

        return { 'return_code': retcode, 'response': resp }

    except OSError as e:
        logger.error(f'{logmsgkey} failed cmdline "{cmdline}": {sys.stderr} {e}', e)
    except Exception as e:
        logger.error(f'{logmsgkey} failed cmdline "{cmdline}": {e}', e)
    finally:
        if outloc and outloc != -1 and outloc != subprocess.STDOUT:
            outloc.close()
