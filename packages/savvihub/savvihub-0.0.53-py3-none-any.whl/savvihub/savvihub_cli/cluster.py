import re
import sys

import typer

from savvihub import Context
from savvihub.common import kubectl
from savvihub.common.constants import WEB_HOST

cluster_app = typer.Typer()


@cluster_app.callback()
def main():
    """
    Manage custom clusters
    """


@cluster_app.command()
def register(
    kubectl_context_name: str = typer.Argument(...),
    namespace: str = typer.Option('savvihub', '--namespace', help='Kubernetes namespace SavviHub will use.'),
    cluster_name: str = typer.Option(None, '--cluster-name', help='Cluster name. The default value is kubectl context name.'),
):
    """
    Register a new kubernetes cluster to SavviHub
    """
    if not kubectl.check_context(kubectl_context_name):
        typer.echo(f'Current kubectl context should be set to {kubectl_context_name}.\n'
                   f'Please run \'kubectl config use-context {kubectl_context_name}\'.')
        sys.exit(1)

    master_endpoint, ssl_ca_cert_base64_encoded = kubectl.get_cluster_info(kubectl_context_name)
    sa_token = kubectl.get_service_account_token(namespace)
    if cluster_name is None:
        cluster_name = re.sub('[^0-9a-zA-Z]', '-', kubectl_context_name).strip('-')

    context = Context(user_required=True, project_required=True)
    workspace_name = context.project.workspace.name
    client = context.authorized_client
    cluster = client.cluster_register(workspace_name, cluster_name,
                                      master_endpoint, namespace, sa_token, ssl_ca_cert_base64_encoded)
    typer.echo(f'Custom cluster \'{cluster.name}\' is successfully registered to workspace \'{workspace_name}\'.\n'
               f'{WEB_HOST}/workspaces/{workspace_name}/custom_clusters')
