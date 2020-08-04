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
    

    $jdata stock --symbol STOCK1 -f yyyy-mm-dd -t yyyy-mm-dd --o file_name.csv
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
    
    

    
    

if __name__ == "__main__":
    cli()


