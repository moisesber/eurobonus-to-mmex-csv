import click

@click.command()
def cli():
    """Example script."""
    click.echo('Hello World!')


@click.command()
@click.option('--file', help='Comma separated file from eurobonus mastercard', required=True)
def eurobonus(file):
    click.echo("Need to call script with {} as argument".format(file))
    

#from argparse import ArgumentParser
#
#
#def main():
#    parser = ArgumentParser(prog='cli')
#    parser.add_argument('name', help="The user's name.")
#    args = parser.parse_args()
#    print("Hello, %s!" % args.name)
#
#
#if __name__ == '__main__':
#    main()
