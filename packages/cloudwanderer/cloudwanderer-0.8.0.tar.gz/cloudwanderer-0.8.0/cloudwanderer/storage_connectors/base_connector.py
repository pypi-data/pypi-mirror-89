"""Module containing abstract classes for CloudWanderer storage connectors."""
from abc import ABC, abstractmethod
from typing import List, Iterator
from ..aws_urn import AwsUrn
from ..cloud_wanderer import CloudWandererResource


class BaseStorageConnector(ABC):
    """Abstract class for specification of the CloudWanderer storage connector interface."""

    @abstractmethod
    def init(self) -> None:
        """Initialise the storage backend whatever it is."""

    @abstractmethod
    def write_resource(self, urn: AwsUrn, resource: str) -> None:
        """Persist a single resource to storage."""

    @abstractmethod
    def read_all(self) -> Iterator[dict]:
        """Return all records from storage."""

    @abstractmethod
    def read_resource(self, urn: AwsUrn) -> 'CloudWandererResource':
        """Return a resource matching the supplied urn from storage."""

    @abstractmethod
    def read_resources(
            self, urn: AwsUrn, account_id: str, region: str, service: str,
            resource_type: str) -> Iterator['CloudWandererResource']:
        """Yield a resource matching the supplied urn from storage."""

    @abstractmethod
    def delete_resource(self, urn: AwsUrn) -> None:
        """Delete this resource and all its resource attributes."""

    @abstractmethod
    def delete_resource_of_type_in_account_region(
            self, service: str, resource_type: str, account_id: str,
            region: str, urns_to_keep: List[AwsUrn] = None) -> None:
        """Delete resources of type in account and region unless in list of URNs.

        This is used primarily to clean up old resources.
        """
