# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from . import _utilities, _tables

__all__ = ['Store']


class Store(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 distribution_channels: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 key: Optional[pulumi.Input[str]] = None,
                 languages: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[Mapping[str, Any]]] = None,
                 supply_channels: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Create a Store resource with the given unique name, props, and options.
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        if __name__ is not None:
            warnings.warn("explicit use of __name__ is deprecated", DeprecationWarning)
            resource_name = __name__
        if __opts__ is not None:
            warnings.warn("explicit use of __opts__ is deprecated, use 'opts' instead", DeprecationWarning)
            opts = __opts__
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = dict()

            __props__['distribution_channels'] = distribution_channels
            if key is None:
                raise TypeError("Missing required property 'key'")
            __props__['key'] = key
            __props__['languages'] = languages
            __props__['name'] = name
            __props__['supply_channels'] = supply_channels
            __props__['version'] = None
        super(Store, __self__).__init__(
            'commercetools:index/store:Store',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            distribution_channels: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            key: Optional[pulumi.Input[str]] = None,
            languages: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            name: Optional[pulumi.Input[Mapping[str, Any]]] = None,
            supply_channels: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            version: Optional[pulumi.Input[int]] = None) -> 'Store':
        """
        Get an existing Store resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["distribution_channels"] = distribution_channels
        __props__["key"] = key
        __props__["languages"] = languages
        __props__["name"] = name
        __props__["supply_channels"] = supply_channels
        __props__["version"] = version
        return Store(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="distributionChannels")
    def distribution_channels(self) -> pulumi.Output[Optional[Sequence[str]]]:
        return pulumi.get(self, "distribution_channels")

    @property
    @pulumi.getter
    def key(self) -> pulumi.Output[str]:
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def languages(self) -> pulumi.Output[Optional[Sequence[str]]]:
        return pulumi.get(self, "languages")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[Mapping[str, Any]]:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="supplyChannels")
    def supply_channels(self) -> pulumi.Output[Optional[Sequence[str]]]:
        return pulumi.get(self, "supply_channels")

    @property
    @pulumi.getter
    def version(self) -> pulumi.Output[int]:
        return pulumi.get(self, "version")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

