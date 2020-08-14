from pyfakefs.fake_filesystem_unittest import TestCase
import csv
from click.testing import CliRunner
from appdirs import user_cache_dir
from jugaad_data.cli import cli

class TestCli(TestCase):
    def setUp(self):
        """
        FakeFS creates a fake file systems and in process looses the CA Certs
        Which fails the test while running stocks
        To fix that CA certificates will be read and then placed back
        """
        import certifi
        self.path = certifi.where()
        with open(self.path) as fp:
            self.certs = fp.read()
        self.setUpPyfakefs()        
        ## Restoring the CA certs
        self.fs.create_file(self.path)
        with open(self.path, "w") as fp:
            fp.write(self.certs)

    def test_stock_cli(self):
        symbol = "RELIANCE"
        from_ = "2020-07-01"
        to = "2020-07-07"
        output = "/tmp/abc.csv"
        runner = CliRunner()
        cmd = "stock -s {} -f {} -t {} -o {}".format(symbol, from_, to, output)
        result = runner.invoke(cli, cmd.split())
        print(cmd)
        assert result.exit_code == 0
        with open(output) as fp:
            reader = csv.reader(fp)
            rows = list(reader)
            assert rows[1][0] == to
            assert rows[-1][0] == from_
            assert len(rows) == 6
        
        from_ = "2019-07-01"
        to = "2020-07-07"
        output = "/tmp/abc.csv"
        runner = CliRunner()
        cmd = "stock -s {} -f {} -t {} -o {}".format(symbol, from_, to, output)
        result = runner.invoke(cli, cmd.split())
        print(cmd)
        assert result.exit_code == 0
        with open(output) as fp:
            reader = csv.reader(fp)
            rows = list(reader)
            assert rows[1][0] == to
            assert rows[-1][0] == from_
            assert len(rows) > 200 and len(rows) < 260
    
