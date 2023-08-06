import os
import pytest
from . import helpers

class TestChooseFile:
    def test_can_return_path_if_file_exists(self, tmpdir):
        the_file_path = self.write_sample(tmpdir, 'test.test')

        result = helpers.choose_file([self.build_path_template(tmpdir)], "test.test")
        assert result
        assert the_file_path == result

    def test_can_return_none_if_file_does_not_exist(self, tmpdir):
        result = helpers.choose_file([self.build_path_template(tmpdir)], 'test')
        assert (not result)

    def test_can_return_correct_path_if_file_exists_when_have_multi_templates(self, tmpdir):
        the_file_path = self.write_sample(tmpdir, 'test.test')

        result = helpers.choose_file(['./?', self.build_path_template(tmpdir)], 'test.test')
        assert result
        assert the_file_path == result

    @staticmethod
    def build_path_template(path):
        return os.path.join(path, '?')

    @staticmethod
    def write_sample(path, filename):
        fpath = os.path.join(path, filename)
        with open(fpath, 'w+') as f:
            f.write("sample")
        return fpath


class TextRecorder(object):
    def __init__(self):
        self.text = ""

    def record(self, x):
        self.text += x


class TestCheckBinary:
    def test_can_find_echo(self):
        """
        This test depends on the fact that most system have a binary "echo"
        """
        assert helpers.check_binary("echo")


class TestShell:
    def test_can_run_command(self):
        """
        This test depends on a fact that most system have a binary "echo"
        """
        if not helpers.check_binary("echo"):
            pytest.skip("could not found binary echo for this test")
        recorder = TextRecorder()

        helpers.shell(["echo", "test"], printf=recorder.record)

        lines = list(filter(lambda x: x != '', recorder.text.split(os.linesep)))
        assert len(lines) == 2
        assert lines[0].startswith('$')
        assert "echo test" in lines[0]
        assert lines[1] == "test"
