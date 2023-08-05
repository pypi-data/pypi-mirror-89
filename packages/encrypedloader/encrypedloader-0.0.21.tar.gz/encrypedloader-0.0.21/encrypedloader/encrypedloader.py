from .loader import encrypt_file, gen_key
import click

@click.group()
def cmd():
    pass


@cmd.command()
@click.argument('key', help="encrypt key string")
@click.argument('fp', help="file to be encrypted")
def encrypt(key, fp):
    print(f"{fp} with key {key}")
    encrypt_file(fp, key)
    click.echo('encrypted!')


@cmd.command()
def genkey():
    gen_key()


cli = click.CommandCollection(sources=[cmd,])


def main():
    cli()