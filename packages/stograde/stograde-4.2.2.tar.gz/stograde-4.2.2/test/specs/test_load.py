import os

import pytest

from stograde.specs import load_specs
from stograde.specs.load import check_for_spec_updates
from test.utils import git, touch

_dir = os.path.dirname(os.path.realpath(__file__))


@pytest.mark.datafiles(os.path.join(_dir, 'fixtures'))
def test_load_specs(datafiles):
    specs = load_specs(['hw1', 'hw2', 'hw3'], str(datafiles), skip_spec_update=True)

    assert len(specs) == 3


@pytest.mark.datafiles(os.path.join(_dir, 'fixtures'))
def test_load_specs_failed_update(datafiles, capsys):
    specs = load_specs(['hw1', 'hw2', 'hw3'], str(datafiles), skip_spec_update=False)

    assert len(specs) == 3

    _, err = capsys.readouterr()

    assert err == 'Error fetching specs\ngit log failed\n'


def test_check_for_spec_updates_update_found(tmpdir, capsys):
    with tmpdir.as_cwd():
        git('init')
        git('config', 'user.email', 'an_email@email_provider.com')
        git('config', 'user.name', 'Some Random Name')
        touch('hw1.yaml')
        git('add', 'hw1.yaml')
        git('commit', '-m', '"Add hw1"')
        git('branch', 'origin/master')
        git('checkout', 'origin/master')
        touch('hw2.yaml')
        git('add', 'hw2.yaml')
        git('commit', '-m', '"Create hw2"')
        git('checkout', 'master')

        check_for_spec_updates(os.getcwd())

    _, err = capsys.readouterr()

    assert err == 'Error fetching specs\nSpec updates found - Updating\n'


def test_check_for_spec_updates_no_update(tmpdir, capsys):
    with tmpdir.as_cwd():
        git('init')
        git('config', 'user.email', 'an_email@email_provider.com')
        git('config', 'user.name', 'Some Random Name')
        touch('hw1.yaml')
        git('add', 'hw1.yaml')
        git('commit', '-m', '"Add hw1"')
        git('branch', 'origin/master')

        check_for_spec_updates(os.getcwd())

    _, err = capsys.readouterr()

    assert err == 'Error fetching specs\n'
