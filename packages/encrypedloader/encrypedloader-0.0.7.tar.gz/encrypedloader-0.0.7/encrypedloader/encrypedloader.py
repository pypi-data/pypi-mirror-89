import loader
import click

@click.group()
def cmd():
    pass


@cmd.command()
@click.argument('keyfile')
@click.argument('file_path')
def encrypt(keyfile, file_path):
    loader.encrypt_file(file_path, keyfile)
    click.echo('encrypted!')


@cmd.command()
def genkey():
    loader.gen_key()


cli = click.CommandCollection(sources=[cmd,])


def main():
    cli()