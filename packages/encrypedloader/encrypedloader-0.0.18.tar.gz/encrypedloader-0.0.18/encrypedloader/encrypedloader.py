from .loader import encrypt_file, gen_key
import click

@click.group()
def cmd():
    pass


@cmd.command()
@click.option('--key', default=None, help="encrypt key string")
@click.option('--file', default=None, help="file to be encrypt")
def encrypt(key, file):
    encrypt_file(file, key)
    click.echo('encrypted!')


@cmd.command()
def genkey():
    gen_key()


cli = click.CommandCollection(sources=[cmd,])


def main():
    cli()