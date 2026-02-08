import click


def line_wrapper(type_line: str = "---", num_lines: int = 30):
    def decorator(func):
        def wrapper(*args, **kwargs):
            click.echo(type_line * num_lines)
            func(*args, **kwargs)
            click.echo(type_line * num_lines)

        return wrapper

    return decorator


def group_line_wrapper(type_line: str = "---", num_lines: int = 30):
    def decorator(func):
        def wrapper(*args, **kwargs):
            click.echo(f"┌{type_line * num_lines}")
            func(*args, **kwargs)
            click.echo(f"└{type_line * num_lines}")

        return wrapper

    return decorator
