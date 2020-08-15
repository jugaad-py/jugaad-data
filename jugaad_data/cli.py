import click
from datetime import date, datetime
from jugaad_data import nse



@click.group()
def cli():
    """ This is a command line tool to download stock market data to csv files.
        
    """  

@cli.command("stock")
@click.option("--symbol", "-s", required=True)
@click.option("--from", "-f", "from_", required=True)
@click.option("--to", "-t", required=True)
@click.option("--series", "-S", default="EQ", show_default=True)
@click.option("--output", "-o", default="")
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
    
    
@cli.command("derivatives")
@click.option("--symbol", "-s", required=True)
@click.option("--from", "-f", "from_", required=True)
@click.option("--to", "-t", required=True)
@click.option("--expiry", "-e", required=True)
@click.option("--instru", "-i", required=True)
@click.option("--price", "-p")
@click.option("--ce/--pe")
@click.option("--output", "-o", default="")
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
    jdata derivatives -s SBIN -f 2020-01-01 -t 2020-01-30 -e 2020-01-30 -i OPTSTK -p 200 --ce -o file_name.csv

    Download stock options-

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
                                output)

    click.echo("\nSaved file to : {}".format(o))
 
    
    

if __name__ == "__main__":
    cli()


