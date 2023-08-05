"""Console script for runinside."""
import sys
import click
try:
    import runinside.runinside as ri
except:
    import runinside as ri


@click.command()
@click.option('--source', '-s',
    type=click.Path(),
    help='Source file.  For multiples, use wildcards or a manifest.')
@click.option('--manifest', '-m',
    type=click.Path(exists=True),
    help='Manifest of files to copy into the container.')
@click.option('--destination', '-d',
    type=click.Path(),
    help='Destination directory inside the container.')
@click.option('--container', '-c',
    required=True,
    help='Target container by name or ID.')
@click.argument('execution', required=False)
def main(args=None, source='', manifest='', destination='/',
    container=None, execution=''):
    """
    runinside -s "*.py" -m manifestfile.txt -c mycontainer "ls | grep py"
    """
    if manifest:
        with open(manifest) as FHmanifest:
            sourcelist = FHmanifest.readlines()
    else:
        sourcelist = []
    if source:
        sourcelist += source
    if not destination:
        destination = '/'
    r = ri.runinside(container=container,
        destination=destination,
        manifest=sourcelist,
        command=execution)
    try:
        o = r.out.output.decode('utf-8')
        print(o)
    except:
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
