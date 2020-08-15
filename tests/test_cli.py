import warnings
import csv
from click.testing import CliRunner
from pyfakefs.fake_filesystem_unittest import TestCase
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
     
    def test_derivatives_cli(self):
        runner = CliRunner()
        output = "file_name.csv"
        cmd = "derivatives -s SBIN -f 2020-01-01 -t 2020-01-30 -e 2020-01-30 -i FUTSTK -o file_name.csv"
        result = runner.invoke(cli, cmd.split())
        assert result.exit_code == 0
        with open(output) as fp:
            reader = csv.reader(fp)
            rows = list(reader)
            assert rows[1][0] == "30-Jan-2020"
            assert rows[-1][0] == "01-JAN-2020"
            assert len(rows) == 23 
        cmd = "derivatives -s NIFTY -f 2020-01-01 -t 2020-01-23 -e 2020-01-23 -i OPTIDX --pe -p 12000 -o file_name.csv"
        result = runner.invoke(cli, cmd.split())
        assert result.exit_code == 0
        with open(output) as fp:
            reader = csv.reader(fp)
            rows = list(reader)
            assert rows[1][0] == "23-Jan-2020"
        warnings.warn("Test cannot be completed, NSE's website is providing only partial data") 
