# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from Tea.model import TeaModel
from typing import List, Dict


class AddContainerAppRequest(TeaModel):
    def __init__(
        self,
        name: str = None,
        repository: str = None,
        description: str = None,
        image_tag: str = None,
        container_type: str = None,
    ):
        self.name = name
        self.repository = repository
        self.description = description
        self.image_tag = image_tag
        self.container_type = container_type

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.name is not None:
            result['Name'] = self.name
        if self.repository is not None:
            result['Repository'] = self.repository
        if self.description is not None:
            result['Description'] = self.description
        if self.image_tag is not None:
            result['ImageTag'] = self.image_tag
        if self.container_type is not None:
            result['ContainerType'] = self.container_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Repository') is not None:
            self.repository = m.get('Repository')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('ImageTag') is not None:
            self.image_tag = m.get('ImageTag')
        if m.get('ContainerType') is not None:
            self.container_type = m.get('ContainerType')
        return self


class AddContainerAppResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        container_id: List[str] = None,
    ):
        self.request_id = request_id
        self.container_id = container_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.container_id is not None:
            result['ContainerId'] = self.container_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('ContainerId') is not None:
            self.container_id = m.get('ContainerId')
        return self


class AddContainerAppResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: AddContainerAppResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = AddContainerAppResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class AddLocalNodesRequest(TeaModel):
    def __init__(
        self,
        cluster_id: str = None,
        nodes: str = None,
    ):
        self.cluster_id = cluster_id
        self.nodes = nodes

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        if self.nodes is not None:
            result['Nodes'] = self.nodes
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        if m.get('Nodes') is not None:
            self.nodes = m.get('Nodes')
        return self


class AddLocalNodesResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        instance_ids: List[str] = None,
    ):
        self.request_id = request_id
        self.instance_ids = instance_ids

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.instance_ids is not None:
            result['InstanceIds'] = self.instance_ids
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('InstanceIds') is not None:
            self.instance_ids = m.get('InstanceIds')
        return self


class AddLocalNodesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: AddLocalNodesResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = AddLocalNodesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class AddNodesRequest(TeaModel):
    def __init__(
        self,
        cluster_id: str = None,
        image_owner_alias: str = None,
        image_id: str = None,
        count: int = None,
        instance_type: str = None,
        compute_spot_strategy: str = None,
        compute_spot_price_limit: str = None,
        ecs_charge_type: str = None,
        period: int = None,
        period_unit: str = None,
        auto_renew: str = None,
        auto_renew_period: int = None,
        job_queue: str = None,
        create_mode: str = None,
        system_disk_type: str = None,
        system_disk_size: int = None,
        zone_id: str = None,
        v_switch_id: str = None,
        host_name_prefix: str = None,
        host_name_suffix: str = None,
        compute_enable_ht: bool = None,
        allocate_public_address: bool = None,
        internet_charge_type: str = None,
        internet_max_band_width_in: int = None,
        internet_max_band_width_out: int = None,
        client_token: str = None,
    ):
        self.cluster_id = cluster_id
        self.image_owner_alias = image_owner_alias
        self.image_id = image_id
        self.count = count
        self.instance_type = instance_type
        self.compute_spot_strategy = compute_spot_strategy
        self.compute_spot_price_limit = compute_spot_price_limit
        self.ecs_charge_type = ecs_charge_type
        self.period = period
        self.period_unit = period_unit
        self.auto_renew = auto_renew
        self.auto_renew_period = auto_renew_period
        self.job_queue = job_queue
        self.create_mode = create_mode
        self.system_disk_type = system_disk_type
        self.system_disk_size = system_disk_size
        self.zone_id = zone_id
        self.v_switch_id = v_switch_id
        self.host_name_prefix = host_name_prefix
        self.host_name_suffix = host_name_suffix
        self.compute_enable_ht = compute_enable_ht
        self.allocate_public_address = allocate_public_address
        self.internet_charge_type = internet_charge_type
        self.internet_max_band_width_in = internet_max_band_width_in
        self.internet_max_band_width_out = internet_max_band_width_out
        self.client_token = client_token

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        if self.image_owner_alias is not None:
            result['ImageOwnerAlias'] = self.image_owner_alias
        if self.image_id is not None:
            result['ImageId'] = self.image_id
        if self.count is not None:
            result['Count'] = self.count
        if self.instance_type is not None:
            result['InstanceType'] = self.instance_type
        if self.compute_spot_strategy is not None:
            result['ComputeSpotStrategy'] = self.compute_spot_strategy
        if self.compute_spot_price_limit is not None:
            result['ComputeSpotPriceLimit'] = self.compute_spot_price_limit
        if self.ecs_charge_type is not None:
            result['EcsChargeType'] = self.ecs_charge_type
        if self.period is not None:
            result['Period'] = self.period
        if self.period_unit is not None:
            result['PeriodUnit'] = self.period_unit
        if self.auto_renew is not None:
            result['AutoRenew'] = self.auto_renew
        if self.auto_renew_period is not None:
            result['AutoRenewPeriod'] = self.auto_renew_period
        if self.job_queue is not None:
            result['JobQueue'] = self.job_queue
        if self.create_mode is not None:
            result['CreateMode'] = self.create_mode
        if self.system_disk_type is not None:
            result['SystemDiskType'] = self.system_disk_type
        if self.system_disk_size is not None:
            result['SystemDiskSize'] = self.system_disk_size
        if self.zone_id is not None:
            result['ZoneId'] = self.zone_id
        if self.v_switch_id is not None:
            result['VSwitchId'] = self.v_switch_id
        if self.host_name_prefix is not None:
            result['HostNamePrefix'] = self.host_name_prefix
        if self.host_name_suffix is not None:
            result['HostNameSuffix'] = self.host_name_suffix
        if self.compute_enable_ht is not None:
            result['ComputeEnableHt'] = self.compute_enable_ht
        if self.allocate_public_address is not None:
            result['AllocatePublicAddress'] = self.allocate_public_address
        if self.internet_charge_type is not None:
            result['InternetChargeType'] = self.internet_charge_type
        if self.internet_max_band_width_in is not None:
            result['InternetMaxBandWidthIn'] = self.internet_max_band_width_in
        if self.internet_max_band_width_out is not None:
            result['InternetMaxBandWidthOut'] = self.internet_max_band_width_out
        if self.client_token is not None:
            result['ClientToken'] = self.client_token
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        if m.get('ImageOwnerAlias') is not None:
            self.image_owner_alias = m.get('ImageOwnerAlias')
        if m.get('ImageId') is not None:
            self.image_id = m.get('ImageId')
        if m.get('Count') is not None:
            self.count = m.get('Count')
        if m.get('InstanceType') is not None:
            self.instance_type = m.get('InstanceType')
        if m.get('ComputeSpotStrategy') is not None:
            self.compute_spot_strategy = m.get('ComputeSpotStrategy')
        if m.get('ComputeSpotPriceLimit') is not None:
            self.compute_spot_price_limit = m.get('ComputeSpotPriceLimit')
        if m.get('EcsChargeType') is not None:
            self.ecs_charge_type = m.get('EcsChargeType')
        if m.get('Period') is not None:
            self.period = m.get('Period')
        if m.get('PeriodUnit') is not None:
            self.period_unit = m.get('PeriodUnit')
        if m.get('AutoRenew') is not None:
            self.auto_renew = m.get('AutoRenew')
        if m.get('AutoRenewPeriod') is not None:
            self.auto_renew_period = m.get('AutoRenewPeriod')
        if m.get('JobQueue') is not None:
            self.job_queue = m.get('JobQueue')
        if m.get('CreateMode') is not None:
            self.create_mode = m.get('CreateMode')
        if m.get('SystemDiskType') is not None:
            self.system_disk_type = m.get('SystemDiskType')
        if m.get('SystemDiskSize') is not None:
            self.system_disk_size = m.get('SystemDiskSize')
        if m.get('ZoneId') is not None:
            self.zone_id = m.get('ZoneId')
        if m.get('VSwitchId') is not None:
            self.v_switch_id = m.get('VSwitchId')
        if m.get('HostNamePrefix') is not None:
            self.host_name_prefix = m.get('HostNamePrefix')
        if m.get('HostNameSuffix') is not None:
            self.host_name_suffix = m.get('HostNameSuffix')
        if m.get('ComputeEnableHt') is not None:
            self.compute_enable_ht = m.get('ComputeEnableHt')
        if m.get('AllocatePublicAddress') is not None:
            self.allocate_public_address = m.get('AllocatePublicAddress')
        if m.get('InternetChargeType') is not None:
            self.internet_charge_type = m.get('InternetChargeType')
        if m.get('InternetMaxBandWidthIn') is not None:
            self.internet_max_band_width_in = m.get('InternetMaxBandWidthIn')
        if m.get('InternetMaxBandWidthOut') is not None:
            self.internet_max_band_width_out = m.get('InternetMaxBandWidthOut')
        if m.get('ClientToken') is not None:
            self.client_token = m.get('ClientToken')
        return self


class AddNodesResponseBody(TeaModel):
    def __init__(
        self,
        task_id: str = None,
        request_id: str = None,
        instance_ids: List[str] = None,
    ):
        self.task_id = task_id
        self.request_id = request_id
        self.instance_ids = instance_ids

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.task_id is not None:
            result['TaskId'] = self.task_id
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.instance_ids is not None:
            result['InstanceIds'] = self.instance_ids
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TaskId') is not None:
            self.task_id = m.get('TaskId')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('InstanceIds') is not None:
            self.instance_ids = m.get('InstanceIds')
        return self


class AddNodesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: AddNodesResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = AddNodesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class AddQueueRequest(TeaModel):
    def __init__(
        self,
        cluster_id: str = None,
        queue_name: str = None,
    ):
        self.cluster_id = cluster_id
        self.queue_name = queue_name

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        if self.queue_name is not None:
            result['QueueName'] = self.queue_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        if m.get('QueueName') is not None:
            self.queue_name = m.get('QueueName')
        return self


class AddQueueResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class AddQueueResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: AddQueueResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = AddQueueResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class AddSecurityGroupRequest(TeaModel):
    def __init__(
        self,
        cluster_id: str = None,
        security_group_id: str = None,
        client_token: str = None,
    ):
        self.cluster_id = cluster_id
        self.security_group_id = security_group_id
        self.client_token = client_token

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        if self.security_group_id is not None:
            result['SecurityGroupId'] = self.security_group_id
        if self.client_token is not None:
            result['ClientToken'] = self.client_token
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        if m.get('SecurityGroupId') is not None:
            self.security_group_id = m.get('SecurityGroupId')
        if m.get('ClientToken') is not None:
            self.client_token = m.get('ClientToken')
        return self


class AddSecurityGroupResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class AddSecurityGroupResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: AddSecurityGroupResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = AddSecurityGroupResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class AddUsersRequestUser(TeaModel):
    def __init__(
        self,
        password: str = None,
        name: str = None,
        group: str = None,
    ):
        self.password = password
        self.name = name
        self.group = group

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.password is not None:
            result['Password'] = self.password
        if self.name is not None:
            result['Name'] = self.name
        if self.group is not None:
            result['Group'] = self.group
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Password') is not None:
            self.password = m.get('Password')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Group') is not None:
            self.group = m.get('Group')
        return self


class AddUsersRequest(TeaModel):
    def __init__(
        self,
        cluster_id: str = None,
        user: List[AddUsersRequestUser] = None,
    ):
        self.cluster_id = cluster_id
        self.user = user

    def validate(self):
        if self.user:
            for k in self.user:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        result['User'] = []
        if self.user is not None:
            for k in self.user:
                result['User'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        self.user = []
        if m.get('User') is not None:
            for k in m.get('User'):
                temp_model = AddUsersRequestUser()
                self.user.append(temp_model.from_map(k))
        return self


class AddUsersResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class AddUsersResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: AddUsersResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = AddUsersResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ApplyNodesRequestZoneInfos(TeaModel):
    def __init__(
        self,
        v_switch_id: str = None,
        zone_id: str = None,
    ):
        self.v_switch_id = v_switch_id
        self.zone_id = zone_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.v_switch_id is not None:
            result['VSwitchId'] = self.v_switch_id
        if self.zone_id is not None:
            result['ZoneId'] = self.zone_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('VSwitchId') is not None:
            self.v_switch_id = m.get('VSwitchId')
        if m.get('ZoneId') is not None:
            self.zone_id = m.get('ZoneId')
        return self


class ApplyNodesRequestInstanceTypeModel(TeaModel):
    def __init__(
        self,
        max_price: float = None,
        target_image_id: str = None,
        instance_type: str = None,
    ):
        self.max_price = max_price
        self.target_image_id = target_image_id
        self.instance_type = instance_type

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.max_price is not None:
            result['MaxPrice'] = self.max_price
        if self.target_image_id is not None:
            result['TargetImageId'] = self.target_image_id
        if self.instance_type is not None:
            result['InstanceType'] = self.instance_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('MaxPrice') is not None:
            self.max_price = m.get('MaxPrice')
        if m.get('TargetImageId') is not None:
            self.target_image_id = m.get('TargetImageId')
        if m.get('InstanceType') is not None:
            self.instance_type = m.get('InstanceType')
        return self


class ApplyNodesRequest(TeaModel):
    def __init__(
        self,
        cluster_id: str = None,
        image_id: str = None,
        compute_spot_strategy: str = None,
        compute_spot_price_limit: float = None,
        system_disk_type: str = None,
        system_disk_size: int = None,
        host_name_prefix: str = None,
        host_name_suffix: str = None,
        allocate_public_address: bool = None,
        internet_charge_type: str = None,
        internet_max_band_width_in: int = None,
        internet_max_band_width_out: int = None,
        cores: int = None,
        memory: int = None,
        instance_family_level: str = None,
        target_capacity: int = None,
        resource_amount_type: str = None,
        priority_strategy: str = None,
        strict_satisfied_target_capacity: bool = None,
        zone_infos: List[ApplyNodesRequestZoneInfos] = None,
        instance_type_model: List[ApplyNodesRequestInstanceTypeModel] = None,
    ):
        self.cluster_id = cluster_id
        self.image_id = image_id
        self.compute_spot_strategy = compute_spot_strategy
        self.compute_spot_price_limit = compute_spot_price_limit
        self.system_disk_type = system_disk_type
        self.system_disk_size = system_disk_size
        self.host_name_prefix = host_name_prefix
        self.host_name_suffix = host_name_suffix
        self.allocate_public_address = allocate_public_address
        self.internet_charge_type = internet_charge_type
        self.internet_max_band_width_in = internet_max_band_width_in
        self.internet_max_band_width_out = internet_max_band_width_out
        self.cores = cores
        self.memory = memory
        self.instance_family_level = instance_family_level
        self.target_capacity = target_capacity
        self.resource_amount_type = resource_amount_type
        self.priority_strategy = priority_strategy
        self.strict_satisfied_target_capacity = strict_satisfied_target_capacity
        self.zone_infos = zone_infos
        self.instance_type_model = instance_type_model

    def validate(self):
        if self.zone_infos:
            for k in self.zone_infos:
                if k:
                    k.validate()
        if self.instance_type_model:
            for k in self.instance_type_model:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        if self.image_id is not None:
            result['ImageId'] = self.image_id
        if self.compute_spot_strategy is not None:
            result['ComputeSpotStrategy'] = self.compute_spot_strategy
        if self.compute_spot_price_limit is not None:
            result['ComputeSpotPriceLimit'] = self.compute_spot_price_limit
        if self.system_disk_type is not None:
            result['SystemDiskType'] = self.system_disk_type
        if self.system_disk_size is not None:
            result['SystemDiskSize'] = self.system_disk_size
        if self.host_name_prefix is not None:
            result['HostNamePrefix'] = self.host_name_prefix
        if self.host_name_suffix is not None:
            result['HostNameSuffix'] = self.host_name_suffix
        if self.allocate_public_address is not None:
            result['AllocatePublicAddress'] = self.allocate_public_address
        if self.internet_charge_type is not None:
            result['InternetChargeType'] = self.internet_charge_type
        if self.internet_max_band_width_in is not None:
            result['InternetMaxBandWidthIn'] = self.internet_max_band_width_in
        if self.internet_max_band_width_out is not None:
            result['InternetMaxBandWidthOut'] = self.internet_max_band_width_out
        if self.cores is not None:
            result['Cores'] = self.cores
        if self.memory is not None:
            result['Memory'] = self.memory
        if self.instance_family_level is not None:
            result['InstanceFamilyLevel'] = self.instance_family_level
        if self.target_capacity is not None:
            result['TargetCapacity'] = self.target_capacity
        if self.resource_amount_type is not None:
            result['ResourceAmountType'] = self.resource_amount_type
        if self.priority_strategy is not None:
            result['PriorityStrategy'] = self.priority_strategy
        if self.strict_satisfied_target_capacity is not None:
            result['StrictSatisfiedTargetCapacity'] = self.strict_satisfied_target_capacity
        result['ZoneInfos'] = []
        if self.zone_infos is not None:
            for k in self.zone_infos:
                result['ZoneInfos'].append(k.to_map() if k else None)
        result['InstanceTypeModel'] = []
        if self.instance_type_model is not None:
            for k in self.instance_type_model:
                result['InstanceTypeModel'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        if m.get('ImageId') is not None:
            self.image_id = m.get('ImageId')
        if m.get('ComputeSpotStrategy') is not None:
            self.compute_spot_strategy = m.get('ComputeSpotStrategy')
        if m.get('ComputeSpotPriceLimit') is not None:
            self.compute_spot_price_limit = m.get('ComputeSpotPriceLimit')
        if m.get('SystemDiskType') is not None:
            self.system_disk_type = m.get('SystemDiskType')
        if m.get('SystemDiskSize') is not None:
            self.system_disk_size = m.get('SystemDiskSize')
        if m.get('HostNamePrefix') is not None:
            self.host_name_prefix = m.get('HostNamePrefix')
        if m.get('HostNameSuffix') is not None:
            self.host_name_suffix = m.get('HostNameSuffix')
        if m.get('AllocatePublicAddress') is not None:
            self.allocate_public_address = m.get('AllocatePublicAddress')
        if m.get('InternetChargeType') is not None:
            self.internet_charge_type = m.get('InternetChargeType')
        if m.get('InternetMaxBandWidthIn') is not None:
            self.internet_max_band_width_in = m.get('InternetMaxBandWidthIn')
        if m.get('InternetMaxBandWidthOut') is not None:
            self.internet_max_band_width_out = m.get('InternetMaxBandWidthOut')
        if m.get('Cores') is not None:
            self.cores = m.get('Cores')
        if m.get('Memory') is not None:
            self.memory = m.get('Memory')
        if m.get('InstanceFamilyLevel') is not None:
            self.instance_family_level = m.get('InstanceFamilyLevel')
        if m.get('TargetCapacity') is not None:
            self.target_capacity = m.get('TargetCapacity')
        if m.get('ResourceAmountType') is not None:
            self.resource_amount_type = m.get('ResourceAmountType')
        if m.get('PriorityStrategy') is not None:
            self.priority_strategy = m.get('PriorityStrategy')
        if m.get('StrictSatisfiedTargetCapacity') is not None:
            self.strict_satisfied_target_capacity = m.get('StrictSatisfiedTargetCapacity')
        self.zone_infos = []
        if m.get('ZoneInfos') is not None:
            for k in m.get('ZoneInfos'):
                temp_model = ApplyNodesRequestZoneInfos()
                self.zone_infos.append(temp_model.from_map(k))
        self.instance_type_model = []
        if m.get('InstanceTypeModel') is not None:
            for k in m.get('InstanceTypeModel'):
                temp_model = ApplyNodesRequestInstanceTypeModel()
                self.instance_type_model.append(temp_model.from_map(k))
        return self


class ApplyNodesResponseBody(TeaModel):
    def __init__(
        self,
        task_id: str = None,
        request_id: str = None,
        satisfied_amount: int = None,
        instance_ids: List[str] = None,
        detail: str = None,
    ):
        self.task_id = task_id
        self.request_id = request_id
        self.satisfied_amount = satisfied_amount
        self.instance_ids = instance_ids
        self.detail = detail

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.task_id is not None:
            result['TaskId'] = self.task_id
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.satisfied_amount is not None:
            result['SatisfiedAmount'] = self.satisfied_amount
        if self.instance_ids is not None:
            result['InstanceIds'] = self.instance_ids
        if self.detail is not None:
            result['Detail'] = self.detail
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TaskId') is not None:
            self.task_id = m.get('TaskId')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('SatisfiedAmount') is not None:
            self.satisfied_amount = m.get('SatisfiedAmount')
        if m.get('InstanceIds') is not None:
            self.instance_ids = m.get('InstanceIds')
        if m.get('Detail') is not None:
            self.detail = m.get('Detail')
        return self


class ApplyNodesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ApplyNodesResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ApplyNodesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class BindAccountToClusterUserRequest(TeaModel):
    def __init__(
        self,
        cluster_id: str = None,
        user_name: str = None,
        user_pwd: str = None,
        account_uid: str = None,
        account_name: str = None,
    ):
        self.cluster_id = cluster_id
        self.user_name = user_name
        self.user_pwd = user_pwd
        self.account_uid = account_uid
        self.account_name = account_name

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        if self.user_name is not None:
            result['UserName'] = self.user_name
        if self.user_pwd is not None:
            result['UserPwd'] = self.user_pwd
        if self.account_uid is not None:
            result['AccountUid'] = self.account_uid
        if self.account_name is not None:
            result['AccountName'] = self.account_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        if m.get('UserName') is not None:
            self.user_name = m.get('UserName')
        if m.get('UserPwd') is not None:
            self.user_pwd = m.get('UserPwd')
        if m.get('AccountUid') is not None:
            self.account_uid = m.get('AccountUid')
        if m.get('AccountName') is not None:
            self.account_name = m.get('AccountName')
        return self


class BindAccountToClusterUserResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class BindAccountToClusterUserResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: BindAccountToClusterUserResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = BindAccountToClusterUserResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateClusterRequestEcsOrderManager(TeaModel):
    def __init__(
        self,
        count: int = None,
        instance_type: str = None,
    ):
        self.count = count
        self.instance_type = instance_type

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.count is not None:
            result['Count'] = self.count
        if self.instance_type is not None:
            result['InstanceType'] = self.instance_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Count') is not None:
            self.count = m.get('Count')
        if m.get('InstanceType') is not None:
            self.instance_type = m.get('InstanceType')
        return self


class CreateClusterRequestEcsOrderCompute(TeaModel):
    def __init__(
        self,
        count: int = None,
        instance_type: str = None,
    ):
        self.count = count
        self.instance_type = instance_type

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.count is not None:
            result['Count'] = self.count
        if self.instance_type is not None:
            result['InstanceType'] = self.instance_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Count') is not None:
            self.count = m.get('Count')
        if m.get('InstanceType') is not None:
            self.instance_type = m.get('InstanceType')
        return self


class CreateClusterRequestEcsOrderLogin(TeaModel):
    def __init__(
        self,
        count: int = None,
        instance_type: str = None,
    ):
        self.count = count
        self.instance_type = instance_type

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.count is not None:
            result['Count'] = self.count
        if self.instance_type is not None:
            result['InstanceType'] = self.instance_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Count') is not None:
            self.count = m.get('Count')
        if m.get('InstanceType') is not None:
            self.instance_type = m.get('InstanceType')
        return self


class CreateClusterRequestEcsOrder(TeaModel):
    def __init__(
        self,
        manager: CreateClusterRequestEcsOrderManager = None,
        compute: CreateClusterRequestEcsOrderCompute = None,
        login: CreateClusterRequestEcsOrderLogin = None,
    ):
        self.manager = manager
        self.compute = compute
        self.login = login

    def validate(self):
        self.validate_required(self.manager, 'manager')
        if self.manager:
            self.manager.validate()
        self.validate_required(self.compute, 'compute')
        if self.compute:
            self.compute.validate()
        self.validate_required(self.login, 'login')
        if self.login:
            self.login.validate()

    def to_map(self):
        result = dict()
        if self.manager is not None:
            result['Manager'] = self.manager.to_map()
        if self.compute is not None:
            result['Compute'] = self.compute.to_map()
        if self.login is not None:
            result['Login'] = self.login.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Manager') is not None:
            temp_model = CreateClusterRequestEcsOrderManager()
            self.manager = temp_model.from_map(m['Manager'])
        if m.get('Compute') is not None:
            temp_model = CreateClusterRequestEcsOrderCompute()
            self.compute = temp_model.from_map(m['Compute'])
        if m.get('Login') is not None:
            temp_model = CreateClusterRequestEcsOrderLogin()
            self.login = temp_model.from_map(m['Login'])
        return self


class CreateClusterRequestApplication(TeaModel):
    def __init__(
        self,
        tag: str = None,
    ):
        self.tag = tag

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.tag is not None:
            result['Tag'] = self.tag
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Tag') is not None:
            self.tag = m.get('Tag')
        return self


class CreateClusterRequestAdditionalVolumesRoles(TeaModel):
    def __init__(
        self,
        name: str = None,
    ):
        self.name = name

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.name is not None:
            result['Name'] = self.name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Name') is not None:
            self.name = m.get('Name')
        return self


class CreateClusterRequestAdditionalVolumes(TeaModel):
    def __init__(
        self,
        job_queue: str = None,
        volume_id: str = None,
        roles: List[CreateClusterRequestAdditionalVolumesRoles] = None,
        remote_directory: str = None,
        volume_mountpoint: str = None,
        local_directory: str = None,
        volume_type: str = None,
        volume_protocol: str = None,
        location: str = None,
    ):
        self.job_queue = job_queue
        self.volume_id = volume_id
        self.roles = roles
        self.remote_directory = remote_directory
        self.volume_mountpoint = volume_mountpoint
        self.local_directory = local_directory
        self.volume_type = volume_type
        self.volume_protocol = volume_protocol
        self.location = location

    def validate(self):
        if self.roles:
            for k in self.roles:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.job_queue is not None:
            result['JobQueue'] = self.job_queue
        if self.volume_id is not None:
            result['VolumeId'] = self.volume_id
        result['Roles'] = []
        if self.roles is not None:
            for k in self.roles:
                result['Roles'].append(k.to_map() if k else None)
        if self.remote_directory is not None:
            result['RemoteDirectory'] = self.remote_directory
        if self.volume_mountpoint is not None:
            result['VolumeMountpoint'] = self.volume_mountpoint
        if self.local_directory is not None:
            result['LocalDirectory'] = self.local_directory
        if self.volume_type is not None:
            result['VolumeType'] = self.volume_type
        if self.volume_protocol is not None:
            result['VolumeProtocol'] = self.volume_protocol
        if self.location is not None:
            result['Location'] = self.location
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('JobQueue') is not None:
            self.job_queue = m.get('JobQueue')
        if m.get('VolumeId') is not None:
            self.volume_id = m.get('VolumeId')
        self.roles = []
        if m.get('Roles') is not None:
            for k in m.get('Roles'):
                temp_model = CreateClusterRequestAdditionalVolumesRoles()
                self.roles.append(temp_model.from_map(k))
        if m.get('RemoteDirectory') is not None:
            self.remote_directory = m.get('RemoteDirectory')
        if m.get('VolumeMountpoint') is not None:
            self.volume_mountpoint = m.get('VolumeMountpoint')
        if m.get('LocalDirectory') is not None:
            self.local_directory = m.get('LocalDirectory')
        if m.get('VolumeType') is not None:
            self.volume_type = m.get('VolumeType')
        if m.get('VolumeProtocol') is not None:
            self.volume_protocol = m.get('VolumeProtocol')
        if m.get('Location') is not None:
            self.location = m.get('Location')
        return self


class CreateClusterRequestPostInstallScript(TeaModel):
    def __init__(
        self,
        args: str = None,
        url: str = None,
    ):
        self.args = args
        self.url = url

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.args is not None:
            result['Args'] = self.args
        if self.url is not None:
            result['Url'] = self.url
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Args') is not None:
            self.args = m.get('Args')
        if m.get('Url') is not None:
            self.url = m.get('Url')
        return self


class CreateClusterRequest(TeaModel):
    def __init__(
        self,
        ecs_order: CreateClusterRequestEcsOrder = None,
        zone_id: str = None,
        name: str = None,
        description: str = None,
        ehpc_version: str = None,
        client_version: str = None,
        os_tag: str = None,
        account_type: str = None,
        scheduler_type: str = None,
        security_group_id: str = None,
        security_group_name: str = None,
        vpc_id: str = None,
        v_switch_id: str = None,
        volume_type: str = None,
        volume_id: str = None,
        volume_protocol: str = None,
        volume_mountpoint: str = None,
        remote_directory: str = None,
        deploy_mode: str = None,
        ha_enable: bool = None,
        ecs_charge_type: str = None,
        password: str = None,
        key_pair_name: str = None,
        image_owner_alias: str = None,
        image_id: str = None,
        scc_cluster_id: str = None,
        compute_spot_strategy: str = None,
        compute_spot_price_limit: str = None,
        compute_enable_ht: bool = None,
        period: int = None,
        period_unit: str = None,
        auto_renew: str = None,
        auto_renew_period: int = None,
        input_file_url: str = None,
        job_queue: str = None,
        system_disk_type: str = None,
        system_disk_size: int = None,
        remote_vis_enable: str = None,
        resource_group_id: str = None,
        client_token: str = None,
        without_elastic_ip: bool = None,
        application: List[CreateClusterRequestApplication] = None,
        additional_volumes: List[CreateClusterRequestAdditionalVolumes] = None,
        post_install_script: List[CreateClusterRequestPostInstallScript] = None,
    ):
        self.ecs_order = ecs_order
        self.zone_id = zone_id
        self.name = name
        self.description = description
        self.ehpc_version = ehpc_version
        self.client_version = client_version
        self.os_tag = os_tag
        self.account_type = account_type
        self.scheduler_type = scheduler_type
        self.security_group_id = security_group_id
        self.security_group_name = security_group_name
        self.vpc_id = vpc_id
        self.v_switch_id = v_switch_id
        self.volume_type = volume_type
        self.volume_id = volume_id
        self.volume_protocol = volume_protocol
        self.volume_mountpoint = volume_mountpoint
        self.remote_directory = remote_directory
        self.deploy_mode = deploy_mode
        self.ha_enable = ha_enable
        self.ecs_charge_type = ecs_charge_type
        self.password = password
        self.key_pair_name = key_pair_name
        self.image_owner_alias = image_owner_alias
        self.image_id = image_id
        self.scc_cluster_id = scc_cluster_id
        self.compute_spot_strategy = compute_spot_strategy
        self.compute_spot_price_limit = compute_spot_price_limit
        self.compute_enable_ht = compute_enable_ht
        self.period = period
        self.period_unit = period_unit
        self.auto_renew = auto_renew
        self.auto_renew_period = auto_renew_period
        self.input_file_url = input_file_url
        self.job_queue = job_queue
        self.system_disk_type = system_disk_type
        self.system_disk_size = system_disk_size
        self.remote_vis_enable = remote_vis_enable
        self.resource_group_id = resource_group_id
        self.client_token = client_token
        self.without_elastic_ip = without_elastic_ip
        self.application = application
        self.additional_volumes = additional_volumes
        self.post_install_script = post_install_script

    def validate(self):
        if self.ecs_order:
            self.ecs_order.validate()
        if self.application:
            for k in self.application:
                if k:
                    k.validate()
        if self.additional_volumes:
            for k in self.additional_volumes:
                if k:
                    k.validate()
        if self.post_install_script:
            for k in self.post_install_script:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.ecs_order is not None:
            result['EcsOrder'] = self.ecs_order.to_map()
        if self.zone_id is not None:
            result['ZoneId'] = self.zone_id
        if self.name is not None:
            result['Name'] = self.name
        if self.description is not None:
            result['Description'] = self.description
        if self.ehpc_version is not None:
            result['EhpcVersion'] = self.ehpc_version
        if self.client_version is not None:
            result['ClientVersion'] = self.client_version
        if self.os_tag is not None:
            result['OsTag'] = self.os_tag
        if self.account_type is not None:
            result['AccountType'] = self.account_type
        if self.scheduler_type is not None:
            result['SchedulerType'] = self.scheduler_type
        if self.security_group_id is not None:
            result['SecurityGroupId'] = self.security_group_id
        if self.security_group_name is not None:
            result['SecurityGroupName'] = self.security_group_name
        if self.vpc_id is not None:
            result['VpcId'] = self.vpc_id
        if self.v_switch_id is not None:
            result['VSwitchId'] = self.v_switch_id
        if self.volume_type is not None:
            result['VolumeType'] = self.volume_type
        if self.volume_id is not None:
            result['VolumeId'] = self.volume_id
        if self.volume_protocol is not None:
            result['VolumeProtocol'] = self.volume_protocol
        if self.volume_mountpoint is not None:
            result['VolumeMountpoint'] = self.volume_mountpoint
        if self.remote_directory is not None:
            result['RemoteDirectory'] = self.remote_directory
        if self.deploy_mode is not None:
            result['DeployMode'] = self.deploy_mode
        if self.ha_enable is not None:
            result['HaEnable'] = self.ha_enable
        if self.ecs_charge_type is not None:
            result['EcsChargeType'] = self.ecs_charge_type
        if self.password is not None:
            result['Password'] = self.password
        if self.key_pair_name is not None:
            result['KeyPairName'] = self.key_pair_name
        if self.image_owner_alias is not None:
            result['ImageOwnerAlias'] = self.image_owner_alias
        if self.image_id is not None:
            result['ImageId'] = self.image_id
        if self.scc_cluster_id is not None:
            result['SccClusterId'] = self.scc_cluster_id
        if self.compute_spot_strategy is not None:
            result['ComputeSpotStrategy'] = self.compute_spot_strategy
        if self.compute_spot_price_limit is not None:
            result['ComputeSpotPriceLimit'] = self.compute_spot_price_limit
        if self.compute_enable_ht is not None:
            result['ComputeEnableHt'] = self.compute_enable_ht
        if self.period is not None:
            result['Period'] = self.period
        if self.period_unit is not None:
            result['PeriodUnit'] = self.period_unit
        if self.auto_renew is not None:
            result['AutoRenew'] = self.auto_renew
        if self.auto_renew_period is not None:
            result['AutoRenewPeriod'] = self.auto_renew_period
        if self.input_file_url is not None:
            result['InputFileUrl'] = self.input_file_url
        if self.job_queue is not None:
            result['JobQueue'] = self.job_queue
        if self.system_disk_type is not None:
            result['SystemDiskType'] = self.system_disk_type
        if self.system_disk_size is not None:
            result['SystemDiskSize'] = self.system_disk_size
        if self.remote_vis_enable is not None:
            result['RemoteVisEnable'] = self.remote_vis_enable
        if self.resource_group_id is not None:
            result['ResourceGroupId'] = self.resource_group_id
        if self.client_token is not None:
            result['ClientToken'] = self.client_token
        if self.without_elastic_ip is not None:
            result['WithoutElasticIp'] = self.without_elastic_ip
        result['Application'] = []
        if self.application is not None:
            for k in self.application:
                result['Application'].append(k.to_map() if k else None)
        result['AdditionalVolumes'] = []
        if self.additional_volumes is not None:
            for k in self.additional_volumes:
                result['AdditionalVolumes'].append(k.to_map() if k else None)
        result['PostInstallScript'] = []
        if self.post_install_script is not None:
            for k in self.post_install_script:
                result['PostInstallScript'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('EcsOrder') is not None:
            temp_model = CreateClusterRequestEcsOrder()
            self.ecs_order = temp_model.from_map(m['EcsOrder'])
        if m.get('ZoneId') is not None:
            self.zone_id = m.get('ZoneId')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('EhpcVersion') is not None:
            self.ehpc_version = m.get('EhpcVersion')
        if m.get('ClientVersion') is not None:
            self.client_version = m.get('ClientVersion')
        if m.get('OsTag') is not None:
            self.os_tag = m.get('OsTag')
        if m.get('AccountType') is not None:
            self.account_type = m.get('AccountType')
        if m.get('SchedulerType') is not None:
            self.scheduler_type = m.get('SchedulerType')
        if m.get('SecurityGroupId') is not None:
            self.security_group_id = m.get('SecurityGroupId')
        if m.get('SecurityGroupName') is not None:
            self.security_group_name = m.get('SecurityGroupName')
        if m.get('VpcId') is not None:
            self.vpc_id = m.get('VpcId')
        if m.get('VSwitchId') is not None:
            self.v_switch_id = m.get('VSwitchId')
        if m.get('VolumeType') is not None:
            self.volume_type = m.get('VolumeType')
        if m.get('VolumeId') is not None:
            self.volume_id = m.get('VolumeId')
        if m.get('VolumeProtocol') is not None:
            self.volume_protocol = m.get('VolumeProtocol')
        if m.get('VolumeMountpoint') is not None:
            self.volume_mountpoint = m.get('VolumeMountpoint')
        if m.get('RemoteDirectory') is not None:
            self.remote_directory = m.get('RemoteDirectory')
        if m.get('DeployMode') is not None:
            self.deploy_mode = m.get('DeployMode')
        if m.get('HaEnable') is not None:
            self.ha_enable = m.get('HaEnable')
        if m.get('EcsChargeType') is not None:
            self.ecs_charge_type = m.get('EcsChargeType')
        if m.get('Password') is not None:
            self.password = m.get('Password')
        if m.get('KeyPairName') is not None:
            self.key_pair_name = m.get('KeyPairName')
        if m.get('ImageOwnerAlias') is not None:
            self.image_owner_alias = m.get('ImageOwnerAlias')
        if m.get('ImageId') is not None:
            self.image_id = m.get('ImageId')
        if m.get('SccClusterId') is not None:
            self.scc_cluster_id = m.get('SccClusterId')
        if m.get('ComputeSpotStrategy') is not None:
            self.compute_spot_strategy = m.get('ComputeSpotStrategy')
        if m.get('ComputeSpotPriceLimit') is not None:
            self.compute_spot_price_limit = m.get('ComputeSpotPriceLimit')
        if m.get('ComputeEnableHt') is not None:
            self.compute_enable_ht = m.get('ComputeEnableHt')
        if m.get('Period') is not None:
            self.period = m.get('Period')
        if m.get('PeriodUnit') is not None:
            self.period_unit = m.get('PeriodUnit')
        if m.get('AutoRenew') is not None:
            self.auto_renew = m.get('AutoRenew')
        if m.get('AutoRenewPeriod') is not None:
            self.auto_renew_period = m.get('AutoRenewPeriod')
        if m.get('InputFileUrl') is not None:
            self.input_file_url = m.get('InputFileUrl')
        if m.get('JobQueue') is not None:
            self.job_queue = m.get('JobQueue')
        if m.get('SystemDiskType') is not None:
            self.system_disk_type = m.get('SystemDiskType')
        if m.get('SystemDiskSize') is not None:
            self.system_disk_size = m.get('SystemDiskSize')
        if m.get('RemoteVisEnable') is not None:
            self.remote_vis_enable = m.get('RemoteVisEnable')
        if m.get('ResourceGroupId') is not None:
            self.resource_group_id = m.get('ResourceGroupId')
        if m.get('ClientToken') is not None:
            self.client_token = m.get('ClientToken')
        if m.get('WithoutElasticIp') is not None:
            self.without_elastic_ip = m.get('WithoutElasticIp')
        self.application = []
        if m.get('Application') is not None:
            for k in m.get('Application'):
                temp_model = CreateClusterRequestApplication()
                self.application.append(temp_model.from_map(k))
        self.additional_volumes = []
        if m.get('AdditionalVolumes') is not None:
            for k in m.get('AdditionalVolumes'):
                temp_model = CreateClusterRequestAdditionalVolumes()
                self.additional_volumes.append(temp_model.from_map(k))
        self.post_install_script = []
        if m.get('PostInstallScript') is not None:
            for k in m.get('PostInstallScript'):
                temp_model = CreateClusterRequestPostInstallScript()
                self.post_install_script.append(temp_model.from_map(k))
        return self


class CreateClusterResponseBody(TeaModel):
    def __init__(
        self,
        task_id: str = None,
        request_id: str = None,
        cluster_id: str = None,
    ):
        self.task_id = task_id
        self.request_id = request_id
        self.cluster_id = cluster_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.task_id is not None:
            result['TaskId'] = self.task_id
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TaskId') is not None:
            self.task_id = m.get('TaskId')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        return self


class CreateClusterResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: CreateClusterResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = CreateClusterResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateGWSClusterRequest(TeaModel):
    def __init__(
        self,
        vpc_id: str = None,
        cluster_type: str = None,
        name: str = None,
        v_switch_id: str = None,
    ):
        self.vpc_id = vpc_id
        self.cluster_type = cluster_type
        self.name = name
        self.v_switch_id = v_switch_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.vpc_id is not None:
            result['VpcId'] = self.vpc_id
        if self.cluster_type is not None:
            result['ClusterType'] = self.cluster_type
        if self.name is not None:
            result['Name'] = self.name
        if self.v_switch_id is not None:
            result['VSwitchId'] = self.v_switch_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('VpcId') is not None:
            self.vpc_id = m.get('VpcId')
        if m.get('ClusterType') is not None:
            self.cluster_type = m.get('ClusterType')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('VSwitchId') is not None:
            self.v_switch_id = m.get('VSwitchId')
        return self


class CreateGWSClusterResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        cluster_id: str = None,
    ):
        self.request_id = request_id
        self.cluster_id = cluster_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        return self


class CreateGWSClusterResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: CreateGWSClusterResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = CreateGWSClusterResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateGWSImageRequest(TeaModel):
    def __init__(
        self,
        instance_id: str = None,
        name: str = None,
    ):
        self.instance_id = instance_id
        self.name = name

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.name is not None:
            result['Name'] = self.name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        return self


class CreateGWSImageResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        image_id: str = None,
    ):
        self.request_id = request_id
        self.image_id = image_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.image_id is not None:
            result['ImageId'] = self.image_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('ImageId') is not None:
            self.image_id = m.get('ImageId')
        return self


class CreateGWSImageResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: CreateGWSImageResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = CreateGWSImageResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateGWSInstanceRequest(TeaModel):
    def __init__(
        self,
        cluster_id: str = None,
        image_id: str = None,
        system_disk_size: int = None,
        system_disk_category: str = None,
        instance_type: str = None,
        instance_charge_type: str = None,
        work_mode: str = None,
        allocate_public_address: bool = None,
        internet_charge_type: str = None,
        internet_max_bandwidth_in: int = None,
        internet_max_bandwidth_out: int = None,
        name: str = None,
        period: str = None,
        period_unit: str = None,
        auto_renew: bool = None,
        app_list: str = None,
        v_switch_id: str = None,
    ):
        self.cluster_id = cluster_id
        self.image_id = image_id
        self.system_disk_size = system_disk_size
        self.system_disk_category = system_disk_category
        self.instance_type = instance_type
        self.instance_charge_type = instance_charge_type
        self.work_mode = work_mode
        self.allocate_public_address = allocate_public_address
        self.internet_charge_type = internet_charge_type
        self.internet_max_bandwidth_in = internet_max_bandwidth_in
        self.internet_max_bandwidth_out = internet_max_bandwidth_out
        self.name = name
        self.period = period
        self.period_unit = period_unit
        self.auto_renew = auto_renew
        self.app_list = app_list
        self.v_switch_id = v_switch_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        if self.image_id is not None:
            result['ImageId'] = self.image_id
        if self.system_disk_size is not None:
            result['SystemDiskSize'] = self.system_disk_size
        if self.system_disk_category is not None:
            result['SystemDiskCategory'] = self.system_disk_category
        if self.instance_type is not None:
            result['InstanceType'] = self.instance_type
        if self.instance_charge_type is not None:
            result['InstanceChargeType'] = self.instance_charge_type
        if self.work_mode is not None:
            result['WorkMode'] = self.work_mode
        if self.allocate_public_address is not None:
            result['AllocatePublicAddress'] = self.allocate_public_address
        if self.internet_charge_type is not None:
            result['InternetChargeType'] = self.internet_charge_type
        if self.internet_max_bandwidth_in is not None:
            result['InternetMaxBandwidthIn'] = self.internet_max_bandwidth_in
        if self.internet_max_bandwidth_out is not None:
            result['InternetMaxBandwidthOut'] = self.internet_max_bandwidth_out
        if self.name is not None:
            result['Name'] = self.name
        if self.period is not None:
            result['Period'] = self.period
        if self.period_unit is not None:
            result['PeriodUnit'] = self.period_unit
        if self.auto_renew is not None:
            result['AutoRenew'] = self.auto_renew
        if self.app_list is not None:
            result['AppList'] = self.app_list
        if self.v_switch_id is not None:
            result['VSwitchId'] = self.v_switch_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        if m.get('ImageId') is not None:
            self.image_id = m.get('ImageId')
        if m.get('SystemDiskSize') is not None:
            self.system_disk_size = m.get('SystemDiskSize')
        if m.get('SystemDiskCategory') is not None:
            self.system_disk_category = m.get('SystemDiskCategory')
        if m.get('InstanceType') is not None:
            self.instance_type = m.get('InstanceType')
        if m.get('InstanceChargeType') is not None:
            self.instance_charge_type = m.get('InstanceChargeType')
        if m.get('WorkMode') is not None:
            self.work_mode = m.get('WorkMode')
        if m.get('AllocatePublicAddress') is not None:
            self.allocate_public_address = m.get('AllocatePublicAddress')
        if m.get('InternetChargeType') is not None:
            self.internet_charge_type = m.get('InternetChargeType')
        if m.get('InternetMaxBandwidthIn') is not None:
            self.internet_max_bandwidth_in = m.get('InternetMaxBandwidthIn')
        if m.get('InternetMaxBandwidthOut') is not None:
            self.internet_max_bandwidth_out = m.get('InternetMaxBandwidthOut')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Period') is not None:
            self.period = m.get('Period')
        if m.get('PeriodUnit') is not None:
            self.period_unit = m.get('PeriodUnit')
        if m.get('AutoRenew') is not None:
            self.auto_renew = m.get('AutoRenew')
        if m.get('AppList') is not None:
            self.app_list = m.get('AppList')
        if m.get('VSwitchId') is not None:
            self.v_switch_id = m.get('VSwitchId')
        return self


class CreateGWSInstanceResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        instance_id: str = None,
    ):
        self.request_id = request_id
        self.instance_id = instance_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        return self


class CreateGWSInstanceResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: CreateGWSInstanceResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = CreateGWSInstanceResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateHybridClusterRequestEcsOrderCompute(TeaModel):
    def __init__(
        self,
        instance_type: str = None,
    ):
        self.instance_type = instance_type

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.instance_type is not None:
            result['InstanceType'] = self.instance_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('InstanceType') is not None:
            self.instance_type = m.get('InstanceType')
        return self


class CreateHybridClusterRequestEcsOrder(TeaModel):
    def __init__(
        self,
        compute: CreateHybridClusterRequestEcsOrderCompute = None,
    ):
        self.compute = compute

    def validate(self):
        self.validate_required(self.compute, 'compute')
        if self.compute:
            self.compute.validate()

    def to_map(self):
        result = dict()
        if self.compute is not None:
            result['Compute'] = self.compute.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Compute') is not None:
            temp_model = CreateHybridClusterRequestEcsOrderCompute()
            self.compute = temp_model.from_map(m['Compute'])
        return self


class CreateHybridClusterRequestNodes(TeaModel):
    def __init__(
        self,
        scheduler_type: str = None,
        ip_address: str = None,
        host_name: str = None,
        role: str = None,
        account_type: str = None,
    ):
        self.scheduler_type = scheduler_type
        self.ip_address = ip_address
        self.host_name = host_name
        self.role = role
        self.account_type = account_type

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.scheduler_type is not None:
            result['SchedulerType'] = self.scheduler_type
        if self.ip_address is not None:
            result['IpAddress'] = self.ip_address
        if self.host_name is not None:
            result['HostName'] = self.host_name
        if self.role is not None:
            result['Role'] = self.role
        if self.account_type is not None:
            result['AccountType'] = self.account_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('SchedulerType') is not None:
            self.scheduler_type = m.get('SchedulerType')
        if m.get('IpAddress') is not None:
            self.ip_address = m.get('IpAddress')
        if m.get('HostName') is not None:
            self.host_name = m.get('HostName')
        if m.get('Role') is not None:
            self.role = m.get('Role')
        if m.get('AccountType') is not None:
            self.account_type = m.get('AccountType')
        return self


class CreateHybridClusterRequestApplication(TeaModel):
    def __init__(
        self,
        tag: str = None,
    ):
        self.tag = tag

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.tag is not None:
            result['Tag'] = self.tag
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Tag') is not None:
            self.tag = m.get('Tag')
        return self


class CreateHybridClusterRequestPostInstallScript(TeaModel):
    def __init__(
        self,
        args: str = None,
        url: str = None,
    ):
        self.args = args
        self.url = url

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.args is not None:
            result['Args'] = self.args
        if self.url is not None:
            result['Url'] = self.url
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Args') is not None:
            self.args = m.get('Args')
        if m.get('Url') is not None:
            self.url = m.get('Url')
        return self


class CreateHybridClusterRequest(TeaModel):
    def __init__(
        self,
        ecs_order: CreateHybridClusterRequestEcsOrder = None,
        zone_id: str = None,
        name: str = None,
        description: str = None,
        ehpc_version: str = None,
        client_version: str = None,
        os_tag: str = None,
        domain: str = None,
        location: str = None,
        security_group_id: str = None,
        security_group_name: str = None,
        vpc_id: str = None,
        v_switch_id: str = None,
        volume_type: str = None,
        volume_id: str = None,
        volume_protocol: str = None,
        volume_mountpoint: str = None,
        remote_directory: str = None,
        on_premise_volume_protocol: str = None,
        on_premise_volume_mount_point: str = None,
        on_premise_volume_remote_path: str = None,
        on_premise_volume_local_path: str = None,
        password: str = None,
        key_pair_name: str = None,
        job_queue: str = None,
        resource_group_id: str = None,
        scheduler_pre_install: bool = None,
        compute_spot_strategy: str = None,
        compute_spot_price_limit: float = None,
        image_owner_alias: str = None,
        image_id: str = None,
        client_token: str = None,
        nodes: List[CreateHybridClusterRequestNodes] = None,
        application: List[CreateHybridClusterRequestApplication] = None,
        post_install_script: List[CreateHybridClusterRequestPostInstallScript] = None,
    ):
        self.ecs_order = ecs_order
        self.zone_id = zone_id
        self.name = name
        self.description = description
        self.ehpc_version = ehpc_version
        self.client_version = client_version
        self.os_tag = os_tag
        self.domain = domain
        self.location = location
        self.security_group_id = security_group_id
        self.security_group_name = security_group_name
        self.vpc_id = vpc_id
        self.v_switch_id = v_switch_id
        self.volume_type = volume_type
        self.volume_id = volume_id
        self.volume_protocol = volume_protocol
        self.volume_mountpoint = volume_mountpoint
        self.remote_directory = remote_directory
        self.on_premise_volume_protocol = on_premise_volume_protocol
        self.on_premise_volume_mount_point = on_premise_volume_mount_point
        self.on_premise_volume_remote_path = on_premise_volume_remote_path
        self.on_premise_volume_local_path = on_premise_volume_local_path
        self.password = password
        self.key_pair_name = key_pair_name
        self.job_queue = job_queue
        self.resource_group_id = resource_group_id
        self.scheduler_pre_install = scheduler_pre_install
        self.compute_spot_strategy = compute_spot_strategy
        self.compute_spot_price_limit = compute_spot_price_limit
        self.image_owner_alias = image_owner_alias
        self.image_id = image_id
        self.client_token = client_token
        self.nodes = nodes
        self.application = application
        self.post_install_script = post_install_script

    def validate(self):
        if self.ecs_order:
            self.ecs_order.validate()
        if self.nodes:
            for k in self.nodes:
                if k:
                    k.validate()
        if self.application:
            for k in self.application:
                if k:
                    k.validate()
        if self.post_install_script:
            for k in self.post_install_script:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.ecs_order is not None:
            result['EcsOrder'] = self.ecs_order.to_map()
        if self.zone_id is not None:
            result['ZoneId'] = self.zone_id
        if self.name is not None:
            result['Name'] = self.name
        if self.description is not None:
            result['Description'] = self.description
        if self.ehpc_version is not None:
            result['EhpcVersion'] = self.ehpc_version
        if self.client_version is not None:
            result['ClientVersion'] = self.client_version
        if self.os_tag is not None:
            result['OsTag'] = self.os_tag
        if self.domain is not None:
            result['Domain'] = self.domain
        if self.location is not None:
            result['Location'] = self.location
        if self.security_group_id is not None:
            result['SecurityGroupId'] = self.security_group_id
        if self.security_group_name is not None:
            result['SecurityGroupName'] = self.security_group_name
        if self.vpc_id is not None:
            result['VpcId'] = self.vpc_id
        if self.v_switch_id is not None:
            result['VSwitchId'] = self.v_switch_id
        if self.volume_type is not None:
            result['VolumeType'] = self.volume_type
        if self.volume_id is not None:
            result['VolumeId'] = self.volume_id
        if self.volume_protocol is not None:
            result['VolumeProtocol'] = self.volume_protocol
        if self.volume_mountpoint is not None:
            result['VolumeMountpoint'] = self.volume_mountpoint
        if self.remote_directory is not None:
            result['RemoteDirectory'] = self.remote_directory
        if self.on_premise_volume_protocol is not None:
            result['OnPremiseVolumeProtocol'] = self.on_premise_volume_protocol
        if self.on_premise_volume_mount_point is not None:
            result['OnPremiseVolumeMountPoint'] = self.on_premise_volume_mount_point
        if self.on_premise_volume_remote_path is not None:
            result['OnPremiseVolumeRemotePath'] = self.on_premise_volume_remote_path
        if self.on_premise_volume_local_path is not None:
            result['OnPremiseVolumeLocalPath'] = self.on_premise_volume_local_path
        if self.password is not None:
            result['Password'] = self.password
        if self.key_pair_name is not None:
            result['KeyPairName'] = self.key_pair_name
        if self.job_queue is not None:
            result['JobQueue'] = self.job_queue
        if self.resource_group_id is not None:
            result['ResourceGroupId'] = self.resource_group_id
        if self.scheduler_pre_install is not None:
            result['SchedulerPreInstall'] = self.scheduler_pre_install
        if self.compute_spot_strategy is not None:
            result['ComputeSpotStrategy'] = self.compute_spot_strategy
        if self.compute_spot_price_limit is not None:
            result['ComputeSpotPriceLimit'] = self.compute_spot_price_limit
        if self.image_owner_alias is not None:
            result['ImageOwnerAlias'] = self.image_owner_alias
        if self.image_id is not None:
            result['ImageId'] = self.image_id
        if self.client_token is not None:
            result['ClientToken'] = self.client_token
        result['Nodes'] = []
        if self.nodes is not None:
            for k in self.nodes:
                result['Nodes'].append(k.to_map() if k else None)
        result['Application'] = []
        if self.application is not None:
            for k in self.application:
                result['Application'].append(k.to_map() if k else None)
        result['PostInstallScript'] = []
        if self.post_install_script is not None:
            for k in self.post_install_script:
                result['PostInstallScript'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('EcsOrder') is not None:
            temp_model = CreateHybridClusterRequestEcsOrder()
            self.ecs_order = temp_model.from_map(m['EcsOrder'])
        if m.get('ZoneId') is not None:
            self.zone_id = m.get('ZoneId')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('EhpcVersion') is not None:
            self.ehpc_version = m.get('EhpcVersion')
        if m.get('ClientVersion') is not None:
            self.client_version = m.get('ClientVersion')
        if m.get('OsTag') is not None:
            self.os_tag = m.get('OsTag')
        if m.get('Domain') is not None:
            self.domain = m.get('Domain')
        if m.get('Location') is not None:
            self.location = m.get('Location')
        if m.get('SecurityGroupId') is not None:
            self.security_group_id = m.get('SecurityGroupId')
        if m.get('SecurityGroupName') is not None:
            self.security_group_name = m.get('SecurityGroupName')
        if m.get('VpcId') is not None:
            self.vpc_id = m.get('VpcId')
        if m.get('VSwitchId') is not None:
            self.v_switch_id = m.get('VSwitchId')
        if m.get('VolumeType') is not None:
            self.volume_type = m.get('VolumeType')
        if m.get('VolumeId') is not None:
            self.volume_id = m.get('VolumeId')
        if m.get('VolumeProtocol') is not None:
            self.volume_protocol = m.get('VolumeProtocol')
        if m.get('VolumeMountpoint') is not None:
            self.volume_mountpoint = m.get('VolumeMountpoint')
        if m.get('RemoteDirectory') is not None:
            self.remote_directory = m.get('RemoteDirectory')
        if m.get('OnPremiseVolumeProtocol') is not None:
            self.on_premise_volume_protocol = m.get('OnPremiseVolumeProtocol')
        if m.get('OnPremiseVolumeMountPoint') is not None:
            self.on_premise_volume_mount_point = m.get('OnPremiseVolumeMountPoint')
        if m.get('OnPremiseVolumeRemotePath') is not None:
            self.on_premise_volume_remote_path = m.get('OnPremiseVolumeRemotePath')
        if m.get('OnPremiseVolumeLocalPath') is not None:
            self.on_premise_volume_local_path = m.get('OnPremiseVolumeLocalPath')
        if m.get('Password') is not None:
            self.password = m.get('Password')
        if m.get('KeyPairName') is not None:
            self.key_pair_name = m.get('KeyPairName')
        if m.get('JobQueue') is not None:
            self.job_queue = m.get('JobQueue')
        if m.get('ResourceGroupId') is not None:
            self.resource_group_id = m.get('ResourceGroupId')
        if m.get('SchedulerPreInstall') is not None:
            self.scheduler_pre_install = m.get('SchedulerPreInstall')
        if m.get('ComputeSpotStrategy') is not None:
            self.compute_spot_strategy = m.get('ComputeSpotStrategy')
        if m.get('ComputeSpotPriceLimit') is not None:
            self.compute_spot_price_limit = m.get('ComputeSpotPriceLimit')
        if m.get('ImageOwnerAlias') is not None:
            self.image_owner_alias = m.get('ImageOwnerAlias')
        if m.get('ImageId') is not None:
            self.image_id = m.get('ImageId')
        if m.get('ClientToken') is not None:
            self.client_token = m.get('ClientToken')
        self.nodes = []
        if m.get('Nodes') is not None:
            for k in m.get('Nodes'):
                temp_model = CreateHybridClusterRequestNodes()
                self.nodes.append(temp_model.from_map(k))
        self.application = []
        if m.get('Application') is not None:
            for k in m.get('Application'):
                temp_model = CreateHybridClusterRequestApplication()
                self.application.append(temp_model.from_map(k))
        self.post_install_script = []
        if m.get('PostInstallScript') is not None:
            for k in m.get('PostInstallScript'):
                temp_model = CreateHybridClusterRequestPostInstallScript()
                self.post_install_script.append(temp_model.from_map(k))
        return self


class CreateHybridClusterResponseBody(TeaModel):
    def __init__(
        self,
        task_id: str = None,
        request_id: str = None,
        cluster_id: str = None,
    ):
        self.task_id = task_id
        self.request_id = request_id
        self.cluster_id = cluster_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.task_id is not None:
            result['TaskId'] = self.task_id
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TaskId') is not None:
            self.task_id = m.get('TaskId')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        return self


class CreateHybridClusterResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: CreateHybridClusterResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = CreateHybridClusterResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateJobFileRequest(TeaModel):
    def __init__(
        self,
        cluster_id: str = None,
        runas_user: str = None,
        runas_user_password: str = None,
        content: str = None,
        target_file: str = None,
    ):
        self.cluster_id = cluster_id
        self.runas_user = runas_user
        self.runas_user_password = runas_user_password
        self.content = content
        self.target_file = target_file

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        if self.runas_user is not None:
            result['RunasUser'] = self.runas_user
        if self.runas_user_password is not None:
            result['RunasUserPassword'] = self.runas_user_password
        if self.content is not None:
            result['Content'] = self.content
        if self.target_file is not None:
            result['TargetFile'] = self.target_file
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        if m.get('RunasUser') is not None:
            self.runas_user = m.get('RunasUser')
        if m.get('RunasUserPassword') is not None:
            self.runas_user_password = m.get('RunasUserPassword')
        if m.get('Content') is not None:
            self.content = m.get('Content')
        if m.get('TargetFile') is not None:
            self.target_file = m.get('TargetFile')
        return self


class CreateJobFileResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        template_id: str = None,
    ):
        self.request_id = request_id
        self.template_id = template_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.template_id is not None:
            result['TemplateId'] = self.template_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('TemplateId') is not None:
            self.template_id = m.get('TemplateId')
        return self


class CreateJobFileResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: CreateJobFileResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = CreateJobFileResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateJobTemplateRequest(TeaModel):
    def __init__(
        self,
        command_line: str = None,
        name: str = None,
        runas_user: str = None,
        priority: int = None,
        package_path: str = None,
        stdout_redirect_path: str = None,
        stderr_redirect_path: str = None,
        re_runable: bool = None,
        array_request: str = None,
        variables: str = None,
    ):
        self.command_line = command_line
        self.name = name
        self.runas_user = runas_user
        self.priority = priority
        self.package_path = package_path
        self.stdout_redirect_path = stdout_redirect_path
        self.stderr_redirect_path = stderr_redirect_path
        self.re_runable = re_runable
        self.array_request = array_request
        self.variables = variables

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.command_line is not None:
            result['CommandLine'] = self.command_line
        if self.name is not None:
            result['Name'] = self.name
        if self.runas_user is not None:
            result['RunasUser'] = self.runas_user
        if self.priority is not None:
            result['Priority'] = self.priority
        if self.package_path is not None:
            result['PackagePath'] = self.package_path
        if self.stdout_redirect_path is not None:
            result['StdoutRedirectPath'] = self.stdout_redirect_path
        if self.stderr_redirect_path is not None:
            result['StderrRedirectPath'] = self.stderr_redirect_path
        if self.re_runable is not None:
            result['ReRunable'] = self.re_runable
        if self.array_request is not None:
            result['ArrayRequest'] = self.array_request
        if self.variables is not None:
            result['Variables'] = self.variables
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('CommandLine') is not None:
            self.command_line = m.get('CommandLine')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('RunasUser') is not None:
            self.runas_user = m.get('RunasUser')
        if m.get('Priority') is not None:
            self.priority = m.get('Priority')
        if m.get('PackagePath') is not None:
            self.package_path = m.get('PackagePath')
        if m.get('StdoutRedirectPath') is not None:
            self.stdout_redirect_path = m.get('StdoutRedirectPath')
        if m.get('StderrRedirectPath') is not None:
            self.stderr_redirect_path = m.get('StderrRedirectPath')
        if m.get('ReRunable') is not None:
            self.re_runable = m.get('ReRunable')
        if m.get('ArrayRequest') is not None:
            self.array_request = m.get('ArrayRequest')
        if m.get('Variables') is not None:
            self.variables = m.get('Variables')
        return self


class CreateJobTemplateResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        template_id: str = None,
    ):
        self.request_id = request_id
        self.template_id = template_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.template_id is not None:
            result['TemplateId'] = self.template_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('TemplateId') is not None:
            self.template_id = m.get('TemplateId')
        return self


class CreateJobTemplateResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: CreateJobTemplateResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = CreateJobTemplateResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteClusterRequest(TeaModel):
    def __init__(
        self,
        cluster_id: str = None,
        release_instance: str = None,
    ):
        self.cluster_id = cluster_id
        self.release_instance = release_instance

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        if self.release_instance is not None:
            result['ReleaseInstance'] = self.release_instance
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        if m.get('ReleaseInstance') is not None:
            self.release_instance = m.get('ReleaseInstance')
        return self


class DeleteClusterResponseBody(TeaModel):
    def __init__(
        self,
        task_id: str = None,
        request_id: str = None,
    ):
        self.task_id = task_id
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.task_id is not None:
            result['TaskId'] = self.task_id
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TaskId') is not None:
            self.task_id = m.get('TaskId')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class DeleteClusterResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DeleteClusterResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DeleteClusterResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteContainerAppsRequestContainerApp(TeaModel):
    def __init__(
        self,
        id: str = None,
    ):
        self.id = id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.id is not None:
            result['Id'] = self.id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Id') is not None:
            self.id = m.get('Id')
        return self


class DeleteContainerAppsRequest(TeaModel):
    def __init__(
        self,
        container_app: List[DeleteContainerAppsRequestContainerApp] = None,
    ):
        self.container_app = container_app

    def validate(self):
        if self.container_app:
            for k in self.container_app:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['ContainerApp'] = []
        if self.container_app is not None:
            for k in self.container_app:
                result['ContainerApp'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.container_app = []
        if m.get('ContainerApp') is not None:
            for k in m.get('ContainerApp'):
                temp_model = DeleteContainerAppsRequestContainerApp()
                self.container_app.append(temp_model.from_map(k))
        return self


class DeleteContainerAppsResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class DeleteContainerAppsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DeleteContainerAppsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DeleteContainerAppsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteGWSClusterRequest(TeaModel):
    def __init__(
        self,
        cluster_id: str = None,
    ):
        self.cluster_id = cluster_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        return self


class DeleteGWSClusterResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class DeleteGWSClusterResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DeleteGWSClusterResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DeleteGWSClusterResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteGWSInstanceRequest(TeaModel):
    def __init__(
        self,
        instance_id: str = None,
    ):
        self.instance_id = instance_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        return self


class DeleteGWSInstanceResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class DeleteGWSInstanceResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DeleteGWSInstanceResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DeleteGWSInstanceResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteImageRequest(TeaModel):
    def __init__(
        self,
        cluster_id: str = None,
        repository: str = None,
        image_tag: str = None,
        container_type: str = None,
    ):
        self.cluster_id = cluster_id
        self.repository = repository
        self.image_tag = image_tag
        self.container_type = container_type

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        if self.repository is not None:
            result['Repository'] = self.repository
        if self.image_tag is not None:
            result['ImageTag'] = self.image_tag
        if self.container_type is not None:
            result['ContainerType'] = self.container_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        if m.get('Repository') is not None:
            self.repository = m.get('Repository')
        if m.get('ImageTag') is not None:
            self.image_tag = m.get('ImageTag')
        if m.get('ContainerType') is not None:
            self.container_type = m.get('ContainerType')
        return self


class DeleteImageResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class DeleteImageResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DeleteImageResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DeleteImageResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteJobsRequest(TeaModel):
    def __init__(
        self,
        cluster_id: str = None,
        jobs: str = None,
    ):
        self.cluster_id = cluster_id
        self.jobs = jobs

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        if self.jobs is not None:
            result['Jobs'] = self.jobs
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        if m.get('Jobs') is not None:
            self.jobs = m.get('Jobs')
        return self


class DeleteJobsResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class DeleteJobsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DeleteJobsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DeleteJobsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteJobTemplatesRequest(TeaModel):
    def __init__(
        self,
        templates: str = None,
    ):
        self.templates = templates

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.templates is not None:
            result['Templates'] = self.templates
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Templates') is not None:
            self.templates = m.get('Templates')
        return self


class DeleteJobTemplatesResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class DeleteJobTemplatesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DeleteJobTemplatesResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DeleteJobTemplatesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteNodesRequestInstance(TeaModel):
    def __init__(
        self,
        id: str = None,
    ):
        self.id = id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.id is not None:
            result['Id'] = self.id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Id') is not None:
            self.id = m.get('Id')
        return self


class DeleteNodesRequest(TeaModel):
    def __init__(
        self,
        cluster_id: str = None,
        release_instance: bool = None,
        instance: List[DeleteNodesRequestInstance] = None,
    ):
        self.cluster_id = cluster_id
        self.release_instance = release_instance
        self.instance = instance

    def validate(self):
        if self.instance:
            for k in self.instance:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        if self.release_instance is not None:
            result['ReleaseInstance'] = self.release_instance
        result['Instance'] = []
        if self.instance is not None:
            for k in self.instance:
                result['Instance'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        if m.get('ReleaseInstance') is not None:
            self.release_instance = m.get('ReleaseInstance')
        self.instance = []
        if m.get('Instance') is not None:
            for k in m.get('Instance'):
                temp_model = DeleteNodesRequestInstance()
                self.instance.append(temp_model.from_map(k))
        return self


class DeleteNodesResponseBody(TeaModel):
    def __init__(
        self,
        task_id: str = None,
        request_id: str = None,
    ):
        self.task_id = task_id
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.task_id is not None:
            result['TaskId'] = self.task_id
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TaskId') is not None:
            self.task_id = m.get('TaskId')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class DeleteNodesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DeleteNodesResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DeleteNodesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteQueueRequest(TeaModel):
    def __init__(
        self,
        cluster_id: str = None,
        queue_name: str = None,
    ):
        self.cluster_id = cluster_id
        self.queue_name = queue_name

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        if self.queue_name is not None:
            result['QueueName'] = self.queue_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        if m.get('QueueName') is not None:
            self.queue_name = m.get('QueueName')
        return self


class DeleteQueueResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class DeleteQueueResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DeleteQueueResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DeleteQueueResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteSecurityGroupRequest(TeaModel):
    def __init__(
        self,
        cluster_id: str = None,
        security_group_id: str = None,
    ):
        self.cluster_id = cluster_id
        self.security_group_id = security_group_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        if self.security_group_id is not None:
            result['SecurityGroupId'] = self.security_group_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        if m.get('SecurityGroupId') is not None:
            self.security_group_id = m.get('SecurityGroupId')
        return self


class DeleteSecurityGroupResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class DeleteSecurityGroupResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DeleteSecurityGroupResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DeleteSecurityGroupResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteUsersRequestUser(TeaModel):
    def __init__(
        self,
        name: str = None,
    ):
        self.name = name

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.name is not None:
            result['Name'] = self.name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Name') is not None:
            self.name = m.get('Name')
        return self


class DeleteUsersRequest(TeaModel):
    def __init__(
        self,
        cluster_id: str = None,
        user: List[DeleteUsersRequestUser] = None,
    ):
        self.cluster_id = cluster_id
        self.user = user

    def validate(self):
        if self.user:
            for k in self.user:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        result['User'] = []
        if self.user is not None:
            for k in self.user:
                result['User'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        self.user = []
        if m.get('User') is not None:
            for k in m.get('User'):
                temp_model = DeleteUsersRequestUser()
                self.user.append(temp_model.from_map(k))
        return self


class DeleteUsersResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class DeleteUsersResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DeleteUsersResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DeleteUsersResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeAutoScaleConfigRequest(TeaModel):
    def __init__(
        self,
        cluster_id: str = None,
    ):
        self.cluster_id = cluster_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        return self


class DescribeAutoScaleConfigResponseBody(TeaModel):
    def __init__(
        self,
        extra_nodes_grow_ratio: int = None,
        request_id: str = None,
        enable_auto_grow: bool = None,
        cluster_id: str = None,
        max_nodes_in_cluster: int = None,
        shrink_idle_times: int = None,
        enable_auto_shrink: bool = None,
        cluster_type: str = None,
        grow_ratio: int = None,
        grow_interval_in_minutes: int = None,
        uid: str = None,
        grow_timeout_in_minutes: int = None,
        shrink_interval_in_minutes: int = None,
        spot_price_limit: str = None,
        exclude_nodes: str = None,
        spot_strategy: str = None,
    ):
        self.extra_nodes_grow_ratio = extra_nodes_grow_ratio
        self.request_id = request_id
        self.enable_auto_grow = enable_auto_grow
        self.cluster_id = cluster_id
        self.max_nodes_in_cluster = max_nodes_in_cluster
        self.shrink_idle_times = shrink_idle_times
        self.enable_auto_shrink = enable_auto_shrink
        self.cluster_type = cluster_type
        self.grow_ratio = grow_ratio
        self.grow_interval_in_minutes = grow_interval_in_minutes
        self.uid = uid
        self.grow_timeout_in_minutes = grow_timeout_in_minutes
        self.shrink_interval_in_minutes = shrink_interval_in_minutes
        self.spot_price_limit = spot_price_limit
        self.exclude_nodes = exclude_nodes
        self.spot_strategy = spot_strategy

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.extra_nodes_grow_ratio is not None:
            result['ExtraNodesGrowRatio'] = self.extra_nodes_grow_ratio
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.enable_auto_grow is not None:
            result['EnableAutoGrow'] = self.enable_auto_grow
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        if self.max_nodes_in_cluster is not None:
            result['MaxNodesInCluster'] = self.max_nodes_in_cluster
        if self.shrink_idle_times is not None:
            result['ShrinkIdleTimes'] = self.shrink_idle_times
        if self.enable_auto_shrink is not None:
            result['EnableAutoShrink'] = self.enable_auto_shrink
        if self.cluster_type is not None:
            result['ClusterType'] = self.cluster_type
        if self.grow_ratio is not None:
            result['GrowRatio'] = self.grow_ratio
        if self.grow_interval_in_minutes is not None:
            result['GrowIntervalInMinutes'] = self.grow_interval_in_minutes
        if self.uid is not None:
            result['Uid'] = self.uid
        if self.grow_timeout_in_minutes is not None:
            result['GrowTimeoutInMinutes'] = self.grow_timeout_in_minutes
        if self.shrink_interval_in_minutes is not None:
            result['ShrinkIntervalInMinutes'] = self.shrink_interval_in_minutes
        if self.spot_price_limit is not None:
            result['SpotPriceLimit'] = self.spot_price_limit
        if self.exclude_nodes is not None:
            result['ExcludeNodes'] = self.exclude_nodes
        if self.spot_strategy is not None:
            result['SpotStrategy'] = self.spot_strategy
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ExtraNodesGrowRatio') is not None:
            self.extra_nodes_grow_ratio = m.get('ExtraNodesGrowRatio')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('EnableAutoGrow') is not None:
            self.enable_auto_grow = m.get('EnableAutoGrow')
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        if m.get('MaxNodesInCluster') is not None:
            self.max_nodes_in_cluster = m.get('MaxNodesInCluster')
        if m.get('ShrinkIdleTimes') is not None:
            self.shrink_idle_times = m.get('ShrinkIdleTimes')
        if m.get('EnableAutoShrink') is not None:
            self.enable_auto_shrink = m.get('EnableAutoShrink')
        if m.get('ClusterType') is not None:
            self.cluster_type = m.get('ClusterType')
        if m.get('GrowRatio') is not None:
            self.grow_ratio = m.get('GrowRatio')
        if m.get('GrowIntervalInMinutes') is not None:
            self.grow_interval_in_minutes = m.get('GrowIntervalInMinutes')
        if m.get('Uid') is not None:
            self.uid = m.get('Uid')
        if m.get('GrowTimeoutInMinutes') is not None:
            self.grow_timeout_in_minutes = m.get('GrowTimeoutInMinutes')
        if m.get('ShrinkIntervalInMinutes') is not None:
            self.shrink_interval_in_minutes = m.get('ShrinkIntervalInMinutes')
        if m.get('SpotPriceLimit') is not None:
            self.spot_price_limit = m.get('SpotPriceLimit')
        if m.get('ExcludeNodes') is not None:
            self.exclude_nodes = m.get('ExcludeNodes')
        if m.get('SpotStrategy') is not None:
            self.spot_strategy = m.get('SpotStrategy')
        return self


class DescribeAutoScaleConfigResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeAutoScaleConfigResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeAutoScaleConfigResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeClusterRequest(TeaModel):
    def __init__(
        self,
        cluster_id: str = None,
    ):
        self.cluster_id = cluster_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        return self


class DescribeClusterResponseBodyClusterInfoPostInstallScripts(TeaModel):
    def __init__(
        self,
        args: str = None,
        url: str = None,
    ):
        self.args = args
        self.url = url

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.args is not None:
            result['Args'] = self.args
        if self.url is not None:
            result['Url'] = self.url
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Args') is not None:
            self.args = m.get('Args')
        if m.get('Url') is not None:
            self.url = m.get('Url')
        return self


class DescribeClusterResponseBodyClusterInfoEcsInfoManager(TeaModel):
    def __init__(
        self,
        instance_type: str = None,
        count: int = None,
    ):
        self.instance_type = instance_type
        self.count = count

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.instance_type is not None:
            result['InstanceType'] = self.instance_type
        if self.count is not None:
            result['Count'] = self.count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('InstanceType') is not None:
            self.instance_type = m.get('InstanceType')
        if m.get('Count') is not None:
            self.count = m.get('Count')
        return self


class DescribeClusterResponseBodyClusterInfoEcsInfoCompute(TeaModel):
    def __init__(
        self,
        instance_type: str = None,
        count: int = None,
    ):
        self.instance_type = instance_type
        self.count = count

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.instance_type is not None:
            result['InstanceType'] = self.instance_type
        if self.count is not None:
            result['Count'] = self.count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('InstanceType') is not None:
            self.instance_type = m.get('InstanceType')
        if m.get('Count') is not None:
            self.count = m.get('Count')
        return self


class DescribeClusterResponseBodyClusterInfoEcsInfoLogin(TeaModel):
    def __init__(
        self,
        instance_type: str = None,
        count: int = None,
    ):
        self.instance_type = instance_type
        self.count = count

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.instance_type is not None:
            result['InstanceType'] = self.instance_type
        if self.count is not None:
            result['Count'] = self.count
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('InstanceType') is not None:
            self.instance_type = m.get('InstanceType')
        if m.get('Count') is not None:
            self.count = m.get('Count')
        return self


class DescribeClusterResponseBodyClusterInfoEcsInfo(TeaModel):
    def __init__(
        self,
        manager: DescribeClusterResponseBodyClusterInfoEcsInfoManager = None,
        compute: DescribeClusterResponseBodyClusterInfoEcsInfoCompute = None,
        login: DescribeClusterResponseBodyClusterInfoEcsInfoLogin = None,
    ):
        self.manager = manager
        self.compute = compute
        self.login = login

    def validate(self):
        if self.manager:
            self.manager.validate()
        if self.compute:
            self.compute.validate()
        if self.login:
            self.login.validate()

    def to_map(self):
        result = dict()
        if self.manager is not None:
            result['Manager'] = self.manager.to_map()
        if self.compute is not None:
            result['Compute'] = self.compute.to_map()
        if self.login is not None:
            result['Login'] = self.login.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Manager') is not None:
            temp_model = DescribeClusterResponseBodyClusterInfoEcsInfoManager()
            self.manager = temp_model.from_map(m['Manager'])
        if m.get('Compute') is not None:
            temp_model = DescribeClusterResponseBodyClusterInfoEcsInfoCompute()
            self.compute = temp_model.from_map(m['Compute'])
        if m.get('Login') is not None:
            temp_model = DescribeClusterResponseBodyClusterInfoEcsInfoLogin()
            self.login = temp_model.from_map(m['Login'])
        return self


class DescribeClusterResponseBodyClusterInfoApplications(TeaModel):
    def __init__(
        self,
        version: str = None,
        tag: str = None,
        name: str = None,
    ):
        self.version = version
        self.tag = tag
        self.name = name

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.version is not None:
            result['Version'] = self.version
        if self.tag is not None:
            result['Tag'] = self.tag
        if self.name is not None:
            result['Name'] = self.name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Version') is not None:
            self.version = m.get('Version')
        if m.get('Tag') is not None:
            self.tag = m.get('Tag')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        return self


class DescribeClusterResponseBodyClusterInfo(TeaModel):
    def __init__(
        self,
        status: str = None,
        vpc_id: str = None,
        key_pair_name: str = None,
        ecs_charge_type: str = None,
        security_group_id: str = None,
        scc_cluster_id: str = None,
        create_time: str = None,
        account_type: str = None,
        volume_protocol: str = None,
        description: str = None,
        volume_id: str = None,
        ha_enable: bool = None,
        base_os_tag: str = None,
        name: str = None,
        image_id: str = None,
        post_install_scripts: List[DescribeClusterResponseBodyClusterInfoPostInstallScripts] = None,
        scheduler_type: str = None,
        deploy_mode: str = None,
        image_owner_alias: str = None,
        remote_directory: str = None,
        volume_mountpoint: str = None,
        os_tag: str = None,
        region_id: str = None,
        v_switch_id: str = None,
        ecs_info: DescribeClusterResponseBodyClusterInfoEcsInfo = None,
        image_name: str = None,
        applications: List[DescribeClusterResponseBodyClusterInfoApplications] = None,
        volume_type: str = None,
        location: str = None,
        id: str = None,
        client_version: str = None,
    ):
        self.status = status
        self.vpc_id = vpc_id
        self.key_pair_name = key_pair_name
        self.ecs_charge_type = ecs_charge_type
        self.security_group_id = security_group_id
        self.scc_cluster_id = scc_cluster_id
        self.create_time = create_time
        self.account_type = account_type
        self.volume_protocol = volume_protocol
        self.description = description
        self.volume_id = volume_id
        self.ha_enable = ha_enable
        self.base_os_tag = base_os_tag
        self.name = name
        self.image_id = image_id
        self.post_install_scripts = post_install_scripts
        self.scheduler_type = scheduler_type
        self.deploy_mode = deploy_mode
        self.image_owner_alias = image_owner_alias
        self.remote_directory = remote_directory
        self.volume_mountpoint = volume_mountpoint
        self.os_tag = os_tag
        self.region_id = region_id
        self.v_switch_id = v_switch_id
        self.ecs_info = ecs_info
        self.image_name = image_name
        self.applications = applications
        self.volume_type = volume_type
        self.location = location
        self.id = id
        self.client_version = client_version

    def validate(self):
        if self.post_install_scripts:
            for k in self.post_install_scripts:
                if k:
                    k.validate()
        if self.ecs_info:
            self.ecs_info.validate()
        if self.applications:
            for k in self.applications:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.status is not None:
            result['Status'] = self.status
        if self.vpc_id is not None:
            result['VpcId'] = self.vpc_id
        if self.key_pair_name is not None:
            result['KeyPairName'] = self.key_pair_name
        if self.ecs_charge_type is not None:
            result['EcsChargeType'] = self.ecs_charge_type
        if self.security_group_id is not None:
            result['SecurityGroupId'] = self.security_group_id
        if self.scc_cluster_id is not None:
            result['SccClusterId'] = self.scc_cluster_id
        if self.create_time is not None:
            result['CreateTime'] = self.create_time
        if self.account_type is not None:
            result['AccountType'] = self.account_type
        if self.volume_protocol is not None:
            result['VolumeProtocol'] = self.volume_protocol
        if self.description is not None:
            result['Description'] = self.description
        if self.volume_id is not None:
            result['VolumeId'] = self.volume_id
        if self.ha_enable is not None:
            result['HaEnable'] = self.ha_enable
        if self.base_os_tag is not None:
            result['BaseOsTag'] = self.base_os_tag
        if self.name is not None:
            result['Name'] = self.name
        if self.image_id is not None:
            result['ImageId'] = self.image_id
        result['PostInstallScripts'] = []
        if self.post_install_scripts is not None:
            for k in self.post_install_scripts:
                result['PostInstallScripts'].append(k.to_map() if k else None)
        if self.scheduler_type is not None:
            result['SchedulerType'] = self.scheduler_type
        if self.deploy_mode is not None:
            result['DeployMode'] = self.deploy_mode
        if self.image_owner_alias is not None:
            result['ImageOwnerAlias'] = self.image_owner_alias
        if self.remote_directory is not None:
            result['RemoteDirectory'] = self.remote_directory
        if self.volume_mountpoint is not None:
            result['VolumeMountpoint'] = self.volume_mountpoint
        if self.os_tag is not None:
            result['OsTag'] = self.os_tag
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.v_switch_id is not None:
            result['VSwitchId'] = self.v_switch_id
        if self.ecs_info is not None:
            result['EcsInfo'] = self.ecs_info.to_map()
        if self.image_name is not None:
            result['ImageName'] = self.image_name
        result['Applications'] = []
        if self.applications is not None:
            for k in self.applications:
                result['Applications'].append(k.to_map() if k else None)
        if self.volume_type is not None:
            result['VolumeType'] = self.volume_type
        if self.location is not None:
            result['Location'] = self.location
        if self.id is not None:
            result['Id'] = self.id
        if self.client_version is not None:
            result['ClientVersion'] = self.client_version
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('VpcId') is not None:
            self.vpc_id = m.get('VpcId')
        if m.get('KeyPairName') is not None:
            self.key_pair_name = m.get('KeyPairName')
        if m.get('EcsChargeType') is not None:
            self.ecs_charge_type = m.get('EcsChargeType')
        if m.get('SecurityGroupId') is not None:
            self.security_group_id = m.get('SecurityGroupId')
        if m.get('SccClusterId') is not None:
            self.scc_cluster_id = m.get('SccClusterId')
        if m.get('CreateTime') is not None:
            self.create_time = m.get('CreateTime')
        if m.get('AccountType') is not None:
            self.account_type = m.get('AccountType')
        if m.get('VolumeProtocol') is not None:
            self.volume_protocol = m.get('VolumeProtocol')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('VolumeId') is not None:
            self.volume_id = m.get('VolumeId')
        if m.get('HaEnable') is not None:
            self.ha_enable = m.get('HaEnable')
        if m.get('BaseOsTag') is not None:
            self.base_os_tag = m.get('BaseOsTag')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('ImageId') is not None:
            self.image_id = m.get('ImageId')
        self.post_install_scripts = []
        if m.get('PostInstallScripts') is not None:
            for k in m.get('PostInstallScripts'):
                temp_model = DescribeClusterResponseBodyClusterInfoPostInstallScripts()
                self.post_install_scripts.append(temp_model.from_map(k))
        if m.get('SchedulerType') is not None:
            self.scheduler_type = m.get('SchedulerType')
        if m.get('DeployMode') is not None:
            self.deploy_mode = m.get('DeployMode')
        if m.get('ImageOwnerAlias') is not None:
            self.image_owner_alias = m.get('ImageOwnerAlias')
        if m.get('RemoteDirectory') is not None:
            self.remote_directory = m.get('RemoteDirectory')
        if m.get('VolumeMountpoint') is not None:
            self.volume_mountpoint = m.get('VolumeMountpoint')
        if m.get('OsTag') is not None:
            self.os_tag = m.get('OsTag')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('VSwitchId') is not None:
            self.v_switch_id = m.get('VSwitchId')
        if m.get('EcsInfo') is not None:
            temp_model = DescribeClusterResponseBodyClusterInfoEcsInfo()
            self.ecs_info = temp_model.from_map(m['EcsInfo'])
        if m.get('ImageName') is not None:
            self.image_name = m.get('ImageName')
        self.applications = []
        if m.get('Applications') is not None:
            for k in m.get('Applications'):
                temp_model = DescribeClusterResponseBodyClusterInfoApplications()
                self.applications.append(temp_model.from_map(k))
        if m.get('VolumeType') is not None:
            self.volume_type = m.get('VolumeType')
        if m.get('Location') is not None:
            self.location = m.get('Location')
        if m.get('Id') is not None:
            self.id = m.get('Id')
        if m.get('ClientVersion') is not None:
            self.client_version = m.get('ClientVersion')
        return self


class DescribeClusterResponseBody(TeaModel):
    def __init__(
        self,
        cluster_info: DescribeClusterResponseBodyClusterInfo = None,
        request_id: str = None,
    ):
        self.cluster_info = cluster_info
        self.request_id = request_id

    def validate(self):
        if self.cluster_info:
            self.cluster_info.validate()

    def to_map(self):
        result = dict()
        if self.cluster_info is not None:
            result['ClusterInfo'] = self.cluster_info.to_map()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClusterInfo') is not None:
            temp_model = DescribeClusterResponseBodyClusterInfo()
            self.cluster_info = temp_model.from_map(m['ClusterInfo'])
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class DescribeClusterResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeClusterResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeClusterResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeContainerAppRequest(TeaModel):
    def __init__(
        self,
        container_id: str = None,
    ):
        self.container_id = container_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.container_id is not None:
            result['ContainerId'] = self.container_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ContainerId') is not None:
            self.container_id = m.get('ContainerId')
        return self


class DescribeContainerAppResponseBodyContainerAppInfo(TeaModel):
    def __init__(
        self,
        type: str = None,
        description: str = None,
        create_time: str = None,
        repository: str = None,
        image_tag: str = None,
        name: str = None,
        id: str = None,
    ):
        self.type = type
        self.description = description
        self.create_time = create_time
        self.repository = repository
        self.image_tag = image_tag
        self.name = name
        self.id = id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.type is not None:
            result['Type'] = self.type
        if self.description is not None:
            result['Description'] = self.description
        if self.create_time is not None:
            result['CreateTime'] = self.create_time
        if self.repository is not None:
            result['Repository'] = self.repository
        if self.image_tag is not None:
            result['ImageTag'] = self.image_tag
        if self.name is not None:
            result['Name'] = self.name
        if self.id is not None:
            result['Id'] = self.id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('CreateTime') is not None:
            self.create_time = m.get('CreateTime')
        if m.get('Repository') is not None:
            self.repository = m.get('Repository')
        if m.get('ImageTag') is not None:
            self.image_tag = m.get('ImageTag')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Id') is not None:
            self.id = m.get('Id')
        return self


class DescribeContainerAppResponseBody(TeaModel):
    def __init__(
        self,
        container_app_info: DescribeContainerAppResponseBodyContainerAppInfo = None,
        request_id: str = None,
    ):
        self.container_app_info = container_app_info
        self.request_id = request_id

    def validate(self):
        if self.container_app_info:
            self.container_app_info.validate()

    def to_map(self):
        result = dict()
        if self.container_app_info is not None:
            result['ContainerAppInfo'] = self.container_app_info.to_map()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ContainerAppInfo') is not None:
            temp_model = DescribeContainerAppResponseBodyContainerAppInfo()
            self.container_app_info = temp_model.from_map(m['ContainerAppInfo'])
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class DescribeContainerAppResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeContainerAppResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeContainerAppResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeGWSClusterPolicyRequest(TeaModel):
    def __init__(
        self,
        cluster_id: str = None,
        task_id: str = None,
        async_mode: bool = None,
    ):
        self.cluster_id = cluster_id
        self.task_id = task_id
        self.async_mode = async_mode

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        if self.task_id is not None:
            result['TaskId'] = self.task_id
        if self.async_mode is not None:
            result['AsyncMode'] = self.async_mode
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        if m.get('TaskId') is not None:
            self.task_id = m.get('TaskId')
        if m.get('AsyncMode') is not None:
            self.async_mode = m.get('AsyncMode')
        return self


class DescribeGWSClusterPolicyResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        local_drive: str = None,
        usb_redirect: str = None,
        clipboard: str = None,
        watermark: str = None,
    ):
        self.request_id = request_id
        self.local_drive = local_drive
        self.usb_redirect = usb_redirect
        self.clipboard = clipboard
        self.watermark = watermark

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.local_drive is not None:
            result['LocalDrive'] = self.local_drive
        if self.usb_redirect is not None:
            result['UsbRedirect'] = self.usb_redirect
        if self.clipboard is not None:
            result['Clipboard'] = self.clipboard
        if self.watermark is not None:
            result['Watermark'] = self.watermark
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('LocalDrive') is not None:
            self.local_drive = m.get('LocalDrive')
        if m.get('UsbRedirect') is not None:
            self.usb_redirect = m.get('UsbRedirect')
        if m.get('Clipboard') is not None:
            self.clipboard = m.get('Clipboard')
        if m.get('Watermark') is not None:
            self.watermark = m.get('Watermark')
        return self


class DescribeGWSClusterPolicyResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeGWSClusterPolicyResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeGWSClusterPolicyResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeGWSClustersRequest(TeaModel):
    def __init__(
        self,
        cluster_id: str = None,
        page_number: int = None,
        page_size: int = None,
    ):
        self.cluster_id = cluster_id
        self.page_number = page_number
        self.page_size = page_size

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        return self


class DescribeGWSClustersResponseBodyClusters(TeaModel):
    def __init__(
        self,
        vpc_id: str = None,
        status: str = None,
        instance_count: int = None,
        create_time: str = None,
        cluster_id: str = None,
    ):
        self.vpc_id = vpc_id
        self.status = status
        self.instance_count = instance_count
        self.create_time = create_time
        self.cluster_id = cluster_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.vpc_id is not None:
            result['VpcId'] = self.vpc_id
        if self.status is not None:
            result['Status'] = self.status
        if self.instance_count is not None:
            result['InstanceCount'] = self.instance_count
        if self.create_time is not None:
            result['CreateTime'] = self.create_time
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('VpcId') is not None:
            self.vpc_id = m.get('VpcId')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('InstanceCount') is not None:
            self.instance_count = m.get('InstanceCount')
        if m.get('CreateTime') is not None:
            self.create_time = m.get('CreateTime')
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        return self


class DescribeGWSClustersResponseBody(TeaModel):
    def __init__(
        self,
        total_count: int = None,
        page_size: int = None,
        request_id: str = None,
        page_number: int = None,
        clusters: List[DescribeGWSClustersResponseBodyClusters] = None,
        caller_type: str = None,
    ):
        self.total_count = total_count
        self.page_size = page_size
        self.request_id = request_id
        self.page_number = page_number
        self.clusters = clusters
        self.caller_type = caller_type

    def validate(self):
        if self.clusters:
            for k in self.clusters:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        result['Clusters'] = []
        if self.clusters is not None:
            for k in self.clusters:
                result['Clusters'].append(k.to_map() if k else None)
        if self.caller_type is not None:
            result['CallerType'] = self.caller_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        self.clusters = []
        if m.get('Clusters') is not None:
            for k in m.get('Clusters'):
                temp_model = DescribeGWSClustersResponseBodyClusters()
                self.clusters.append(temp_model.from_map(k))
        if m.get('CallerType') is not None:
            self.caller_type = m.get('CallerType')
        return self


class DescribeGWSClustersResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeGWSClustersResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeGWSClustersResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeGWSImagesRequest(TeaModel):
    def __init__(
        self,
        page_number: int = None,
        page_size: int = None,
    ):
        self.page_number = page_number
        self.page_size = page_size

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        return self


class DescribeGWSImagesResponseBodyImages(TeaModel):
    def __init__(
        self,
        status: str = None,
        image_type: str = None,
        progress: str = None,
        size: int = None,
        create_time: str = None,
        name: str = None,
        image_id: str = None,
    ):
        self.status = status
        self.image_type = image_type
        self.progress = progress
        self.size = size
        self.create_time = create_time
        self.name = name
        self.image_id = image_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.status is not None:
            result['Status'] = self.status
        if self.image_type is not None:
            result['ImageType'] = self.image_type
        if self.progress is not None:
            result['Progress'] = self.progress
        if self.size is not None:
            result['Size'] = self.size
        if self.create_time is not None:
            result['CreateTime'] = self.create_time
        if self.name is not None:
            result['Name'] = self.name
        if self.image_id is not None:
            result['ImageId'] = self.image_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('ImageType') is not None:
            self.image_type = m.get('ImageType')
        if m.get('Progress') is not None:
            self.progress = m.get('Progress')
        if m.get('Size') is not None:
            self.size = m.get('Size')
        if m.get('CreateTime') is not None:
            self.create_time = m.get('CreateTime')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('ImageId') is not None:
            self.image_id = m.get('ImageId')
        return self


class DescribeGWSImagesResponseBody(TeaModel):
    def __init__(
        self,
        total_count: int = None,
        page_size: int = None,
        request_id: str = None,
        page_number: int = None,
        images: List[DescribeGWSImagesResponseBodyImages] = None,
    ):
        self.total_count = total_count
        self.page_size = page_size
        self.request_id = request_id
        self.page_number = page_number
        self.images = images

    def validate(self):
        if self.images:
            for k in self.images:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        result['Images'] = []
        if self.images is not None:
            for k in self.images:
                result['Images'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        self.images = []
        if m.get('Images') is not None:
            for k in m.get('Images'):
                temp_model = DescribeGWSImagesResponseBodyImages()
                self.images.append(temp_model.from_map(k))
        return self


class DescribeGWSImagesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeGWSImagesResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeGWSImagesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeGWSInstancesRequest(TeaModel):
    def __init__(
        self,
        cluster_id: str = None,
        instance_id: str = None,
        page_number: int = None,
        page_size: int = None,
        user_uid: int = None,
        user_name: str = None,
    ):
        self.cluster_id = cluster_id
        self.instance_id = instance_id
        self.page_number = page_number
        self.page_size = page_size
        self.user_uid = user_uid
        self.user_name = user_name

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.user_uid is not None:
            result['UserUid'] = self.user_uid
        if self.user_name is not None:
            result['UserName'] = self.user_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('UserUid') is not None:
            self.user_uid = m.get('UserUid')
        if m.get('UserName') is not None:
            self.user_name = m.get('UserName')
        return self


class DescribeGWSInstancesResponseBodyInstancesAppList(TeaModel):
    def __init__(
        self,
        app_name: str = None,
        app_path: str = None,
        app_args: str = None,
    ):
        self.app_name = app_name
        self.app_path = app_path
        self.app_args = app_args

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.app_name is not None:
            result['AppName'] = self.app_name
        if self.app_path is not None:
            result['AppPath'] = self.app_path
        if self.app_args is not None:
            result['AppArgs'] = self.app_args
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AppName') is not None:
            self.app_name = m.get('AppName')
        if m.get('AppPath') is not None:
            self.app_path = m.get('AppPath')
        if m.get('AppArgs') is not None:
            self.app_args = m.get('AppArgs')
        return self


class DescribeGWSInstancesResponseBodyInstances(TeaModel):
    def __init__(
        self,
        status: str = None,
        app_list: List[DescribeGWSInstancesResponseBodyInstancesAppList] = None,
        work_mode: str = None,
        expire_time: str = None,
        create_time: str = None,
        instance_id: str = None,
        name: str = None,
        instance_type: str = None,
        user_name: str = None,
        cluster_id: str = None,
    ):
        self.status = status
        self.app_list = app_list
        self.work_mode = work_mode
        self.expire_time = expire_time
        self.create_time = create_time
        self.instance_id = instance_id
        self.name = name
        self.instance_type = instance_type
        self.user_name = user_name
        self.cluster_id = cluster_id

    def validate(self):
        if self.app_list:
            for k in self.app_list:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.status is not None:
            result['Status'] = self.status
        result['AppList'] = []
        if self.app_list is not None:
            for k in self.app_list:
                result['AppList'].append(k.to_map() if k else None)
        if self.work_mode is not None:
            result['WorkMode'] = self.work_mode
        if self.expire_time is not None:
            result['ExpireTime'] = self.expire_time
        if self.create_time is not None:
            result['CreateTime'] = self.create_time
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.name is not None:
            result['Name'] = self.name
        if self.instance_type is not None:
            result['InstanceType'] = self.instance_type
        if self.user_name is not None:
            result['UserName'] = self.user_name
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Status') is not None:
            self.status = m.get('Status')
        self.app_list = []
        if m.get('AppList') is not None:
            for k in m.get('AppList'):
                temp_model = DescribeGWSInstancesResponseBodyInstancesAppList()
                self.app_list.append(temp_model.from_map(k))
        if m.get('WorkMode') is not None:
            self.work_mode = m.get('WorkMode')
        if m.get('ExpireTime') is not None:
            self.expire_time = m.get('ExpireTime')
        if m.get('CreateTime') is not None:
            self.create_time = m.get('CreateTime')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('InstanceType') is not None:
            self.instance_type = m.get('InstanceType')
        if m.get('UserName') is not None:
            self.user_name = m.get('UserName')
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        return self


class DescribeGWSInstancesResponseBody(TeaModel):
    def __init__(
        self,
        instances: List[DescribeGWSInstancesResponseBodyInstances] = None,
        total_count: int = None,
        page_size: int = None,
        request_id: str = None,
        page_number: int = None,
    ):
        self.instances = instances
        self.total_count = total_count
        self.page_size = page_size
        self.request_id = request_id
        self.page_number = page_number

    def validate(self):
        if self.instances:
            for k in self.instances:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['Instances'] = []
        if self.instances is not None:
            for k in self.instances:
                result['Instances'].append(k.to_map() if k else None)
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.instances = []
        if m.get('Instances') is not None:
            for k in m.get('Instances'):
                temp_model = DescribeGWSInstancesResponseBodyInstances()
                self.instances.append(temp_model.from_map(k))
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        return self


class DescribeGWSInstancesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeGWSInstancesResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeGWSInstancesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeImageRequest(TeaModel):
    def __init__(
        self,
        cluster_id: str = None,
        repository: str = None,
        image_tag: str = None,
        container_type: str = None,
    ):
        self.cluster_id = cluster_id
        self.repository = repository
        self.image_tag = image_tag
        self.container_type = container_type

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        if self.repository is not None:
            result['Repository'] = self.repository
        if self.image_tag is not None:
            result['ImageTag'] = self.image_tag
        if self.container_type is not None:
            result['ContainerType'] = self.container_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        if m.get('Repository') is not None:
            self.repository = m.get('Repository')
        if m.get('ImageTag') is not None:
            self.image_tag = m.get('ImageTag')
        if m.get('ContainerType') is not None:
            self.container_type = m.get('ContainerType')
        return self


class DescribeImageResponseBodyImageInfo(TeaModel):
    def __init__(
        self,
        type: str = None,
        status: str = None,
        update_date_time: str = None,
        repository: str = None,
        tag: str = None,
        system: str = None,
        image_id: str = None,
    ):
        self.type = type
        self.status = status
        self.update_date_time = update_date_time
        self.repository = repository
        self.tag = tag
        self.system = system
        self.image_id = image_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.type is not None:
            result['Type'] = self.type
        if self.status is not None:
            result['Status'] = self.status
        if self.update_date_time is not None:
            result['UpdateDateTime'] = self.update_date_time
        if self.repository is not None:
            result['Repository'] = self.repository
        if self.tag is not None:
            result['Tag'] = self.tag
        if self.system is not None:
            result['System'] = self.system
        if self.image_id is not None:
            result['ImageId'] = self.image_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('UpdateDateTime') is not None:
            self.update_date_time = m.get('UpdateDateTime')
        if m.get('Repository') is not None:
            self.repository = m.get('Repository')
        if m.get('Tag') is not None:
            self.tag = m.get('Tag')
        if m.get('System') is not None:
            self.system = m.get('System')
        if m.get('ImageId') is not None:
            self.image_id = m.get('ImageId')
        return self


class DescribeImageResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        image_info: DescribeImageResponseBodyImageInfo = None,
    ):
        self.request_id = request_id
        self.image_info = image_info

    def validate(self):
        if self.image_info:
            self.image_info.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.image_info is not None:
            result['ImageInfo'] = self.image_info.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('ImageInfo') is not None:
            temp_model = DescribeImageResponseBodyImageInfo()
            self.image_info = temp_model.from_map(m['ImageInfo'])
        return self


class DescribeImageResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeImageResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeImageResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeImageGatewayConfigRequest(TeaModel):
    def __init__(
        self,
        cluster_id: str = None,
    ):
        self.cluster_id = cluster_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        return self


class DescribeImageGatewayConfigResponseBodyImagegwLocations(TeaModel):
    def __init__(
        self,
        remote_type: str = None,
        url: str = None,
        location: str = None,
        authentication: str = None,
    ):
        self.remote_type = remote_type
        self.url = url
        self.location = location
        self.authentication = authentication

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.remote_type is not None:
            result['RemoteType'] = self.remote_type
        if self.url is not None:
            result['URL'] = self.url
        if self.location is not None:
            result['Location'] = self.location
        if self.authentication is not None:
            result['Authentication'] = self.authentication
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RemoteType') is not None:
            self.remote_type = m.get('RemoteType')
        if m.get('URL') is not None:
            self.url = m.get('URL')
        if m.get('Location') is not None:
            self.location = m.get('Location')
        if m.get('Authentication') is not None:
            self.authentication = m.get('Authentication')
        return self


class DescribeImageGatewayConfigResponseBodyImagegw(TeaModel):
    def __init__(
        self,
        locations: List[DescribeImageGatewayConfigResponseBodyImagegwLocations] = None,
        update_date_time: str = None,
        image_expiration_timeout: str = None,
        mongo_dburi: str = None,
        default_image_location: str = None,
        pull_update_timeout: int = None,
    ):
        self.locations = locations
        self.update_date_time = update_date_time
        self.image_expiration_timeout = image_expiration_timeout
        self.mongo_dburi = mongo_dburi
        self.default_image_location = default_image_location
        self.pull_update_timeout = pull_update_timeout

    def validate(self):
        if self.locations:
            for k in self.locations:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['Locations'] = []
        if self.locations is not None:
            for k in self.locations:
                result['Locations'].append(k.to_map() if k else None)
        if self.update_date_time is not None:
            result['UpdateDateTime'] = self.update_date_time
        if self.image_expiration_timeout is not None:
            result['ImageExpirationTimeout'] = self.image_expiration_timeout
        if self.mongo_dburi is not None:
            result['MongoDBURI'] = self.mongo_dburi
        if self.default_image_location is not None:
            result['DefaultImageLocation'] = self.default_image_location
        if self.pull_update_timeout is not None:
            result['PullUpdateTimeout'] = self.pull_update_timeout
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.locations = []
        if m.get('Locations') is not None:
            for k in m.get('Locations'):
                temp_model = DescribeImageGatewayConfigResponseBodyImagegwLocations()
                self.locations.append(temp_model.from_map(k))
        if m.get('UpdateDateTime') is not None:
            self.update_date_time = m.get('UpdateDateTime')
        if m.get('ImageExpirationTimeout') is not None:
            self.image_expiration_timeout = m.get('ImageExpirationTimeout')
        if m.get('MongoDBURI') is not None:
            self.mongo_dburi = m.get('MongoDBURI')
        if m.get('DefaultImageLocation') is not None:
            self.default_image_location = m.get('DefaultImageLocation')
        if m.get('PullUpdateTimeout') is not None:
            self.pull_update_timeout = m.get('PullUpdateTimeout')
        return self


class DescribeImageGatewayConfigResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        imagegw: DescribeImageGatewayConfigResponseBodyImagegw = None,
    ):
        self.request_id = request_id
        self.imagegw = imagegw

    def validate(self):
        if self.imagegw:
            self.imagegw.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.imagegw is not None:
            result['Imagegw'] = self.imagegw.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Imagegw') is not None:
            temp_model = DescribeImageGatewayConfigResponseBodyImagegw()
            self.imagegw = temp_model.from_map(m['Imagegw'])
        return self


class DescribeImageGatewayConfigResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeImageGatewayConfigResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeImageGatewayConfigResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeImagePriceRequest(TeaModel):
    def __init__(
        self,
        image_id: str = None,
        price_unit: str = None,
        sku_code: str = None,
        period: int = None,
        amount: int = None,
        order_type: str = None,
    ):
        self.image_id = image_id
        self.price_unit = price_unit
        self.sku_code = sku_code
        self.period = period
        self.amount = amount
        self.order_type = order_type

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.image_id is not None:
            result['ImageId'] = self.image_id
        if self.price_unit is not None:
            result['PriceUnit'] = self.price_unit
        if self.sku_code is not None:
            result['SkuCode'] = self.sku_code
        if self.period is not None:
            result['Period'] = self.period
        if self.amount is not None:
            result['Amount'] = self.amount
        if self.order_type is not None:
            result['OrderType'] = self.order_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ImageId') is not None:
            self.image_id = m.get('ImageId')
        if m.get('PriceUnit') is not None:
            self.price_unit = m.get('PriceUnit')
        if m.get('SkuCode') is not None:
            self.sku_code = m.get('SkuCode')
        if m.get('Period') is not None:
            self.period = m.get('Period')
        if m.get('Amount') is not None:
            self.amount = m.get('Amount')
        if m.get('OrderType') is not None:
            self.order_type = m.get('OrderType')
        return self


class DescribeImagePriceResponseBody(TeaModel):
    def __init__(
        self,
        original_price: float = None,
        request_id: str = None,
        amount: int = None,
        discount_price: float = None,
        image_id: str = None,
        trade_price: float = None,
    ):
        self.original_price = original_price
        self.request_id = request_id
        self.amount = amount
        self.discount_price = discount_price
        self.image_id = image_id
        self.trade_price = trade_price

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.original_price is not None:
            result['OriginalPrice'] = self.original_price
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.amount is not None:
            result['Amount'] = self.amount
        if self.discount_price is not None:
            result['DiscountPrice'] = self.discount_price
        if self.image_id is not None:
            result['ImageId'] = self.image_id
        if self.trade_price is not None:
            result['TradePrice'] = self.trade_price
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('OriginalPrice') is not None:
            self.original_price = m.get('OriginalPrice')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Amount') is not None:
            self.amount = m.get('Amount')
        if m.get('DiscountPrice') is not None:
            self.discount_price = m.get('DiscountPrice')
        if m.get('ImageId') is not None:
            self.image_id = m.get('ImageId')
        if m.get('TradePrice') is not None:
            self.trade_price = m.get('TradePrice')
        return self


class DescribeImagePriceResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeImagePriceResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeImagePriceResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeJobRequest(TeaModel):
    def __init__(
        self,
        cluster_id: str = None,
        job_id: str = None,
    ):
        self.cluster_id = cluster_id
        self.job_id = job_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        if self.job_id is not None:
            result['JobId'] = self.job_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        if m.get('JobId') is not None:
            self.job_id = m.get('JobId')
        return self


class DescribeJobResponseBodyMessage(TeaModel):
    def __init__(
        self,
        job_info: str = None,
    ):
        self.job_info = job_info

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.job_info is not None:
            result['JobInfo'] = self.job_info
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('JobInfo') is not None:
            self.job_info = m.get('JobInfo')
        return self


class DescribeJobResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        message: DescribeJobResponseBodyMessage = None,
    ):
        self.request_id = request_id
        self.message = message

    def validate(self):
        if self.message:
            self.message.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.message is not None:
            result['Message'] = self.message.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Message') is not None:
            temp_model = DescribeJobResponseBodyMessage()
            self.message = temp_model.from_map(m['Message'])
        return self


class DescribeJobResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeJobResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeJobResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeNFSClientStatusRequest(TeaModel):
    def __init__(
        self,
        instance_id: str = None,
    ):
        self.instance_id = instance_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        return self


class DescribeNFSClientStatusResponseBodyResult(TeaModel):
    def __init__(
        self,
        output: str = None,
        invoke_record_status: str = None,
        exit_code: int = None,
    ):
        self.output = output
        self.invoke_record_status = invoke_record_status
        self.exit_code = exit_code

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.output is not None:
            result['Output'] = self.output
        if self.invoke_record_status is not None:
            result['InvokeRecordStatus'] = self.invoke_record_status
        if self.exit_code is not None:
            result['ExitCode'] = self.exit_code
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Output') is not None:
            self.output = m.get('Output')
        if m.get('InvokeRecordStatus') is not None:
            self.invoke_record_status = m.get('InvokeRecordStatus')
        if m.get('ExitCode') is not None:
            self.exit_code = m.get('ExitCode')
        return self


class DescribeNFSClientStatusResponseBody(TeaModel):
    def __init__(
        self,
        status: str = None,
        request_id: str = None,
        result: DescribeNFSClientStatusResponseBodyResult = None,
    ):
        self.status = status
        self.request_id = request_id
        self.result = result

    def validate(self):
        if self.result:
            self.result.validate()

    def to_map(self):
        result = dict()
        if self.status is not None:
            result['Status'] = self.status
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.result is not None:
            result['Result'] = self.result.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Result') is not None:
            temp_model = DescribeNFSClientStatusResponseBodyResult()
            self.result = temp_model.from_map(m['Result'])
        return self


class DescribeNFSClientStatusResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeNFSClientStatusResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeNFSClientStatusResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribePriceRequestCommodities(TeaModel):
    def __init__(
        self,
        amount: int = None,
        system_disk_size: int = None,
        node_type: str = None,
        system_disk_category: str = None,
        internet_charge_type: str = None,
        network_type: str = None,
        instance_type: str = None,
        period: int = None,
        internet_max_band_width_out: int = None,
    ):
        self.amount = amount
        self.system_disk_size = system_disk_size
        self.node_type = node_type
        self.system_disk_category = system_disk_category
        self.internet_charge_type = internet_charge_type
        self.network_type = network_type
        self.instance_type = instance_type
        self.period = period
        self.internet_max_band_width_out = internet_max_band_width_out

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.amount is not None:
            result['Amount'] = self.amount
        if self.system_disk_size is not None:
            result['SystemDiskSize'] = self.system_disk_size
        if self.node_type is not None:
            result['NodeType'] = self.node_type
        if self.system_disk_category is not None:
            result['SystemDiskCategory'] = self.system_disk_category
        if self.internet_charge_type is not None:
            result['InternetChargeType'] = self.internet_charge_type
        if self.network_type is not None:
            result['NetworkType'] = self.network_type
        if self.instance_type is not None:
            result['InstanceType'] = self.instance_type
        if self.period is not None:
            result['Period'] = self.period
        if self.internet_max_band_width_out is not None:
            result['InternetMaxBandWidthOut'] = self.internet_max_band_width_out
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Amount') is not None:
            self.amount = m.get('Amount')
        if m.get('SystemDiskSize') is not None:
            self.system_disk_size = m.get('SystemDiskSize')
        if m.get('NodeType') is not None:
            self.node_type = m.get('NodeType')
        if m.get('SystemDiskCategory') is not None:
            self.system_disk_category = m.get('SystemDiskCategory')
        if m.get('InternetChargeType') is not None:
            self.internet_charge_type = m.get('InternetChargeType')
        if m.get('NetworkType') is not None:
            self.network_type = m.get('NetworkType')
        if m.get('InstanceType') is not None:
            self.instance_type = m.get('InstanceType')
        if m.get('Period') is not None:
            self.period = m.get('Period')
        if m.get('InternetMaxBandWidthOut') is not None:
            self.internet_max_band_width_out = m.get('InternetMaxBandWidthOut')
        return self


class DescribePriceRequest(TeaModel):
    def __init__(
        self,
        price_unit: str = None,
        charge_type: str = None,
        order_type: str = None,
        commodities: List[DescribePriceRequestCommodities] = None,
    ):
        self.price_unit = price_unit
        self.charge_type = charge_type
        self.order_type = order_type
        self.commodities = commodities

    def validate(self):
        if self.commodities:
            for k in self.commodities:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.price_unit is not None:
            result['PriceUnit'] = self.price_unit
        if self.charge_type is not None:
            result['ChargeType'] = self.charge_type
        if self.order_type is not None:
            result['OrderType'] = self.order_type
        result['Commodities'] = []
        if self.commodities is not None:
            for k in self.commodities:
                result['Commodities'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('PriceUnit') is not None:
            self.price_unit = m.get('PriceUnit')
        if m.get('ChargeType') is not None:
            self.charge_type = m.get('ChargeType')
        if m.get('OrderType') is not None:
            self.order_type = m.get('OrderType')
        self.commodities = []
        if m.get('Commodities') is not None:
            for k in m.get('Commodities'):
                temp_model = DescribePriceRequestCommodities()
                self.commodities.append(temp_model.from_map(k))
        return self


class DescribePriceResponseBodyPrices(TeaModel):
    def __init__(
        self,
        node_type: str = None,
        trade_price: float = None,
        original_price: float = None,
        currency: str = None,
    ):
        self.node_type = node_type
        self.trade_price = trade_price
        self.original_price = original_price
        self.currency = currency

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.node_type is not None:
            result['NodeType'] = self.node_type
        if self.trade_price is not None:
            result['TradePrice'] = self.trade_price
        if self.original_price is not None:
            result['OriginalPrice'] = self.original_price
        if self.currency is not None:
            result['Currency'] = self.currency
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('NodeType') is not None:
            self.node_type = m.get('NodeType')
        if m.get('TradePrice') is not None:
            self.trade_price = m.get('TradePrice')
        if m.get('OriginalPrice') is not None:
            self.original_price = m.get('OriginalPrice')
        if m.get('Currency') is not None:
            self.currency = m.get('Currency')
        return self


class DescribePriceResponseBody(TeaModel):
    def __init__(
        self,
        prices: List[DescribePriceResponseBodyPrices] = None,
        total_trade_price: float = None,
        request_id: str = None,
    ):
        self.prices = prices
        self.total_trade_price = total_trade_price
        self.request_id = request_id

    def validate(self):
        if self.prices:
            for k in self.prices:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['Prices'] = []
        if self.prices is not None:
            for k in self.prices:
                result['Prices'].append(k.to_map() if k else None)
        if self.total_trade_price is not None:
            result['TotalTradePrice'] = self.total_trade_price
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.prices = []
        if m.get('Prices') is not None:
            for k in m.get('Prices'):
                temp_model = DescribePriceResponseBodyPrices()
                self.prices.append(temp_model.from_map(k))
        if m.get('TotalTradePrice') is not None:
            self.total_trade_price = m.get('TotalTradePrice')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class DescribePriceResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribePriceResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribePriceResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class EditJobTemplateRequest(TeaModel):
    def __init__(
        self,
        template_id: str = None,
        command_line: str = None,
        name: str = None,
        runas_user: str = None,
        priority: int = None,
        package_path: str = None,
        stdout_redirect_path: str = None,
        stderr_redirect_path: str = None,
        re_runable: bool = None,
        array_request: str = None,
        variables: str = None,
    ):
        self.template_id = template_id
        self.command_line = command_line
        self.name = name
        self.runas_user = runas_user
        self.priority = priority
        self.package_path = package_path
        self.stdout_redirect_path = stdout_redirect_path
        self.stderr_redirect_path = stderr_redirect_path
        self.re_runable = re_runable
        self.array_request = array_request
        self.variables = variables

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.template_id is not None:
            result['TemplateId'] = self.template_id
        if self.command_line is not None:
            result['CommandLine'] = self.command_line
        if self.name is not None:
            result['Name'] = self.name
        if self.runas_user is not None:
            result['RunasUser'] = self.runas_user
        if self.priority is not None:
            result['Priority'] = self.priority
        if self.package_path is not None:
            result['PackagePath'] = self.package_path
        if self.stdout_redirect_path is not None:
            result['StdoutRedirectPath'] = self.stdout_redirect_path
        if self.stderr_redirect_path is not None:
            result['StderrRedirectPath'] = self.stderr_redirect_path
        if self.re_runable is not None:
            result['ReRunable'] = self.re_runable
        if self.array_request is not None:
            result['ArrayRequest'] = self.array_request
        if self.variables is not None:
            result['Variables'] = self.variables
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TemplateId') is not None:
            self.template_id = m.get('TemplateId')
        if m.get('CommandLine') is not None:
            self.command_line = m.get('CommandLine')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('RunasUser') is not None:
            self.runas_user = m.get('RunasUser')
        if m.get('Priority') is not None:
            self.priority = m.get('Priority')
        if m.get('PackagePath') is not None:
            self.package_path = m.get('PackagePath')
        if m.get('StdoutRedirectPath') is not None:
            self.stdout_redirect_path = m.get('StdoutRedirectPath')
        if m.get('StderrRedirectPath') is not None:
            self.stderr_redirect_path = m.get('StderrRedirectPath')
        if m.get('ReRunable') is not None:
            self.re_runable = m.get('ReRunable')
        if m.get('ArrayRequest') is not None:
            self.array_request = m.get('ArrayRequest')
        if m.get('Variables') is not None:
            self.variables = m.get('Variables')
        return self


class EditJobTemplateResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        template_id: str = None,
    ):
        self.request_id = request_id
        self.template_id = template_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.template_id is not None:
            result['TemplateId'] = self.template_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('TemplateId') is not None:
            self.template_id = m.get('TemplateId')
        return self


class EditJobTemplateResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: EditJobTemplateResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = EditJobTemplateResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetAccountingReportRequest(TeaModel):
    def __init__(
        self,
        cluster_id: str = None,
        start_time: int = None,
        end_time: int = None,
        report_type: str = None,
        filter_value: str = None,
        dim: str = None,
        job_id: str = None,
        page_size: int = None,
        page_number: int = None,
    ):
        self.cluster_id = cluster_id
        self.start_time = start_time
        self.end_time = end_time
        self.report_type = report_type
        self.filter_value = filter_value
        self.dim = dim
        self.job_id = job_id
        self.page_size = page_size
        self.page_number = page_number

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        if self.start_time is not None:
            result['StartTime'] = self.start_time
        if self.end_time is not None:
            result['EndTime'] = self.end_time
        if self.report_type is not None:
            result['ReportType'] = self.report_type
        if self.filter_value is not None:
            result['FilterValue'] = self.filter_value
        if self.dim is not None:
            result['Dim'] = self.dim
        if self.job_id is not None:
            result['JobId'] = self.job_id
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')
        if m.get('EndTime') is not None:
            self.end_time = m.get('EndTime')
        if m.get('ReportType') is not None:
            self.report_type = m.get('ReportType')
        if m.get('FilterValue') is not None:
            self.filter_value = m.get('FilterValue')
        if m.get('Dim') is not None:
            self.dim = m.get('Dim')
        if m.get('JobId') is not None:
            self.job_id = m.get('JobId')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        return self


class GetAccountingReportResponseBody(TeaModel):
    def __init__(
        self,
        metrics: str = None,
        total_count: int = None,
        request_id: str = None,
        page_size: int = None,
        page_number: int = None,
        total_core_time: int = None,
        data: List[str] = None,
    ):
        self.metrics = metrics
        self.total_count = total_count
        self.request_id = request_id
        self.page_size = page_size
        self.page_number = page_number
        self.total_core_time = total_core_time
        self.data = data

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.metrics is not None:
            result['Metrics'] = self.metrics
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.total_core_time is not None:
            result['TotalCoreTime'] = self.total_core_time
        if self.data is not None:
            result['Data'] = self.data
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Metrics') is not None:
            self.metrics = m.get('Metrics')
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('TotalCoreTime') is not None:
            self.total_core_time = m.get('TotalCoreTime')
        if m.get('Data') is not None:
            self.data = m.get('Data')
        return self


class GetAccountingReportResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: GetAccountingReportResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = GetAccountingReportResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetAutoScaleConfigRequest(TeaModel):
    def __init__(
        self,
        cluster_id: str = None,
    ):
        self.cluster_id = cluster_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        return self


class GetAutoScaleConfigResponseBodyQueuesInstanceTypes(TeaModel):
    def __init__(
        self,
        host_name_prefix: str = None,
        v_switch_id: str = None,
        zone_id: str = None,
        spot_price_limit: float = None,
        instance_type: str = None,
        spot_strategy: str = None,
    ):
        self.host_name_prefix = host_name_prefix
        self.v_switch_id = v_switch_id
        self.zone_id = zone_id
        self.spot_price_limit = spot_price_limit
        self.instance_type = instance_type
        self.spot_strategy = spot_strategy

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.host_name_prefix is not None:
            result['HostNamePrefix'] = self.host_name_prefix
        if self.v_switch_id is not None:
            result['VSwitchId'] = self.v_switch_id
        if self.zone_id is not None:
            result['ZoneId'] = self.zone_id
        if self.spot_price_limit is not None:
            result['SpotPriceLimit'] = self.spot_price_limit
        if self.instance_type is not None:
            result['InstanceType'] = self.instance_type
        if self.spot_strategy is not None:
            result['SpotStrategy'] = self.spot_strategy
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('HostNamePrefix') is not None:
            self.host_name_prefix = m.get('HostNamePrefix')
        if m.get('VSwitchId') is not None:
            self.v_switch_id = m.get('VSwitchId')
        if m.get('ZoneId') is not None:
            self.zone_id = m.get('ZoneId')
        if m.get('SpotPriceLimit') is not None:
            self.spot_price_limit = m.get('SpotPriceLimit')
        if m.get('InstanceType') is not None:
            self.instance_type = m.get('InstanceType')
        if m.get('SpotStrategy') is not None:
            self.spot_strategy = m.get('SpotStrategy')
        return self


class GetAutoScaleConfigResponseBodyQueues(TeaModel):
    def __init__(
        self,
        min_nodes_in_queue: int = None,
        max_nodes_in_queue: int = None,
        enable_auto_shrink: bool = None,
        queue_name: str = None,
        queue_image_id: str = None,
        enable_auto_grow: bool = None,
        resource_group_id: str = None,
        spot_price_limit: float = None,
        instance_types: List[GetAutoScaleConfigResponseBodyQueuesInstanceTypes] = None,
        instance_type: str = None,
        spot_strategy: str = None,
    ):
        self.min_nodes_in_queue = min_nodes_in_queue
        self.max_nodes_in_queue = max_nodes_in_queue
        self.enable_auto_shrink = enable_auto_shrink
        self.queue_name = queue_name
        self.queue_image_id = queue_image_id
        self.enable_auto_grow = enable_auto_grow
        self.resource_group_id = resource_group_id
        self.spot_price_limit = spot_price_limit
        self.instance_types = instance_types
        self.instance_type = instance_type
        self.spot_strategy = spot_strategy

    def validate(self):
        if self.instance_types:
            for k in self.instance_types:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.min_nodes_in_queue is not None:
            result['MinNodesInQueue'] = self.min_nodes_in_queue
        if self.max_nodes_in_queue is not None:
            result['MaxNodesInQueue'] = self.max_nodes_in_queue
        if self.enable_auto_shrink is not None:
            result['EnableAutoShrink'] = self.enable_auto_shrink
        if self.queue_name is not None:
            result['QueueName'] = self.queue_name
        if self.queue_image_id is not None:
            result['QueueImageId'] = self.queue_image_id
        if self.enable_auto_grow is not None:
            result['EnableAutoGrow'] = self.enable_auto_grow
        if self.resource_group_id is not None:
            result['ResourceGroupId'] = self.resource_group_id
        if self.spot_price_limit is not None:
            result['SpotPriceLimit'] = self.spot_price_limit
        result['InstanceTypes'] = []
        if self.instance_types is not None:
            for k in self.instance_types:
                result['InstanceTypes'].append(k.to_map() if k else None)
        if self.instance_type is not None:
            result['InstanceType'] = self.instance_type
        if self.spot_strategy is not None:
            result['SpotStrategy'] = self.spot_strategy
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('MinNodesInQueue') is not None:
            self.min_nodes_in_queue = m.get('MinNodesInQueue')
        if m.get('MaxNodesInQueue') is not None:
            self.max_nodes_in_queue = m.get('MaxNodesInQueue')
        if m.get('EnableAutoShrink') is not None:
            self.enable_auto_shrink = m.get('EnableAutoShrink')
        if m.get('QueueName') is not None:
            self.queue_name = m.get('QueueName')
        if m.get('QueueImageId') is not None:
            self.queue_image_id = m.get('QueueImageId')
        if m.get('EnableAutoGrow') is not None:
            self.enable_auto_grow = m.get('EnableAutoGrow')
        if m.get('ResourceGroupId') is not None:
            self.resource_group_id = m.get('ResourceGroupId')
        if m.get('SpotPriceLimit') is not None:
            self.spot_price_limit = m.get('SpotPriceLimit')
        self.instance_types = []
        if m.get('InstanceTypes') is not None:
            for k in m.get('InstanceTypes'):
                temp_model = GetAutoScaleConfigResponseBodyQueuesInstanceTypes()
                self.instance_types.append(temp_model.from_map(k))
        if m.get('InstanceType') is not None:
            self.instance_type = m.get('InstanceType')
        if m.get('SpotStrategy') is not None:
            self.spot_strategy = m.get('SpotStrategy')
        return self


class GetAutoScaleConfigResponseBody(TeaModel):
    def __init__(
        self,
        extra_nodes_grow_ratio: int = None,
        request_id: str = None,
        enable_auto_grow: bool = None,
        cluster_id: str = None,
        max_nodes_in_cluster: int = None,
        shrink_idle_times: int = None,
        enable_auto_shrink: bool = None,
        cluster_type: str = None,
        grow_ratio: int = None,
        grow_interval_in_minutes: int = None,
        uid: str = None,
        grow_timeout_in_minutes: int = None,
        image_id: str = None,
        shrink_interval_in_minutes: int = None,
        spot_price_limit: float = None,
        queues: List[GetAutoScaleConfigResponseBodyQueues] = None,
        exclude_nodes: str = None,
        spot_strategy: str = None,
    ):
        self.extra_nodes_grow_ratio = extra_nodes_grow_ratio
        self.request_id = request_id
        self.enable_auto_grow = enable_auto_grow
        self.cluster_id = cluster_id
        self.max_nodes_in_cluster = max_nodes_in_cluster
        self.shrink_idle_times = shrink_idle_times
        self.enable_auto_shrink = enable_auto_shrink
        self.cluster_type = cluster_type
        self.grow_ratio = grow_ratio
        self.grow_interval_in_minutes = grow_interval_in_minutes
        self.uid = uid
        self.grow_timeout_in_minutes = grow_timeout_in_minutes
        self.image_id = image_id
        self.shrink_interval_in_minutes = shrink_interval_in_minutes
        self.spot_price_limit = spot_price_limit
        self.queues = queues
        self.exclude_nodes = exclude_nodes
        self.spot_strategy = spot_strategy

    def validate(self):
        if self.queues:
            for k in self.queues:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.extra_nodes_grow_ratio is not None:
            result['ExtraNodesGrowRatio'] = self.extra_nodes_grow_ratio
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.enable_auto_grow is not None:
            result['EnableAutoGrow'] = self.enable_auto_grow
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        if self.max_nodes_in_cluster is not None:
            result['MaxNodesInCluster'] = self.max_nodes_in_cluster
        if self.shrink_idle_times is not None:
            result['ShrinkIdleTimes'] = self.shrink_idle_times
        if self.enable_auto_shrink is not None:
            result['EnableAutoShrink'] = self.enable_auto_shrink
        if self.cluster_type is not None:
            result['ClusterType'] = self.cluster_type
        if self.grow_ratio is not None:
            result['GrowRatio'] = self.grow_ratio
        if self.grow_interval_in_minutes is not None:
            result['GrowIntervalInMinutes'] = self.grow_interval_in_minutes
        if self.uid is not None:
            result['Uid'] = self.uid
        if self.grow_timeout_in_minutes is not None:
            result['GrowTimeoutInMinutes'] = self.grow_timeout_in_minutes
        if self.image_id is not None:
            result['ImageId'] = self.image_id
        if self.shrink_interval_in_minutes is not None:
            result['ShrinkIntervalInMinutes'] = self.shrink_interval_in_minutes
        if self.spot_price_limit is not None:
            result['SpotPriceLimit'] = self.spot_price_limit
        result['Queues'] = []
        if self.queues is not None:
            for k in self.queues:
                result['Queues'].append(k.to_map() if k else None)
        if self.exclude_nodes is not None:
            result['ExcludeNodes'] = self.exclude_nodes
        if self.spot_strategy is not None:
            result['SpotStrategy'] = self.spot_strategy
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ExtraNodesGrowRatio') is not None:
            self.extra_nodes_grow_ratio = m.get('ExtraNodesGrowRatio')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('EnableAutoGrow') is not None:
            self.enable_auto_grow = m.get('EnableAutoGrow')
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        if m.get('MaxNodesInCluster') is not None:
            self.max_nodes_in_cluster = m.get('MaxNodesInCluster')
        if m.get('ShrinkIdleTimes') is not None:
            self.shrink_idle_times = m.get('ShrinkIdleTimes')
        if m.get('EnableAutoShrink') is not None:
            self.enable_auto_shrink = m.get('EnableAutoShrink')
        if m.get('ClusterType') is not None:
            self.cluster_type = m.get('ClusterType')
        if m.get('GrowRatio') is not None:
            self.grow_ratio = m.get('GrowRatio')
        if m.get('GrowIntervalInMinutes') is not None:
            self.grow_interval_in_minutes = m.get('GrowIntervalInMinutes')
        if m.get('Uid') is not None:
            self.uid = m.get('Uid')
        if m.get('GrowTimeoutInMinutes') is not None:
            self.grow_timeout_in_minutes = m.get('GrowTimeoutInMinutes')
        if m.get('ImageId') is not None:
            self.image_id = m.get('ImageId')
        if m.get('ShrinkIntervalInMinutes') is not None:
            self.shrink_interval_in_minutes = m.get('ShrinkIntervalInMinutes')
        if m.get('SpotPriceLimit') is not None:
            self.spot_price_limit = m.get('SpotPriceLimit')
        self.queues = []
        if m.get('Queues') is not None:
            for k in m.get('Queues'):
                temp_model = GetAutoScaleConfigResponseBodyQueues()
                self.queues.append(temp_model.from_map(k))
        if m.get('ExcludeNodes') is not None:
            self.exclude_nodes = m.get('ExcludeNodes')
        if m.get('SpotStrategy') is not None:
            self.spot_strategy = m.get('SpotStrategy')
        return self


class GetAutoScaleConfigResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: GetAutoScaleConfigResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = GetAutoScaleConfigResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetCloudMetricLogsRequest(TeaModel):
    def __init__(
        self,
        cluster_id: str = None,
        from_: int = None,
        to: int = None,
        reverse: bool = None,
        aggregation_type: str = None,
        aggregation_interval: int = None,
        metric_scope: str = None,
        filter: str = None,
        metric_categories: str = None,
    ):
        self.cluster_id = cluster_id
        self.from_ = from_
        self.to = to
        self.reverse = reverse
        self.aggregation_type = aggregation_type
        self.aggregation_interval = aggregation_interval
        self.metric_scope = metric_scope
        self.filter = filter
        self.metric_categories = metric_categories

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        if self.from_ is not None:
            result['From'] = self.from_
        if self.to is not None:
            result['To'] = self.to
        if self.reverse is not None:
            result['Reverse'] = self.reverse
        if self.aggregation_type is not None:
            result['AggregationType'] = self.aggregation_type
        if self.aggregation_interval is not None:
            result['AggregationInterval'] = self.aggregation_interval
        if self.metric_scope is not None:
            result['MetricScope'] = self.metric_scope
        if self.filter is not None:
            result['Filter'] = self.filter
        if self.metric_categories is not None:
            result['MetricCategories'] = self.metric_categories
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        if m.get('From') is not None:
            self.from_ = m.get('From')
        if m.get('To') is not None:
            self.to = m.get('To')
        if m.get('Reverse') is not None:
            self.reverse = m.get('Reverse')
        if m.get('AggregationType') is not None:
            self.aggregation_type = m.get('AggregationType')
        if m.get('AggregationInterval') is not None:
            self.aggregation_interval = m.get('AggregationInterval')
        if m.get('MetricScope') is not None:
            self.metric_scope = m.get('MetricScope')
        if m.get('Filter') is not None:
            self.filter = m.get('Filter')
        if m.get('MetricCategories') is not None:
            self.metric_categories = m.get('MetricCategories')
        return self


class GetCloudMetricLogsResponseBodyMetricLogs(TeaModel):
    def __init__(
        self,
        time: int = None,
        disk_device: str = None,
        network_interface: str = None,
        metric_data: str = None,
        hostname: str = None,
        instance_id: str = None,
    ):
        self.time = time
        self.disk_device = disk_device
        self.network_interface = network_interface
        self.metric_data = metric_data
        self.hostname = hostname
        self.instance_id = instance_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.time is not None:
            result['Time'] = self.time
        if self.disk_device is not None:
            result['DiskDevice'] = self.disk_device
        if self.network_interface is not None:
            result['NetworkInterface'] = self.network_interface
        if self.metric_data is not None:
            result['MetricData'] = self.metric_data
        if self.hostname is not None:
            result['Hostname'] = self.hostname
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Time') is not None:
            self.time = m.get('Time')
        if m.get('DiskDevice') is not None:
            self.disk_device = m.get('DiskDevice')
        if m.get('NetworkInterface') is not None:
            self.network_interface = m.get('NetworkInterface')
        if m.get('MetricData') is not None:
            self.metric_data = m.get('MetricData')
        if m.get('Hostname') is not None:
            self.hostname = m.get('Hostname')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        return self


class GetCloudMetricLogsResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        metric_logs: List[GetCloudMetricLogsResponseBodyMetricLogs] = None,
    ):
        self.request_id = request_id
        self.metric_logs = metric_logs

    def validate(self):
        if self.metric_logs:
            for k in self.metric_logs:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        result['MetricLogs'] = []
        if self.metric_logs is not None:
            for k in self.metric_logs:
                result['MetricLogs'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        self.metric_logs = []
        if m.get('MetricLogs') is not None:
            for k in m.get('MetricLogs'):
                temp_model = GetCloudMetricLogsResponseBodyMetricLogs()
                self.metric_logs.append(temp_model.from_map(k))
        return self


class GetCloudMetricLogsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: GetCloudMetricLogsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = GetCloudMetricLogsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetCloudMetricProfilingRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        cluster_id: str = None,
        profiling_id: str = None,
    ):
        self.region_id = region_id
        self.cluster_id = cluster_id
        self.profiling_id = profiling_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        if self.profiling_id is not None:
            result['ProfilingId'] = self.profiling_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        if m.get('ProfilingId') is not None:
            self.profiling_id = m.get('ProfilingId')
        return self


class GetCloudMetricProfilingResponseBodySvgUrls(TeaModel):
    def __init__(
        self,
        type: str = None,
        size: int = None,
        url: str = None,
        name: str = None,
    ):
        self.type = type
        self.size = size
        self.url = url
        self.name = name

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.type is not None:
            result['Type'] = self.type
        if self.size is not None:
            result['Size'] = self.size
        if self.url is not None:
            result['Url'] = self.url
        if self.name is not None:
            result['Name'] = self.name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('Size') is not None:
            self.size = m.get('Size')
        if m.get('Url') is not None:
            self.url = m.get('Url')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        return self


class GetCloudMetricProfilingResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        svg_urls: List[GetCloudMetricProfilingResponseBodySvgUrls] = None,
    ):
        self.request_id = request_id
        self.svg_urls = svg_urls

    def validate(self):
        if self.svg_urls:
            for k in self.svg_urls:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        result['SvgUrls'] = []
        if self.svg_urls is not None:
            for k in self.svg_urls:
                result['SvgUrls'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        self.svg_urls = []
        if m.get('SvgUrls') is not None:
            for k in m.get('SvgUrls'):
                temp_model = GetCloudMetricProfilingResponseBodySvgUrls()
                self.svg_urls.append(temp_model.from_map(k))
        return self


class GetCloudMetricProfilingResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: GetCloudMetricProfilingResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = GetCloudMetricProfilingResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetClusterVolumesRequest(TeaModel):
    def __init__(
        self,
        cluster_id: str = None,
    ):
        self.cluster_id = cluster_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        return self


class GetClusterVolumesResponseBodyVolumesRoles(TeaModel):
    def __init__(
        self,
        name: str = None,
    ):
        self.name = name

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.name is not None:
            result['Name'] = self.name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Name') is not None:
            self.name = m.get('Name')
        return self


class GetClusterVolumesResponseBodyVolumes(TeaModel):
    def __init__(
        self,
        job_queue: str = None,
        volume_id: str = None,
        roles: List[GetClusterVolumesResponseBodyVolumesRoles] = None,
        remote_directory: str = None,
        volume_mountpoint: str = None,
        local_directory: str = None,
        volume_type: str = None,
        must_keep: bool = None,
        location: str = None,
        volume_protocol: str = None,
    ):
        self.job_queue = job_queue
        self.volume_id = volume_id
        self.roles = roles
        self.remote_directory = remote_directory
        self.volume_mountpoint = volume_mountpoint
        self.local_directory = local_directory
        self.volume_type = volume_type
        self.must_keep = must_keep
        self.location = location
        self.volume_protocol = volume_protocol

    def validate(self):
        if self.roles:
            for k in self.roles:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.job_queue is not None:
            result['JobQueue'] = self.job_queue
        if self.volume_id is not None:
            result['VolumeId'] = self.volume_id
        result['Roles'] = []
        if self.roles is not None:
            for k in self.roles:
                result['Roles'].append(k.to_map() if k else None)
        if self.remote_directory is not None:
            result['RemoteDirectory'] = self.remote_directory
        if self.volume_mountpoint is not None:
            result['VolumeMountpoint'] = self.volume_mountpoint
        if self.local_directory is not None:
            result['LocalDirectory'] = self.local_directory
        if self.volume_type is not None:
            result['VolumeType'] = self.volume_type
        if self.must_keep is not None:
            result['MustKeep'] = self.must_keep
        if self.location is not None:
            result['Location'] = self.location
        if self.volume_protocol is not None:
            result['VolumeProtocol'] = self.volume_protocol
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('JobQueue') is not None:
            self.job_queue = m.get('JobQueue')
        if m.get('VolumeId') is not None:
            self.volume_id = m.get('VolumeId')
        self.roles = []
        if m.get('Roles') is not None:
            for k in m.get('Roles'):
                temp_model = GetClusterVolumesResponseBodyVolumesRoles()
                self.roles.append(temp_model.from_map(k))
        if m.get('RemoteDirectory') is not None:
            self.remote_directory = m.get('RemoteDirectory')
        if m.get('VolumeMountpoint') is not None:
            self.volume_mountpoint = m.get('VolumeMountpoint')
        if m.get('LocalDirectory') is not None:
            self.local_directory = m.get('LocalDirectory')
        if m.get('VolumeType') is not None:
            self.volume_type = m.get('VolumeType')
        if m.get('MustKeep') is not None:
            self.must_keep = m.get('MustKeep')
        if m.get('Location') is not None:
            self.location = m.get('Location')
        if m.get('VolumeProtocol') is not None:
            self.volume_protocol = m.get('VolumeProtocol')
        return self


class GetClusterVolumesResponseBody(TeaModel):
    def __init__(
        self,
        volumes: List[GetClusterVolumesResponseBodyVolumes] = None,
        request_id: str = None,
        region_id: str = None,
    ):
        self.volumes = volumes
        self.request_id = request_id
        self.region_id = region_id

    def validate(self):
        if self.volumes:
            for k in self.volumes:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['Volumes'] = []
        if self.volumes is not None:
            for k in self.volumes:
                result['Volumes'].append(k.to_map() if k else None)
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.volumes = []
        if m.get('Volumes') is not None:
            for k in m.get('Volumes'):
                temp_model = GetClusterVolumesResponseBodyVolumes()
                self.volumes.append(temp_model.from_map(k))
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        return self


class GetClusterVolumesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: GetClusterVolumesResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = GetClusterVolumesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetGWSConnectTicketRequest(TeaModel):
    def __init__(
        self,
        instance_id: str = None,
        app_name: str = None,
    ):
        self.instance_id = instance_id
        self.app_name = app_name

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.app_name is not None:
            result['AppName'] = self.app_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('AppName') is not None:
            self.app_name = m.get('AppName')
        return self


class GetGWSConnectTicketResponseBody(TeaModel):
    def __init__(
        self,
        ticket: str = None,
        request_id: str = None,
    ):
        self.ticket = ticket
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.ticket is not None:
            result['Ticket'] = self.ticket
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Ticket') is not None:
            self.ticket = m.get('Ticket')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class GetGWSConnectTicketResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: GetGWSConnectTicketResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = GetGWSConnectTicketResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetHealthMonitorLogsRequest(TeaModel):
    def __init__(
        self,
        cluster_id: str = None,
        start_time: int = None,
        end_time: int = None,
        enable_reverse: bool = None,
        filter: str = None,
    ):
        self.cluster_id = cluster_id
        self.start_time = start_time
        self.end_time = end_time
        self.enable_reverse = enable_reverse
        self.filter = filter

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        if self.start_time is not None:
            result['StartTime'] = self.start_time
        if self.end_time is not None:
            result['EndTime'] = self.end_time
        if self.enable_reverse is not None:
            result['EnableReverse'] = self.enable_reverse
        if self.filter is not None:
            result['Filter'] = self.filter
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')
        if m.get('EndTime') is not None:
            self.end_time = m.get('EndTime')
        if m.get('EnableReverse') is not None:
            self.enable_reverse = m.get('EnableReverse')
        if m.get('Filter') is not None:
            self.filter = m.get('Filter')
        return self


class GetHealthMonitorLogsResponseBodyLogInfoCheckList(TeaModel):
    def __init__(
        self,
        check_info: str = None,
        check_description: str = None,
        check_solution: str = None,
        check_name: str = None,
    ):
        self.check_info = check_info
        self.check_description = check_description
        self.check_solution = check_solution
        self.check_name = check_name

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.check_info is not None:
            result['CheckInfo'] = self.check_info
        if self.check_description is not None:
            result['CheckDescription'] = self.check_description
        if self.check_solution is not None:
            result['CheckSolution'] = self.check_solution
        if self.check_name is not None:
            result['CheckName'] = self.check_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('CheckInfo') is not None:
            self.check_info = m.get('CheckInfo')
        if m.get('CheckDescription') is not None:
            self.check_description = m.get('CheckDescription')
        if m.get('CheckSolution') is not None:
            self.check_solution = m.get('CheckSolution')
        if m.get('CheckName') is not None:
            self.check_name = m.get('CheckName')
        return self


class GetHealthMonitorLogsResponseBodyLogInfo(TeaModel):
    def __init__(
        self,
        time: int = None,
        item_description: str = None,
        item_name: str = None,
        health_id: str = None,
        check_list: List[GetHealthMonitorLogsResponseBodyLogInfoCheckList] = None,
        scene_description: str = None,
        host_name: str = None,
        scene_name: str = None,
        instance_id: str = None,
        level: str = None,
    ):
        self.time = time
        self.item_description = item_description
        self.item_name = item_name
        self.health_id = health_id
        self.check_list = check_list
        self.scene_description = scene_description
        self.host_name = host_name
        self.scene_name = scene_name
        self.instance_id = instance_id
        self.level = level

    def validate(self):
        if self.check_list:
            for k in self.check_list:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.time is not None:
            result['Time'] = self.time
        if self.item_description is not None:
            result['ItemDescription'] = self.item_description
        if self.item_name is not None:
            result['ItemName'] = self.item_name
        if self.health_id is not None:
            result['HealthId'] = self.health_id
        result['CheckList'] = []
        if self.check_list is not None:
            for k in self.check_list:
                result['CheckList'].append(k.to_map() if k else None)
        if self.scene_description is not None:
            result['SceneDescription'] = self.scene_description
        if self.host_name is not None:
            result['HostName'] = self.host_name
        if self.scene_name is not None:
            result['SceneName'] = self.scene_name
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.level is not None:
            result['Level'] = self.level
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Time') is not None:
            self.time = m.get('Time')
        if m.get('ItemDescription') is not None:
            self.item_description = m.get('ItemDescription')
        if m.get('ItemName') is not None:
            self.item_name = m.get('ItemName')
        if m.get('HealthId') is not None:
            self.health_id = m.get('HealthId')
        self.check_list = []
        if m.get('CheckList') is not None:
            for k in m.get('CheckList'):
                temp_model = GetHealthMonitorLogsResponseBodyLogInfoCheckList()
                self.check_list.append(temp_model.from_map(k))
        if m.get('SceneDescription') is not None:
            self.scene_description = m.get('SceneDescription')
        if m.get('HostName') is not None:
            self.host_name = m.get('HostName')
        if m.get('SceneName') is not None:
            self.scene_name = m.get('SceneName')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('Level') is not None:
            self.level = m.get('Level')
        return self


class GetHealthMonitorLogsResponseBody(TeaModel):
    def __init__(
        self,
        log_info: List[GetHealthMonitorLogsResponseBodyLogInfo] = None,
        request_id: str = None,
    ):
        self.log_info = log_info
        self.request_id = request_id

    def validate(self):
        if self.log_info:
            for k in self.log_info:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['LogInfo'] = []
        if self.log_info is not None:
            for k in self.log_info:
                result['LogInfo'].append(k.to_map() if k else None)
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.log_info = []
        if m.get('LogInfo') is not None:
            for k in m.get('LogInfo'):
                temp_model = GetHealthMonitorLogsResponseBodyLogInfo()
                self.log_info.append(temp_model.from_map(k))
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class GetHealthMonitorLogsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: GetHealthMonitorLogsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = GetHealthMonitorLogsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetHybridClusterConfigRequest(TeaModel):
    def __init__(
        self,
        cluster_id: str = None,
        node: str = None,
    ):
        self.cluster_id = cluster_id
        self.node = node

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        if self.node is not None:
            result['Node'] = self.node
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        if m.get('Node') is not None:
            self.node = m.get('Node')
        return self


class GetHybridClusterConfigResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        cluster_config: str = None,
    ):
        self.request_id = request_id
        self.cluster_config = cluster_config

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.cluster_config is not None:
            result['ClusterConfig'] = self.cluster_config
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('ClusterConfig') is not None:
            self.cluster_config = m.get('ClusterConfig')
        return self


class GetHybridClusterConfigResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: GetHybridClusterConfigResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = GetHybridClusterConfigResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetIfEcsTypeSupportHtConfigRequest(TeaModel):
    def __init__(
        self,
        instance_type: str = None,
    ):
        self.instance_type = instance_type

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.instance_type is not None:
            result['InstanceType'] = self.instance_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('InstanceType') is not None:
            self.instance_type = m.get('InstanceType')
        return self


class GetIfEcsTypeSupportHtConfigResponseBody(TeaModel):
    def __init__(
        self,
        default_ht_enabled: bool = None,
        request_id: str = None,
        support_ht_config: bool = None,
        instance_type: str = None,
    ):
        self.default_ht_enabled = default_ht_enabled
        self.request_id = request_id
        self.support_ht_config = support_ht_config
        self.instance_type = instance_type

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.default_ht_enabled is not None:
            result['DefaultHtEnabled'] = self.default_ht_enabled
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.support_ht_config is not None:
            result['SupportHtConfig'] = self.support_ht_config
        if self.instance_type is not None:
            result['InstanceType'] = self.instance_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DefaultHtEnabled') is not None:
            self.default_ht_enabled = m.get('DefaultHtEnabled')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('SupportHtConfig') is not None:
            self.support_ht_config = m.get('SupportHtConfig')
        if m.get('InstanceType') is not None:
            self.instance_type = m.get('InstanceType')
        return self


class GetIfEcsTypeSupportHtConfigResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: GetIfEcsTypeSupportHtConfigResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = GetIfEcsTypeSupportHtConfigResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetVisualServiceStatusRequest(TeaModel):
    def __init__(
        self,
        cluster_id: str = None,
    ):
        self.cluster_id = cluster_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        return self


class GetVisualServiceStatusResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
    ):
        self.message = message
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class GetVisualServiceStatusResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: GetVisualServiceStatusResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = GetVisualServiceStatusResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetWorkbenchTokenRequest(TeaModel):
    def __init__(
        self,
        cluster_id: str = None,
        user_name: str = None,
        user_password: str = None,
        port: int = None,
        account_session_ticket: str = None,
        account_uid: str = None,
        instance_id: str = None,
    ):
        self.cluster_id = cluster_id
        self.user_name = user_name
        self.user_password = user_password
        self.port = port
        self.account_session_ticket = account_session_ticket
        self.account_uid = account_uid
        self.instance_id = instance_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        if self.user_name is not None:
            result['UserName'] = self.user_name
        if self.user_password is not None:
            result['UserPassword'] = self.user_password
        if self.port is not None:
            result['Port'] = self.port
        if self.account_session_ticket is not None:
            result['AccountSessionTicket'] = self.account_session_ticket
        if self.account_uid is not None:
            result['AccountUid'] = self.account_uid
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        if m.get('UserName') is not None:
            self.user_name = m.get('UserName')
        if m.get('UserPassword') is not None:
            self.user_password = m.get('UserPassword')
        if m.get('Port') is not None:
            self.port = m.get('Port')
        if m.get('AccountSessionTicket') is not None:
            self.account_session_ticket = m.get('AccountSessionTicket')
        if m.get('AccountUid') is not None:
            self.account_uid = m.get('AccountUid')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        return self


class GetWorkbenchTokenResponseBodyRootInstanceLoginView(TeaModel):
    def __init__(
        self,
        default_view_url: str = None,
        rdp_view_url: str = None,
        base_view_url: str = None,
        file_tree_view_url: str = None,
        terminal_view_url: str = None,
        view_name: str = None,
    ):
        self.default_view_url = default_view_url
        self.rdp_view_url = rdp_view_url
        self.base_view_url = base_view_url
        self.file_tree_view_url = file_tree_view_url
        self.terminal_view_url = terminal_view_url
        self.view_name = view_name

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.default_view_url is not None:
            result['defaultViewUrl'] = self.default_view_url
        if self.rdp_view_url is not None:
            result['rdpViewUrl'] = self.rdp_view_url
        if self.base_view_url is not None:
            result['baseViewUrl'] = self.base_view_url
        if self.file_tree_view_url is not None:
            result['fileTreeViewUrl'] = self.file_tree_view_url
        if self.terminal_view_url is not None:
            result['terminalViewUrl'] = self.terminal_view_url
        if self.view_name is not None:
            result['viewName'] = self.view_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('defaultViewUrl') is not None:
            self.default_view_url = m.get('defaultViewUrl')
        if m.get('rdpViewUrl') is not None:
            self.rdp_view_url = m.get('rdpViewUrl')
        if m.get('baseViewUrl') is not None:
            self.base_view_url = m.get('baseViewUrl')
        if m.get('fileTreeViewUrl') is not None:
            self.file_tree_view_url = m.get('fileTreeViewUrl')
        if m.get('terminalViewUrl') is not None:
            self.terminal_view_url = m.get('terminalViewUrl')
        if m.get('viewName') is not None:
            self.view_name = m.get('viewName')
        return self


class GetWorkbenchTokenResponseBodyRoot(TeaModel):
    def __init__(
        self,
        instance_login_view: GetWorkbenchTokenResponseBodyRootInstanceLoginView = None,
    ):
        self.instance_login_view = instance_login_view

    def validate(self):
        if self.instance_login_view:
            self.instance_login_view.validate()

    def to_map(self):
        result = dict()
        if self.instance_login_view is not None:
            result['instanceLoginView'] = self.instance_login_view.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('instanceLoginView') is not None:
            temp_model = GetWorkbenchTokenResponseBodyRootInstanceLoginView()
            self.instance_login_view = temp_model.from_map(m['instanceLoginView'])
        return self


class GetWorkbenchTokenResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        root: GetWorkbenchTokenResponseBodyRoot = None,
    ):
        self.request_id = request_id
        self.root = root

    def validate(self):
        if self.root:
            self.root.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.root is not None:
            result['root'] = self.root.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('root') is not None:
            temp_model = GetWorkbenchTokenResponseBodyRoot()
            self.root = temp_model.from_map(m['root'])
        return self


class GetWorkbenchTokenResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: GetWorkbenchTokenResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = GetWorkbenchTokenResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class InitializeEHPCRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
    ):
        self.region_id = region_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        return self


class InitializeEHPCResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class InitializeEHPCResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: InitializeEHPCResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = InitializeEHPCResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class InstallSoftwareRequest(TeaModel):
    def __init__(
        self,
        cluster_id: str = None,
        application: str = None,
    ):
        self.cluster_id = cluster_id
        self.application = application

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        if self.application is not None:
            result['Application'] = self.application
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        if m.get('Application') is not None:
            self.application = m.get('Application')
        return self


class InstallSoftwareResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class InstallSoftwareResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: InstallSoftwareResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = InstallSoftwareResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class InvokeShellCommandRequestInstance(TeaModel):
    def __init__(
        self,
        id: str = None,
    ):
        self.id = id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.id is not None:
            result['Id'] = self.id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Id') is not None:
            self.id = m.get('Id')
        return self


class InvokeShellCommandRequest(TeaModel):
    def __init__(
        self,
        cluster_id: str = None,
        command: str = None,
        working_dir: str = None,
        timeout: int = None,
        instance: List[InvokeShellCommandRequestInstance] = None,
    ):
        self.cluster_id = cluster_id
        self.command = command
        self.working_dir = working_dir
        self.timeout = timeout
        self.instance = instance

    def validate(self):
        if self.instance:
            for k in self.instance:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        if self.command is not None:
            result['Command'] = self.command
        if self.working_dir is not None:
            result['WorkingDir'] = self.working_dir
        if self.timeout is not None:
            result['Timeout'] = self.timeout
        result['Instance'] = []
        if self.instance is not None:
            for k in self.instance:
                result['Instance'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        if m.get('Command') is not None:
            self.command = m.get('Command')
        if m.get('WorkingDir') is not None:
            self.working_dir = m.get('WorkingDir')
        if m.get('Timeout') is not None:
            self.timeout = m.get('Timeout')
        self.instance = []
        if m.get('Instance') is not None:
            for k in m.get('Instance'):
                temp_model = InvokeShellCommandRequestInstance()
                self.instance.append(temp_model.from_map(k))
        return self


class InvokeShellCommandResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        command_id: str = None,
        instance_ids: List[str] = None,
    ):
        self.request_id = request_id
        self.command_id = command_id
        self.instance_ids = instance_ids

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.command_id is not None:
            result['CommandId'] = self.command_id
        if self.instance_ids is not None:
            result['InstanceIds'] = self.instance_ids
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('CommandId') is not None:
            self.command_id = m.get('CommandId')
        if m.get('InstanceIds') is not None:
            self.instance_ids = m.get('InstanceIds')
        return self


class InvokeShellCommandResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: InvokeShellCommandResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = InvokeShellCommandResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListAccountMappingRequest(TeaModel):
    def __init__(
        self,
        cluster_id: str = None,
    ):
        self.cluster_id = cluster_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        return self


class ListAccountMappingResponseBodyUserMappings(TeaModel):
    def __init__(
        self,
        account_id: str = None,
        user_name: str = None,
        account_name: str = None,
    ):
        self.account_id = account_id
        self.user_name = user_name
        self.account_name = account_name

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.account_id is not None:
            result['AccountId'] = self.account_id
        if self.user_name is not None:
            result['UserName'] = self.user_name
        if self.account_name is not None:
            result['AccountName'] = self.account_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AccountId') is not None:
            self.account_id = m.get('AccountId')
        if m.get('UserName') is not None:
            self.user_name = m.get('UserName')
        if m.get('AccountName') is not None:
            self.account_name = m.get('AccountName')
        return self


class ListAccountMappingResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        user_mappings: List[ListAccountMappingResponseBodyUserMappings] = None,
    ):
        self.request_id = request_id
        self.user_mappings = user_mappings

    def validate(self):
        if self.user_mappings:
            for k in self.user_mappings:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        result['UserMappings'] = []
        if self.user_mappings is not None:
            for k in self.user_mappings:
                result['UserMappings'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        self.user_mappings = []
        if m.get('UserMappings') is not None:
            for k in m.get('UserMappings'):
                temp_model = ListAccountMappingResponseBodyUserMappings()
                self.user_mappings.append(temp_model.from_map(k))
        return self


class ListAccountMappingResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ListAccountMappingResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ListAccountMappingResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListAvailableEcsTypesRequest(TeaModel):
    def __init__(
        self,
        zone_id: str = None,
        spot_strategy: str = None,
        instance_charge_type: str = None,
        show_sold_out: bool = None,
    ):
        self.zone_id = zone_id
        self.spot_strategy = spot_strategy
        self.instance_charge_type = instance_charge_type
        self.show_sold_out = show_sold_out

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.zone_id is not None:
            result['ZoneId'] = self.zone_id
        if self.spot_strategy is not None:
            result['SpotStrategy'] = self.spot_strategy
        if self.instance_charge_type is not None:
            result['InstanceChargeType'] = self.instance_charge_type
        if self.show_sold_out is not None:
            result['ShowSoldOut'] = self.show_sold_out
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ZoneId') is not None:
            self.zone_id = m.get('ZoneId')
        if m.get('SpotStrategy') is not None:
            self.spot_strategy = m.get('SpotStrategy')
        if m.get('InstanceChargeType') is not None:
            self.instance_charge_type = m.get('InstanceChargeType')
        if m.get('ShowSoldOut') is not None:
            self.show_sold_out = m.get('ShowSoldOut')
        return self


class ListAvailableEcsTypesResponseBodyInstanceTypeFamiliesTypes(TeaModel):
    def __init__(
        self,
        status: str = None,
        instance_type_id: str = None,
        instance_bandwidth_rx: int = None,
        gpuspec: str = None,
        instance_bandwidth_tx: int = None,
        instance_pps_rx: int = None,
        instance_pps_tx: int = None,
        gpuamount: int = None,
        cpu_core_count: int = None,
        memory_size: int = None,
        eni_quantity: int = None,
    ):
        self.status = status
        self.instance_type_id = instance_type_id
        self.instance_bandwidth_rx = instance_bandwidth_rx
        self.gpuspec = gpuspec
        self.instance_bandwidth_tx = instance_bandwidth_tx
        self.instance_pps_rx = instance_pps_rx
        self.instance_pps_tx = instance_pps_tx
        self.gpuamount = gpuamount
        self.cpu_core_count = cpu_core_count
        self.memory_size = memory_size
        self.eni_quantity = eni_quantity

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.status is not None:
            result['Status'] = self.status
        if self.instance_type_id is not None:
            result['InstanceTypeId'] = self.instance_type_id
        if self.instance_bandwidth_rx is not None:
            result['InstanceBandwidthRx'] = self.instance_bandwidth_rx
        if self.gpuspec is not None:
            result['GPUSpec'] = self.gpuspec
        if self.instance_bandwidth_tx is not None:
            result['InstanceBandwidthTx'] = self.instance_bandwidth_tx
        if self.instance_pps_rx is not None:
            result['InstancePpsRx'] = self.instance_pps_rx
        if self.instance_pps_tx is not None:
            result['InstancePpsTx'] = self.instance_pps_tx
        if self.gpuamount is not None:
            result['GPUAmount'] = self.gpuamount
        if self.cpu_core_count is not None:
            result['CpuCoreCount'] = self.cpu_core_count
        if self.memory_size is not None:
            result['MemorySize'] = self.memory_size
        if self.eni_quantity is not None:
            result['EniQuantity'] = self.eni_quantity
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('InstanceTypeId') is not None:
            self.instance_type_id = m.get('InstanceTypeId')
        if m.get('InstanceBandwidthRx') is not None:
            self.instance_bandwidth_rx = m.get('InstanceBandwidthRx')
        if m.get('GPUSpec') is not None:
            self.gpuspec = m.get('GPUSpec')
        if m.get('InstanceBandwidthTx') is not None:
            self.instance_bandwidth_tx = m.get('InstanceBandwidthTx')
        if m.get('InstancePpsRx') is not None:
            self.instance_pps_rx = m.get('InstancePpsRx')
        if m.get('InstancePpsTx') is not None:
            self.instance_pps_tx = m.get('InstancePpsTx')
        if m.get('GPUAmount') is not None:
            self.gpuamount = m.get('GPUAmount')
        if m.get('CpuCoreCount') is not None:
            self.cpu_core_count = m.get('CpuCoreCount')
        if m.get('MemorySize') is not None:
            self.memory_size = m.get('MemorySize')
        if m.get('EniQuantity') is not None:
            self.eni_quantity = m.get('EniQuantity')
        return self


class ListAvailableEcsTypesResponseBodyInstanceTypeFamilies(TeaModel):
    def __init__(
        self,
        instance_type_family_id: str = None,
        types: List[ListAvailableEcsTypesResponseBodyInstanceTypeFamiliesTypes] = None,
        generation: str = None,
    ):
        self.instance_type_family_id = instance_type_family_id
        self.types = types
        self.generation = generation

    def validate(self):
        if self.types:
            for k in self.types:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.instance_type_family_id is not None:
            result['InstanceTypeFamilyId'] = self.instance_type_family_id
        result['Types'] = []
        if self.types is not None:
            for k in self.types:
                result['Types'].append(k.to_map() if k else None)
        if self.generation is not None:
            result['Generation'] = self.generation
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('InstanceTypeFamilyId') is not None:
            self.instance_type_family_id = m.get('InstanceTypeFamilyId')
        self.types = []
        if m.get('Types') is not None:
            for k in m.get('Types'):
                temp_model = ListAvailableEcsTypesResponseBodyInstanceTypeFamiliesTypes()
                self.types.append(temp_model.from_map(k))
        if m.get('Generation') is not None:
            self.generation = m.get('Generation')
        return self


class ListAvailableEcsTypesResponseBody(TeaModel):
    def __init__(
        self,
        support_spot_instance: bool = None,
        request_id: str = None,
        instance_type_families: List[ListAvailableEcsTypesResponseBodyInstanceTypeFamilies] = None,
    ):
        self.support_spot_instance = support_spot_instance
        self.request_id = request_id
        self.instance_type_families = instance_type_families

    def validate(self):
        if self.instance_type_families:
            for k in self.instance_type_families:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.support_spot_instance is not None:
            result['SupportSpotInstance'] = self.support_spot_instance
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        result['InstanceTypeFamilies'] = []
        if self.instance_type_families is not None:
            for k in self.instance_type_families:
                result['InstanceTypeFamilies'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('SupportSpotInstance') is not None:
            self.support_spot_instance = m.get('SupportSpotInstance')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        self.instance_type_families = []
        if m.get('InstanceTypeFamilies') is not None:
            for k in m.get('InstanceTypeFamilies'):
                temp_model = ListAvailableEcsTypesResponseBodyInstanceTypeFamilies()
                self.instance_type_families.append(temp_model.from_map(k))
        return self


class ListAvailableEcsTypesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ListAvailableEcsTypesResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ListAvailableEcsTypesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListAvailableFileSystemTypesResponseBodyFileSystemTypeList(TeaModel):
    def __init__(
        self,
        file_system_type: str = None,
        available: bool = None,
        protocol_type: str = None,
        storage_types: List[str] = None,
    ):
        self.file_system_type = file_system_type
        self.available = available
        self.protocol_type = protocol_type
        self.storage_types = storage_types

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.file_system_type is not None:
            result['FileSystemType'] = self.file_system_type
        if self.available is not None:
            result['Available'] = self.available
        if self.protocol_type is not None:
            result['ProtocolType'] = self.protocol_type
        if self.storage_types is not None:
            result['StorageTypes'] = self.storage_types
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('FileSystemType') is not None:
            self.file_system_type = m.get('FileSystemType')
        if m.get('Available') is not None:
            self.available = m.get('Available')
        if m.get('ProtocolType') is not None:
            self.protocol_type = m.get('ProtocolType')
        if m.get('StorageTypes') is not None:
            self.storage_types = m.get('StorageTypes')
        return self


class ListAvailableFileSystemTypesResponseBody(TeaModel):
    def __init__(
        self,
        file_system_type_list: List[ListAvailableFileSystemTypesResponseBodyFileSystemTypeList] = None,
        request_id: str = None,
    ):
        self.file_system_type_list = file_system_type_list
        self.request_id = request_id

    def validate(self):
        if self.file_system_type_list:
            for k in self.file_system_type_list:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['FileSystemTypeList'] = []
        if self.file_system_type_list is not None:
            for k in self.file_system_type_list:
                result['FileSystemTypeList'].append(k.to_map() if k else None)
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.file_system_type_list = []
        if m.get('FileSystemTypeList') is not None:
            for k in m.get('FileSystemTypeList'):
                temp_model = ListAvailableFileSystemTypesResponseBodyFileSystemTypeList()
                self.file_system_type_list.append(temp_model.from_map(k))
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class ListAvailableFileSystemTypesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ListAvailableFileSystemTypesResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ListAvailableFileSystemTypesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListCloudMetricProfilingsRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        cluster_id: str = None,
        page_number: int = None,
        page_size: int = None,
    ):
        self.region_id = region_id
        self.cluster_id = cluster_id
        self.page_number = page_number
        self.page_size = page_size

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        return self


class ListCloudMetricProfilingsResponseBodyProfilings(TeaModel):
    def __init__(
        self,
        profiling_id: str = None,
        trigger_time: str = None,
        pid: int = None,
        host_name: str = None,
        duration: int = None,
        instance_id: str = None,
        freq: int = None,
    ):
        self.profiling_id = profiling_id
        self.trigger_time = trigger_time
        self.pid = pid
        self.host_name = host_name
        self.duration = duration
        self.instance_id = instance_id
        self.freq = freq

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.profiling_id is not None:
            result['ProfilingId'] = self.profiling_id
        if self.trigger_time is not None:
            result['TriggerTime'] = self.trigger_time
        if self.pid is not None:
            result['Pid'] = self.pid
        if self.host_name is not None:
            result['HostName'] = self.host_name
        if self.duration is not None:
            result['Duration'] = self.duration
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.freq is not None:
            result['Freq'] = self.freq
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ProfilingId') is not None:
            self.profiling_id = m.get('ProfilingId')
        if m.get('TriggerTime') is not None:
            self.trigger_time = m.get('TriggerTime')
        if m.get('Pid') is not None:
            self.pid = m.get('Pid')
        if m.get('HostName') is not None:
            self.host_name = m.get('HostName')
        if m.get('Duration') is not None:
            self.duration = m.get('Duration')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('Freq') is not None:
            self.freq = m.get('Freq')
        return self


class ListCloudMetricProfilingsResponseBody(TeaModel):
    def __init__(
        self,
        total_count: int = None,
        page_size: int = None,
        request_id: str = None,
        page_number: int = None,
        profilings: List[ListCloudMetricProfilingsResponseBodyProfilings] = None,
    ):
        self.total_count = total_count
        self.page_size = page_size
        self.request_id = request_id
        self.page_number = page_number
        self.profilings = profilings

    def validate(self):
        if self.profilings:
            for k in self.profilings:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        result['Profilings'] = []
        if self.profilings is not None:
            for k in self.profilings:
                result['Profilings'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        self.profilings = []
        if m.get('Profilings') is not None:
            for k in m.get('Profilings'):
                temp_model = ListCloudMetricProfilingsResponseBodyProfilings()
                self.profilings.append(temp_model.from_map(k))
        return self


class ListCloudMetricProfilingsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ListCloudMetricProfilingsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ListCloudMetricProfilingsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListClusterLogsRequest(TeaModel):
    def __init__(
        self,
        cluster_id: str = None,
        page_number: int = None,
        page_size: int = None,
    ):
        self.cluster_id = cluster_id
        self.page_number = page_number
        self.page_size = page_size

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        return self


class ListClusterLogsResponseBodyLogs(TeaModel):
    def __init__(
        self,
        operation: str = None,
        create_time: str = None,
        message: str = None,
        level: str = None,
    ):
        self.operation = operation
        self.create_time = create_time
        self.message = message
        self.level = level

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.operation is not None:
            result['Operation'] = self.operation
        if self.create_time is not None:
            result['CreateTime'] = self.create_time
        if self.message is not None:
            result['Message'] = self.message
        if self.level is not None:
            result['Level'] = self.level
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Operation') is not None:
            self.operation = m.get('Operation')
        if m.get('CreateTime') is not None:
            self.create_time = m.get('CreateTime')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('Level') is not None:
            self.level = m.get('Level')
        return self


class ListClusterLogsResponseBody(TeaModel):
    def __init__(
        self,
        total_count: int = None,
        page_size: int = None,
        request_id: str = None,
        page_number: int = None,
        cluster_id: str = None,
        logs: List[ListClusterLogsResponseBodyLogs] = None,
    ):
        self.total_count = total_count
        self.page_size = page_size
        self.request_id = request_id
        self.page_number = page_number
        self.cluster_id = cluster_id
        self.logs = logs

    def validate(self):
        if self.logs:
            for k in self.logs:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        result['Logs'] = []
        if self.logs is not None:
            for k in self.logs:
                result['Logs'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        self.logs = []
        if m.get('Logs') is not None:
            for k in m.get('Logs'):
                temp_model = ListClusterLogsResponseBodyLogs()
                self.logs.append(temp_model.from_map(k))
        return self


class ListClusterLogsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ListClusterLogsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ListClusterLogsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListClustersRequest(TeaModel):
    def __init__(
        self,
        page_number: int = None,
        page_size: int = None,
    ):
        self.page_number = page_number
        self.page_size = page_size

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        return self


class ListClustersResponseBodyClustersUsedResources(TeaModel):
    def __init__(
        self,
        cpu: int = None,
        gpu: int = None,
        memory: int = None,
    ):
        self.cpu = cpu
        self.gpu = gpu
        self.memory = memory

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.cpu is not None:
            result['Cpu'] = self.cpu
        if self.gpu is not None:
            result['Gpu'] = self.gpu
        if self.memory is not None:
            result['Memory'] = self.memory
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Cpu') is not None:
            self.cpu = m.get('Cpu')
        if m.get('Gpu') is not None:
            self.gpu = m.get('Gpu')
        if m.get('Memory') is not None:
            self.memory = m.get('Memory')
        return self


class ListClustersResponseBodyClustersManagers(TeaModel):
    def __init__(
        self,
        exception_count: int = None,
        normal_count: int = None,
        operating_count: int = None,
        stopped_count: int = None,
        total: int = None,
    ):
        self.exception_count = exception_count
        self.normal_count = normal_count
        self.operating_count = operating_count
        self.stopped_count = stopped_count
        self.total = total

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.exception_count is not None:
            result['ExceptionCount'] = self.exception_count
        if self.normal_count is not None:
            result['NormalCount'] = self.normal_count
        if self.operating_count is not None:
            result['OperatingCount'] = self.operating_count
        if self.stopped_count is not None:
            result['StoppedCount'] = self.stopped_count
        if self.total is not None:
            result['Total'] = self.total
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ExceptionCount') is not None:
            self.exception_count = m.get('ExceptionCount')
        if m.get('NormalCount') is not None:
            self.normal_count = m.get('NormalCount')
        if m.get('OperatingCount') is not None:
            self.operating_count = m.get('OperatingCount')
        if m.get('StoppedCount') is not None:
            self.stopped_count = m.get('StoppedCount')
        if m.get('Total') is not None:
            self.total = m.get('Total')
        return self


class ListClustersResponseBodyClustersTotalResources(TeaModel):
    def __init__(
        self,
        cpu: int = None,
        gpu: int = None,
        memory: int = None,
    ):
        self.cpu = cpu
        self.gpu = gpu
        self.memory = memory

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.cpu is not None:
            result['Cpu'] = self.cpu
        if self.gpu is not None:
            result['Gpu'] = self.gpu
        if self.memory is not None:
            result['Memory'] = self.memory
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Cpu') is not None:
            self.cpu = m.get('Cpu')
        if m.get('Gpu') is not None:
            self.gpu = m.get('Gpu')
        if m.get('Memory') is not None:
            self.memory = m.get('Memory')
        return self


class ListClustersResponseBodyClustersComputes(TeaModel):
    def __init__(
        self,
        exception_count: int = None,
        normal_count: int = None,
        operating_count: int = None,
        stopped_count: int = None,
        total: int = None,
    ):
        self.exception_count = exception_count
        self.normal_count = normal_count
        self.operating_count = operating_count
        self.stopped_count = stopped_count
        self.total = total

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.exception_count is not None:
            result['ExceptionCount'] = self.exception_count
        if self.normal_count is not None:
            result['NormalCount'] = self.normal_count
        if self.operating_count is not None:
            result['OperatingCount'] = self.operating_count
        if self.stopped_count is not None:
            result['StoppedCount'] = self.stopped_count
        if self.total is not None:
            result['Total'] = self.total
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ExceptionCount') is not None:
            self.exception_count = m.get('ExceptionCount')
        if m.get('NormalCount') is not None:
            self.normal_count = m.get('NormalCount')
        if m.get('OperatingCount') is not None:
            self.operating_count = m.get('OperatingCount')
        if m.get('StoppedCount') is not None:
            self.stopped_count = m.get('StoppedCount')
        if m.get('Total') is not None:
            self.total = m.get('Total')
        return self


class ListClustersResponseBodyClusters(TeaModel):
    def __init__(
        self,
        vpc_id: str = None,
        status: str = None,
        create_time: str = None,
        used_resources: ListClustersResponseBodyClustersUsedResources = None,
        compute_spot_strategy: str = None,
        account_type: str = None,
        count: int = None,
        ehpc_version: str = None,
        description: str = None,
        base_os_tag: str = None,
        name: str = None,
        image_id: str = None,
        compute_spot_price_limit: float = None,
        scheduler_type: str = None,
        node_suffix: str = None,
        deploy_mode: str = None,
        image_owner_alias: str = None,
        os_tag: str = None,
        node_prefix: str = None,
        instance_type: str = None,
        managers: ListClustersResponseBodyClustersManagers = None,
        instance_charge_type: str = None,
        region_id: str = None,
        v_switch_id: str = None,
        total_resources: ListClustersResponseBodyClustersTotalResources = None,
        zone_id: str = None,
        computes: ListClustersResponseBodyClustersComputes = None,
        login_nodes: str = None,
        id: str = None,
        location: str = None,
        client_version: str = None,
    ):
        self.vpc_id = vpc_id
        self.status = status
        self.create_time = create_time
        self.used_resources = used_resources
        self.compute_spot_strategy = compute_spot_strategy
        self.account_type = account_type
        self.count = count
        self.ehpc_version = ehpc_version
        self.description = description
        self.base_os_tag = base_os_tag
        self.name = name
        self.image_id = image_id
        self.compute_spot_price_limit = compute_spot_price_limit
        self.scheduler_type = scheduler_type
        self.node_suffix = node_suffix
        self.deploy_mode = deploy_mode
        self.image_owner_alias = image_owner_alias
        self.os_tag = os_tag
        self.node_prefix = node_prefix
        self.instance_type = instance_type
        self.managers = managers
        self.instance_charge_type = instance_charge_type
        self.region_id = region_id
        self.v_switch_id = v_switch_id
        self.total_resources = total_resources
        self.zone_id = zone_id
        self.computes = computes
        self.login_nodes = login_nodes
        self.id = id
        self.location = location
        self.client_version = client_version

    def validate(self):
        if self.used_resources:
            self.used_resources.validate()
        if self.managers:
            self.managers.validate()
        if self.total_resources:
            self.total_resources.validate()
        if self.computes:
            self.computes.validate()

    def to_map(self):
        result = dict()
        if self.vpc_id is not None:
            result['VpcId'] = self.vpc_id
        if self.status is not None:
            result['Status'] = self.status
        if self.create_time is not None:
            result['CreateTime'] = self.create_time
        if self.used_resources is not None:
            result['UsedResources'] = self.used_resources.to_map()
        if self.compute_spot_strategy is not None:
            result['ComputeSpotStrategy'] = self.compute_spot_strategy
        if self.account_type is not None:
            result['AccountType'] = self.account_type
        if self.count is not None:
            result['Count'] = self.count
        if self.ehpc_version is not None:
            result['EhpcVersion'] = self.ehpc_version
        if self.description is not None:
            result['Description'] = self.description
        if self.base_os_tag is not None:
            result['BaseOsTag'] = self.base_os_tag
        if self.name is not None:
            result['Name'] = self.name
        if self.image_id is not None:
            result['ImageId'] = self.image_id
        if self.compute_spot_price_limit is not None:
            result['ComputeSpotPriceLimit'] = self.compute_spot_price_limit
        if self.scheduler_type is not None:
            result['SchedulerType'] = self.scheduler_type
        if self.node_suffix is not None:
            result['NodeSuffix'] = self.node_suffix
        if self.deploy_mode is not None:
            result['DeployMode'] = self.deploy_mode
        if self.image_owner_alias is not None:
            result['ImageOwnerAlias'] = self.image_owner_alias
        if self.os_tag is not None:
            result['OsTag'] = self.os_tag
        if self.node_prefix is not None:
            result['NodePrefix'] = self.node_prefix
        if self.instance_type is not None:
            result['InstanceType'] = self.instance_type
        if self.managers is not None:
            result['Managers'] = self.managers.to_map()
        if self.instance_charge_type is not None:
            result['InstanceChargeType'] = self.instance_charge_type
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.v_switch_id is not None:
            result['VSwitchId'] = self.v_switch_id
        if self.total_resources is not None:
            result['TotalResources'] = self.total_resources.to_map()
        if self.zone_id is not None:
            result['ZoneId'] = self.zone_id
        if self.computes is not None:
            result['Computes'] = self.computes.to_map()
        if self.login_nodes is not None:
            result['LoginNodes'] = self.login_nodes
        if self.id is not None:
            result['Id'] = self.id
        if self.location is not None:
            result['Location'] = self.location
        if self.client_version is not None:
            result['ClientVersion'] = self.client_version
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('VpcId') is not None:
            self.vpc_id = m.get('VpcId')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('CreateTime') is not None:
            self.create_time = m.get('CreateTime')
        if m.get('UsedResources') is not None:
            temp_model = ListClustersResponseBodyClustersUsedResources()
            self.used_resources = temp_model.from_map(m['UsedResources'])
        if m.get('ComputeSpotStrategy') is not None:
            self.compute_spot_strategy = m.get('ComputeSpotStrategy')
        if m.get('AccountType') is not None:
            self.account_type = m.get('AccountType')
        if m.get('Count') is not None:
            self.count = m.get('Count')
        if m.get('EhpcVersion') is not None:
            self.ehpc_version = m.get('EhpcVersion')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('BaseOsTag') is not None:
            self.base_os_tag = m.get('BaseOsTag')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('ImageId') is not None:
            self.image_id = m.get('ImageId')
        if m.get('ComputeSpotPriceLimit') is not None:
            self.compute_spot_price_limit = m.get('ComputeSpotPriceLimit')
        if m.get('SchedulerType') is not None:
            self.scheduler_type = m.get('SchedulerType')
        if m.get('NodeSuffix') is not None:
            self.node_suffix = m.get('NodeSuffix')
        if m.get('DeployMode') is not None:
            self.deploy_mode = m.get('DeployMode')
        if m.get('ImageOwnerAlias') is not None:
            self.image_owner_alias = m.get('ImageOwnerAlias')
        if m.get('OsTag') is not None:
            self.os_tag = m.get('OsTag')
        if m.get('NodePrefix') is not None:
            self.node_prefix = m.get('NodePrefix')
        if m.get('InstanceType') is not None:
            self.instance_type = m.get('InstanceType')
        if m.get('Managers') is not None:
            temp_model = ListClustersResponseBodyClustersManagers()
            self.managers = temp_model.from_map(m['Managers'])
        if m.get('InstanceChargeType') is not None:
            self.instance_charge_type = m.get('InstanceChargeType')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('VSwitchId') is not None:
            self.v_switch_id = m.get('VSwitchId')
        if m.get('TotalResources') is not None:
            temp_model = ListClustersResponseBodyClustersTotalResources()
            self.total_resources = temp_model.from_map(m['TotalResources'])
        if m.get('ZoneId') is not None:
            self.zone_id = m.get('ZoneId')
        if m.get('Computes') is not None:
            temp_model = ListClustersResponseBodyClustersComputes()
            self.computes = temp_model.from_map(m['Computes'])
        if m.get('LoginNodes') is not None:
            self.login_nodes = m.get('LoginNodes')
        if m.get('Id') is not None:
            self.id = m.get('Id')
        if m.get('Location') is not None:
            self.location = m.get('Location')
        if m.get('ClientVersion') is not None:
            self.client_version = m.get('ClientVersion')
        return self


class ListClustersResponseBody(TeaModel):
    def __init__(
        self,
        total_count: int = None,
        page_size: int = None,
        request_id: str = None,
        page_number: int = None,
        clusters: List[ListClustersResponseBodyClusters] = None,
    ):
        self.total_count = total_count
        self.page_size = page_size
        self.request_id = request_id
        self.page_number = page_number
        self.clusters = clusters

    def validate(self):
        if self.clusters:
            for k in self.clusters:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        result['Clusters'] = []
        if self.clusters is not None:
            for k in self.clusters:
                result['Clusters'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        self.clusters = []
        if m.get('Clusters') is not None:
            for k in m.get('Clusters'):
                temp_model = ListClustersResponseBodyClusters()
                self.clusters.append(temp_model.from_map(k))
        return self


class ListClustersResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ListClustersResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ListClustersResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListClustersMetaRequest(TeaModel):
    def __init__(
        self,
        page_number: int = None,
        page_size: int = None,
    ):
        self.page_number = page_number
        self.page_size = page_size

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        return self


class ListClustersMetaResponseBodyClusters(TeaModel):
    def __init__(
        self,
        vpc_id: str = None,
        status: str = None,
        scheduler_type: str = None,
        description: str = None,
        deploy_mode: str = None,
        os_tag: str = None,
        name: str = None,
        account_type: str = None,
        location: str = None,
        id: str = None,
        client_version: str = None,
    ):
        self.vpc_id = vpc_id
        self.status = status
        self.scheduler_type = scheduler_type
        self.description = description
        self.deploy_mode = deploy_mode
        self.os_tag = os_tag
        self.name = name
        self.account_type = account_type
        self.location = location
        self.id = id
        self.client_version = client_version

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.vpc_id is not None:
            result['VpcId'] = self.vpc_id
        if self.status is not None:
            result['Status'] = self.status
        if self.scheduler_type is not None:
            result['SchedulerType'] = self.scheduler_type
        if self.description is not None:
            result['Description'] = self.description
        if self.deploy_mode is not None:
            result['DeployMode'] = self.deploy_mode
        if self.os_tag is not None:
            result['OsTag'] = self.os_tag
        if self.name is not None:
            result['Name'] = self.name
        if self.account_type is not None:
            result['AccountType'] = self.account_type
        if self.location is not None:
            result['Location'] = self.location
        if self.id is not None:
            result['Id'] = self.id
        if self.client_version is not None:
            result['ClientVersion'] = self.client_version
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('VpcId') is not None:
            self.vpc_id = m.get('VpcId')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('SchedulerType') is not None:
            self.scheduler_type = m.get('SchedulerType')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('DeployMode') is not None:
            self.deploy_mode = m.get('DeployMode')
        if m.get('OsTag') is not None:
            self.os_tag = m.get('OsTag')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('AccountType') is not None:
            self.account_type = m.get('AccountType')
        if m.get('Location') is not None:
            self.location = m.get('Location')
        if m.get('Id') is not None:
            self.id = m.get('Id')
        if m.get('ClientVersion') is not None:
            self.client_version = m.get('ClientVersion')
        return self


class ListClustersMetaResponseBody(TeaModel):
    def __init__(
        self,
        total_count: int = None,
        page_size: int = None,
        request_id: str = None,
        page_number: int = None,
        clusters: List[ListClustersMetaResponseBodyClusters] = None,
    ):
        self.total_count = total_count
        self.page_size = page_size
        self.request_id = request_id
        self.page_number = page_number
        self.clusters = clusters

    def validate(self):
        if self.clusters:
            for k in self.clusters:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        result['Clusters'] = []
        if self.clusters is not None:
            for k in self.clusters:
                result['Clusters'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        self.clusters = []
        if m.get('Clusters') is not None:
            for k in m.get('Clusters'):
                temp_model = ListClustersMetaResponseBodyClusters()
                self.clusters.append(temp_model.from_map(k))
        return self


class ListClustersMetaResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ListClustersMetaResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ListClustersMetaResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListCommandsRequest(TeaModel):
    def __init__(
        self,
        cluster_id: str = None,
        command_id: str = None,
        page_number: int = None,
        page_size: int = None,
    ):
        self.cluster_id = cluster_id
        self.command_id = command_id
        self.page_number = page_number
        self.page_size = page_size

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        if self.command_id is not None:
            result['CommandId'] = self.command_id
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        if m.get('CommandId') is not None:
            self.command_id = m.get('CommandId')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        return self


class ListCommandsResponseBodyCommands(TeaModel):
    def __init__(
        self,
        timeout: str = None,
        working_dir: str = None,
        command_content: str = None,
        command_id: str = None,
    ):
        self.timeout = timeout
        self.working_dir = working_dir
        self.command_content = command_content
        self.command_id = command_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.timeout is not None:
            result['Timeout'] = self.timeout
        if self.working_dir is not None:
            result['WorkingDir'] = self.working_dir
        if self.command_content is not None:
            result['CommandContent'] = self.command_content
        if self.command_id is not None:
            result['CommandId'] = self.command_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Timeout') is not None:
            self.timeout = m.get('Timeout')
        if m.get('WorkingDir') is not None:
            self.working_dir = m.get('WorkingDir')
        if m.get('CommandContent') is not None:
            self.command_content = m.get('CommandContent')
        if m.get('CommandId') is not None:
            self.command_id = m.get('CommandId')
        return self


class ListCommandsResponseBody(TeaModel):
    def __init__(
        self,
        total_count: int = None,
        page_size: int = None,
        request_id: str = None,
        page_number: int = None,
        commands: List[ListCommandsResponseBodyCommands] = None,
    ):
        self.total_count = total_count
        self.page_size = page_size
        self.request_id = request_id
        self.page_number = page_number
        self.commands = commands

    def validate(self):
        if self.commands:
            for k in self.commands:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        result['Commands'] = []
        if self.commands is not None:
            for k in self.commands:
                result['Commands'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        self.commands = []
        if m.get('Commands') is not None:
            for k in m.get('Commands'):
                temp_model = ListCommandsResponseBodyCommands()
                self.commands.append(temp_model.from_map(k))
        return self


class ListCommandsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ListCommandsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ListCommandsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListContainerAppsRequest(TeaModel):
    def __init__(
        self,
        page_number: int = None,
        page_size: int = None,
    ):
        self.page_number = page_number
        self.page_size = page_size

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        return self


class ListContainerAppsResponseBodyContainerApps(TeaModel):
    def __init__(
        self,
        type: str = None,
        description: str = None,
        create_time: str = None,
        repository: str = None,
        image_tag: str = None,
        name: str = None,
        id: str = None,
    ):
        self.type = type
        self.description = description
        self.create_time = create_time
        self.repository = repository
        self.image_tag = image_tag
        self.name = name
        self.id = id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.type is not None:
            result['Type'] = self.type
        if self.description is not None:
            result['Description'] = self.description
        if self.create_time is not None:
            result['CreateTime'] = self.create_time
        if self.repository is not None:
            result['Repository'] = self.repository
        if self.image_tag is not None:
            result['ImageTag'] = self.image_tag
        if self.name is not None:
            result['Name'] = self.name
        if self.id is not None:
            result['Id'] = self.id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('CreateTime') is not None:
            self.create_time = m.get('CreateTime')
        if m.get('Repository') is not None:
            self.repository = m.get('Repository')
        if m.get('ImageTag') is not None:
            self.image_tag = m.get('ImageTag')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Id') is not None:
            self.id = m.get('Id')
        return self


class ListContainerAppsResponseBody(TeaModel):
    def __init__(
        self,
        container_apps: List[ListContainerAppsResponseBodyContainerApps] = None,
        total_count: int = None,
        page_size: int = None,
        request_id: str = None,
        page_number: int = None,
    ):
        self.container_apps = container_apps
        self.total_count = total_count
        self.page_size = page_size
        self.request_id = request_id
        self.page_number = page_number

    def validate(self):
        if self.container_apps:
            for k in self.container_apps:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['ContainerApps'] = []
        if self.container_apps is not None:
            for k in self.container_apps:
                result['ContainerApps'].append(k.to_map() if k else None)
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.container_apps = []
        if m.get('ContainerApps') is not None:
            for k in m.get('ContainerApps'):
                temp_model = ListContainerAppsResponseBodyContainerApps()
                self.container_apps.append(temp_model.from_map(k))
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        return self


class ListContainerAppsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ListContainerAppsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ListContainerAppsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListContainerImagesRequest(TeaModel):
    def __init__(
        self,
        cluster_id: str = None,
        container_type: str = None,
        page_number: int = None,
        page_size: int = None,
    ):
        self.cluster_id = cluster_id
        self.container_type = container_type
        self.page_number = page_number
        self.page_size = page_size

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        if self.container_type is not None:
            result['ContainerType'] = self.container_type
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        if m.get('ContainerType') is not None:
            self.container_type = m.get('ContainerType')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        return self


class ListContainerImagesResponseBodyImages(TeaModel):
    def __init__(
        self,
        type: str = None,
        status: str = None,
        update_date_time: str = None,
        repository: str = None,
        tag: str = None,
        system: str = None,
        image_id: str = None,
    ):
        self.type = type
        self.status = status
        self.update_date_time = update_date_time
        self.repository = repository
        self.tag = tag
        self.system = system
        self.image_id = image_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.type is not None:
            result['Type'] = self.type
        if self.status is not None:
            result['Status'] = self.status
        if self.update_date_time is not None:
            result['UpdateDateTime'] = self.update_date_time
        if self.repository is not None:
            result['Repository'] = self.repository
        if self.tag is not None:
            result['Tag'] = self.tag
        if self.system is not None:
            result['System'] = self.system
        if self.image_id is not None:
            result['ImageId'] = self.image_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('UpdateDateTime') is not None:
            self.update_date_time = m.get('UpdateDateTime')
        if m.get('Repository') is not None:
            self.repository = m.get('Repository')
        if m.get('Tag') is not None:
            self.tag = m.get('Tag')
        if m.get('System') is not None:
            self.system = m.get('System')
        if m.get('ImageId') is not None:
            self.image_id = m.get('ImageId')
        return self


class ListContainerImagesResponseBody(TeaModel):
    def __init__(
        self,
        total_count: int = None,
        dbinfo: str = None,
        page_size: int = None,
        request_id: str = None,
        page_number: int = None,
        images: List[ListContainerImagesResponseBodyImages] = None,
    ):
        self.total_count = total_count
        self.dbinfo = dbinfo
        self.page_size = page_size
        self.request_id = request_id
        self.page_number = page_number
        self.images = images

    def validate(self):
        if self.images:
            for k in self.images:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        if self.dbinfo is not None:
            result['DBInfo'] = self.dbinfo
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        result['Images'] = []
        if self.images is not None:
            for k in self.images:
                result['Images'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        if m.get('DBInfo') is not None:
            self.dbinfo = m.get('DBInfo')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        self.images = []
        if m.get('Images') is not None:
            for k in m.get('Images'):
                temp_model = ListContainerImagesResponseBodyImages()
                self.images.append(temp_model.from_map(k))
        return self


class ListContainerImagesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ListContainerImagesResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ListContainerImagesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListCpfsFileSystemsRequest(TeaModel):
    def __init__(
        self,
        file_system_id: str = None,
        page_number: int = None,
        page_size: int = None,
    ):
        self.file_system_id = file_system_id
        self.page_number = page_number
        self.page_size = page_size

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.file_system_id is not None:
            result['FileSystemId'] = self.file_system_id
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('FileSystemId') is not None:
            self.file_system_id = m.get('FileSystemId')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        return self


class ListCpfsFileSystemsResponseBodyFileSystemListMountTargetList(TeaModel):
    def __init__(
        self,
        vpc_id: str = None,
        status: str = None,
        mount_target_domain: str = None,
        vsw_id: str = None,
        network_type: str = None,
    ):
        self.vpc_id = vpc_id
        self.status = status
        self.mount_target_domain = mount_target_domain
        self.vsw_id = vsw_id
        self.network_type = network_type

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.vpc_id is not None:
            result['VpcId'] = self.vpc_id
        if self.status is not None:
            result['Status'] = self.status
        if self.mount_target_domain is not None:
            result['MountTargetDomain'] = self.mount_target_domain
        if self.vsw_id is not None:
            result['VswId'] = self.vsw_id
        if self.network_type is not None:
            result['NetworkType'] = self.network_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('VpcId') is not None:
            self.vpc_id = m.get('VpcId')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('MountTargetDomain') is not None:
            self.mount_target_domain = m.get('MountTargetDomain')
        if m.get('VswId') is not None:
            self.vsw_id = m.get('VswId')
        if m.get('NetworkType') is not None:
            self.network_type = m.get('NetworkType')
        return self


class ListCpfsFileSystemsResponseBodyFileSystemList(TeaModel):
    def __init__(
        self,
        file_system_id: str = None,
        capacity: str = None,
        create_time: str = None,
        mount_target_list: List[ListCpfsFileSystemsResponseBodyFileSystemListMountTargetList] = None,
        zone_id: str = None,
        protocol_type: str = None,
        destription: str = None,
        region_id: str = None,
    ):
        self.file_system_id = file_system_id
        self.capacity = capacity
        self.create_time = create_time
        self.mount_target_list = mount_target_list
        self.zone_id = zone_id
        self.protocol_type = protocol_type
        self.destription = destription
        self.region_id = region_id

    def validate(self):
        if self.mount_target_list:
            for k in self.mount_target_list:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.file_system_id is not None:
            result['FileSystemId'] = self.file_system_id
        if self.capacity is not None:
            result['Capacity'] = self.capacity
        if self.create_time is not None:
            result['CreateTime'] = self.create_time
        result['MountTargetList'] = []
        if self.mount_target_list is not None:
            for k in self.mount_target_list:
                result['MountTargetList'].append(k.to_map() if k else None)
        if self.zone_id is not None:
            result['ZoneId'] = self.zone_id
        if self.protocol_type is not None:
            result['ProtocolType'] = self.protocol_type
        if self.destription is not None:
            result['Destription'] = self.destription
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('FileSystemId') is not None:
            self.file_system_id = m.get('FileSystemId')
        if m.get('Capacity') is not None:
            self.capacity = m.get('Capacity')
        if m.get('CreateTime') is not None:
            self.create_time = m.get('CreateTime')
        self.mount_target_list = []
        if m.get('MountTargetList') is not None:
            for k in m.get('MountTargetList'):
                temp_model = ListCpfsFileSystemsResponseBodyFileSystemListMountTargetList()
                self.mount_target_list.append(temp_model.from_map(k))
        if m.get('ZoneId') is not None:
            self.zone_id = m.get('ZoneId')
        if m.get('ProtocolType') is not None:
            self.protocol_type = m.get('ProtocolType')
        if m.get('Destription') is not None:
            self.destription = m.get('Destription')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        return self


class ListCpfsFileSystemsResponseBody(TeaModel):
    def __init__(
        self,
        total_count: int = None,
        page_size: int = None,
        request_id: str = None,
        page_number: int = None,
        file_system_list: List[ListCpfsFileSystemsResponseBodyFileSystemList] = None,
    ):
        self.total_count = total_count
        self.page_size = page_size
        self.request_id = request_id
        self.page_number = page_number
        self.file_system_list = file_system_list

    def validate(self):
        if self.file_system_list:
            for k in self.file_system_list:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        result['FileSystemList'] = []
        if self.file_system_list is not None:
            for k in self.file_system_list:
                result['FileSystemList'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        self.file_system_list = []
        if m.get('FileSystemList') is not None:
            for k in m.get('FileSystemList'):
                temp_model = ListCpfsFileSystemsResponseBodyFileSystemList()
                self.file_system_list.append(temp_model.from_map(k))
        return self


class ListCpfsFileSystemsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ListCpfsFileSystemsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ListCpfsFileSystemsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListCurrentClientVersionResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        client_version: str = None,
    ):
        self.request_id = request_id
        self.client_version = client_version

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.client_version is not None:
            result['ClientVersion'] = self.client_version
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('ClientVersion') is not None:
            self.client_version = m.get('ClientVersion')
        return self


class ListCurrentClientVersionResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ListCurrentClientVersionResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ListCurrentClientVersionResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListCustomImagesRequest(TeaModel):
    def __init__(
        self,
        image_owner_alias: str = None,
        base_os_tag: str = None,
        instance_type: str = None,
    ):
        self.image_owner_alias = image_owner_alias
        self.base_os_tag = base_os_tag
        self.instance_type = instance_type

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.image_owner_alias is not None:
            result['ImageOwnerAlias'] = self.image_owner_alias
        if self.base_os_tag is not None:
            result['BaseOsTag'] = self.base_os_tag
        if self.instance_type is not None:
            result['InstanceType'] = self.instance_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ImageOwnerAlias') is not None:
            self.image_owner_alias = m.get('ImageOwnerAlias')
        if m.get('BaseOsTag') is not None:
            self.base_os_tag = m.get('BaseOsTag')
        if m.get('InstanceType') is not None:
            self.instance_type = m.get('InstanceType')
        return self


class ListCustomImagesResponseBodyImagesOsTag(TeaModel):
    def __init__(
        self,
        version: str = None,
        base_os_tag: str = None,
        platform: str = None,
        os_tag: str = None,
        architecture: str = None,
    ):
        self.version = version
        self.base_os_tag = base_os_tag
        self.platform = platform
        self.os_tag = os_tag
        self.architecture = architecture

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.version is not None:
            result['Version'] = self.version
        if self.base_os_tag is not None:
            result['BaseOsTag'] = self.base_os_tag
        if self.platform is not None:
            result['Platform'] = self.platform
        if self.os_tag is not None:
            result['OsTag'] = self.os_tag
        if self.architecture is not None:
            result['Architecture'] = self.architecture
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Version') is not None:
            self.version = m.get('Version')
        if m.get('BaseOsTag') is not None:
            self.base_os_tag = m.get('BaseOsTag')
        if m.get('Platform') is not None:
            self.platform = m.get('Platform')
        if m.get('OsTag') is not None:
            self.os_tag = m.get('OsTag')
        if m.get('Architecture') is not None:
            self.architecture = m.get('Architecture')
        return self


class ListCustomImagesResponseBodyImagesBaseOsTag(TeaModel):
    def __init__(
        self,
        version: str = None,
        platform: str = None,
        os_tag: str = None,
        architecture: str = None,
    ):
        self.version = version
        self.platform = platform
        self.os_tag = os_tag
        self.architecture = architecture

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.version is not None:
            result['Version'] = self.version
        if self.platform is not None:
            result['Platform'] = self.platform
        if self.os_tag is not None:
            result['OsTag'] = self.os_tag
        if self.architecture is not None:
            result['Architecture'] = self.architecture
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Version') is not None:
            self.version = m.get('Version')
        if m.get('Platform') is not None:
            self.platform = m.get('Platform')
        if m.get('OsTag') is not None:
            self.os_tag = m.get('OsTag')
        if m.get('Architecture') is not None:
            self.architecture = m.get('Architecture')
        return self


class ListCustomImagesResponseBodyImages(TeaModel):
    def __init__(
        self,
        status: str = None,
        post_install_script: str = None,
        image_owner_alias: str = None,
        os_tag: ListCustomImagesResponseBodyImagesOsTag = None,
        sku_code: str = None,
        pricing_cycle: str = None,
        description: str = None,
        size: int = None,
        base_os_tag: ListCustomImagesResponseBodyImagesBaseOsTag = None,
        image_name: str = None,
        image_id: str = None,
        uid: str = None,
        product_code: str = None,
    ):
        self.status = status
        self.post_install_script = post_install_script
        self.image_owner_alias = image_owner_alias
        self.os_tag = os_tag
        self.sku_code = sku_code
        self.pricing_cycle = pricing_cycle
        self.description = description
        self.size = size
        self.base_os_tag = base_os_tag
        self.image_name = image_name
        self.image_id = image_id
        self.uid = uid
        self.product_code = product_code

    def validate(self):
        if self.os_tag:
            self.os_tag.validate()
        if self.base_os_tag:
            self.base_os_tag.validate()

    def to_map(self):
        result = dict()
        if self.status is not None:
            result['Status'] = self.status
        if self.post_install_script is not None:
            result['PostInstallScript'] = self.post_install_script
        if self.image_owner_alias is not None:
            result['ImageOwnerAlias'] = self.image_owner_alias
        if self.os_tag is not None:
            result['OsTag'] = self.os_tag.to_map()
        if self.sku_code is not None:
            result['SkuCode'] = self.sku_code
        if self.pricing_cycle is not None:
            result['PricingCycle'] = self.pricing_cycle
        if self.description is not None:
            result['Description'] = self.description
        if self.size is not None:
            result['Size'] = self.size
        if self.base_os_tag is not None:
            result['BaseOsTag'] = self.base_os_tag.to_map()
        if self.image_name is not None:
            result['ImageName'] = self.image_name
        if self.image_id is not None:
            result['ImageId'] = self.image_id
        if self.uid is not None:
            result['Uid'] = self.uid
        if self.product_code is not None:
            result['ProductCode'] = self.product_code
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('PostInstallScript') is not None:
            self.post_install_script = m.get('PostInstallScript')
        if m.get('ImageOwnerAlias') is not None:
            self.image_owner_alias = m.get('ImageOwnerAlias')
        if m.get('OsTag') is not None:
            temp_model = ListCustomImagesResponseBodyImagesOsTag()
            self.os_tag = temp_model.from_map(m['OsTag'])
        if m.get('SkuCode') is not None:
            self.sku_code = m.get('SkuCode')
        if m.get('PricingCycle') is not None:
            self.pricing_cycle = m.get('PricingCycle')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('Size') is not None:
            self.size = m.get('Size')
        if m.get('BaseOsTag') is not None:
            temp_model = ListCustomImagesResponseBodyImagesBaseOsTag()
            self.base_os_tag = temp_model.from_map(m['BaseOsTag'])
        if m.get('ImageName') is not None:
            self.image_name = m.get('ImageName')
        if m.get('ImageId') is not None:
            self.image_id = m.get('ImageId')
        if m.get('Uid') is not None:
            self.uid = m.get('Uid')
        if m.get('ProductCode') is not None:
            self.product_code = m.get('ProductCode')
        return self


class ListCustomImagesResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        images: List[ListCustomImagesResponseBodyImages] = None,
    ):
        self.request_id = request_id
        self.images = images

    def validate(self):
        if self.images:
            for k in self.images:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        result['Images'] = []
        if self.images is not None:
            for k in self.images:
                result['Images'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        self.images = []
        if m.get('Images') is not None:
            for k in m.get('Images'):
                temp_model = ListCustomImagesResponseBodyImages()
                self.images.append(temp_model.from_map(k))
        return self


class ListCustomImagesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ListCustomImagesResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ListCustomImagesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListFileSystemWithMountTargetsRequest(TeaModel):
    def __init__(
        self,
        page_number: int = None,
        page_size: int = None,
    ):
        self.page_number = page_number
        self.page_size = page_size

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        return self


class ListFileSystemWithMountTargetsResponseBodyFileSystemListMountTargetList(TeaModel):
    def __init__(
        self,
        status: str = None,
        vpc_id: str = None,
        mount_target_domain: str = None,
        access_group: str = None,
        vsw_id: str = None,
        network_type: str = None,
    ):
        self.status = status
        self.vpc_id = vpc_id
        self.mount_target_domain = mount_target_domain
        self.access_group = access_group
        self.vsw_id = vsw_id
        self.network_type = network_type

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.status is not None:
            result['Status'] = self.status
        if self.vpc_id is not None:
            result['VpcId'] = self.vpc_id
        if self.mount_target_domain is not None:
            result['MountTargetDomain'] = self.mount_target_domain
        if self.access_group is not None:
            result['AccessGroup'] = self.access_group
        if self.vsw_id is not None:
            result['VswId'] = self.vsw_id
        if self.network_type is not None:
            result['NetworkType'] = self.network_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('VpcId') is not None:
            self.vpc_id = m.get('VpcId')
        if m.get('MountTargetDomain') is not None:
            self.mount_target_domain = m.get('MountTargetDomain')
        if m.get('AccessGroup') is not None:
            self.access_group = m.get('AccessGroup')
        if m.get('VswId') is not None:
            self.vsw_id = m.get('VswId')
        if m.get('NetworkType') is not None:
            self.network_type = m.get('NetworkType')
        return self


class ListFileSystemWithMountTargetsResponseBodyFileSystemListPackageList(TeaModel):
    def __init__(
        self,
        package_id: str = None,
    ):
        self.package_id = package_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.package_id is not None:
            result['PackageId'] = self.package_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('PackageId') is not None:
            self.package_id = m.get('PackageId')
        return self


class ListFileSystemWithMountTargetsResponseBodyFileSystemList(TeaModel):
    def __init__(
        self,
        status: str = None,
        capacity: int = None,
        mount_target_list: List[ListFileSystemWithMountTargetsResponseBodyFileSystemListMountTargetList] = None,
        create_time: str = None,
        package_list: List[ListFileSystemWithMountTargetsResponseBodyFileSystemListPackageList] = None,
        storage_type: str = None,
        band_width: int = None,
        region_id: str = None,
        file_system_type: str = None,
        file_system_id: str = None,
        metered_size: int = None,
        encrypt_type: int = None,
        protocol_type: str = None,
        destription: str = None,
    ):
        self.status = status
        self.capacity = capacity
        self.mount_target_list = mount_target_list
        self.create_time = create_time
        self.package_list = package_list
        self.storage_type = storage_type
        self.band_width = band_width
        self.region_id = region_id
        self.file_system_type = file_system_type
        self.file_system_id = file_system_id
        self.metered_size = metered_size
        self.encrypt_type = encrypt_type
        self.protocol_type = protocol_type
        self.destription = destription

    def validate(self):
        if self.mount_target_list:
            for k in self.mount_target_list:
                if k:
                    k.validate()
        if self.package_list:
            for k in self.package_list:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.status is not None:
            result['Status'] = self.status
        if self.capacity is not None:
            result['Capacity'] = self.capacity
        result['MountTargetList'] = []
        if self.mount_target_list is not None:
            for k in self.mount_target_list:
                result['MountTargetList'].append(k.to_map() if k else None)
        if self.create_time is not None:
            result['CreateTime'] = self.create_time
        result['PackageList'] = []
        if self.package_list is not None:
            for k in self.package_list:
                result['PackageList'].append(k.to_map() if k else None)
        if self.storage_type is not None:
            result['StorageType'] = self.storage_type
        if self.band_width is not None:
            result['BandWidth'] = self.band_width
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.file_system_type is not None:
            result['FileSystemType'] = self.file_system_type
        if self.file_system_id is not None:
            result['FileSystemId'] = self.file_system_id
        if self.metered_size is not None:
            result['MeteredSize'] = self.metered_size
        if self.encrypt_type is not None:
            result['EncryptType'] = self.encrypt_type
        if self.protocol_type is not None:
            result['ProtocolType'] = self.protocol_type
        if self.destription is not None:
            result['Destription'] = self.destription
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('Capacity') is not None:
            self.capacity = m.get('Capacity')
        self.mount_target_list = []
        if m.get('MountTargetList') is not None:
            for k in m.get('MountTargetList'):
                temp_model = ListFileSystemWithMountTargetsResponseBodyFileSystemListMountTargetList()
                self.mount_target_list.append(temp_model.from_map(k))
        if m.get('CreateTime') is not None:
            self.create_time = m.get('CreateTime')
        self.package_list = []
        if m.get('PackageList') is not None:
            for k in m.get('PackageList'):
                temp_model = ListFileSystemWithMountTargetsResponseBodyFileSystemListPackageList()
                self.package_list.append(temp_model.from_map(k))
        if m.get('StorageType') is not None:
            self.storage_type = m.get('StorageType')
        if m.get('BandWidth') is not None:
            self.band_width = m.get('BandWidth')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('FileSystemType') is not None:
            self.file_system_type = m.get('FileSystemType')
        if m.get('FileSystemId') is not None:
            self.file_system_id = m.get('FileSystemId')
        if m.get('MeteredSize') is not None:
            self.metered_size = m.get('MeteredSize')
        if m.get('EncryptType') is not None:
            self.encrypt_type = m.get('EncryptType')
        if m.get('ProtocolType') is not None:
            self.protocol_type = m.get('ProtocolType')
        if m.get('Destription') is not None:
            self.destription = m.get('Destription')
        return self


class ListFileSystemWithMountTargetsResponseBody(TeaModel):
    def __init__(
        self,
        total_count: int = None,
        page_size: int = None,
        request_id: str = None,
        page_number: int = None,
        file_system_list: List[ListFileSystemWithMountTargetsResponseBodyFileSystemList] = None,
    ):
        self.total_count = total_count
        self.page_size = page_size
        self.request_id = request_id
        self.page_number = page_number
        self.file_system_list = file_system_list

    def validate(self):
        if self.file_system_list:
            for k in self.file_system_list:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        result['FileSystemList'] = []
        if self.file_system_list is not None:
            for k in self.file_system_list:
                result['FileSystemList'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        self.file_system_list = []
        if m.get('FileSystemList') is not None:
            for k in m.get('FileSystemList'):
                temp_model = ListFileSystemWithMountTargetsResponseBodyFileSystemList()
                self.file_system_list.append(temp_model.from_map(k))
        return self


class ListFileSystemWithMountTargetsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ListFileSystemWithMountTargetsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ListFileSystemWithMountTargetsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListImagesRequest(TeaModel):
    def __init__(
        self,
        base_os_tag: str = None,
        instance_type: str = None,
    ):
        self.base_os_tag = base_os_tag
        self.instance_type = instance_type

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.base_os_tag is not None:
            result['BaseOsTag'] = self.base_os_tag
        if self.instance_type is not None:
            result['InstanceType'] = self.instance_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('BaseOsTag') is not None:
            self.base_os_tag = m.get('BaseOsTag')
        if m.get('InstanceType') is not None:
            self.instance_type = m.get('InstanceType')
        return self


class ListImagesResponseBodyOsTags(TeaModel):
    def __init__(
        self,
        version: str = None,
        base_os_tag: str = None,
        platform: str = None,
        os_tag: str = None,
        image_id: str = None,
        architecture: str = None,
    ):
        self.version = version
        self.base_os_tag = base_os_tag
        self.platform = platform
        self.os_tag = os_tag
        self.image_id = image_id
        self.architecture = architecture

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.version is not None:
            result['Version'] = self.version
        if self.base_os_tag is not None:
            result['BaseOsTag'] = self.base_os_tag
        if self.platform is not None:
            result['Platform'] = self.platform
        if self.os_tag is not None:
            result['OsTag'] = self.os_tag
        if self.image_id is not None:
            result['ImageId'] = self.image_id
        if self.architecture is not None:
            result['Architecture'] = self.architecture
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Version') is not None:
            self.version = m.get('Version')
        if m.get('BaseOsTag') is not None:
            self.base_os_tag = m.get('BaseOsTag')
        if m.get('Platform') is not None:
            self.platform = m.get('Platform')
        if m.get('OsTag') is not None:
            self.os_tag = m.get('OsTag')
        if m.get('ImageId') is not None:
            self.image_id = m.get('ImageId')
        if m.get('Architecture') is not None:
            self.architecture = m.get('Architecture')
        return self


class ListImagesResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        os_tags: List[ListImagesResponseBodyOsTags] = None,
    ):
        self.request_id = request_id
        self.os_tags = os_tags

    def validate(self):
        if self.os_tags:
            for k in self.os_tags:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        result['OsTags'] = []
        if self.os_tags is not None:
            for k in self.os_tags:
                result['OsTags'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        self.os_tags = []
        if m.get('OsTags') is not None:
            for k in m.get('OsTags'):
                temp_model = ListImagesResponseBodyOsTags()
                self.os_tags.append(temp_model.from_map(k))
        return self


class ListImagesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ListImagesResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ListImagesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListInstalledSoftwareRequest(TeaModel):
    def __init__(
        self,
        cluster_id: str = None,
    ):
        self.cluster_id = cluster_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        return self


class ListInstalledSoftwareResponseBodySoftwareList(TeaModel):
    def __init__(
        self,
        software_version: str = None,
        software_name: str = None,
        software_id: str = None,
        software_status: str = None,
    ):
        self.software_version = software_version
        self.software_name = software_name
        self.software_id = software_id
        self.software_status = software_status

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.software_version is not None:
            result['SoftwareVersion'] = self.software_version
        if self.software_name is not None:
            result['SoftwareName'] = self.software_name
        if self.software_id is not None:
            result['SoftwareId'] = self.software_id
        if self.software_status is not None:
            result['SoftwareStatus'] = self.software_status
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('SoftwareVersion') is not None:
            self.software_version = m.get('SoftwareVersion')
        if m.get('SoftwareName') is not None:
            self.software_name = m.get('SoftwareName')
        if m.get('SoftwareId') is not None:
            self.software_id = m.get('SoftwareId')
        if m.get('SoftwareStatus') is not None:
            self.software_status = m.get('SoftwareStatus')
        return self


class ListInstalledSoftwareResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        software_list: List[ListInstalledSoftwareResponseBodySoftwareList] = None,
    ):
        self.request_id = request_id
        self.software_list = software_list

    def validate(self):
        if self.software_list:
            for k in self.software_list:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        result['SoftwareList'] = []
        if self.software_list is not None:
            for k in self.software_list:
                result['SoftwareList'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        self.software_list = []
        if m.get('SoftwareList') is not None:
            for k in m.get('SoftwareList'):
                temp_model = ListInstalledSoftwareResponseBodySoftwareList()
                self.software_list.append(temp_model.from_map(k))
        return self


class ListInstalledSoftwareResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ListInstalledSoftwareResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ListInstalledSoftwareResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListInvocationResultsRequestInstance(TeaModel):
    def __init__(
        self,
        id: str = None,
    ):
        self.id = id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.id is not None:
            result['Id'] = self.id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Id') is not None:
            self.id = m.get('Id')
        return self


class ListInvocationResultsRequest(TeaModel):
    def __init__(
        self,
        cluster_id: str = None,
        command_id: str = None,
        invoke_record_status: str = None,
        page_number: int = None,
        page_size: int = None,
        instance: List[ListInvocationResultsRequestInstance] = None,
    ):
        self.cluster_id = cluster_id
        self.command_id = command_id
        self.invoke_record_status = invoke_record_status
        self.page_number = page_number
        self.page_size = page_size
        self.instance = instance

    def validate(self):
        if self.instance:
            for k in self.instance:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        if self.command_id is not None:
            result['CommandId'] = self.command_id
        if self.invoke_record_status is not None:
            result['InvokeRecordStatus'] = self.invoke_record_status
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        result['Instance'] = []
        if self.instance is not None:
            for k in self.instance:
                result['Instance'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        if m.get('CommandId') is not None:
            self.command_id = m.get('CommandId')
        if m.get('InvokeRecordStatus') is not None:
            self.invoke_record_status = m.get('InvokeRecordStatus')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        self.instance = []
        if m.get('Instance') is not None:
            for k in m.get('Instance'):
                temp_model = ListInvocationResultsRequestInstance()
                self.instance.append(temp_model.from_map(k))
        return self


class ListInvocationResultsResponseBodyInvocationResults(TeaModel):
    def __init__(
        self,
        success: bool = None,
        message: str = None,
        finished_time: str = None,
        command_id: str = None,
        instance_id: str = None,
        invoke_record_status: str = None,
        exit_code: int = None,
    ):
        self.success = success
        self.message = message
        self.finished_time = finished_time
        self.command_id = command_id
        self.instance_id = instance_id
        self.invoke_record_status = invoke_record_status
        self.exit_code = exit_code

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.success is not None:
            result['Success'] = self.success
        if self.message is not None:
            result['Message'] = self.message
        if self.finished_time is not None:
            result['FinishedTime'] = self.finished_time
        if self.command_id is not None:
            result['CommandId'] = self.command_id
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.invoke_record_status is not None:
            result['InvokeRecordStatus'] = self.invoke_record_status
        if self.exit_code is not None:
            result['ExitCode'] = self.exit_code
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Success') is not None:
            self.success = m.get('Success')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('FinishedTime') is not None:
            self.finished_time = m.get('FinishedTime')
        if m.get('CommandId') is not None:
            self.command_id = m.get('CommandId')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('InvokeRecordStatus') is not None:
            self.invoke_record_status = m.get('InvokeRecordStatus')
        if m.get('ExitCode') is not None:
            self.exit_code = m.get('ExitCode')
        return self


class ListInvocationResultsResponseBody(TeaModel):
    def __init__(
        self,
        invocation_results: List[ListInvocationResultsResponseBodyInvocationResults] = None,
        total_count: int = None,
        page_size: int = None,
        request_id: str = None,
        page_number: int = None,
    ):
        self.invocation_results = invocation_results
        self.total_count = total_count
        self.page_size = page_size
        self.request_id = request_id
        self.page_number = page_number

    def validate(self):
        if self.invocation_results:
            for k in self.invocation_results:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['InvocationResults'] = []
        if self.invocation_results is not None:
            for k in self.invocation_results:
                result['InvocationResults'].append(k.to_map() if k else None)
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.invocation_results = []
        if m.get('InvocationResults') is not None:
            for k in m.get('InvocationResults'):
                temp_model = ListInvocationResultsResponseBodyInvocationResults()
                self.invocation_results.append(temp_model.from_map(k))
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        return self


class ListInvocationResultsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ListInvocationResultsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ListInvocationResultsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListInvocationStatusRequest(TeaModel):
    def __init__(
        self,
        cluster_id: str = None,
        command_id: str = None,
    ):
        self.cluster_id = cluster_id
        self.command_id = command_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        if self.command_id is not None:
            result['CommandId'] = self.command_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        if m.get('CommandId') is not None:
            self.command_id = m.get('CommandId')
        return self


class ListInvocationStatusResponseBodyInvokeInstances(TeaModel):
    def __init__(
        self,
        instance_id: str = None,
        instance_invoke_status: str = None,
    ):
        self.instance_id = instance_id
        self.instance_invoke_status = instance_invoke_status

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.instance_invoke_status is not None:
            result['InstanceInvokeStatus'] = self.instance_invoke_status
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('InstanceInvokeStatus') is not None:
            self.instance_invoke_status = m.get('InstanceInvokeStatus')
        return self


class ListInvocationStatusResponseBody(TeaModel):
    def __init__(
        self,
        invoke_status: str = None,
        request_id: str = None,
        command_id: str = None,
        invoke_instances: List[ListInvocationStatusResponseBodyInvokeInstances] = None,
    ):
        self.invoke_status = invoke_status
        self.request_id = request_id
        self.command_id = command_id
        self.invoke_instances = invoke_instances

    def validate(self):
        if self.invoke_instances:
            for k in self.invoke_instances:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.invoke_status is not None:
            result['InvokeStatus'] = self.invoke_status
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.command_id is not None:
            result['CommandId'] = self.command_id
        result['InvokeInstances'] = []
        if self.invoke_instances is not None:
            for k in self.invoke_instances:
                result['InvokeInstances'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('InvokeStatus') is not None:
            self.invoke_status = m.get('InvokeStatus')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('CommandId') is not None:
            self.command_id = m.get('CommandId')
        self.invoke_instances = []
        if m.get('InvokeInstances') is not None:
            for k in m.get('InvokeInstances'):
                temp_model = ListInvocationStatusResponseBodyInvokeInstances()
                self.invoke_instances.append(temp_model.from_map(k))
        return self


class ListInvocationStatusResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ListInvocationStatusResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ListInvocationStatusResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListJobsRequest(TeaModel):
    def __init__(
        self,
        cluster_id: str = None,
        owner: str = None,
        state: str = None,
        rerunable: str = None,
        page_number: int = None,
        page_size: int = None,
    ):
        self.cluster_id = cluster_id
        self.owner = owner
        self.state = state
        self.rerunable = rerunable
        self.page_number = page_number
        self.page_size = page_size

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        if self.owner is not None:
            result['Owner'] = self.owner
        if self.state is not None:
            result['State'] = self.state
        if self.rerunable is not None:
            result['Rerunable'] = self.rerunable
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        if m.get('Owner') is not None:
            self.owner = m.get('Owner')
        if m.get('State') is not None:
            self.state = m.get('State')
        if m.get('Rerunable') is not None:
            self.rerunable = m.get('Rerunable')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        return self


class ListJobsResponseBodyJobsResources(TeaModel):
    def __init__(
        self,
        nodes: int = None,
        cores: int = None,
    ):
        self.nodes = nodes
        self.cores = cores

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.nodes is not None:
            result['Nodes'] = self.nodes
        if self.cores is not None:
            result['Cores'] = self.cores
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Nodes') is not None:
            self.nodes = m.get('Nodes')
        if m.get('Cores') is not None:
            self.cores = m.get('Cores')
        return self


class ListJobsResponseBodyJobs(TeaModel):
    def __init__(
        self,
        owner: str = None,
        comment: str = None,
        stderr: str = None,
        state: str = None,
        priority: str = None,
        shell_path: str = None,
        stdout: str = None,
        array_request: str = None,
        start_time: str = None,
        last_modify_time: str = None,
        node_list: str = None,
        name: str = None,
        id: str = None,
        submit_time: str = None,
        resources: ListJobsResponseBodyJobsResources = None,
    ):
        self.owner = owner
        self.comment = comment
        self.stderr = stderr
        self.state = state
        self.priority = priority
        self.shell_path = shell_path
        self.stdout = stdout
        self.array_request = array_request
        self.start_time = start_time
        self.last_modify_time = last_modify_time
        self.node_list = node_list
        self.name = name
        self.id = id
        self.submit_time = submit_time
        self.resources = resources

    def validate(self):
        if self.resources:
            self.resources.validate()

    def to_map(self):
        result = dict()
        if self.owner is not None:
            result['Owner'] = self.owner
        if self.comment is not None:
            result['Comment'] = self.comment
        if self.stderr is not None:
            result['Stderr'] = self.stderr
        if self.state is not None:
            result['State'] = self.state
        if self.priority is not None:
            result['Priority'] = self.priority
        if self.shell_path is not None:
            result['ShellPath'] = self.shell_path
        if self.stdout is not None:
            result['Stdout'] = self.stdout
        if self.array_request is not None:
            result['ArrayRequest'] = self.array_request
        if self.start_time is not None:
            result['StartTime'] = self.start_time
        if self.last_modify_time is not None:
            result['LastModifyTime'] = self.last_modify_time
        if self.node_list is not None:
            result['NodeList'] = self.node_list
        if self.name is not None:
            result['Name'] = self.name
        if self.id is not None:
            result['Id'] = self.id
        if self.submit_time is not None:
            result['SubmitTime'] = self.submit_time
        if self.resources is not None:
            result['Resources'] = self.resources.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Owner') is not None:
            self.owner = m.get('Owner')
        if m.get('Comment') is not None:
            self.comment = m.get('Comment')
        if m.get('Stderr') is not None:
            self.stderr = m.get('Stderr')
        if m.get('State') is not None:
            self.state = m.get('State')
        if m.get('Priority') is not None:
            self.priority = m.get('Priority')
        if m.get('ShellPath') is not None:
            self.shell_path = m.get('ShellPath')
        if m.get('Stdout') is not None:
            self.stdout = m.get('Stdout')
        if m.get('ArrayRequest') is not None:
            self.array_request = m.get('ArrayRequest')
        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')
        if m.get('LastModifyTime') is not None:
            self.last_modify_time = m.get('LastModifyTime')
        if m.get('NodeList') is not None:
            self.node_list = m.get('NodeList')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Id') is not None:
            self.id = m.get('Id')
        if m.get('SubmitTime') is not None:
            self.submit_time = m.get('SubmitTime')
        if m.get('Resources') is not None:
            temp_model = ListJobsResponseBodyJobsResources()
            self.resources = temp_model.from_map(m['Resources'])
        return self


class ListJobsResponseBody(TeaModel):
    def __init__(
        self,
        total_count: int = None,
        page_size: int = None,
        request_id: str = None,
        page_number: int = None,
        jobs: List[ListJobsResponseBodyJobs] = None,
    ):
        self.total_count = total_count
        self.page_size = page_size
        self.request_id = request_id
        self.page_number = page_number
        self.jobs = jobs

    def validate(self):
        if self.jobs:
            for k in self.jobs:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        result['Jobs'] = []
        if self.jobs is not None:
            for k in self.jobs:
                result['Jobs'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        self.jobs = []
        if m.get('Jobs') is not None:
            for k in m.get('Jobs'):
                temp_model = ListJobsResponseBodyJobs()
                self.jobs.append(temp_model.from_map(k))
        return self


class ListJobsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ListJobsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ListJobsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListJobTemplatesRequest(TeaModel):
    def __init__(
        self,
        name: str = None,
        page_number: int = None,
        page_size: int = None,
    ):
        self.name = name
        self.page_number = page_number
        self.page_size = page_size

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.name is not None:
            result['Name'] = self.name
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        return self


class ListJobTemplatesResponseBodyTemplates(TeaModel):
    def __init__(
        self,
        stdout_redirect_path: str = None,
        variables: str = None,
        command_line: str = None,
        package_path: str = None,
        priority: int = None,
        re_runable: bool = None,
        name: str = None,
        array_request: str = None,
        id: str = None,
        stderr_redirect_path: str = None,
        runas_user: str = None,
    ):
        self.stdout_redirect_path = stdout_redirect_path
        self.variables = variables
        self.command_line = command_line
        self.package_path = package_path
        self.priority = priority
        self.re_runable = re_runable
        self.name = name
        self.array_request = array_request
        self.id = id
        self.stderr_redirect_path = stderr_redirect_path
        self.runas_user = runas_user

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.stdout_redirect_path is not None:
            result['StdoutRedirectPath'] = self.stdout_redirect_path
        if self.variables is not None:
            result['Variables'] = self.variables
        if self.command_line is not None:
            result['CommandLine'] = self.command_line
        if self.package_path is not None:
            result['PackagePath'] = self.package_path
        if self.priority is not None:
            result['Priority'] = self.priority
        if self.re_runable is not None:
            result['ReRunable'] = self.re_runable
        if self.name is not None:
            result['Name'] = self.name
        if self.array_request is not None:
            result['ArrayRequest'] = self.array_request
        if self.id is not None:
            result['Id'] = self.id
        if self.stderr_redirect_path is not None:
            result['StderrRedirectPath'] = self.stderr_redirect_path
        if self.runas_user is not None:
            result['RunasUser'] = self.runas_user
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('StdoutRedirectPath') is not None:
            self.stdout_redirect_path = m.get('StdoutRedirectPath')
        if m.get('Variables') is not None:
            self.variables = m.get('Variables')
        if m.get('CommandLine') is not None:
            self.command_line = m.get('CommandLine')
        if m.get('PackagePath') is not None:
            self.package_path = m.get('PackagePath')
        if m.get('Priority') is not None:
            self.priority = m.get('Priority')
        if m.get('ReRunable') is not None:
            self.re_runable = m.get('ReRunable')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('ArrayRequest') is not None:
            self.array_request = m.get('ArrayRequest')
        if m.get('Id') is not None:
            self.id = m.get('Id')
        if m.get('StderrRedirectPath') is not None:
            self.stderr_redirect_path = m.get('StderrRedirectPath')
        if m.get('RunasUser') is not None:
            self.runas_user = m.get('RunasUser')
        return self


class ListJobTemplatesResponseBody(TeaModel):
    def __init__(
        self,
        total_count: int = None,
        page_size: int = None,
        request_id: str = None,
        page_number: int = None,
        templates: List[ListJobTemplatesResponseBodyTemplates] = None,
    ):
        self.total_count = total_count
        self.page_size = page_size
        self.request_id = request_id
        self.page_number = page_number
        self.templates = templates

    def validate(self):
        if self.templates:
            for k in self.templates:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        result['Templates'] = []
        if self.templates is not None:
            for k in self.templates:
                result['Templates'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        self.templates = []
        if m.get('Templates') is not None:
            for k in m.get('Templates'):
                temp_model = ListJobTemplatesResponseBodyTemplates()
                self.templates.append(temp_model.from_map(k))
        return self


class ListJobTemplatesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ListJobTemplatesResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ListJobTemplatesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListNodesRequest(TeaModel):
    def __init__(
        self,
        cluster_id: str = None,
        role: str = None,
        host_name: str = None,
        page_number: int = None,
        page_size: int = None,
        sequence: str = None,
        sort_by: str = None,
        filter: str = None,
    ):
        self.cluster_id = cluster_id
        self.role = role
        self.host_name = host_name
        self.page_number = page_number
        self.page_size = page_size
        self.sequence = sequence
        self.sort_by = sort_by
        self.filter = filter

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        if self.role is not None:
            result['Role'] = self.role
        if self.host_name is not None:
            result['HostName'] = self.host_name
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.sequence is not None:
            result['Sequence'] = self.sequence
        if self.sort_by is not None:
            result['SortBy'] = self.sort_by
        if self.filter is not None:
            result['Filter'] = self.filter
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        if m.get('Role') is not None:
            self.role = m.get('Role')
        if m.get('HostName') is not None:
            self.host_name = m.get('HostName')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('Sequence') is not None:
            self.sequence = m.get('Sequence')
        if m.get('SortBy') is not None:
            self.sort_by = m.get('SortBy')
        if m.get('Filter') is not None:
            self.filter = m.get('Filter')
        return self


class ListNodesResponseBodyNodesUsedResources(TeaModel):
    def __init__(
        self,
        cpu: int = None,
        gpu: int = None,
        memory: int = None,
    ):
        self.cpu = cpu
        self.gpu = gpu
        self.memory = memory

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.cpu is not None:
            result['Cpu'] = self.cpu
        if self.gpu is not None:
            result['Gpu'] = self.gpu
        if self.memory is not None:
            result['Memory'] = self.memory
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Cpu') is not None:
            self.cpu = m.get('Cpu')
        if m.get('Gpu') is not None:
            self.gpu = m.get('Gpu')
        if m.get('Memory') is not None:
            self.memory = m.get('Memory')
        return self


class ListNodesResponseBodyNodesTotalResources(TeaModel):
    def __init__(
        self,
        cpu: int = None,
        gpu: int = None,
        memory: int = None,
    ):
        self.cpu = cpu
        self.gpu = gpu
        self.memory = memory

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.cpu is not None:
            result['Cpu'] = self.cpu
        if self.gpu is not None:
            result['Gpu'] = self.gpu
        if self.memory is not None:
            result['Memory'] = self.memory
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Cpu') is not None:
            self.cpu = m.get('Cpu')
        if m.get('Gpu') is not None:
            self.gpu = m.get('Gpu')
        if m.get('Memory') is not None:
            self.memory = m.get('Memory')
        return self


class ListNodesResponseBodyNodes(TeaModel):
    def __init__(
        self,
        status: str = None,
        vpc_id: str = None,
        expired: bool = None,
        used_resources: ListNodesResponseBodyNodesUsedResources = None,
        spot_strategy: str = None,
        public_ip_address: str = None,
        created_by_ehpc: bool = None,
        ip_address: str = None,
        version: str = None,
        add_time: str = None,
        image_id: str = None,
        create_mode: str = None,
        ht_enabled: bool = None,
        image_owner_alias: str = None,
        roles: List[str] = None,
        lock_reason: str = None,
        host_name: str = None,
        region_id: str = None,
        total_resources: ListNodesResponseBodyNodesTotalResources = None,
        v_switch_id: str = None,
        expired_time: str = None,
        zone_id: str = None,
        location: str = None,
        id: str = None,
    ):
        self.status = status
        self.vpc_id = vpc_id
        self.expired = expired
        self.used_resources = used_resources
        self.spot_strategy = spot_strategy
        self.public_ip_address = public_ip_address
        self.created_by_ehpc = created_by_ehpc
        self.ip_address = ip_address
        self.version = version
        self.add_time = add_time
        self.image_id = image_id
        self.create_mode = create_mode
        self.ht_enabled = ht_enabled
        self.image_owner_alias = image_owner_alias
        self.roles = roles
        self.lock_reason = lock_reason
        self.host_name = host_name
        self.region_id = region_id
        self.total_resources = total_resources
        self.v_switch_id = v_switch_id
        self.expired_time = expired_time
        self.zone_id = zone_id
        self.location = location
        self.id = id

    def validate(self):
        if self.used_resources:
            self.used_resources.validate()
        if self.total_resources:
            self.total_resources.validate()

    def to_map(self):
        result = dict()
        if self.status is not None:
            result['Status'] = self.status
        if self.vpc_id is not None:
            result['VpcId'] = self.vpc_id
        if self.expired is not None:
            result['Expired'] = self.expired
        if self.used_resources is not None:
            result['UsedResources'] = self.used_resources.to_map()
        if self.spot_strategy is not None:
            result['SpotStrategy'] = self.spot_strategy
        if self.public_ip_address is not None:
            result['PublicIpAddress'] = self.public_ip_address
        if self.created_by_ehpc is not None:
            result['CreatedByEhpc'] = self.created_by_ehpc
        if self.ip_address is not None:
            result['IpAddress'] = self.ip_address
        if self.version is not None:
            result['Version'] = self.version
        if self.add_time is not None:
            result['AddTime'] = self.add_time
        if self.image_id is not None:
            result['ImageId'] = self.image_id
        if self.create_mode is not None:
            result['CreateMode'] = self.create_mode
        if self.ht_enabled is not None:
            result['HtEnabled'] = self.ht_enabled
        if self.image_owner_alias is not None:
            result['ImageOwnerAlias'] = self.image_owner_alias
        if self.roles is not None:
            result['Roles'] = self.roles
        if self.lock_reason is not None:
            result['LockReason'] = self.lock_reason
        if self.host_name is not None:
            result['HostName'] = self.host_name
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.total_resources is not None:
            result['TotalResources'] = self.total_resources.to_map()
        if self.v_switch_id is not None:
            result['VSwitchId'] = self.v_switch_id
        if self.expired_time is not None:
            result['ExpiredTime'] = self.expired_time
        if self.zone_id is not None:
            result['ZoneId'] = self.zone_id
        if self.location is not None:
            result['Location'] = self.location
        if self.id is not None:
            result['Id'] = self.id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('VpcId') is not None:
            self.vpc_id = m.get('VpcId')
        if m.get('Expired') is not None:
            self.expired = m.get('Expired')
        if m.get('UsedResources') is not None:
            temp_model = ListNodesResponseBodyNodesUsedResources()
            self.used_resources = temp_model.from_map(m['UsedResources'])
        if m.get('SpotStrategy') is not None:
            self.spot_strategy = m.get('SpotStrategy')
        if m.get('PublicIpAddress') is not None:
            self.public_ip_address = m.get('PublicIpAddress')
        if m.get('CreatedByEhpc') is not None:
            self.created_by_ehpc = m.get('CreatedByEhpc')
        if m.get('IpAddress') is not None:
            self.ip_address = m.get('IpAddress')
        if m.get('Version') is not None:
            self.version = m.get('Version')
        if m.get('AddTime') is not None:
            self.add_time = m.get('AddTime')
        if m.get('ImageId') is not None:
            self.image_id = m.get('ImageId')
        if m.get('CreateMode') is not None:
            self.create_mode = m.get('CreateMode')
        if m.get('HtEnabled') is not None:
            self.ht_enabled = m.get('HtEnabled')
        if m.get('ImageOwnerAlias') is not None:
            self.image_owner_alias = m.get('ImageOwnerAlias')
        if m.get('Roles') is not None:
            self.roles = m.get('Roles')
        if m.get('LockReason') is not None:
            self.lock_reason = m.get('LockReason')
        if m.get('HostName') is not None:
            self.host_name = m.get('HostName')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('TotalResources') is not None:
            temp_model = ListNodesResponseBodyNodesTotalResources()
            self.total_resources = temp_model.from_map(m['TotalResources'])
        if m.get('VSwitchId') is not None:
            self.v_switch_id = m.get('VSwitchId')
        if m.get('ExpiredTime') is not None:
            self.expired_time = m.get('ExpiredTime')
        if m.get('ZoneId') is not None:
            self.zone_id = m.get('ZoneId')
        if m.get('Location') is not None:
            self.location = m.get('Location')
        if m.get('Id') is not None:
            self.id = m.get('Id')
        return self


class ListNodesResponseBody(TeaModel):
    def __init__(
        self,
        total_count: int = None,
        page_size: int = None,
        request_id: str = None,
        page_number: int = None,
        nodes: List[ListNodesResponseBodyNodes] = None,
    ):
        self.total_count = total_count
        self.page_size = page_size
        self.request_id = request_id
        self.page_number = page_number
        self.nodes = nodes

    def validate(self):
        if self.nodes:
            for k in self.nodes:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        result['Nodes'] = []
        if self.nodes is not None:
            for k in self.nodes:
                result['Nodes'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        self.nodes = []
        if m.get('Nodes') is not None:
            for k in m.get('Nodes'):
                temp_model = ListNodesResponseBodyNodes()
                self.nodes.append(temp_model.from_map(k))
        return self


class ListNodesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ListNodesResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ListNodesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListNodesByQueueRequest(TeaModel):
    def __init__(
        self,
        cluster_id: str = None,
        queue_name: str = None,
        page_number: int = None,
        page_size: int = None,
    ):
        self.cluster_id = cluster_id
        self.queue_name = queue_name
        self.page_number = page_number
        self.page_size = page_size

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        if self.queue_name is not None:
            result['QueueName'] = self.queue_name
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        if m.get('QueueName') is not None:
            self.queue_name = m.get('QueueName')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        return self


class ListNodesByQueueResponseBodyNodesUsedResources(TeaModel):
    def __init__(
        self,
        cpu: int = None,
        gpu: int = None,
        memory: int = None,
    ):
        self.cpu = cpu
        self.gpu = gpu
        self.memory = memory

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.cpu is not None:
            result['Cpu'] = self.cpu
        if self.gpu is not None:
            result['Gpu'] = self.gpu
        if self.memory is not None:
            result['Memory'] = self.memory
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Cpu') is not None:
            self.cpu = m.get('Cpu')
        if m.get('Gpu') is not None:
            self.gpu = m.get('Gpu')
        if m.get('Memory') is not None:
            self.memory = m.get('Memory')
        return self


class ListNodesByQueueResponseBodyNodesTotalResources(TeaModel):
    def __init__(
        self,
        cpu: int = None,
        gpu: int = None,
        memory: int = None,
    ):
        self.cpu = cpu
        self.gpu = gpu
        self.memory = memory

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.cpu is not None:
            result['Cpu'] = self.cpu
        if self.gpu is not None:
            result['Gpu'] = self.gpu
        if self.memory is not None:
            result['Memory'] = self.memory
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Cpu') is not None:
            self.cpu = m.get('Cpu')
        if m.get('Gpu') is not None:
            self.gpu = m.get('Gpu')
        if m.get('Memory') is not None:
            self.memory = m.get('Memory')
        return self


class ListNodesByQueueResponseBodyNodes(TeaModel):
    def __init__(
        self,
        status: str = None,
        vpc_id: str = None,
        ht_enabled: bool = None,
        expired: bool = None,
        image_owner_alias: str = None,
        host_name: str = None,
        lock_reason: str = None,
        used_resources: ListNodesByQueueResponseBodyNodesUsedResources = None,
        spot_strategy: str = None,
        public_ip_address: str = None,
        region_id: str = None,
        created_by_ehpc: bool = None,
        v_switch_id: str = None,
        total_resources: ListNodesByQueueResponseBodyNodesTotalResources = None,
        ip_address: str = None,
        expired_time: str = None,
        version: str = None,
        zone_id: str = None,
        add_time: str = None,
        image_id: str = None,
        location: str = None,
        id: str = None,
        create_mode: str = None,
    ):
        self.status = status
        self.vpc_id = vpc_id
        self.ht_enabled = ht_enabled
        self.expired = expired
        self.image_owner_alias = image_owner_alias
        self.host_name = host_name
        self.lock_reason = lock_reason
        self.used_resources = used_resources
        self.spot_strategy = spot_strategy
        self.public_ip_address = public_ip_address
        self.region_id = region_id
        self.created_by_ehpc = created_by_ehpc
        self.v_switch_id = v_switch_id
        self.total_resources = total_resources
        self.ip_address = ip_address
        self.expired_time = expired_time
        self.version = version
        self.zone_id = zone_id
        self.add_time = add_time
        self.image_id = image_id
        self.location = location
        self.id = id
        self.create_mode = create_mode

    def validate(self):
        if self.used_resources:
            self.used_resources.validate()
        if self.total_resources:
            self.total_resources.validate()

    def to_map(self):
        result = dict()
        if self.status is not None:
            result['Status'] = self.status
        if self.vpc_id is not None:
            result['VpcId'] = self.vpc_id
        if self.ht_enabled is not None:
            result['HtEnabled'] = self.ht_enabled
        if self.expired is not None:
            result['Expired'] = self.expired
        if self.image_owner_alias is not None:
            result['ImageOwnerAlias'] = self.image_owner_alias
        if self.host_name is not None:
            result['HostName'] = self.host_name
        if self.lock_reason is not None:
            result['LockReason'] = self.lock_reason
        if self.used_resources is not None:
            result['UsedResources'] = self.used_resources.to_map()
        if self.spot_strategy is not None:
            result['SpotStrategy'] = self.spot_strategy
        if self.public_ip_address is not None:
            result['PublicIpAddress'] = self.public_ip_address
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.created_by_ehpc is not None:
            result['CreatedByEhpc'] = self.created_by_ehpc
        if self.v_switch_id is not None:
            result['VSwitchId'] = self.v_switch_id
        if self.total_resources is not None:
            result['TotalResources'] = self.total_resources.to_map()
        if self.ip_address is not None:
            result['IpAddress'] = self.ip_address
        if self.expired_time is not None:
            result['ExpiredTime'] = self.expired_time
        if self.version is not None:
            result['Version'] = self.version
        if self.zone_id is not None:
            result['ZoneId'] = self.zone_id
        if self.add_time is not None:
            result['AddTime'] = self.add_time
        if self.image_id is not None:
            result['ImageId'] = self.image_id
        if self.location is not None:
            result['Location'] = self.location
        if self.id is not None:
            result['Id'] = self.id
        if self.create_mode is not None:
            result['CreateMode'] = self.create_mode
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('VpcId') is not None:
            self.vpc_id = m.get('VpcId')
        if m.get('HtEnabled') is not None:
            self.ht_enabled = m.get('HtEnabled')
        if m.get('Expired') is not None:
            self.expired = m.get('Expired')
        if m.get('ImageOwnerAlias') is not None:
            self.image_owner_alias = m.get('ImageOwnerAlias')
        if m.get('HostName') is not None:
            self.host_name = m.get('HostName')
        if m.get('LockReason') is not None:
            self.lock_reason = m.get('LockReason')
        if m.get('UsedResources') is not None:
            temp_model = ListNodesByQueueResponseBodyNodesUsedResources()
            self.used_resources = temp_model.from_map(m['UsedResources'])
        if m.get('SpotStrategy') is not None:
            self.spot_strategy = m.get('SpotStrategy')
        if m.get('PublicIpAddress') is not None:
            self.public_ip_address = m.get('PublicIpAddress')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('CreatedByEhpc') is not None:
            self.created_by_ehpc = m.get('CreatedByEhpc')
        if m.get('VSwitchId') is not None:
            self.v_switch_id = m.get('VSwitchId')
        if m.get('TotalResources') is not None:
            temp_model = ListNodesByQueueResponseBodyNodesTotalResources()
            self.total_resources = temp_model.from_map(m['TotalResources'])
        if m.get('IpAddress') is not None:
            self.ip_address = m.get('IpAddress')
        if m.get('ExpiredTime') is not None:
            self.expired_time = m.get('ExpiredTime')
        if m.get('Version') is not None:
            self.version = m.get('Version')
        if m.get('ZoneId') is not None:
            self.zone_id = m.get('ZoneId')
        if m.get('AddTime') is not None:
            self.add_time = m.get('AddTime')
        if m.get('ImageId') is not None:
            self.image_id = m.get('ImageId')
        if m.get('Location') is not None:
            self.location = m.get('Location')
        if m.get('Id') is not None:
            self.id = m.get('Id')
        if m.get('CreateMode') is not None:
            self.create_mode = m.get('CreateMode')
        return self


class ListNodesByQueueResponseBody(TeaModel):
    def __init__(
        self,
        total_count: int = None,
        page_size: int = None,
        request_id: str = None,
        page_number: int = None,
        nodes: List[ListNodesByQueueResponseBodyNodes] = None,
    ):
        self.total_count = total_count
        self.page_size = page_size
        self.request_id = request_id
        self.page_number = page_number
        self.nodes = nodes

    def validate(self):
        if self.nodes:
            for k in self.nodes:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        result['Nodes'] = []
        if self.nodes is not None:
            for k in self.nodes:
                result['Nodes'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        self.nodes = []
        if m.get('Nodes') is not None:
            for k in m.get('Nodes'):
                temp_model = ListNodesByQueueResponseBodyNodes()
                self.nodes.append(temp_model.from_map(k))
        return self


class ListNodesByQueueResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ListNodesByQueueResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ListNodesByQueueResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListNodesNoPagingRequest(TeaModel):
    def __init__(
        self,
        cluster_id: str = None,
        role: str = None,
        host_name: str = None,
        only_detached: bool = None,
        sequence: str = None,
    ):
        self.cluster_id = cluster_id
        self.role = role
        self.host_name = host_name
        self.only_detached = only_detached
        self.sequence = sequence

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        if self.role is not None:
            result['Role'] = self.role
        if self.host_name is not None:
            result['HostName'] = self.host_name
        if self.only_detached is not None:
            result['OnlyDetached'] = self.only_detached
        if self.sequence is not None:
            result['Sequence'] = self.sequence
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        if m.get('Role') is not None:
            self.role = m.get('Role')
        if m.get('HostName') is not None:
            self.host_name = m.get('HostName')
        if m.get('OnlyDetached') is not None:
            self.only_detached = m.get('OnlyDetached')
        if m.get('Sequence') is not None:
            self.sequence = m.get('Sequence')
        return self


class ListNodesNoPagingResponseBodyNodesUsedResources(TeaModel):
    def __init__(
        self,
        cpu: int = None,
        gpu: int = None,
        memory: int = None,
    ):
        self.cpu = cpu
        self.gpu = gpu
        self.memory = memory

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.cpu is not None:
            result['Cpu'] = self.cpu
        if self.gpu is not None:
            result['Gpu'] = self.gpu
        if self.memory is not None:
            result['Memory'] = self.memory
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Cpu') is not None:
            self.cpu = m.get('Cpu')
        if m.get('Gpu') is not None:
            self.gpu = m.get('Gpu')
        if m.get('Memory') is not None:
            self.memory = m.get('Memory')
        return self


class ListNodesNoPagingResponseBodyNodesTotalResources(TeaModel):
    def __init__(
        self,
        cpu: int = None,
        gpu: int = None,
        memory: int = None,
    ):
        self.cpu = cpu
        self.gpu = gpu
        self.memory = memory

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.cpu is not None:
            result['Cpu'] = self.cpu
        if self.gpu is not None:
            result['Gpu'] = self.gpu
        if self.memory is not None:
            result['Memory'] = self.memory
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Cpu') is not None:
            self.cpu = m.get('Cpu')
        if m.get('Gpu') is not None:
            self.gpu = m.get('Gpu')
        if m.get('Memory') is not None:
            self.memory = m.get('Memory')
        return self


class ListNodesNoPagingResponseBodyNodes(TeaModel):
    def __init__(
        self,
        status: str = None,
        ht_enabled: bool = None,
        expired: bool = None,
        roles: List[str] = None,
        image_owner_alias: str = None,
        lock_reason: str = None,
        host_name: str = None,
        used_resources: ListNodesNoPagingResponseBodyNodesUsedResources = None,
        spot_strategy: str = None,
        created_by_ehpc: bool = None,
        region_id: str = None,
        total_resources: ListNodesNoPagingResponseBodyNodesTotalResources = None,
        version: str = None,
        expired_time: str = None,
        add_time: str = None,
        image_id: str = None,
        id: str = None,
    ):
        self.status = status
        self.ht_enabled = ht_enabled
        self.expired = expired
        self.roles = roles
        self.image_owner_alias = image_owner_alias
        self.lock_reason = lock_reason
        self.host_name = host_name
        self.used_resources = used_resources
        self.spot_strategy = spot_strategy
        self.created_by_ehpc = created_by_ehpc
        self.region_id = region_id
        self.total_resources = total_resources
        self.version = version
        self.expired_time = expired_time
        self.add_time = add_time
        self.image_id = image_id
        self.id = id

    def validate(self):
        if self.used_resources:
            self.used_resources.validate()
        if self.total_resources:
            self.total_resources.validate()

    def to_map(self):
        result = dict()
        if self.status is not None:
            result['Status'] = self.status
        if self.ht_enabled is not None:
            result['HtEnabled'] = self.ht_enabled
        if self.expired is not None:
            result['Expired'] = self.expired
        if self.roles is not None:
            result['Roles'] = self.roles
        if self.image_owner_alias is not None:
            result['ImageOwnerAlias'] = self.image_owner_alias
        if self.lock_reason is not None:
            result['LockReason'] = self.lock_reason
        if self.host_name is not None:
            result['HostName'] = self.host_name
        if self.used_resources is not None:
            result['UsedResources'] = self.used_resources.to_map()
        if self.spot_strategy is not None:
            result['SpotStrategy'] = self.spot_strategy
        if self.created_by_ehpc is not None:
            result['CreatedByEhpc'] = self.created_by_ehpc
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.total_resources is not None:
            result['TotalResources'] = self.total_resources.to_map()
        if self.version is not None:
            result['Version'] = self.version
        if self.expired_time is not None:
            result['ExpiredTime'] = self.expired_time
        if self.add_time is not None:
            result['AddTime'] = self.add_time
        if self.image_id is not None:
            result['ImageId'] = self.image_id
        if self.id is not None:
            result['Id'] = self.id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('HtEnabled') is not None:
            self.ht_enabled = m.get('HtEnabled')
        if m.get('Expired') is not None:
            self.expired = m.get('Expired')
        if m.get('Roles') is not None:
            self.roles = m.get('Roles')
        if m.get('ImageOwnerAlias') is not None:
            self.image_owner_alias = m.get('ImageOwnerAlias')
        if m.get('LockReason') is not None:
            self.lock_reason = m.get('LockReason')
        if m.get('HostName') is not None:
            self.host_name = m.get('HostName')
        if m.get('UsedResources') is not None:
            temp_model = ListNodesNoPagingResponseBodyNodesUsedResources()
            self.used_resources = temp_model.from_map(m['UsedResources'])
        if m.get('SpotStrategy') is not None:
            self.spot_strategy = m.get('SpotStrategy')
        if m.get('CreatedByEhpc') is not None:
            self.created_by_ehpc = m.get('CreatedByEhpc')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('TotalResources') is not None:
            temp_model = ListNodesNoPagingResponseBodyNodesTotalResources()
            self.total_resources = temp_model.from_map(m['TotalResources'])
        if m.get('Version') is not None:
            self.version = m.get('Version')
        if m.get('ExpiredTime') is not None:
            self.expired_time = m.get('ExpiredTime')
        if m.get('AddTime') is not None:
            self.add_time = m.get('AddTime')
        if m.get('ImageId') is not None:
            self.image_id = m.get('ImageId')
        if m.get('Id') is not None:
            self.id = m.get('Id')
        return self


class ListNodesNoPagingResponseBody(TeaModel):
    def __init__(
        self,
        total_count: int = None,
        page_size: int = None,
        request_id: str = None,
        page_number: int = None,
        nodes: List[ListNodesNoPagingResponseBodyNodes] = None,
    ):
        self.total_count = total_count
        self.page_size = page_size
        self.request_id = request_id
        self.page_number = page_number
        self.nodes = nodes

    def validate(self):
        if self.nodes:
            for k in self.nodes:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        result['Nodes'] = []
        if self.nodes is not None:
            for k in self.nodes:
                result['Nodes'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        self.nodes = []
        if m.get('Nodes') is not None:
            for k in m.get('Nodes'):
                temp_model = ListNodesNoPagingResponseBodyNodes()
                self.nodes.append(temp_model.from_map(k))
        return self


class ListNodesNoPagingResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ListNodesNoPagingResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ListNodesNoPagingResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListPreferredEcsTypesRequest(TeaModel):
    def __init__(
        self,
        zone_id: str = None,
        spot_strategy: str = None,
        instance_charge_type: str = None,
    ):
        self.zone_id = zone_id
        self.spot_strategy = spot_strategy
        self.instance_charge_type = instance_charge_type

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.zone_id is not None:
            result['ZoneId'] = self.zone_id
        if self.spot_strategy is not None:
            result['SpotStrategy'] = self.spot_strategy
        if self.instance_charge_type is not None:
            result['InstanceChargeType'] = self.instance_charge_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ZoneId') is not None:
            self.zone_id = m.get('ZoneId')
        if m.get('SpotStrategy') is not None:
            self.spot_strategy = m.get('SpotStrategy')
        if m.get('InstanceChargeType') is not None:
            self.instance_charge_type = m.get('InstanceChargeType')
        return self


class ListPreferredEcsTypesResponseBodySeriesRoles(TeaModel):
    def __init__(
        self,
        manager: List[str] = None,
        compute: List[str] = None,
        login: List[str] = None,
    ):
        self.manager = manager
        self.compute = compute
        self.login = login

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.manager is not None:
            result['Manager'] = self.manager
        if self.compute is not None:
            result['Compute'] = self.compute
        if self.login is not None:
            result['Login'] = self.login
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Manager') is not None:
            self.manager = m.get('Manager')
        if m.get('Compute') is not None:
            self.compute = m.get('Compute')
        if m.get('Login') is not None:
            self.login = m.get('Login')
        return self


class ListPreferredEcsTypesResponseBodySeries(TeaModel):
    def __init__(
        self,
        series_id: str = None,
        series_name: str = None,
        roles: ListPreferredEcsTypesResponseBodySeriesRoles = None,
    ):
        self.series_id = series_id
        self.series_name = series_name
        self.roles = roles

    def validate(self):
        if self.roles:
            self.roles.validate()

    def to_map(self):
        result = dict()
        if self.series_id is not None:
            result['SeriesId'] = self.series_id
        if self.series_name is not None:
            result['SeriesName'] = self.series_name
        if self.roles is not None:
            result['Roles'] = self.roles.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('SeriesId') is not None:
            self.series_id = m.get('SeriesId')
        if m.get('SeriesName') is not None:
            self.series_name = m.get('SeriesName')
        if m.get('Roles') is not None:
            temp_model = ListPreferredEcsTypesResponseBodySeriesRoles()
            self.roles = temp_model.from_map(m['Roles'])
        return self


class ListPreferredEcsTypesResponseBody(TeaModel):
    def __init__(
        self,
        series: List[ListPreferredEcsTypesResponseBodySeries] = None,
        support_spot_instance: bool = None,
        request_id: str = None,
    ):
        self.series = series
        self.support_spot_instance = support_spot_instance
        self.request_id = request_id

    def validate(self):
        if self.series:
            for k in self.series:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['Series'] = []
        if self.series is not None:
            for k in self.series:
                result['Series'].append(k.to_map() if k else None)
        if self.support_spot_instance is not None:
            result['SupportSpotInstance'] = self.support_spot_instance
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.series = []
        if m.get('Series') is not None:
            for k in m.get('Series'):
                temp_model = ListPreferredEcsTypesResponseBodySeries()
                self.series.append(temp_model.from_map(k))
        if m.get('SupportSpotInstance') is not None:
            self.support_spot_instance = m.get('SupportSpotInstance')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class ListPreferredEcsTypesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ListPreferredEcsTypesResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ListPreferredEcsTypesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListQueuesRequest(TeaModel):
    def __init__(
        self,
        cluster_id: str = None,
    ):
        self.cluster_id = cluster_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        return self


class ListQueuesResponseBodyQueues(TeaModel):
    def __init__(
        self,
        type: str = None,
        queue_name: str = None,
        resource_group_id: str = None,
        compute_instance_type: str = None,
    ):
        self.type = type
        self.queue_name = queue_name
        self.resource_group_id = resource_group_id
        self.compute_instance_type = compute_instance_type

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.type is not None:
            result['Type'] = self.type
        if self.queue_name is not None:
            result['QueueName'] = self.queue_name
        if self.resource_group_id is not None:
            result['ResourceGroupId'] = self.resource_group_id
        if self.compute_instance_type is not None:
            result['ComputeInstanceType'] = self.compute_instance_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('QueueName') is not None:
            self.queue_name = m.get('QueueName')
        if m.get('ResourceGroupId') is not None:
            self.resource_group_id = m.get('ResourceGroupId')
        if m.get('ComputeInstanceType') is not None:
            self.compute_instance_type = m.get('ComputeInstanceType')
        return self


class ListQueuesResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        queues: List[ListQueuesResponseBodyQueues] = None,
    ):
        self.request_id = request_id
        self.queues = queues

    def validate(self):
        if self.queues:
            for k in self.queues:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        result['Queues'] = []
        if self.queues is not None:
            for k in self.queues:
                result['Queues'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        self.queues = []
        if m.get('Queues') is not None:
            for k in m.get('Queues'):
                temp_model = ListQueuesResponseBodyQueues()
                self.queues.append(temp_model.from_map(k))
        return self


class ListQueuesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ListQueuesResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ListQueuesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListRegionsResponseBodyRegions(TeaModel):
    def __init__(
        self,
        local_name: str = None,
        region_id: str = None,
    ):
        self.local_name = local_name
        self.region_id = region_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.local_name is not None:
            result['LocalName'] = self.local_name
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('LocalName') is not None:
            self.local_name = m.get('LocalName')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        return self


class ListRegionsResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        regions: List[ListRegionsResponseBodyRegions] = None,
    ):
        self.request_id = request_id
        self.regions = regions

    def validate(self):
        if self.regions:
            for k in self.regions:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        result['Regions'] = []
        if self.regions is not None:
            for k in self.regions:
                result['Regions'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        self.regions = []
        if m.get('Regions') is not None:
            for k in m.get('Regions'):
                temp_model = ListRegionsResponseBodyRegions()
                self.regions.append(temp_model.from_map(k))
        return self


class ListRegionsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ListRegionsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ListRegionsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListSecurityGroupsRequest(TeaModel):
    def __init__(
        self,
        cluster_id: str = None,
    ):
        self.cluster_id = cluster_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        return self


class ListSecurityGroupsResponseBody(TeaModel):
    def __init__(
        self,
        security_groups: List[str] = None,
        total_count: int = None,
        request_id: str = None,
    ):
        self.security_groups = security_groups
        self.total_count = total_count
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.security_groups is not None:
            result['SecurityGroups'] = self.security_groups
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('SecurityGroups') is not None:
            self.security_groups = m.get('SecurityGroups')
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class ListSecurityGroupsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ListSecurityGroupsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ListSecurityGroupsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListSoftwaresRequest(TeaModel):
    def __init__(
        self,
        ehpc_version: str = None,
        os_tag: str = None,
    ):
        self.ehpc_version = ehpc_version
        self.os_tag = os_tag

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.ehpc_version is not None:
            result['EhpcVersion'] = self.ehpc_version
        if self.os_tag is not None:
            result['OsTag'] = self.os_tag
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('EhpcVersion') is not None:
            self.ehpc_version = m.get('EhpcVersion')
        if m.get('OsTag') is not None:
            self.os_tag = m.get('OsTag')
        return self


class ListSoftwaresResponseBodySoftwaresApplications(TeaModel):
    def __init__(
        self,
        required: bool = None,
        version: str = None,
        tag: str = None,
        name: str = None,
    ):
        self.required = required
        self.version = version
        self.tag = tag
        self.name = name

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.required is not None:
            result['Required'] = self.required
        if self.version is not None:
            result['Version'] = self.version
        if self.tag is not None:
            result['Tag'] = self.tag
        if self.name is not None:
            result['Name'] = self.name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Required') is not None:
            self.required = m.get('Required')
        if m.get('Version') is not None:
            self.version = m.get('Version')
        if m.get('Tag') is not None:
            self.tag = m.get('Tag')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        return self


class ListSoftwaresResponseBodySoftwares(TeaModel):
    def __init__(
        self,
        scheduler_type: str = None,
        os_tag: str = None,
        scheduler_version: str = None,
        account_version: str = None,
        applications: List[ListSoftwaresResponseBodySoftwaresApplications] = None,
        account_type: str = None,
        ehpc_version: str = None,
    ):
        self.scheduler_type = scheduler_type
        self.os_tag = os_tag
        self.scheduler_version = scheduler_version
        self.account_version = account_version
        self.applications = applications
        self.account_type = account_type
        self.ehpc_version = ehpc_version

    def validate(self):
        if self.applications:
            for k in self.applications:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.scheduler_type is not None:
            result['SchedulerType'] = self.scheduler_type
        if self.os_tag is not None:
            result['OsTag'] = self.os_tag
        if self.scheduler_version is not None:
            result['SchedulerVersion'] = self.scheduler_version
        if self.account_version is not None:
            result['AccountVersion'] = self.account_version
        result['Applications'] = []
        if self.applications is not None:
            for k in self.applications:
                result['Applications'].append(k.to_map() if k else None)
        if self.account_type is not None:
            result['AccountType'] = self.account_type
        if self.ehpc_version is not None:
            result['EhpcVersion'] = self.ehpc_version
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('SchedulerType') is not None:
            self.scheduler_type = m.get('SchedulerType')
        if m.get('OsTag') is not None:
            self.os_tag = m.get('OsTag')
        if m.get('SchedulerVersion') is not None:
            self.scheduler_version = m.get('SchedulerVersion')
        if m.get('AccountVersion') is not None:
            self.account_version = m.get('AccountVersion')
        self.applications = []
        if m.get('Applications') is not None:
            for k in m.get('Applications'):
                temp_model = ListSoftwaresResponseBodySoftwaresApplications()
                self.applications.append(temp_model.from_map(k))
        if m.get('AccountType') is not None:
            self.account_type = m.get('AccountType')
        if m.get('EhpcVersion') is not None:
            self.ehpc_version = m.get('EhpcVersion')
        return self


class ListSoftwaresResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        softwares: List[ListSoftwaresResponseBodySoftwares] = None,
    ):
        self.request_id = request_id
        self.softwares = softwares

    def validate(self):
        if self.softwares:
            for k in self.softwares:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        result['Softwares'] = []
        if self.softwares is not None:
            for k in self.softwares:
                result['Softwares'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        self.softwares = []
        if m.get('Softwares') is not None:
            for k in m.get('Softwares'):
                temp_model = ListSoftwaresResponseBodySoftwares()
                self.softwares.append(temp_model.from_map(k))
        return self


class ListSoftwaresResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ListSoftwaresResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ListSoftwaresResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListTasksRequest(TeaModel):
    def __init__(
        self,
        cluster_id: str = None,
        page_number: int = None,
        page_size: int = None,
        task_id: str = None,
        archived: bool = None,
    ):
        self.cluster_id = cluster_id
        self.page_number = page_number
        self.page_size = page_size
        self.task_id = task_id
        self.archived = archived

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.task_id is not None:
            result['TaskId'] = self.task_id
        if self.archived is not None:
            result['Archived'] = self.archived
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('TaskId') is not None:
            self.task_id = m.get('TaskId')
        if m.get('Archived') is not None:
            self.archived = m.get('Archived')
        return self


class ListTasksResponseBodyTasks(TeaModel):
    def __init__(
        self,
        status: str = None,
        task_type: str = None,
        total_steps: int = None,
        current_step: int = None,
        result: str = None,
        errors: str = None,
        task_id: str = None,
        request: str = None,
        cluster_id: str = None,
    ):
        self.status = status
        self.task_type = task_type
        self.total_steps = total_steps
        self.current_step = current_step
        self.result = result
        self.errors = errors
        self.task_id = task_id
        self.request = request
        self.cluster_id = cluster_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.status is not None:
            result['Status'] = self.status
        if self.task_type is not None:
            result['TaskType'] = self.task_type
        if self.total_steps is not None:
            result['TotalSteps'] = self.total_steps
        if self.current_step is not None:
            result['CurrentStep'] = self.current_step
        if self.result is not None:
            result['Result'] = self.result
        if self.errors is not None:
            result['Errors'] = self.errors
        if self.task_id is not None:
            result['TaskId'] = self.task_id
        if self.request is not None:
            result['Request'] = self.request
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('TaskType') is not None:
            self.task_type = m.get('TaskType')
        if m.get('TotalSteps') is not None:
            self.total_steps = m.get('TotalSteps')
        if m.get('CurrentStep') is not None:
            self.current_step = m.get('CurrentStep')
        if m.get('Result') is not None:
            self.result = m.get('Result')
        if m.get('Errors') is not None:
            self.errors = m.get('Errors')
        if m.get('TaskId') is not None:
            self.task_id = m.get('TaskId')
        if m.get('Request') is not None:
            self.request = m.get('Request')
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        return self


class ListTasksResponseBody(TeaModel):
    def __init__(
        self,
        total_count: int = None,
        tasks: List[ListTasksResponseBodyTasks] = None,
        page_size: int = None,
        request_id: str = None,
        page_number: int = None,
    ):
        self.total_count = total_count
        self.tasks = tasks
        self.page_size = page_size
        self.request_id = request_id
        self.page_number = page_number

    def validate(self):
        if self.tasks:
            for k in self.tasks:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        result['Tasks'] = []
        if self.tasks is not None:
            for k in self.tasks:
                result['Tasks'].append(k.to_map() if k else None)
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        self.tasks = []
        if m.get('Tasks') is not None:
            for k in m.get('Tasks'):
                temp_model = ListTasksResponseBodyTasks()
                self.tasks.append(temp_model.from_map(k))
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        return self


class ListTasksResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ListTasksResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ListTasksResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListUsersRequest(TeaModel):
    def __init__(
        self,
        cluster_id: str = None,
        page_number: int = None,
        page_size: int = None,
    ):
        self.cluster_id = cluster_id
        self.page_number = page_number
        self.page_size = page_size

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        return self


class ListUsersResponseBodyUsers(TeaModel):
    def __init__(
        self,
        name: str = None,
        add_time: str = None,
        group: str = None,
    ):
        self.name = name
        self.add_time = add_time
        self.group = group

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.name is not None:
            result['Name'] = self.name
        if self.add_time is not None:
            result['AddTime'] = self.add_time
        if self.group is not None:
            result['Group'] = self.group
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('AddTime') is not None:
            self.add_time = m.get('AddTime')
        if m.get('Group') is not None:
            self.group = m.get('Group')
        return self


class ListUsersResponseBody(TeaModel):
    def __init__(
        self,
        total_count: int = None,
        page_size: int = None,
        request_id: str = None,
        page_number: int = None,
        users: List[ListUsersResponseBodyUsers] = None,
    ):
        self.total_count = total_count
        self.page_size = page_size
        self.request_id = request_id
        self.page_number = page_number
        self.users = users

    def validate(self):
        if self.users:
            for k in self.users:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        result['Users'] = []
        if self.users is not None:
            for k in self.users:
                result['Users'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        self.users = []
        if m.get('Users') is not None:
            for k in m.get('Users'):
                temp_model = ListUsersResponseBodyUsers()
                self.users.append(temp_model.from_map(k))
        return self


class ListUsersResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ListUsersResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ListUsersResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListVolumesRequest(TeaModel):
    def __init__(
        self,
        page_number: int = None,
        page_size: int = None,
    ):
        self.page_number = page_number
        self.page_size = page_size

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        return self


class ListVolumesResponseBodyVolumesAdditionalVolumes(TeaModel):
    def __init__(
        self,
        job_queue: str = None,
        volume_id: str = None,
        remote_directory: str = None,
        volume_mountpoint: str = None,
        role: str = None,
        local_directory: str = None,
        volume_type: str = None,
        location: str = None,
        volume_protocol: str = None,
    ):
        self.job_queue = job_queue
        self.volume_id = volume_id
        self.remote_directory = remote_directory
        self.volume_mountpoint = volume_mountpoint
        self.role = role
        self.local_directory = local_directory
        self.volume_type = volume_type
        self.location = location
        self.volume_protocol = volume_protocol

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.job_queue is not None:
            result['JobQueue'] = self.job_queue
        if self.volume_id is not None:
            result['VolumeId'] = self.volume_id
        if self.remote_directory is not None:
            result['RemoteDirectory'] = self.remote_directory
        if self.volume_mountpoint is not None:
            result['VolumeMountpoint'] = self.volume_mountpoint
        if self.role is not None:
            result['Role'] = self.role
        if self.local_directory is not None:
            result['LocalDirectory'] = self.local_directory
        if self.volume_type is not None:
            result['VolumeType'] = self.volume_type
        if self.location is not None:
            result['Location'] = self.location
        if self.volume_protocol is not None:
            result['VolumeProtocol'] = self.volume_protocol
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('JobQueue') is not None:
            self.job_queue = m.get('JobQueue')
        if m.get('VolumeId') is not None:
            self.volume_id = m.get('VolumeId')
        if m.get('RemoteDirectory') is not None:
            self.remote_directory = m.get('RemoteDirectory')
        if m.get('VolumeMountpoint') is not None:
            self.volume_mountpoint = m.get('VolumeMountpoint')
        if m.get('Role') is not None:
            self.role = m.get('Role')
        if m.get('LocalDirectory') is not None:
            self.local_directory = m.get('LocalDirectory')
        if m.get('VolumeType') is not None:
            self.volume_type = m.get('VolumeType')
        if m.get('Location') is not None:
            self.location = m.get('Location')
        if m.get('VolumeProtocol') is not None:
            self.volume_protocol = m.get('VolumeProtocol')
        return self


class ListVolumesResponseBodyVolumes(TeaModel):
    def __init__(
        self,
        volume_id: str = None,
        cluster_name: str = None,
        remote_directory: str = None,
        volume_mountpoint: str = None,
        additional_volumes: List[ListVolumesResponseBodyVolumesAdditionalVolumes] = None,
        volume_type: str = None,
        volume_protocol: str = None,
        region_id: str = None,
        cluster_id: str = None,
    ):
        self.volume_id = volume_id
        self.cluster_name = cluster_name
        self.remote_directory = remote_directory
        self.volume_mountpoint = volume_mountpoint
        self.additional_volumes = additional_volumes
        self.volume_type = volume_type
        self.volume_protocol = volume_protocol
        self.region_id = region_id
        self.cluster_id = cluster_id

    def validate(self):
        if self.additional_volumes:
            for k in self.additional_volumes:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.volume_id is not None:
            result['VolumeId'] = self.volume_id
        if self.cluster_name is not None:
            result['ClusterName'] = self.cluster_name
        if self.remote_directory is not None:
            result['RemoteDirectory'] = self.remote_directory
        if self.volume_mountpoint is not None:
            result['VolumeMountpoint'] = self.volume_mountpoint
        result['AdditionalVolumes'] = []
        if self.additional_volumes is not None:
            for k in self.additional_volumes:
                result['AdditionalVolumes'].append(k.to_map() if k else None)
        if self.volume_type is not None:
            result['VolumeType'] = self.volume_type
        if self.volume_protocol is not None:
            result['VolumeProtocol'] = self.volume_protocol
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('VolumeId') is not None:
            self.volume_id = m.get('VolumeId')
        if m.get('ClusterName') is not None:
            self.cluster_name = m.get('ClusterName')
        if m.get('RemoteDirectory') is not None:
            self.remote_directory = m.get('RemoteDirectory')
        if m.get('VolumeMountpoint') is not None:
            self.volume_mountpoint = m.get('VolumeMountpoint')
        self.additional_volumes = []
        if m.get('AdditionalVolumes') is not None:
            for k in m.get('AdditionalVolumes'):
                temp_model = ListVolumesResponseBodyVolumesAdditionalVolumes()
                self.additional_volumes.append(temp_model.from_map(k))
        if m.get('VolumeType') is not None:
            self.volume_type = m.get('VolumeType')
        if m.get('VolumeProtocol') is not None:
            self.volume_protocol = m.get('VolumeProtocol')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        return self


class ListVolumesResponseBody(TeaModel):
    def __init__(
        self,
        total_count: int = None,
        volumes: List[ListVolumesResponseBodyVolumes] = None,
        page_size: int = None,
        request_id: str = None,
        page_number: int = None,
    ):
        self.total_count = total_count
        self.volumes = volumes
        self.page_size = page_size
        self.request_id = request_id
        self.page_number = page_number

    def validate(self):
        if self.volumes:
            for k in self.volumes:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        result['Volumes'] = []
        if self.volumes is not None:
            for k in self.volumes:
                result['Volumes'].append(k.to_map() if k else None)
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        self.volumes = []
        if m.get('Volumes') is not None:
            for k in m.get('Volumes'):
                temp_model = ListVolumesResponseBodyVolumes()
                self.volumes.append(temp_model.from_map(k))
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        return self


class ListVolumesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ListVolumesResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ListVolumesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ModifyClusterAttributesRequest(TeaModel):
    def __init__(
        self,
        cluster_id: str = None,
        name: str = None,
        description: str = None,
        image_owner_alias: str = None,
        image_id: str = None,
    ):
        self.cluster_id = cluster_id
        self.name = name
        self.description = description
        self.image_owner_alias = image_owner_alias
        self.image_id = image_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        if self.name is not None:
            result['Name'] = self.name
        if self.description is not None:
            result['Description'] = self.description
        if self.image_owner_alias is not None:
            result['ImageOwnerAlias'] = self.image_owner_alias
        if self.image_id is not None:
            result['ImageId'] = self.image_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('ImageOwnerAlias') is not None:
            self.image_owner_alias = m.get('ImageOwnerAlias')
        if m.get('ImageId') is not None:
            self.image_id = m.get('ImageId')
        return self


class ModifyClusterAttributesResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class ModifyClusterAttributesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ModifyClusterAttributesResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ModifyClusterAttributesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ModifyContainerAppAttributesRequest(TeaModel):
    def __init__(
        self,
        container_id: str = None,
        description: str = None,
    ):
        self.container_id = container_id
        self.description = description

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.container_id is not None:
            result['ContainerId'] = self.container_id
        if self.description is not None:
            result['Description'] = self.description
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ContainerId') is not None:
            self.container_id = m.get('ContainerId')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        return self


class ModifyContainerAppAttributesResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class ModifyContainerAppAttributesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ModifyContainerAppAttributesResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ModifyContainerAppAttributesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ModifyImageGatewayConfigRequestRepo(TeaModel):
    def __init__(
        self,
        auth: str = None,
        url: str = None,
        location: str = None,
    ):
        self.auth = auth
        self.url = url
        self.location = location

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.auth is not None:
            result['Auth'] = self.auth
        if self.url is not None:
            result['URL'] = self.url
        if self.location is not None:
            result['Location'] = self.location
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Auth') is not None:
            self.auth = m.get('Auth')
        if m.get('URL') is not None:
            self.url = m.get('URL')
        if m.get('Location') is not None:
            self.location = m.get('Location')
        return self


class ModifyImageGatewayConfigRequest(TeaModel):
    def __init__(
        self,
        cluster_id: str = None,
        dbtype: str = None,
        dbusername: str = None,
        dbpassword: str = None,
        dbserver_info: str = None,
        default_repo_location: str = None,
        pull_update_timeout: int = None,
        image_expiration_timeout: str = None,
        repo: List[ModifyImageGatewayConfigRequestRepo] = None,
    ):
        self.cluster_id = cluster_id
        self.dbtype = dbtype
        self.dbusername = dbusername
        self.dbpassword = dbpassword
        self.dbserver_info = dbserver_info
        self.default_repo_location = default_repo_location
        self.pull_update_timeout = pull_update_timeout
        self.image_expiration_timeout = image_expiration_timeout
        self.repo = repo

    def validate(self):
        if self.repo:
            for k in self.repo:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        if self.dbtype is not None:
            result['DBType'] = self.dbtype
        if self.dbusername is not None:
            result['DBUsername'] = self.dbusername
        if self.dbpassword is not None:
            result['DBPassword'] = self.dbpassword
        if self.dbserver_info is not None:
            result['DBServerInfo'] = self.dbserver_info
        if self.default_repo_location is not None:
            result['DefaultRepoLocation'] = self.default_repo_location
        if self.pull_update_timeout is not None:
            result['PullUpdateTimeout'] = self.pull_update_timeout
        if self.image_expiration_timeout is not None:
            result['ImageExpirationTimeout'] = self.image_expiration_timeout
        result['Repo'] = []
        if self.repo is not None:
            for k in self.repo:
                result['Repo'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        if m.get('DBType') is not None:
            self.dbtype = m.get('DBType')
        if m.get('DBUsername') is not None:
            self.dbusername = m.get('DBUsername')
        if m.get('DBPassword') is not None:
            self.dbpassword = m.get('DBPassword')
        if m.get('DBServerInfo') is not None:
            self.dbserver_info = m.get('DBServerInfo')
        if m.get('DefaultRepoLocation') is not None:
            self.default_repo_location = m.get('DefaultRepoLocation')
        if m.get('PullUpdateTimeout') is not None:
            self.pull_update_timeout = m.get('PullUpdateTimeout')
        if m.get('ImageExpirationTimeout') is not None:
            self.image_expiration_timeout = m.get('ImageExpirationTimeout')
        self.repo = []
        if m.get('Repo') is not None:
            for k in m.get('Repo'):
                temp_model = ModifyImageGatewayConfigRequestRepo()
                self.repo.append(temp_model.from_map(k))
        return self


class ModifyImageGatewayConfigResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class ModifyImageGatewayConfigResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ModifyImageGatewayConfigResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ModifyImageGatewayConfigResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ModifyUserGroupsRequestUser(TeaModel):
    def __init__(
        self,
        name: str = None,
        group: str = None,
    ):
        self.name = name
        self.group = group

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.name is not None:
            result['Name'] = self.name
        if self.group is not None:
            result['Group'] = self.group
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Group') is not None:
            self.group = m.get('Group')
        return self


class ModifyUserGroupsRequest(TeaModel):
    def __init__(
        self,
        cluster_id: str = None,
        user: List[ModifyUserGroupsRequestUser] = None,
    ):
        self.cluster_id = cluster_id
        self.user = user

    def validate(self):
        if self.user:
            for k in self.user:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        result['User'] = []
        if self.user is not None:
            for k in self.user:
                result['User'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        self.user = []
        if m.get('User') is not None:
            for k in m.get('User'):
                temp_model = ModifyUserGroupsRequestUser()
                self.user.append(temp_model.from_map(k))
        return self


class ModifyUserGroupsResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class ModifyUserGroupsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ModifyUserGroupsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ModifyUserGroupsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ModifyUserPasswordsRequestUser(TeaModel):
    def __init__(
        self,
        password: str = None,
        name: str = None,
    ):
        self.password = password
        self.name = name

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.password is not None:
            result['Password'] = self.password
        if self.name is not None:
            result['Name'] = self.name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Password') is not None:
            self.password = m.get('Password')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        return self


class ModifyUserPasswordsRequest(TeaModel):
    def __init__(
        self,
        cluster_id: str = None,
        user: List[ModifyUserPasswordsRequestUser] = None,
    ):
        self.cluster_id = cluster_id
        self.user = user

    def validate(self):
        if self.user:
            for k in self.user:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        result['User'] = []
        if self.user is not None:
            for k in self.user:
                result['User'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        self.user = []
        if m.get('User') is not None:
            for k in m.get('User'):
                temp_model = ModifyUserPasswordsRequestUser()
                self.user.append(temp_model.from_map(k))
        return self


class ModifyUserPasswordsResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class ModifyUserPasswordsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ModifyUserPasswordsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ModifyUserPasswordsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ModifyVisualServicePasswdRequest(TeaModel):
    def __init__(
        self,
        cluster_id: str = None,
        runas_user: str = None,
        runas_user_password: str = None,
        passwd: str = None,
    ):
        self.cluster_id = cluster_id
        self.runas_user = runas_user
        self.runas_user_password = runas_user_password
        self.passwd = passwd

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        if self.runas_user is not None:
            result['RunasUser'] = self.runas_user
        if self.runas_user_password is not None:
            result['RunasUserPassword'] = self.runas_user_password
        if self.passwd is not None:
            result['Passwd'] = self.passwd
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        if m.get('RunasUser') is not None:
            self.runas_user = m.get('RunasUser')
        if m.get('RunasUserPassword') is not None:
            self.runas_user_password = m.get('RunasUserPassword')
        if m.get('Passwd') is not None:
            self.passwd = m.get('Passwd')
        return self


class ModifyVisualServicePasswdResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
    ):
        self.message = message
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class ModifyVisualServicePasswdResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ModifyVisualServicePasswdResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ModifyVisualServicePasswdResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class MountNFSRequest(TeaModel):
    def __init__(
        self,
        instance_id: str = None,
        nfs_dir: str = None,
        mount_dir: str = None,
        protocol_type: str = None,
        remote_dir: str = None,
    ):
        self.instance_id = instance_id
        self.nfs_dir = nfs_dir
        self.mount_dir = mount_dir
        self.protocol_type = protocol_type
        self.remote_dir = remote_dir

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.nfs_dir is not None:
            result['NfsDir'] = self.nfs_dir
        if self.mount_dir is not None:
            result['MountDir'] = self.mount_dir
        if self.protocol_type is not None:
            result['ProtocolType'] = self.protocol_type
        if self.remote_dir is not None:
            result['RemoteDir'] = self.remote_dir
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('NfsDir') is not None:
            self.nfs_dir = m.get('NfsDir')
        if m.get('MountDir') is not None:
            self.mount_dir = m.get('MountDir')
        if m.get('ProtocolType') is not None:
            self.protocol_type = m.get('ProtocolType')
        if m.get('RemoteDir') is not None:
            self.remote_dir = m.get('RemoteDir')
        return self


class MountNFSResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        invoke_id: str = None,
    ):
        self.request_id = request_id
        self.invoke_id = invoke_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.invoke_id is not None:
            result['InvokeId'] = self.invoke_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('InvokeId') is not None:
            self.invoke_id = m.get('InvokeId')
        return self


class MountNFSResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: MountNFSResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = MountNFSResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class PullImageRequest(TeaModel):
    def __init__(
        self,
        cluster_id: str = None,
        repository: str = None,
        image_tag: str = None,
        container_type: str = None,
    ):
        self.cluster_id = cluster_id
        self.repository = repository
        self.image_tag = image_tag
        self.container_type = container_type

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        if self.repository is not None:
            result['Repository'] = self.repository
        if self.image_tag is not None:
            result['ImageTag'] = self.image_tag
        if self.container_type is not None:
            result['ContainerType'] = self.container_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        if m.get('Repository') is not None:
            self.repository = m.get('Repository')
        if m.get('ImageTag') is not None:
            self.image_tag = m.get('ImageTag')
        if m.get('ContainerType') is not None:
            self.container_type = m.get('ContainerType')
        return self


class PullImageResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class PullImageResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: PullImageResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = PullImageResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class QueryServicePackAndPriceResponseBodyServicePack(TeaModel):
    def __init__(
        self,
        end_time: int = None,
        capacity: int = None,
        start_time: int = None,
        instance_name: str = None,
    ):
        self.end_time = end_time
        self.capacity = capacity
        self.start_time = start_time
        self.instance_name = instance_name

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.end_time is not None:
            result['EndTime'] = self.end_time
        if self.capacity is not None:
            result['Capacity'] = self.capacity
        if self.start_time is not None:
            result['StartTime'] = self.start_time
        if self.instance_name is not None:
            result['InstanceName'] = self.instance_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('EndTime') is not None:
            self.end_time = m.get('EndTime')
        if m.get('Capacity') is not None:
            self.capacity = m.get('Capacity')
        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')
        if m.get('InstanceName') is not None:
            self.instance_name = m.get('InstanceName')
        return self


class QueryServicePackAndPriceResponseBody(TeaModel):
    def __init__(
        self,
        original_price: float = None,
        request_id: str = None,
        discount_price: float = None,
        currency: str = None,
        service_pack: List[QueryServicePackAndPriceResponseBodyServicePack] = None,
        region_id: str = None,
        trade_price: float = None,
        original_amount: int = None,
        charge_amount: int = None,
    ):
        self.original_price = original_price
        self.request_id = request_id
        self.discount_price = discount_price
        self.currency = currency
        self.service_pack = service_pack
        self.region_id = region_id
        self.trade_price = trade_price
        self.original_amount = original_amount
        self.charge_amount = charge_amount

    def validate(self):
        if self.service_pack:
            for k in self.service_pack:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.original_price is not None:
            result['OriginalPrice'] = self.original_price
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.discount_price is not None:
            result['DiscountPrice'] = self.discount_price
        if self.currency is not None:
            result['Currency'] = self.currency
        result['ServicePack'] = []
        if self.service_pack is not None:
            for k in self.service_pack:
                result['ServicePack'].append(k.to_map() if k else None)
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.trade_price is not None:
            result['TradePrice'] = self.trade_price
        if self.original_amount is not None:
            result['OriginalAmount'] = self.original_amount
        if self.charge_amount is not None:
            result['ChargeAmount'] = self.charge_amount
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('OriginalPrice') is not None:
            self.original_price = m.get('OriginalPrice')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('DiscountPrice') is not None:
            self.discount_price = m.get('DiscountPrice')
        if m.get('Currency') is not None:
            self.currency = m.get('Currency')
        self.service_pack = []
        if m.get('ServicePack') is not None:
            for k in m.get('ServicePack'):
                temp_model = QueryServicePackAndPriceResponseBodyServicePack()
                self.service_pack.append(temp_model.from_map(k))
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('TradePrice') is not None:
            self.trade_price = m.get('TradePrice')
        if m.get('OriginalAmount') is not None:
            self.original_amount = m.get('OriginalAmount')
        if m.get('ChargeAmount') is not None:
            self.charge_amount = m.get('ChargeAmount')
        return self


class QueryServicePackAndPriceResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: QueryServicePackAndPriceResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = QueryServicePackAndPriceResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class RecoverClusterRequest(TeaModel):
    def __init__(
        self,
        cluster_id: str = None,
        os_tag: str = None,
        account_type: str = None,
        scheduler_type: str = None,
        image_owner_alias: str = None,
        image_id: str = None,
        client_version: str = None,
    ):
        self.cluster_id = cluster_id
        self.os_tag = os_tag
        self.account_type = account_type
        self.scheduler_type = scheduler_type
        self.image_owner_alias = image_owner_alias
        self.image_id = image_id
        self.client_version = client_version

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        if self.os_tag is not None:
            result['OsTag'] = self.os_tag
        if self.account_type is not None:
            result['AccountType'] = self.account_type
        if self.scheduler_type is not None:
            result['SchedulerType'] = self.scheduler_type
        if self.image_owner_alias is not None:
            result['ImageOwnerAlias'] = self.image_owner_alias
        if self.image_id is not None:
            result['ImageId'] = self.image_id
        if self.client_version is not None:
            result['ClientVersion'] = self.client_version
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        if m.get('OsTag') is not None:
            self.os_tag = m.get('OsTag')
        if m.get('AccountType') is not None:
            self.account_type = m.get('AccountType')
        if m.get('SchedulerType') is not None:
            self.scheduler_type = m.get('SchedulerType')
        if m.get('ImageOwnerAlias') is not None:
            self.image_owner_alias = m.get('ImageOwnerAlias')
        if m.get('ImageId') is not None:
            self.image_id = m.get('ImageId')
        if m.get('ClientVersion') is not None:
            self.client_version = m.get('ClientVersion')
        return self


class RecoverClusterResponseBody(TeaModel):
    def __init__(
        self,
        task_id: str = None,
        request_id: str = None,
    ):
        self.task_id = task_id
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.task_id is not None:
            result['TaskId'] = self.task_id
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TaskId') is not None:
            self.task_id = m.get('TaskId')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class RecoverClusterResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: RecoverClusterResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = RecoverClusterResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class RerunJobsRequest(TeaModel):
    def __init__(
        self,
        cluster_id: str = None,
        jobs: str = None,
    ):
        self.cluster_id = cluster_id
        self.jobs = jobs

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        if self.jobs is not None:
            result['Jobs'] = self.jobs
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        if m.get('Jobs') is not None:
            self.jobs = m.get('Jobs')
        return self


class RerunJobsResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class RerunJobsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: RerunJobsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = RerunJobsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ResetNodesRequestInstance(TeaModel):
    def __init__(
        self,
        id: str = None,
    ):
        self.id = id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.id is not None:
            result['Id'] = self.id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Id') is not None:
            self.id = m.get('Id')
        return self


class ResetNodesRequest(TeaModel):
    def __init__(
        self,
        cluster_id: str = None,
        instance: List[ResetNodesRequestInstance] = None,
    ):
        self.cluster_id = cluster_id
        self.instance = instance

    def validate(self):
        if self.instance:
            for k in self.instance:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        result['Instance'] = []
        if self.instance is not None:
            for k in self.instance:
                result['Instance'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        self.instance = []
        if m.get('Instance') is not None:
            for k in m.get('Instance'):
                temp_model = ResetNodesRequestInstance()
                self.instance.append(temp_model.from_map(k))
        return self


class ResetNodesResponseBody(TeaModel):
    def __init__(
        self,
        task_id: str = None,
        request_id: str = None,
    ):
        self.task_id = task_id
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.task_id is not None:
            result['TaskId'] = self.task_id
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TaskId') is not None:
            self.task_id = m.get('TaskId')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class ResetNodesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ResetNodesResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ResetNodesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class RunCloudMetricProfilingRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        cluster_id: str = None,
        host_name: str = None,
        process_id: int = None,
        duration: int = None,
        freq: int = None,
    ):
        self.region_id = region_id
        self.cluster_id = cluster_id
        self.host_name = host_name
        self.process_id = process_id
        self.duration = duration
        self.freq = freq

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        if self.host_name is not None:
            result['HostName'] = self.host_name
        if self.process_id is not None:
            result['ProcessId'] = self.process_id
        if self.duration is not None:
            result['Duration'] = self.duration
        if self.freq is not None:
            result['Freq'] = self.freq
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        if m.get('HostName') is not None:
            self.host_name = m.get('HostName')
        if m.get('ProcessId') is not None:
            self.process_id = m.get('ProcessId')
        if m.get('Duration') is not None:
            self.duration = m.get('Duration')
        if m.get('Freq') is not None:
            self.freq = m.get('Freq')
        return self


class RunCloudMetricProfilingResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class RunCloudMetricProfilingResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: RunCloudMetricProfilingResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = RunCloudMetricProfilingResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class SetAutoScaleConfigRequestQueuesInstanceTypes(TeaModel):
    def __init__(
        self,
        host_name_prefix: str = None,
        v_switch_id: str = None,
        zone_id: str = None,
        spot_price_limit: float = None,
        instance_type: str = None,
        spot_strategy: str = None,
    ):
        self.host_name_prefix = host_name_prefix
        self.v_switch_id = v_switch_id
        self.zone_id = zone_id
        self.spot_price_limit = spot_price_limit
        self.instance_type = instance_type
        self.spot_strategy = spot_strategy

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.host_name_prefix is not None:
            result['HostNamePrefix'] = self.host_name_prefix
        if self.v_switch_id is not None:
            result['VSwitchId'] = self.v_switch_id
        if self.zone_id is not None:
            result['ZoneId'] = self.zone_id
        if self.spot_price_limit is not None:
            result['SpotPriceLimit'] = self.spot_price_limit
        if self.instance_type is not None:
            result['InstanceType'] = self.instance_type
        if self.spot_strategy is not None:
            result['SpotStrategy'] = self.spot_strategy
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('HostNamePrefix') is not None:
            self.host_name_prefix = m.get('HostNamePrefix')
        if m.get('VSwitchId') is not None:
            self.v_switch_id = m.get('VSwitchId')
        if m.get('ZoneId') is not None:
            self.zone_id = m.get('ZoneId')
        if m.get('SpotPriceLimit') is not None:
            self.spot_price_limit = m.get('SpotPriceLimit')
        if m.get('InstanceType') is not None:
            self.instance_type = m.get('InstanceType')
        if m.get('SpotStrategy') is not None:
            self.spot_strategy = m.get('SpotStrategy')
        return self


class SetAutoScaleConfigRequestQueues(TeaModel):
    def __init__(
        self,
        min_nodes_in_queue: int = None,
        max_nodes_in_queue: int = None,
        enable_auto_shrink: bool = None,
        queue_name: str = None,
        enable_auto_grow: bool = None,
        queue_image_id: str = None,
        spot_price_limit: float = None,
        instance_types: List[SetAutoScaleConfigRequestQueuesInstanceTypes] = None,
        instance_type: str = None,
        spot_strategy: str = None,
    ):
        self.min_nodes_in_queue = min_nodes_in_queue
        self.max_nodes_in_queue = max_nodes_in_queue
        self.enable_auto_shrink = enable_auto_shrink
        self.queue_name = queue_name
        self.enable_auto_grow = enable_auto_grow
        self.queue_image_id = queue_image_id
        self.spot_price_limit = spot_price_limit
        self.instance_types = instance_types
        self.instance_type = instance_type
        self.spot_strategy = spot_strategy

    def validate(self):
        if self.instance_types:
            for k in self.instance_types:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.min_nodes_in_queue is not None:
            result['MinNodesInQueue'] = self.min_nodes_in_queue
        if self.max_nodes_in_queue is not None:
            result['MaxNodesInQueue'] = self.max_nodes_in_queue
        if self.enable_auto_shrink is not None:
            result['EnableAutoShrink'] = self.enable_auto_shrink
        if self.queue_name is not None:
            result['QueueName'] = self.queue_name
        if self.enable_auto_grow is not None:
            result['EnableAutoGrow'] = self.enable_auto_grow
        if self.queue_image_id is not None:
            result['QueueImageId'] = self.queue_image_id
        if self.spot_price_limit is not None:
            result['SpotPriceLimit'] = self.spot_price_limit
        result['InstanceTypes'] = []
        if self.instance_types is not None:
            for k in self.instance_types:
                result['InstanceTypes'].append(k.to_map() if k else None)
        if self.instance_type is not None:
            result['InstanceType'] = self.instance_type
        if self.spot_strategy is not None:
            result['SpotStrategy'] = self.spot_strategy
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('MinNodesInQueue') is not None:
            self.min_nodes_in_queue = m.get('MinNodesInQueue')
        if m.get('MaxNodesInQueue') is not None:
            self.max_nodes_in_queue = m.get('MaxNodesInQueue')
        if m.get('EnableAutoShrink') is not None:
            self.enable_auto_shrink = m.get('EnableAutoShrink')
        if m.get('QueueName') is not None:
            self.queue_name = m.get('QueueName')
        if m.get('EnableAutoGrow') is not None:
            self.enable_auto_grow = m.get('EnableAutoGrow')
        if m.get('QueueImageId') is not None:
            self.queue_image_id = m.get('QueueImageId')
        if m.get('SpotPriceLimit') is not None:
            self.spot_price_limit = m.get('SpotPriceLimit')
        self.instance_types = []
        if m.get('InstanceTypes') is not None:
            for k in m.get('InstanceTypes'):
                temp_model = SetAutoScaleConfigRequestQueuesInstanceTypes()
                self.instance_types.append(temp_model.from_map(k))
        if m.get('InstanceType') is not None:
            self.instance_type = m.get('InstanceType')
        if m.get('SpotStrategy') is not None:
            self.spot_strategy = m.get('SpotStrategy')
        return self


class SetAutoScaleConfigRequest(TeaModel):
    def __init__(
        self,
        cluster_id: str = None,
        enable_auto_grow: bool = None,
        enable_auto_shrink: bool = None,
        grow_interval_in_minutes: int = None,
        shrink_interval_in_minutes: int = None,
        shrink_idle_times: int = None,
        grow_timeout_in_minutes: int = None,
        extra_nodes_grow_ratio: int = None,
        grow_ratio: int = None,
        max_nodes_in_cluster: int = None,
        exclude_nodes: str = None,
        spot_strategy: str = None,
        spot_price_limit: float = None,
        image_id: str = None,
        queues: List[SetAutoScaleConfigRequestQueues] = None,
    ):
        self.cluster_id = cluster_id
        self.enable_auto_grow = enable_auto_grow
        self.enable_auto_shrink = enable_auto_shrink
        self.grow_interval_in_minutes = grow_interval_in_minutes
        self.shrink_interval_in_minutes = shrink_interval_in_minutes
        self.shrink_idle_times = shrink_idle_times
        self.grow_timeout_in_minutes = grow_timeout_in_minutes
        self.extra_nodes_grow_ratio = extra_nodes_grow_ratio
        self.grow_ratio = grow_ratio
        self.max_nodes_in_cluster = max_nodes_in_cluster
        self.exclude_nodes = exclude_nodes
        self.spot_strategy = spot_strategy
        self.spot_price_limit = spot_price_limit
        self.image_id = image_id
        self.queues = queues

    def validate(self):
        if self.queues:
            for k in self.queues:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        if self.enable_auto_grow is not None:
            result['EnableAutoGrow'] = self.enable_auto_grow
        if self.enable_auto_shrink is not None:
            result['EnableAutoShrink'] = self.enable_auto_shrink
        if self.grow_interval_in_minutes is not None:
            result['GrowIntervalInMinutes'] = self.grow_interval_in_minutes
        if self.shrink_interval_in_minutes is not None:
            result['ShrinkIntervalInMinutes'] = self.shrink_interval_in_minutes
        if self.shrink_idle_times is not None:
            result['ShrinkIdleTimes'] = self.shrink_idle_times
        if self.grow_timeout_in_minutes is not None:
            result['GrowTimeoutInMinutes'] = self.grow_timeout_in_minutes
        if self.extra_nodes_grow_ratio is not None:
            result['ExtraNodesGrowRatio'] = self.extra_nodes_grow_ratio
        if self.grow_ratio is not None:
            result['GrowRatio'] = self.grow_ratio
        if self.max_nodes_in_cluster is not None:
            result['MaxNodesInCluster'] = self.max_nodes_in_cluster
        if self.exclude_nodes is not None:
            result['ExcludeNodes'] = self.exclude_nodes
        if self.spot_strategy is not None:
            result['SpotStrategy'] = self.spot_strategy
        if self.spot_price_limit is not None:
            result['SpotPriceLimit'] = self.spot_price_limit
        if self.image_id is not None:
            result['ImageId'] = self.image_id
        result['Queues'] = []
        if self.queues is not None:
            for k in self.queues:
                result['Queues'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        if m.get('EnableAutoGrow') is not None:
            self.enable_auto_grow = m.get('EnableAutoGrow')
        if m.get('EnableAutoShrink') is not None:
            self.enable_auto_shrink = m.get('EnableAutoShrink')
        if m.get('GrowIntervalInMinutes') is not None:
            self.grow_interval_in_minutes = m.get('GrowIntervalInMinutes')
        if m.get('ShrinkIntervalInMinutes') is not None:
            self.shrink_interval_in_minutes = m.get('ShrinkIntervalInMinutes')
        if m.get('ShrinkIdleTimes') is not None:
            self.shrink_idle_times = m.get('ShrinkIdleTimes')
        if m.get('GrowTimeoutInMinutes') is not None:
            self.grow_timeout_in_minutes = m.get('GrowTimeoutInMinutes')
        if m.get('ExtraNodesGrowRatio') is not None:
            self.extra_nodes_grow_ratio = m.get('ExtraNodesGrowRatio')
        if m.get('GrowRatio') is not None:
            self.grow_ratio = m.get('GrowRatio')
        if m.get('MaxNodesInCluster') is not None:
            self.max_nodes_in_cluster = m.get('MaxNodesInCluster')
        if m.get('ExcludeNodes') is not None:
            self.exclude_nodes = m.get('ExcludeNodes')
        if m.get('SpotStrategy') is not None:
            self.spot_strategy = m.get('SpotStrategy')
        if m.get('SpotPriceLimit') is not None:
            self.spot_price_limit = m.get('SpotPriceLimit')
        if m.get('ImageId') is not None:
            self.image_id = m.get('ImageId')
        self.queues = []
        if m.get('Queues') is not None:
            for k in m.get('Queues'):
                temp_model = SetAutoScaleConfigRequestQueues()
                self.queues.append(temp_model.from_map(k))
        return self


class SetAutoScaleConfigResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class SetAutoScaleConfigResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: SetAutoScaleConfigResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = SetAutoScaleConfigResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class SetGWSClusterPolicyRequest(TeaModel):
    def __init__(
        self,
        cluster_id: str = None,
        clipboard: str = None,
        local_drive: str = None,
        usb_redirect: str = None,
        watermark: str = None,
        udp_port: str = None,
        async_mode: bool = None,
    ):
        self.cluster_id = cluster_id
        self.clipboard = clipboard
        self.local_drive = local_drive
        self.usb_redirect = usb_redirect
        self.watermark = watermark
        self.udp_port = udp_port
        self.async_mode = async_mode

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        if self.clipboard is not None:
            result['Clipboard'] = self.clipboard
        if self.local_drive is not None:
            result['LocalDrive'] = self.local_drive
        if self.usb_redirect is not None:
            result['UsbRedirect'] = self.usb_redirect
        if self.watermark is not None:
            result['Watermark'] = self.watermark
        if self.udp_port is not None:
            result['UdpPort'] = self.udp_port
        if self.async_mode is not None:
            result['AsyncMode'] = self.async_mode
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        if m.get('Clipboard') is not None:
            self.clipboard = m.get('Clipboard')
        if m.get('LocalDrive') is not None:
            self.local_drive = m.get('LocalDrive')
        if m.get('UsbRedirect') is not None:
            self.usb_redirect = m.get('UsbRedirect')
        if m.get('Watermark') is not None:
            self.watermark = m.get('Watermark')
        if m.get('UdpPort') is not None:
            self.udp_port = m.get('UdpPort')
        if m.get('AsyncMode') is not None:
            self.async_mode = m.get('AsyncMode')
        return self


class SetGWSClusterPolicyResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class SetGWSClusterPolicyResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: SetGWSClusterPolicyResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = SetGWSClusterPolicyResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class SetGWSInstanceNameRequest(TeaModel):
    def __init__(
        self,
        instance_id: str = None,
        name: str = None,
    ):
        self.instance_id = instance_id
        self.name = name

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.name is not None:
            result['Name'] = self.name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        return self


class SetGWSInstanceNameResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class SetGWSInstanceNameResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: SetGWSInstanceNameResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = SetGWSInstanceNameResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class SetGWSInstanceUserRequest(TeaModel):
    def __init__(
        self,
        instance_id: str = None,
        user_uid: str = None,
        user_name: str = None,
    ):
        self.instance_id = instance_id
        self.user_uid = user_uid
        self.user_name = user_name

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.user_uid is not None:
            result['UserUid'] = self.user_uid
        if self.user_name is not None:
            result['UserName'] = self.user_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('UserUid') is not None:
            self.user_uid = m.get('UserUid')
        if m.get('UserName') is not None:
            self.user_name = m.get('UserName')
        return self


class SetGWSInstanceUserResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class SetGWSInstanceUserResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: SetGWSInstanceUserResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = SetGWSInstanceUserResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class SetJobUserRequest(TeaModel):
    def __init__(
        self,
        cluster_id: str = None,
        runas_user: str = None,
        runas_user_password: str = None,
    ):
        self.cluster_id = cluster_id
        self.runas_user = runas_user
        self.runas_user_password = runas_user_password

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        if self.runas_user is not None:
            result['RunasUser'] = self.runas_user
        if self.runas_user_password is not None:
            result['RunasUserPassword'] = self.runas_user_password
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        if m.get('RunasUser') is not None:
            self.runas_user = m.get('RunasUser')
        if m.get('RunasUserPassword') is not None:
            self.runas_user_password = m.get('RunasUserPassword')
        return self


class SetJobUserResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class SetJobUserResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: SetJobUserResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = SetJobUserResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class SetQueueRequestNode(TeaModel):
    def __init__(
        self,
        name: str = None,
    ):
        self.name = name

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.name is not None:
            result['Name'] = self.name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Name') is not None:
            self.name = m.get('Name')
        return self


class SetQueueRequest(TeaModel):
    def __init__(
        self,
        cluster_id: str = None,
        queue_name: str = None,
        node: List[SetQueueRequestNode] = None,
    ):
        self.cluster_id = cluster_id
        self.queue_name = queue_name
        self.node = node

    def validate(self):
        if self.node:
            for k in self.node:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        if self.queue_name is not None:
            result['QueueName'] = self.queue_name
        result['Node'] = []
        if self.node is not None:
            for k in self.node:
                result['Node'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        if m.get('QueueName') is not None:
            self.queue_name = m.get('QueueName')
        self.node = []
        if m.get('Node') is not None:
            for k in m.get('Node'):
                temp_model = SetQueueRequestNode()
                self.node.append(temp_model.from_map(k))
        return self


class SetQueueResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class SetQueueResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: SetQueueResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = SetQueueResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class StartClusterRequest(TeaModel):
    def __init__(
        self,
        cluster_id: str = None,
    ):
        self.cluster_id = cluster_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        return self


class StartClusterResponseBody(TeaModel):
    def __init__(
        self,
        task_id: str = None,
        request_id: str = None,
    ):
        self.task_id = task_id
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.task_id is not None:
            result['TaskId'] = self.task_id
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TaskId') is not None:
            self.task_id = m.get('TaskId')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class StartClusterResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: StartClusterResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = StartClusterResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class StartGWSInstanceRequest(TeaModel):
    def __init__(
        self,
        instance_id: str = None,
    ):
        self.instance_id = instance_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        return self


class StartGWSInstanceResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class StartGWSInstanceResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: StartGWSInstanceResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = StartGWSInstanceResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class StartNodesRequestInstance(TeaModel):
    def __init__(
        self,
        id: str = None,
    ):
        self.id = id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.id is not None:
            result['Id'] = self.id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Id') is not None:
            self.id = m.get('Id')
        return self


class StartNodesRequest(TeaModel):
    def __init__(
        self,
        cluster_id: str = None,
        role: str = None,
        instance: List[StartNodesRequestInstance] = None,
    ):
        self.cluster_id = cluster_id
        self.role = role
        self.instance = instance

    def validate(self):
        if self.instance:
            for k in self.instance:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        if self.role is not None:
            result['Role'] = self.role
        result['Instance'] = []
        if self.instance is not None:
            for k in self.instance:
                result['Instance'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        if m.get('Role') is not None:
            self.role = m.get('Role')
        self.instance = []
        if m.get('Instance') is not None:
            for k in m.get('Instance'):
                temp_model = StartNodesRequestInstance()
                self.instance.append(temp_model.from_map(k))
        return self


class StartNodesResponseBody(TeaModel):
    def __init__(
        self,
        task_id: str = None,
        request_id: str = None,
    ):
        self.task_id = task_id
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.task_id is not None:
            result['TaskId'] = self.task_id
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TaskId') is not None:
            self.task_id = m.get('TaskId')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class StartNodesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: StartNodesResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = StartNodesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class StartVisualServiceRequest(TeaModel):
    def __init__(
        self,
        cluster_id: str = None,
        cidr_ip: str = None,
        port: int = None,
    ):
        self.cluster_id = cluster_id
        self.cidr_ip = cidr_ip
        self.port = port

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        if self.cidr_ip is not None:
            result['CidrIp'] = self.cidr_ip
        if self.port is not None:
            result['Port'] = self.port
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        if m.get('CidrIp') is not None:
            self.cidr_ip = m.get('CidrIp')
        if m.get('Port') is not None:
            self.port = m.get('Port')
        return self


class StartVisualServiceResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
    ):
        self.message = message
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class StartVisualServiceResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: StartVisualServiceResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = StartVisualServiceResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class StopClusterRequest(TeaModel):
    def __init__(
        self,
        cluster_id: str = None,
    ):
        self.cluster_id = cluster_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        return self


class StopClusterResponseBody(TeaModel):
    def __init__(
        self,
        task_id: str = None,
        request_id: str = None,
    ):
        self.task_id = task_id
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.task_id is not None:
            result['TaskId'] = self.task_id
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TaskId') is not None:
            self.task_id = m.get('TaskId')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class StopClusterResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: StopClusterResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = StopClusterResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class StopGWSInstanceRequest(TeaModel):
    def __init__(
        self,
        instance_id: str = None,
    ):
        self.instance_id = instance_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        return self


class StopGWSInstanceResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class StopGWSInstanceResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: StopGWSInstanceResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = StopGWSInstanceResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class StopJobsRequest(TeaModel):
    def __init__(
        self,
        cluster_id: str = None,
        jobs: str = None,
    ):
        self.cluster_id = cluster_id
        self.jobs = jobs

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        if self.jobs is not None:
            result['Jobs'] = self.jobs
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        if m.get('Jobs') is not None:
            self.jobs = m.get('Jobs')
        return self


class StopJobsResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class StopJobsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: StopJobsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = StopJobsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class StopNodesRequestInstance(TeaModel):
    def __init__(
        self,
        id: str = None,
    ):
        self.id = id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.id is not None:
            result['Id'] = self.id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Id') is not None:
            self.id = m.get('Id')
        return self


class StopNodesRequest(TeaModel):
    def __init__(
        self,
        cluster_id: str = None,
        role: str = None,
        instance: List[StopNodesRequestInstance] = None,
    ):
        self.cluster_id = cluster_id
        self.role = role
        self.instance = instance

    def validate(self):
        if self.instance:
            for k in self.instance:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        if self.role is not None:
            result['Role'] = self.role
        result['Instance'] = []
        if self.instance is not None:
            for k in self.instance:
                result['Instance'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        if m.get('Role') is not None:
            self.role = m.get('Role')
        self.instance = []
        if m.get('Instance') is not None:
            for k in m.get('Instance'):
                temp_model = StopNodesRequestInstance()
                self.instance.append(temp_model.from_map(k))
        return self


class StopNodesResponseBody(TeaModel):
    def __init__(
        self,
        task_id: str = None,
        request_id: str = None,
    ):
        self.task_id = task_id
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.task_id is not None:
            result['TaskId'] = self.task_id
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TaskId') is not None:
            self.task_id = m.get('TaskId')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class StopNodesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: StopNodesResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = StopNodesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class StopVisualServiceRequest(TeaModel):
    def __init__(
        self,
        cluster_id: str = None,
        cidr_ip: str = None,
        port: int = None,
    ):
        self.cluster_id = cluster_id
        self.cidr_ip = cidr_ip
        self.port = port

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        if self.cidr_ip is not None:
            result['CidrIp'] = self.cidr_ip
        if self.port is not None:
            result['Port'] = self.port
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        if m.get('CidrIp') is not None:
            self.cidr_ip = m.get('CidrIp')
        if m.get('Port') is not None:
            self.port = m.get('Port')
        return self


class StopVisualServiceResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
    ):
        self.message = message
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class StopVisualServiceResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: StopVisualServiceResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = StopVisualServiceResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class SubmitJobRequest(TeaModel):
    def __init__(
        self,
        cluster_id: str = None,
        command_line: str = None,
        runas_user: str = None,
        runas_user_password: str = None,
        name: str = None,
        priority: int = None,
        package_path: str = None,
        stdout_redirect_path: str = None,
        stderr_redirect_path: str = None,
        re_runable: bool = None,
        array_request: str = None,
        variables: str = None,
        input_file_url: str = None,
        unzip_cmd: str = None,
        post_cmd_line: str = None,
        container_id: str = None,
        job_queue: str = None,
        node: int = None,
        task: int = None,
        thread: int = None,
        mem: str = None,
        gpu: int = None,
        clock_time: str = None,
    ):
        self.cluster_id = cluster_id
        self.command_line = command_line
        self.runas_user = runas_user
        self.runas_user_password = runas_user_password
        self.name = name
        self.priority = priority
        self.package_path = package_path
        self.stdout_redirect_path = stdout_redirect_path
        self.stderr_redirect_path = stderr_redirect_path
        self.re_runable = re_runable
        self.array_request = array_request
        self.variables = variables
        self.input_file_url = input_file_url
        self.unzip_cmd = unzip_cmd
        self.post_cmd_line = post_cmd_line
        self.container_id = container_id
        self.job_queue = job_queue
        self.node = node
        self.task = task
        self.thread = thread
        self.mem = mem
        self.gpu = gpu
        self.clock_time = clock_time

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        if self.command_line is not None:
            result['CommandLine'] = self.command_line
        if self.runas_user is not None:
            result['RunasUser'] = self.runas_user
        if self.runas_user_password is not None:
            result['RunasUserPassword'] = self.runas_user_password
        if self.name is not None:
            result['Name'] = self.name
        if self.priority is not None:
            result['Priority'] = self.priority
        if self.package_path is not None:
            result['PackagePath'] = self.package_path
        if self.stdout_redirect_path is not None:
            result['StdoutRedirectPath'] = self.stdout_redirect_path
        if self.stderr_redirect_path is not None:
            result['StderrRedirectPath'] = self.stderr_redirect_path
        if self.re_runable is not None:
            result['ReRunable'] = self.re_runable
        if self.array_request is not None:
            result['ArrayRequest'] = self.array_request
        if self.variables is not None:
            result['Variables'] = self.variables
        if self.input_file_url is not None:
            result['InputFileUrl'] = self.input_file_url
        if self.unzip_cmd is not None:
            result['UnzipCmd'] = self.unzip_cmd
        if self.post_cmd_line is not None:
            result['PostCmdLine'] = self.post_cmd_line
        if self.container_id is not None:
            result['ContainerId'] = self.container_id
        if self.job_queue is not None:
            result['JobQueue'] = self.job_queue
        if self.node is not None:
            result['Node'] = self.node
        if self.task is not None:
            result['Task'] = self.task
        if self.thread is not None:
            result['Thread'] = self.thread
        if self.mem is not None:
            result['Mem'] = self.mem
        if self.gpu is not None:
            result['Gpu'] = self.gpu
        if self.clock_time is not None:
            result['ClockTime'] = self.clock_time
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        if m.get('CommandLine') is not None:
            self.command_line = m.get('CommandLine')
        if m.get('RunasUser') is not None:
            self.runas_user = m.get('RunasUser')
        if m.get('RunasUserPassword') is not None:
            self.runas_user_password = m.get('RunasUserPassword')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Priority') is not None:
            self.priority = m.get('Priority')
        if m.get('PackagePath') is not None:
            self.package_path = m.get('PackagePath')
        if m.get('StdoutRedirectPath') is not None:
            self.stdout_redirect_path = m.get('StdoutRedirectPath')
        if m.get('StderrRedirectPath') is not None:
            self.stderr_redirect_path = m.get('StderrRedirectPath')
        if m.get('ReRunable') is not None:
            self.re_runable = m.get('ReRunable')
        if m.get('ArrayRequest') is not None:
            self.array_request = m.get('ArrayRequest')
        if m.get('Variables') is not None:
            self.variables = m.get('Variables')
        if m.get('InputFileUrl') is not None:
            self.input_file_url = m.get('InputFileUrl')
        if m.get('UnzipCmd') is not None:
            self.unzip_cmd = m.get('UnzipCmd')
        if m.get('PostCmdLine') is not None:
            self.post_cmd_line = m.get('PostCmdLine')
        if m.get('ContainerId') is not None:
            self.container_id = m.get('ContainerId')
        if m.get('JobQueue') is not None:
            self.job_queue = m.get('JobQueue')
        if m.get('Node') is not None:
            self.node = m.get('Node')
        if m.get('Task') is not None:
            self.task = m.get('Task')
        if m.get('Thread') is not None:
            self.thread = m.get('Thread')
        if m.get('Mem') is not None:
            self.mem = m.get('Mem')
        if m.get('Gpu') is not None:
            self.gpu = m.get('Gpu')
        if m.get('ClockTime') is not None:
            self.clock_time = m.get('ClockTime')
        return self


class SubmitJobResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        job_id: str = None,
    ):
        self.request_id = request_id
        self.job_id = job_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.job_id is not None:
            result['JobId'] = self.job_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('JobId') is not None:
            self.job_id = m.get('JobId')
        return self


class SubmitJobResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: SubmitJobResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = SubmitJobResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UnbindAccountToClusterUserRequest(TeaModel):
    def __init__(
        self,
        cluster_id: str = None,
        user_name: str = None,
        account_uid: str = None,
    ):
        self.cluster_id = cluster_id
        self.user_name = user_name
        self.account_uid = account_uid

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        if self.user_name is not None:
            result['UserName'] = self.user_name
        if self.account_uid is not None:
            result['AccountUid'] = self.account_uid
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        if m.get('UserName') is not None:
            self.user_name = m.get('UserName')
        if m.get('AccountUid') is not None:
            self.account_uid = m.get('AccountUid')
        return self


class UnbindAccountToClusterUserResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class UnbindAccountToClusterUserResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: UnbindAccountToClusterUserResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = UnbindAccountToClusterUserResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UninstallSoftwareRequest(TeaModel):
    def __init__(
        self,
        cluster_id: str = None,
        application: str = None,
    ):
        self.cluster_id = cluster_id
        self.application = application

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        if self.application is not None:
            result['Application'] = self.application
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        if m.get('Application') is not None:
            self.application = m.get('Application')
        return self


class UninstallSoftwareResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class UninstallSoftwareResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: UninstallSoftwareResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = UninstallSoftwareResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdateClusterVolumesRequestAdditionalVolumesRoles(TeaModel):
    def __init__(
        self,
        name: str = None,
    ):
        self.name = name

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.name is not None:
            result['Name'] = self.name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Name') is not None:
            self.name = m.get('Name')
        return self


class UpdateClusterVolumesRequestAdditionalVolumes(TeaModel):
    def __init__(
        self,
        job_queue: str = None,
        volume_id: str = None,
        roles: List[UpdateClusterVolumesRequestAdditionalVolumesRoles] = None,
        remote_directory: str = None,
        volume_mountpoint: str = None,
        local_directory: str = None,
        volume_type: str = None,
        volume_protocol: str = None,
        location: str = None,
    ):
        self.job_queue = job_queue
        self.volume_id = volume_id
        self.roles = roles
        self.remote_directory = remote_directory
        self.volume_mountpoint = volume_mountpoint
        self.local_directory = local_directory
        self.volume_type = volume_type
        self.volume_protocol = volume_protocol
        self.location = location

    def validate(self):
        if self.roles:
            for k in self.roles:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.job_queue is not None:
            result['JobQueue'] = self.job_queue
        if self.volume_id is not None:
            result['VolumeId'] = self.volume_id
        result['Roles'] = []
        if self.roles is not None:
            for k in self.roles:
                result['Roles'].append(k.to_map() if k else None)
        if self.remote_directory is not None:
            result['RemoteDirectory'] = self.remote_directory
        if self.volume_mountpoint is not None:
            result['VolumeMountpoint'] = self.volume_mountpoint
        if self.local_directory is not None:
            result['LocalDirectory'] = self.local_directory
        if self.volume_type is not None:
            result['VolumeType'] = self.volume_type
        if self.volume_protocol is not None:
            result['VolumeProtocol'] = self.volume_protocol
        if self.location is not None:
            result['Location'] = self.location
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('JobQueue') is not None:
            self.job_queue = m.get('JobQueue')
        if m.get('VolumeId') is not None:
            self.volume_id = m.get('VolumeId')
        self.roles = []
        if m.get('Roles') is not None:
            for k in m.get('Roles'):
                temp_model = UpdateClusterVolumesRequestAdditionalVolumesRoles()
                self.roles.append(temp_model.from_map(k))
        if m.get('RemoteDirectory') is not None:
            self.remote_directory = m.get('RemoteDirectory')
        if m.get('VolumeMountpoint') is not None:
            self.volume_mountpoint = m.get('VolumeMountpoint')
        if m.get('LocalDirectory') is not None:
            self.local_directory = m.get('LocalDirectory')
        if m.get('VolumeType') is not None:
            self.volume_type = m.get('VolumeType')
        if m.get('VolumeProtocol') is not None:
            self.volume_protocol = m.get('VolumeProtocol')
        if m.get('Location') is not None:
            self.location = m.get('Location')
        return self


class UpdateClusterVolumesRequest(TeaModel):
    def __init__(
        self,
        cluster_id: str = None,
        additional_volumes: List[UpdateClusterVolumesRequestAdditionalVolumes] = None,
    ):
        self.cluster_id = cluster_id
        self.additional_volumes = additional_volumes

    def validate(self):
        if self.additional_volumes:
            for k in self.additional_volumes:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        result['AdditionalVolumes'] = []
        if self.additional_volumes is not None:
            for k in self.additional_volumes:
                result['AdditionalVolumes'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        self.additional_volumes = []
        if m.get('AdditionalVolumes') is not None:
            for k in m.get('AdditionalVolumes'):
                temp_model = UpdateClusterVolumesRequestAdditionalVolumes()
                self.additional_volumes.append(temp_model.from_map(k))
        return self


class UpdateClusterVolumesResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class UpdateClusterVolumesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: UpdateClusterVolumesResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = UpdateClusterVolumesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdateQueueConfigRequest(TeaModel):
    def __init__(
        self,
        cluster_id: str = None,
        queue_name: str = None,
        resource_group_id: str = None,
        compute_instance_type: str = None,
    ):
        self.cluster_id = cluster_id
        self.queue_name = queue_name
        self.resource_group_id = resource_group_id
        self.compute_instance_type = compute_instance_type

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        if self.queue_name is not None:
            result['QueueName'] = self.queue_name
        if self.resource_group_id is not None:
            result['ResourceGroupId'] = self.resource_group_id
        if self.compute_instance_type is not None:
            result['ComputeInstanceType'] = self.compute_instance_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        if m.get('QueueName') is not None:
            self.queue_name = m.get('QueueName')
        if m.get('ResourceGroupId') is not None:
            self.resource_group_id = m.get('ResourceGroupId')
        if m.get('ComputeInstanceType') is not None:
            self.compute_instance_type = m.get('ComputeInstanceType')
        return self


class UpdateQueueConfigResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class UpdateQueueConfigResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: UpdateQueueConfigResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = UpdateQueueConfigResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpgradeClientRequest(TeaModel):
    def __init__(
        self,
        cluster_id: str = None,
        client_version: str = None,
    ):
        self.cluster_id = cluster_id
        self.client_version = client_version

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.cluster_id is not None:
            result['ClusterId'] = self.cluster_id
        if self.client_version is not None:
            result['ClientVersion'] = self.client_version
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClusterId') is not None:
            self.cluster_id = m.get('ClusterId')
        if m.get('ClientVersion') is not None:
            self.client_version = m.get('ClientVersion')
        return self


class UpgradeClientResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class UpgradeClientResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: UpgradeClientResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = UpgradeClientResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


