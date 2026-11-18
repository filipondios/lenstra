import json
import subprocess
import sys
from pathlib import Path

import pytest

import lenstra

SCRIPT = Path(__file__).resolve().parents[1] / 'lenstra.py'


def test_entry_point_subprocess():
    ok = subprocess.run([sys.executable, str(SCRIPT), '-n', '561'],
                        capture_output=True, text=True)
    assert ok.returncode == 0
    assert '561 = 3 * 11 * 17' in ok.stdout

    mal = subprocess.run([sys.executable, str(SCRIPT), '-n', '1'],
                         capture_output=True, text=True)
    assert mal.returncode == 2
    assert '--number must be >= 2' in mal.stderr

    incomplete = subprocess.run(
        [sys.executable, str(SCRIPT), '-n', '4951760154835678088235319297',
         '--b1', '2', '--curves', '1'],
        capture_output=True, text=True)
    assert incomplete.returncode == 1
    assert 'Could not factorize' in incomplete.stdout


def test_invalid_input(monkeypatch):
    cases = [
        ['lenstra.py', '-n', '1'],
        ['lenstra.py', '-n', '15', '--curves', '0'],
        ['lenstra.py', '-n', '15', '-b', 'foo'],
        ['lenstra.py', '-n', 'xyz'],
        ['lenstra.py', '-n', '15', '--rounds', '0'],
    ]
    for argv in cases:
        monkeypatch.setattr('sys.argv', argv)
        with pytest.raises(SystemExit) as result:
            lenstra.main()
        assert result.value.code == 2


def test_prime_number(monkeypatch, capsys):
    monkeypatch.setattr('sys.argv', ['lenstra.py', '-n', '104729'])
    assert lenstra.main() == 0
    assert '104729 is prime (Miller-Rabin)' in capsys.readouterr().out


def test_factor_found(monkeypatch, capsys):
    monkeypatch.setattr('sys.argv', ['lenstra.py', '-n', '15'])
    assert lenstra.main() == 0
    assert capsys.readouterr().out.strip() == (
        '15 = 3 * 5  (composite, verified with Miller-Rabin)')


def test_json(monkeypatch, capsys):
    monkeypatch.setattr('sys.argv', ['lenstra.py', '-n', '561', '--json'])
    assert lenstra.main() == 0
    data = json.loads(capsys.readouterr().out)
    assert data['number'] == 561
    assert data['prime'] is False
    assert data['factors'] == {'3': 1, '11': 1, '17': 1}
    assert data['seconds'] >= 0


def test_json_prime(monkeypatch, capsys):
    monkeypatch.setattr('sys.argv', ['lenstra.py', '-n', '104729', '--json'])
    assert lenstra.main() == 0
    data = json.loads(capsys.readouterr().out)
    assert data['prime'] is True
    assert data['factors'] == {'104729': 1}


def test_reproducible_seed(monkeypatch, capsys):
    argv = ['lenstra.py', '-n', '15', '--seed', '7', '-v']
    monkeypatch.setattr('sys.argv', argv)
    assert lenstra.main() == 0
    first = capsys.readouterr().out

    monkeypatch.setattr('sys.argv', argv)
    assert lenstra.main() == 0
    second = capsys.readouterr().out
    assert first == second
