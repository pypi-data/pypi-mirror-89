import click

from spell.cli.utils import tabulate_rows, with_emoji, group
from spell.cli.exceptions import api_client_exception_handler


@group(
    name="project",
    short_help="Manage Spell Projects",
    help="Create, List, Archive and manage Projects on Spell",
    hidden=True,
)
@click.pass_context
def project(ctx):
    pass


@project.command(name="create", short_help="Create a new Project")
@click.option(
    "-n", "--name", "name", prompt="Enter a name for the project", help="Name of the project"
)
@click.option("-d", "--description", "description", help="Optional description of the project")
@click.pass_context
def create(ctx, name, description):
    proj_req = {
        "name": name,
        "description": description,
    }
    client = ctx.obj["client"]
    with api_client_exception_handler():
        project = client.create_project(proj_req)
    click.echo(with_emoji("💫", f"Created project {name} - #{project.id}", ctx.obj["utf8"]))


@project.command(name="list", short_help="List all Projects")
@click.pass_context
def list(ctx):
    client = ctx.obj["client"]
    with api_client_exception_handler():
        projects = client.list_projects()

    def create_row(proj):
        return (
            proj.id,
            proj.name,
            proj.description,
            proj.creator.user_name,
            proj.created_at,
        )

    tabulate_rows(
        [create_row(proj) for proj in projects],
        headers=["ID", "NAME", "DESCRIPTION", "CREATOR", "CREATED AT"],
    )


@project.command(name="get", short_help="Get a Project by ID or Name")
@click.argument("id", type=int)
@click.pass_context
def get(ctx, id):
    # TODO(Benno): This should support "get by name"
    # TODO(Benno): Have it list out all the included runs below the project details
    client = ctx.obj["client"]
    with api_client_exception_handler():
        proj = client.get_project(id)

    def create_row(proj):
        return (
            proj.id,
            proj.name,
            proj.description,
            proj.creator.user_name,
            proj.created_at,
        )

    tabulate_rows(
        [create_row(proj)], headers=["ID", "NAME", "DESCRIPTION", "CREATOR", "CREATED AT"],
    )
