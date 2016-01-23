# -*- coding: utf-8 -*-

import pytest
from thefuck.shells import Bash


@pytest.mark.usefixtures('isfile')
class TestBash(object):
    @pytest.fixture
    def shell(self):
        return Bash()

    @pytest.fixture(autouse=True)
    def Popen(self, mocker):
        mock = mocker.patch('thefuck.shells.bash.Popen')
        mock.return_value.stdout.read.return_value = (
            b'alias fuck=\'eval $(thefuck $(fc -ln -1))\'\n'
            b'alias l=\'ls -CF\'\n'
            b'alias la=\'ls -A\'\n'
            b'alias ll=\'ls -alF\'')
        return mock

    @pytest.mark.parametrize('before, after', [
        ('pwd', 'pwd'),
        ('fuck', 'eval $(thefuck $(fc -ln -1))'),
        ('awk', 'awk'),
        ('ll', 'ls -alF')])
    def test_from_shell(self, before, after, shell):
        assert shell.from_shell(before) == after

    def test_to_shell(self, shell):
        assert shell.to_shell('pwd') == 'pwd'

    @pytest.mark.parametrize('entry, entry_utf8', [
        ('ls', 'ls\n'),
        (u'echo café', 'echo café\n')])
    def test_put_to_history(self, entry, entry_utf8, builtins_open, shell):
        shell.put_to_history(entry)
        builtins_open.return_value.__enter__.return_value. \
            write.assert_called_once_with(entry_utf8)

    def test_and_(self, shell):
        assert shell.and_('ls', 'cd') == 'ls && cd'

    def test_get_aliases(self, shell):
        assert shell.get_aliases() == {'fuck': 'eval $(thefuck $(fc -ln -1))',
                                       'l': 'ls -CF',
                                       'la': 'ls -A',
                                       'll': 'ls -alF'}

    def test_app_alias(self, shell):
        assert 'alias fuck' in shell.app_alias('fuck')
        assert 'alias FUCK' in shell.app_alias('FUCK')
        assert 'thefuck' in shell.app_alias('fuck')
        assert 'TF_ALIAS=fuck PYTHONIOENCODING' in shell.app_alias('fuck')
        assert 'PYTHONIOENCODING=utf-8 thefuck' in shell.app_alias('fuck')

    def test_get_history(self, history_lines, shell):
        history_lines(['ls', 'rm'])
        assert list(shell.get_history()) == ['ls', 'rm']
