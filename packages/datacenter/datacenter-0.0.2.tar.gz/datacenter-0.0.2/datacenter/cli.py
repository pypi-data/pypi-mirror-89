"""Console script for datacenter."""
import click


@click.command()
def main(args=None):
    """Console script for datacenter."""
    click.echo("Replace this message by putting your code into "
               "datacenter.cli.main")
    click.echo("See click documentation at https://click.palletsprojects.com/")
    return 0

@click.command()
def install_deps():
    pass


if __name__ == "__main__":
    import platform
    print(platform.platform())
    # sys.exit(main())  # pragma: no cover
