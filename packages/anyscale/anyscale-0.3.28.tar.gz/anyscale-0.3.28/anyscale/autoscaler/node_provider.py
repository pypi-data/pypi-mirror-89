"""NodeProvider classes that add product-specific behaviour."""

import logging
from types import ModuleType
from typing import Any, Dict, List, Optional

from ray.autoscaler._private.command_runner import DockerCommandRunner, SSHCommandRunner
from ray.autoscaler.command_runner import CommandRunnerInterface

# This try block exists because
# 1. This module is passed to the autoscaler on the head node as an external node provider
# 2. Import paths are different for different versions of ray
try:
    from ray.autoscaler._private.aws.node_provider import NodeProvider
    from ray.autoscaler._private.providers import (
        _get_node_provider,
        _NODE_PROVIDERS,
    )
except ModuleNotFoundError:
    from ray.autoscaler.aws.node_provider import NodeProvider
    from ray.autoscaler.node_provider import (
        get_node_provider as _get_node_provider,
        NODE_PROVIDERS as _NODE_PROVIDERS,
    )

from anyscale.api import instantiate_api_client
from anyscale.client.openapi_client.models.create_nodes_options import (  # type: ignore
    CreateNodesOptions,
)
from anyscale.client.openapi_client.models.nodes_options import NodesOptions  # type: ignore
from anyscale.client.openapi_client.models.non_terminated_nodes_options import (  # type: ignore
    NonTerminatedNodesOptions,
)
from anyscale.client.openapi_client.models.set_node_tags_options import (  # type: ignore
    SetNodeTagsOptions,
)

logger = logging.getLogger(__name__)


class AnyscalePoolingNodeProvider:
    """NodeProvider wrapper for injecting product-specific functionality.

    Currently a no-op wrapper,
    but we plan on adding instance pool functionality here soon:
        https://docs.google.com/document/d/15goOexCiGkbzz7tUbILMc10Gmjf86PiyCtIl75-xGUw/edit
    """

    def __init__(self, provider_config: Dict[str, Any], cluster_name: str) -> None:
        """Implements manual inheritance from NodeProvider.

        This class follows the signature of the NodeProvider base class.
        However, we are not inheriting from NodeProvider
        because we are wrapping around a class that is
        dynamically provided in provider_config;
        we implement this inheritance manually using __getattr__.

        provider_config:
            a configuration dictionary as per the NodeProvider base class,
            but must also have a "inner_provider" key.
            The "inner_provider" field is the provider_config
            of the original NodeProvider class which we are wrapping around.
        """

        inner_provider_config = provider_config["inner_provider"]
        # This is the actual NodeProvider object we are wrapping around.
        self.inner_provider = _get_node_provider(inner_provider_config, cluster_name)

    @staticmethod
    def _get_inner_provider_class_from_config(cluster_config: Dict[str, Any]) -> Any:
        """Helper for passing through static methods.

        NodeProvider has static methods.
        To pass these through to an inner provider object,
        we must also have a static method for getting the inner provider class.

        This is a helper method takes a cluster_config and returns the
        *class* (not the object) of the inner provider.
        """
        inner_provider_config = cluster_config["provider"]["inner_provider"]
        importer = _NODE_PROVIDERS.get(inner_provider_config["type"])
        inner_provider_cls = importer(inner_provider_config)
        return inner_provider_cls

    @staticmethod
    def bootstrap_config(cluster_config: Dict[str, Any]) -> Dict[str, Any]:
        # Get the inner_provider class for the static method.
        inner_provider_cls = AnyscalePoolingNodeProvider._get_inner_provider_class_from_config(
            cluster_config
        )

        # We can't just call the inner_provider method directly,
        # since it expects cluster_config["provider"] to be its own class.
        # Thus, we'll swap in the inner_provider for the primary provider first
        # (and save the primary provider for later).
        primary_provider = cluster_config["provider"]
        cluster_config["provider"] = cluster_config["provider"]["inner_provider"]

        # Pass through to submethod.
        cluster_config = inner_provider_cls.bootstrap_config(cluster_config)

        # Restore primary provider.
        primary_provider["inner_provider"] = cluster_config["provider"]
        cluster_config["provider"] = primary_provider
        return cluster_config

    @staticmethod
    def fillout_available_node_types_resources(
        cluster_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        inner_provider_cls = AnyscalePoolingNodeProvider._get_inner_provider_class_from_config(
            cluster_config
        )

        primary_provider = cluster_config["provider"]
        cluster_config["provider"] = cluster_config["provider"]["inner_provider"]

        cluster_config = inner_provider_cls.fillout_available_node_types_resources(
            cluster_config
        )

        primary_provider["inner_provider"] = cluster_config["provider"]
        cluster_config["provider"] = primary_provider
        return cluster_config

    def __getattr__(self, name: str) -> Any:
        """Implements inheritance from self.inner_provider."""
        return getattr(self.inner_provider, name)


class AnyscaleInstanceManagerNodeProvider:
    """NodeProvider for managing nodes with instance manager.
    """

    def __init__(self, provider_config: Dict[str, Any], cluster_name: str) -> None:
        self.inner_provider_config = provider_config["inner_provider"]
        self.inner_provider = _get_node_provider(
            self.inner_provider_config, cluster_name
        )
        cli_token = self.inner_provider_config["cli_token"]
        self.api_client = instantiate_api_client(cli_token=cli_token)
        self.is_provider_supported = self._is_provider_supported()

    def _is_provider_supported(self) -> bool:
        """Currently instance manager only suppport AWS."""
        # TODO(yifei) move checks from _configure_for_cloud to here
        return True

    def __getattr__(self, name: str) -> Any:
        """Implements inheritance from self.inner_provider."""
        return getattr(self.inner_provider, name)

    # Use the same methodology as AnyscalePoolingNodeProvider for the following
    # static methods
    @staticmethod
    def _get_inner_provider_class_from_config(cluster_config: Dict[str, Any]) -> Any:

        inner_provider_config = cluster_config["provider"]["inner_provider"]
        importer = _NODE_PROVIDERS.get(inner_provider_config["type"])
        inner_provider_cls = importer(inner_provider_config)
        return inner_provider_cls

    @staticmethod
    def bootstrap_config(cluster_config: Dict[str, Any]) -> Dict[str, Any]:
        inner_provider_cls = AnyscalePoolingNodeProvider._get_inner_provider_class_from_config(
            cluster_config
        )
        primary_provider = cluster_config["provider"]
        cluster_config["provider"] = cluster_config["provider"]["inner_provider"]

        cluster_config = inner_provider_cls.bootstrap_config(cluster_config)

        primary_provider["inner_provider"] = cluster_config["provider"]
        cluster_config["provider"] = primary_provider
        return cluster_config

    @staticmethod
    def fillout_available_node_types_resources(
        cluster_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        inner_provider_cls = AnyscalePoolingNodeProvider._get_inner_provider_class_from_config(
            cluster_config
        )

        primary_provider = cluster_config["provider"]
        cluster_config["provider"] = cluster_config["provider"]["inner_provider"]

        cluster_config = inner_provider_cls.fillout_available_node_types_resources(
            cluster_config
        )

        primary_provider["inner_provider"] = cluster_config["provider"]
        cluster_config["provider"] = primary_provider
        return cluster_config

    def non_terminated_nodes(self, tag_filters: Dict[str, str]) -> Any:
        if not self.is_provider_supported:
            return self.inner_provider.non_terminated_nodes(tag_filters)

        non_terminated_nodes_request = NonTerminatedNodesOptions(
            provider_config=self.inner_provider.provider_config,
            cluster_name=self.inner_provider.cluster_name,
            tag_filters=tag_filters,
        )
        resp = self.api_client.non_terminated_nodes_api_v2_instances_non_terminated_nodes_post(
            non_terminated_nodes_request
        )
        return [instance.instance_id for instance in resp.results]

    def is_running(self, node_id: str) -> Any:
        if not self.is_provider_supported:
            return self.inner_provider.is_running(node_id)

        resp = self.api_client.is_running_api_v2_instances_instance_id_is_running_get(
            node_id
        )
        return resp.result.is_running

    def is_terminated(self, node_id: str) -> Any:
        if not self.is_provider_supported:
            return self.inner_provider.is_terminated(node_id)

        resp = self.api_client.is_terminated_api_v2_instances_instance_id_is_terminated_get(
            node_id
        )
        return resp.result.is_terminated

    def node_tags(self, node_id: str) -> Any:
        if not self.is_provider_supported:
            return self.inner_provider.node_tags(node_id)

        resp = self.api_client.get_instance_api_v2_instances_instance_id_get(node_id)
        return resp.result.tags

    def external_ip(self, node_id: str) -> Any:
        if not self.is_provider_supported:
            return self.inner_provider.external_ip(node_id)

        resp = self.api_client.external_ip_api_v2_instances_instance_id_external_ip_get(
            node_id
        )
        return resp.result.external_ip

    def internal_ip(self, node_id: str) -> Any:
        if not self.is_provider_supported:
            return self.inner_provider.internal_ip(node_id)

        resp = self.api_client.internal_ip_api_v2_instances_instance_id_internal_ip_get(
            node_id
        )
        return resp.result.internal_ip

    def create_node(
        self, node_config: Dict[str, Any], tags: Dict[str, str], count: int
    ) -> None:
        if not self.is_provider_supported:
            self.inner_provider.create_node(node_config, tags, count)
            return

        create_node_request = CreateNodesOptions(
            provider_config=self.inner_provider.provider_config,
            cluster_name=self.inner_provider.cluster_name,
            node_config=node_config,
            tags=tags,
            count=count,
        )
        self.api_client.create_nodes_api_v2_instances_post(create_node_request)

    def set_node_tags(self, node_id: str, tags: Dict[str, str]) -> None:
        if not self.is_provider_supported:
            self.inner_provider.set_node_tags(node_id, tags)
            return

        set_node_tags_request = SetNodeTagsOptions(
            provider_config=self.inner_provider.provider_config,
            cluster_name=self.inner_provider.cluster_name,
            instance_id=node_id,
            tags=tags,
        )
        self.api_client.set_node_tags_api_v2_instances_set_tags_post(
            set_node_tags_request
        )

    def terminate_node(self, node_id: str) -> None:
        if not self.is_provider_supported:
            self.inner_provider.terminate_node(node_id)
            return

        terminate_nodes_request = NodesOptions(
            provider_config=self.inner_provider.provider_config,
            cluster_name=self.inner_provider.cluster_name,
            instance_ids=[node_id],
        )
        self.api_client.terminate_nodes_api_v2_instances_terminate_nodes_post(
            terminate_nodes_request
        )

    def terminate_nodes(self, node_ids: List[str]) -> None:
        if not self.is_provider_supported:
            self.inner_provider.terminate_nodes(node_ids)
            return

        terminate_nodes_request = NodesOptions(
            provider_config=self.inner_provider.provider_config,
            cluster_name=self.inner_provider.cluster_name,
            instance_ids=node_ids,
        )
        self.api_client.terminate_nodes_api_v2_instances_terminate_nodes_post(
            terminate_nodes_request
        )

    def get_command_runner(
        self,
        log_prefix: str,
        node_id: str,
        auth_config: Dict[str, Any],
        cluster_name: str,
        process_runner: ModuleType,
        use_internal_ip: bool,
        docker_config: Optional[Dict[str, Any]] = None,
    ) -> CommandRunnerInterface:
        """Copied from aws node provider. Need to pass
        """
        common_args = {
            "log_prefix": log_prefix,
            "node_id": node_id,
            "provider": self,
            "auth_config": auth_config,
            "cluster_name": cluster_name,
            "process_runner": process_runner,
            "use_internal_ip": use_internal_ip,
        }
        if docker_config and docker_config["container_name"] != "":
            return DockerCommandRunner(docker_config, **common_args)
        else:
            return SSHCommandRunner(**common_args)


class AnyscaleExecNodeProvider(NodeProvider):  # type: ignore
    """A temporary class for making `anyscale exec` faster.

    Only used in the frontend CLI.
    """

    def __init__(self, provider_config: Dict[str, Any], cluster_name: str) -> None:
        super().__init__(provider_config, cluster_name)
        self.dns_address = provider_config["dns_address"]

    def non_terminated_nodes(self, tag_filters: List[str]) -> List[str]:
        return [self.dns_address]

    def external_ip(self, node_id: str) -> str:
        return node_id
