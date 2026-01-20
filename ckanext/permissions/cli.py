import click

import ckan.model as model

import ckanext.permissions.const as perm_const
from ckanext.permissions import utils


def get_commands():
    return [permissions]


@click.group()
def permissions():
    """Permissions management commands."""


@permissions.command()
@click.argument("role", default=perm_const.Roles.User.value, required=False)
@click.argument("scope", default="global", required=False)
def assign_role_to_users(role: str, scope: str):
    """Assign automatic roles to users"""
    users = model.User.all()

    for user in users:
        utils.assign_role_to_user(user.id, role, scope)

    click.secho(f"Role '{role}' assigned to all users in scope '{scope}'", fg="green")


@permissions.command()
@click.argument("role", default=perm_const.Roles.User.value, required=False)
def remove_role_from_users(role: str):
    """Remove automatic roles from users"""
    users = model.User.all()

    for user in users:
        utils.remove_role_from_user(user.id, role)

    click.secho(f"Role '{role}' removed from all users", fg="green")
