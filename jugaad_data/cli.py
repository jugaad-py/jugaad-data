import click
from datetime import date, datetime
from jugaad_data import nse



@click.group()
def cli():
    """ This is a command line tool to download stock market data to csv files.
        
    """  

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


