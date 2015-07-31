import re
import subprocess
from thefuck.utils import replace_command


def match(command, script):
    return command.script.startswith('gulp')\
        and 'is not in your gulpfile' in command.stdout


def get_gulp_tasks():
    proc = subprocess.Popen(['gulp', '--tasks-simple'],
                            stdout=subprocess.PIPE)
    return [line.decode('utf-8')[:-1]
            for line in proc.stdout.readlines()]


def get_new_command(command, script):
    wrong_task = re.findall(r"Task '(\w+)' is not in your gulpfile",
                            command.stdout)[0]
    return replace_command(command, wrong_task, get_gulp_tasks())
