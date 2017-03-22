import pytest

from tests.utils import Command
from thefuck.rules.git_push_without_commits import (
    fix,
    get_new_command,
    match,
    refspec_does_not_match,
)

command = 'git push -u origin master'
expected_error = '''
error: src refspec master does not match any.
error: failed to push some refs to 'git@github.com:User/repo.git'
'''


@pytest.mark.parametrize('command', [Command(command, stderr=expected_error)])
def test_match(command):
    assert match(command)


@pytest.mark.parametrize('command, result', [(
    Command(command, stderr=expected_error),
    fix.format(command=command),
)])
def test_get_new_command(command, result):
    assert get_new_command(command) == result
