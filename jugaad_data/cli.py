import os
import click
from datetime import date, datetime, timedelta
from concurrent.futures import ThreadPoolExecutor
import requests
from jugaad_data import nse



@click.group()
def cli():
    """ This is a command line tool to download stock market data to csv files.
        
    """  

def bhavcopy_wrapper(bhavcopy_function, dt, dest):
    try:
        bhavcopy_function(dt, dest)
        return True
    except:
        return False
    


@cli.command("bhavcopy")
@click.option("--dest", "-d", help="Destination directory path", required=True, type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.option("--from", "-f", "from_", help="From date", type=click.DateTime(["%Y-%m-%d"])) 
@click.option("--to", "-t", help="To date", type=click.DateTime(["%Y-%m-%d"]))
@click.option("--fo/--no-fo", help="Downloads F&O bhavcopy", default=False, type=bool)
@click.option("--idx/--no-idx", help="Downloads Index bhavcopy", default=False, type=bool)
@click.option("--full/--no-full", help="Full Bhavcopy", default=False, type=bool)
def bhavcopy(from_, to, dest, fo, idx, full):
    """Downloads bhavcopy from NSE's website
        
        Download today's bhavcopy
        
        $ jdata bhavcopy -d /path/to/dir

        Download bhavcopy for a date
        
        $ jdata bhavcopy -d /path/to/dir -f 2020-01-01

        Downlad bhavcopy for a date range

        $ jdata bhavcopy -d /path/to/dir -f 2020-01-01 -t 2020-02-01
        
    """ 
        
    downloader = nse.bhavcopy_save
    if full:
        downloader = nse.full_bhavcopy_save
    if idx:
        downloader = nse.bhavcopy_index_save
    if fo:
        downloader = nse.bhavcopy_fo_save
        
    if not from_:
        dt = date.today()
        try:
            path = downloader(dt, dest)
            click.echo("Saved to : " + path)  
        except requests.exceptions.ReadTimeout:
            click.echo("""Error: Timeout while downloading, This may be due to-
        \b1. Bad internet connection
        \b2. Today is holiday or file is not ready yet""", err=True)
    
    if from_ and not to:
        # if from_ provided but not to
        dt = from_.date()
        try:
            path = downloader(dt, dest)
            click.echo("Saved to : " + path)  
        except requests.exceptions.ReadTimeout:
            click.echo("""Error: Timeout while downloading, This may be due to-
        \b1. Bad internet connection
        \b2. {} is holiday or file is not ready yet""".format(dt), err=True)
    
    if from_ and to:
        failed_downloads = []
        date_range = []
        delta = to - from_
        for i in range(delta.days + 1):
            dt = from_ + timedelta(days=i)
            w = dt.weekday()
            if w not in [5,6]:
                date_range.append(dt.date())
        
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(bhavcopy_wrapper, downloader, dt, dest) for dt in date_range]
            
            with click.progressbar(futures, label="Downloading Bhavcopies") as bar:
                for i, future in enumerate(bar):
                    result = future.result()
                    if not result:
                        failed_downloads.append(date_range[i])
        
             
        """
            for dt in bar:
                try:
                    nse.bhavcopy_save(dt, dest)    
                except requests.exceptions.ReadTimeout:
                    failed_downloads.append(dt)
        """
        click.echo("Saved to : " + dest)
        if failed_downloads:
            click.echo("Failed to download for below dates, these might be holidays, please check -") 
            for dt in failed_downloads:
                click.echo(dt)
        
@cli.command("stock")
@click.option("--symbol", "-s", required=True, help="Stock symbol")
@click.option("--from", "-f", "from_", required=True, help="From date - yyyy-mm-dd")
@click.option("--to", "-t", required=True, help="From date - yyyy-mm-dd")
@click.option("--series", "-S", default="EQ", show_default=True, help="Series - EQ, BE etc.")
@click.option("--output", "-o", default="", help="Full path for output file")
def stock(symbol, from_, to, series, output):
    """Download historical stock data 
    

    $jdata stock --symbol STOCK1 -f yyyy-mm-dd -t yyyy-mm-dd -o file_name.csv
    """
    import traceback
    from_date = datetime.strptime(from_, "%Y-%m-%d").date()
    to_date = datetime.strptime(to, "%Y-%m-%d").date()
    try:
        o = nse.stock_csv(symbol, from_date, to_date, series, output, show_progress=True)
    except Exception as e:
        print(e)
        traceback.print_exc()
    click.echo("\nSaved file to : {}".format(o))
    
@cli.command("index")
@click.option("--symbol", "-s", required=True, help="Stock symbol")
@click.option("--from", "-f", "from_", required=True, help="From date - yyyy-mm-dd")
@click.option("--to", "-t", required=True, help="From date - yyyy-mm-dd")
@click.option("--output", "-o", default="", help="Full path for output file")
def index(symbol, from_, to, output):
    """Download historical index data 
    

    $jdata index --symbol "NIFTY 50" -f yyyy-mm-dd -t yyyy-mm-dd -o file_name.csv
    """
    import traceback
    from_date = datetime.strptime(from_, "%Y-%m-%d").date()
    to_date = datetime.strptime(to, "%Y-%m-%d").date()
    try:
        o = nse.index_csv(symbol, from_date, to_date, output, show_progress=True)
    except Exception as e:
        print(e)
        traceback.print_exc()
    click.echo("\nSaved file to : {}".format(o))
    
@cli.command("derivatives")
@click.option("--symbol", "-s", required=True, help="Stock/Index symbol")
@click.option("--from", "-f", "from_", required=True, help="From date - yyyy-mm-dd")
@click.option("--to", "-t", required=True, help="To date - yyyy-mm-dd")
@click.option("--expiry", "-e", required=True, help="Expiry date - yyyy-mm-dd")
@click.option("--instru", "-i", required=True, help="""FUTSTK - Stock futures, FUTIDX - Index Futures,\tOPTSTK - Stock Options, OPTIDX - Index Options""")
@click.option("--price", "-p", help="Strike price (Only for OPTSTK and OPTIDX)")
@click.option("--ce/--pe", help="--ce for call and --pe for put (Only for OPTSTK and OPTIDX)")
@click.option("--output", "-o", default="", help="Full path of output file")
def stock(symbol, from_, to, expiry, instru, price, ce, output):
    """Sample usage-

    Download stock futures-
    
    \b 
    jdata derivatives -s SBIN -f 2020-01-01 -t 2020-01-30 -e 2020-01-30 -i FUTSTK -o file_name.csv
    
    Download index futures-

    \b
    jdata derivatives -s NIFTY -f 2020-01-01 -t 2020-01-30 -e 2020-01-30 -i FUTIDX -o file_name.csv

    Download stock options-

    \b
    jdata derivatives -s SBIN -f 2020-01-01 -t 2020-01-30 -e 2020-01-30 -i OPTSTK -p 330 --ce -o file_name.csv

    Download index options-

    \b
    jdata derivatives -s NIFTY -f 2020-01-01 -t 2020-01-30 -e 2020-01-23 -i OPTIDX -p 11000 --pe -o file_name.csv


    """
    import traceback
    import sys
    from_date = datetime.strptime(from_, "%Y-%m-%d").date()
    to_date = datetime.strptime(to, "%Y-%m-%d").date()
    expiry = datetime.strptime(expiry, "%Y-%m-%d").date()
    if "OPT" in instru:
        if ce:
            ot = "CE"
        else:
            ot = "PE"
        
        if price:
            price = float(price) 
    else:
        ot = None
    o = nse.derivatives_csv(symbol, from_date, to_date, expiry, instru, price, ot, 
                                output, show_progress=True)

    click.echo("\nSaved file to : {}".format(o))
 
    
    

if __name__ == "__main__":
    cli()


