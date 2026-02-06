import click

from cli.main import fast_sync_cli


@fast_sync_cli.command(
    name="help", help="Show help for a specific command. Example: fs help missing left"
)
@click.argument("commands", nargs=-1)
@click.pass_context
def view_help_page_given_command(ctx, commands: tuple):
    main_ctx_group: click.Group = ctx.parent.command
    cmd = main_ctx_group.get_command(ctx, commands[0]) if commands else None
    if cmd is None:
        raise click.ClickException(
            f"Unknown command '{' '.join(commands) if commands else '[empty value]'}' \n"
            f"Use '{ctx.parent.info_name} --help' to see all commands."
        )

    if len(commands) == 1:
        ctx = click.Context(cmd, parent=ctx.parent, info_name=cmd.name)
    else:
        for command in commands[1:]:
            cmd = cmd.get_command(main_ctx_group, command)
        ctx = click.Context(
            cmd, parent=cmd.context_class(cmd).parent, info_name=cmd.name
        )
    click.echo(cmd.get_help(ctx))
