import click

import ckan.model as model

import ckanext.permissions.const as perm_const
from ckanext.permissions import model as perm_model
from ckanext.permissions import utils


def get_commands():
    return [permissions]


@click.group()
def permissions():
    """Permissions management commands."""


@permissions.command()
def init_default_roles():
    """Create default roles (anonymous, authenticated, sysadmin) in the database"""
    default_roles = [
        ("anonymous", "Anonymous", "Default role for anonymous users"),
        (
            "authenticated",
            "Authenticated",
            "Regular user that will be assigned automatically for all users on a portal",
        ),
        ("administrator", "Administrator", "Superuser that can do everything"),
    ]

    for role_id, label, description in default_roles:
        existing_role = perm_model.Role.get(role_id)
        if existing_role:
            click.secho(f"Role '{role_id}' already exists, skipping", fg="yellow")
        else:
            perm_model.Role.create(role_id, label, description)
            click.secho(f"Role '{role_id}' created", fg="green")


@permissions.command()
@click.argument("role", default=perm_const.Roles.Authenticated.value, required=False)
def assign_default_user_roles(role: str):
    """Assign automatic roles to users"""
    users = model.User.all()

    for user in users:
        utils.assign_role_to_user(user.id, role)

    click.secho(f"Role '{role}' assigned to all users", fg="green")


@permissions.command()
@click.argument("role", default=perm_const.Roles.Authenticated.value, required=False)
@click.option(
    "--user-ids",
    "-u",
    multiple=True,
    help="User IDs to remove role from (if not specified, removes from all users)",
)
def remove_role_from_users(role: str, user_ids: tuple[str, ...]):
    """Remove automatic roles from users"""
    if user_ids:
        users = [model.User.get(user_id) for user_id in user_ids]
    else:
        users = model.User.all()

    for user in users:
        if user:
            utils.remove_role_from_user(user.id, role)

    if user_ids:
        click.secho(
            f"Role '{role}' removed from {len(users)} specified user(s)", fg="green"
        )
    else:
        click.secho(f"Role '{role}' removed from all users", fg="green")
