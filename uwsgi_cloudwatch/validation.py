import click


def frequency(ctx, param, value):
    try:
        value = int(value)
        if value < 0:
            raise click.BadParameter('frequency must be greater than zero')
        return value
    except ValueError:
        raise click.BadParameter('')


def namespace(ctx, param, value):
    return value


def prefix(ctx, param, value):
    return value
