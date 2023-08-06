# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from Tea.model import TeaModel
from typing import Dict, List, Any


class ConvertPostPayOrderRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        instance_id: str = None,
        duration: int = None,
    ):
        self.region_id = region_id
        self.instance_id = instance_id
        self.duration = duration

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.duration is not None:
            result['Duration'] = self.duration
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('Duration') is not None:
            self.duration = m.get('Duration')
        return self


class ConvertPostPayOrderResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        order_id: str = None,
        code: int = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.order_id = order_id
        self.code = code
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.order_id is not None:
            result['OrderId'] = self.order_id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('OrderId') is not None:
            self.order_id = m.get('OrderId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class ConvertPostPayOrderResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ConvertPostPayOrderResponseBody = None,
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
            temp_model = ConvertPostPayOrderResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateAclRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        instance_id: str = None,
        username: str = None,
        acl_resource_type: str = None,
        acl_resource_name: str = None,
        acl_resource_pattern_type: str = None,
        acl_operation_type: str = None,
    ):
        self.region_id = region_id
        self.instance_id = instance_id
        self.username = username
        self.acl_resource_type = acl_resource_type
        self.acl_resource_name = acl_resource_name
        self.acl_resource_pattern_type = acl_resource_pattern_type
        self.acl_operation_type = acl_operation_type

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.username is not None:
            result['Username'] = self.username
        if self.acl_resource_type is not None:
            result['AclResourceType'] = self.acl_resource_type
        if self.acl_resource_name is not None:
            result['AclResourceName'] = self.acl_resource_name
        if self.acl_resource_pattern_type is not None:
            result['AclResourcePatternType'] = self.acl_resource_pattern_type
        if self.acl_operation_type is not None:
            result['AclOperationType'] = self.acl_operation_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('Username') is not None:
            self.username = m.get('Username')
        if m.get('AclResourceType') is not None:
            self.acl_resource_type = m.get('AclResourceType')
        if m.get('AclResourceName') is not None:
            self.acl_resource_name = m.get('AclResourceName')
        if m.get('AclResourcePatternType') is not None:
            self.acl_resource_pattern_type = m.get('AclResourcePatternType')
        if m.get('AclOperationType') is not None:
            self.acl_operation_type = m.get('AclOperationType')
        return self


class CreateAclResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        code: int = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.code = code
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class CreateAclResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: CreateAclResponseBody = None,
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
            temp_model = CreateAclResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateConsumerGroupRequest(TeaModel):
    def __init__(
        self,
        instance_id: str = None,
        consumer_id: str = None,
        region_id: str = None,
        remark: str = None,
    ):
        self.instance_id = instance_id
        self.consumer_id = consumer_id
        self.region_id = region_id
        self.remark = remark

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.consumer_id is not None:
            result['ConsumerId'] = self.consumer_id
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.remark is not None:
            result['Remark'] = self.remark
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('ConsumerId') is not None:
            self.consumer_id = m.get('ConsumerId')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('Remark') is not None:
            self.remark = m.get('Remark')
        return self


class CreateConsumerGroupResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        code: int = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.code = code
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class CreateConsumerGroupResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: CreateConsumerGroupResponseBody = None,
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
            temp_model = CreateConsumerGroupResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreatePostPayOrderRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        topic_quota: int = None,
        disk_type: str = None,
        disk_size: int = None,
        deploy_type: int = None,
        io_max: int = None,
        eip_max: int = None,
        paid_type: int = None,
        spec_type: str = None,
        io_max_spec: str = None,
    ):
        self.region_id = region_id
        self.topic_quota = topic_quota
        self.disk_type = disk_type
        self.disk_size = disk_size
        self.deploy_type = deploy_type
        self.io_max = io_max
        self.eip_max = eip_max
        self.paid_type = paid_type
        self.spec_type = spec_type
        self.io_max_spec = io_max_spec

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.topic_quota is not None:
            result['TopicQuota'] = self.topic_quota
        if self.disk_type is not None:
            result['DiskType'] = self.disk_type
        if self.disk_size is not None:
            result['DiskSize'] = self.disk_size
        if self.deploy_type is not None:
            result['DeployType'] = self.deploy_type
        if self.io_max is not None:
            result['IoMax'] = self.io_max
        if self.eip_max is not None:
            result['EipMax'] = self.eip_max
        if self.paid_type is not None:
            result['PaidType'] = self.paid_type
        if self.spec_type is not None:
            result['SpecType'] = self.spec_type
        if self.io_max_spec is not None:
            result['IoMaxSpec'] = self.io_max_spec
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('TopicQuota') is not None:
            self.topic_quota = m.get('TopicQuota')
        if m.get('DiskType') is not None:
            self.disk_type = m.get('DiskType')
        if m.get('DiskSize') is not None:
            self.disk_size = m.get('DiskSize')
        if m.get('DeployType') is not None:
            self.deploy_type = m.get('DeployType')
        if m.get('IoMax') is not None:
            self.io_max = m.get('IoMax')
        if m.get('EipMax') is not None:
            self.eip_max = m.get('EipMax')
        if m.get('PaidType') is not None:
            self.paid_type = m.get('PaidType')
        if m.get('SpecType') is not None:
            self.spec_type = m.get('SpecType')
        if m.get('IoMaxSpec') is not None:
            self.io_max_spec = m.get('IoMaxSpec')
        return self


class CreatePostPayOrderResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        order_id: str = None,
        code: int = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.order_id = order_id
        self.code = code
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.order_id is not None:
            result['OrderId'] = self.order_id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('OrderId') is not None:
            self.order_id = m.get('OrderId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class CreatePostPayOrderResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: CreatePostPayOrderResponseBody = None,
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
            temp_model = CreatePostPayOrderResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreatePrePayOrderRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        topic_quota: int = None,
        disk_type: str = None,
        disk_size: int = None,
        deploy_type: int = None,
        io_max: int = None,
        eip_max: int = None,
        spec_type: str = None,
        io_max_spec: str = None,
    ):
        self.region_id = region_id
        self.topic_quota = topic_quota
        self.disk_type = disk_type
        self.disk_size = disk_size
        self.deploy_type = deploy_type
        self.io_max = io_max
        self.eip_max = eip_max
        self.spec_type = spec_type
        self.io_max_spec = io_max_spec

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.topic_quota is not None:
            result['TopicQuota'] = self.topic_quota
        if self.disk_type is not None:
            result['DiskType'] = self.disk_type
        if self.disk_size is not None:
            result['DiskSize'] = self.disk_size
        if self.deploy_type is not None:
            result['DeployType'] = self.deploy_type
        if self.io_max is not None:
            result['IoMax'] = self.io_max
        if self.eip_max is not None:
            result['EipMax'] = self.eip_max
        if self.spec_type is not None:
            result['SpecType'] = self.spec_type
        if self.io_max_spec is not None:
            result['IoMaxSpec'] = self.io_max_spec
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('TopicQuota') is not None:
            self.topic_quota = m.get('TopicQuota')
        if m.get('DiskType') is not None:
            self.disk_type = m.get('DiskType')
        if m.get('DiskSize') is not None:
            self.disk_size = m.get('DiskSize')
        if m.get('DeployType') is not None:
            self.deploy_type = m.get('DeployType')
        if m.get('IoMax') is not None:
            self.io_max = m.get('IoMax')
        if m.get('EipMax') is not None:
            self.eip_max = m.get('EipMax')
        if m.get('SpecType') is not None:
            self.spec_type = m.get('SpecType')
        if m.get('IoMaxSpec') is not None:
            self.io_max_spec = m.get('IoMaxSpec')
        return self


class CreatePrePayOrderResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        order_id: str = None,
        code: int = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.order_id = order_id
        self.code = code
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.order_id is not None:
            result['OrderId'] = self.order_id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('OrderId') is not None:
            self.order_id = m.get('OrderId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class CreatePrePayOrderResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: CreatePrePayOrderResponseBody = None,
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
            temp_model = CreatePrePayOrderResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateSaslUserRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        instance_id: str = None,
        username: str = None,
        password: str = None,
        type: str = None,
    ):
        self.region_id = region_id
        self.instance_id = instance_id
        self.username = username
        self.password = password
        self.type = type

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.username is not None:
            result['Username'] = self.username
        if self.password is not None:
            result['Password'] = self.password
        if self.type is not None:
            result['Type'] = self.type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('Username') is not None:
            self.username = m.get('Username')
        if m.get('Password') is not None:
            self.password = m.get('Password')
        if m.get('Type') is not None:
            self.type = m.get('Type')
        return self


class CreateSaslUserResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        code: int = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.code = code
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class CreateSaslUserResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: CreateSaslUserResponseBody = None,
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
            temp_model = CreateSaslUserResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateTopicRequest(TeaModel):
    def __init__(
        self,
        instance_id: str = None,
        topic: str = None,
        remark: str = None,
        region_id: str = None,
        compact_topic: bool = None,
        partition_num: str = None,
        local_topic: bool = None,
    ):
        self.instance_id = instance_id
        self.topic = topic
        self.remark = remark
        self.region_id = region_id
        self.compact_topic = compact_topic
        self.partition_num = partition_num
        self.local_topic = local_topic

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.topic is not None:
            result['Topic'] = self.topic
        if self.remark is not None:
            result['Remark'] = self.remark
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.compact_topic is not None:
            result['CompactTopic'] = self.compact_topic
        if self.partition_num is not None:
            result['PartitionNum'] = self.partition_num
        if self.local_topic is not None:
            result['LocalTopic'] = self.local_topic
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('Topic') is not None:
            self.topic = m.get('Topic')
        if m.get('Remark') is not None:
            self.remark = m.get('Remark')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('CompactTopic') is not None:
            self.compact_topic = m.get('CompactTopic')
        if m.get('PartitionNum') is not None:
            self.partition_num = m.get('PartitionNum')
        if m.get('LocalTopic') is not None:
            self.local_topic = m.get('LocalTopic')
        return self


class CreateTopicResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        code: int = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.code = code
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class CreateTopicResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: CreateTopicResponseBody = None,
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
            temp_model = CreateTopicResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteAclRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        instance_id: str = None,
        username: str = None,
        acl_resource_type: str = None,
        acl_resource_name: str = None,
        acl_resource_pattern_type: str = None,
        acl_operation_type: str = None,
    ):
        self.region_id = region_id
        self.instance_id = instance_id
        self.username = username
        self.acl_resource_type = acl_resource_type
        self.acl_resource_name = acl_resource_name
        self.acl_resource_pattern_type = acl_resource_pattern_type
        self.acl_operation_type = acl_operation_type

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.username is not None:
            result['Username'] = self.username
        if self.acl_resource_type is not None:
            result['AclResourceType'] = self.acl_resource_type
        if self.acl_resource_name is not None:
            result['AclResourceName'] = self.acl_resource_name
        if self.acl_resource_pattern_type is not None:
            result['AclResourcePatternType'] = self.acl_resource_pattern_type
        if self.acl_operation_type is not None:
            result['AclOperationType'] = self.acl_operation_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('Username') is not None:
            self.username = m.get('Username')
        if m.get('AclResourceType') is not None:
            self.acl_resource_type = m.get('AclResourceType')
        if m.get('AclResourceName') is not None:
            self.acl_resource_name = m.get('AclResourceName')
        if m.get('AclResourcePatternType') is not None:
            self.acl_resource_pattern_type = m.get('AclResourcePatternType')
        if m.get('AclOperationType') is not None:
            self.acl_operation_type = m.get('AclOperationType')
        return self


class DeleteAclResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        code: int = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.code = code
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DeleteAclResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DeleteAclResponseBody = None,
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
            temp_model = DeleteAclResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteConsumerGroupRequest(TeaModel):
    def __init__(
        self,
        instance_id: str = None,
        consumer_id: str = None,
        region_id: str = None,
    ):
        self.instance_id = instance_id
        self.consumer_id = consumer_id
        self.region_id = region_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.consumer_id is not None:
            result['ConsumerId'] = self.consumer_id
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('ConsumerId') is not None:
            self.consumer_id = m.get('ConsumerId')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        return self


class DeleteConsumerGroupResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        code: int = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.code = code
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DeleteConsumerGroupResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DeleteConsumerGroupResponseBody = None,
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
            temp_model = DeleteConsumerGroupResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteInstanceRequest(TeaModel):
    def __init__(
        self,
        instance_id: str = None,
        region_id: str = None,
    ):
        self.instance_id = instance_id
        self.region_id = region_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        return self


class DeleteInstanceResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        code: int = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.code = code
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DeleteInstanceResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DeleteInstanceResponseBody = None,
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
            temp_model = DeleteInstanceResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteSaslUserRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        instance_id: str = None,
        username: str = None,
        type: str = None,
    ):
        self.region_id = region_id
        self.instance_id = instance_id
        self.username = username
        self.type = type

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.username is not None:
            result['Username'] = self.username
        if self.type is not None:
            result['Type'] = self.type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('Username') is not None:
            self.username = m.get('Username')
        if m.get('Type') is not None:
            self.type = m.get('Type')
        return self


class DeleteSaslUserResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        code: int = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.code = code
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DeleteSaslUserResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DeleteSaslUserResponseBody = None,
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
            temp_model = DeleteSaslUserResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteTopicRequest(TeaModel):
    def __init__(
        self,
        instance_id: str = None,
        topic: str = None,
        region_id: str = None,
    ):
        self.instance_id = instance_id
        self.topic = topic
        self.region_id = region_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.topic is not None:
            result['Topic'] = self.topic
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('Topic') is not None:
            self.topic = m.get('Topic')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        return self


class DeleteTopicResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        code: int = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.code = code
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DeleteTopicResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DeleteTopicResponseBody = None,
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
            temp_model = DeleteTopicResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeAclsRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        instance_id: str = None,
        username: str = None,
        acl_resource_type: str = None,
        acl_resource_name: str = None,
    ):
        self.region_id = region_id
        self.instance_id = instance_id
        self.username = username
        self.acl_resource_type = acl_resource_type
        self.acl_resource_name = acl_resource_name

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.username is not None:
            result['Username'] = self.username
        if self.acl_resource_type is not None:
            result['AclResourceType'] = self.acl_resource_type
        if self.acl_resource_name is not None:
            result['AclResourceName'] = self.acl_resource_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('Username') is not None:
            self.username = m.get('Username')
        if m.get('AclResourceType') is not None:
            self.acl_resource_type = m.get('AclResourceType')
        if m.get('AclResourceName') is not None:
            self.acl_resource_name = m.get('AclResourceName')
        return self


class DescribeAclsResponseBodyKafkaAclList(TeaModel):
    def __init__(
        self,
        acl_resource_type: str = None,
        host: str = None,
        acl_operation_type: str = None,
        acl_resource_name: str = None,
        acl_resource_pattern_type: str = None,
        username: str = None,
    ):
        self.acl_resource_type = acl_resource_type
        self.host = host
        self.acl_operation_type = acl_operation_type
        self.acl_resource_name = acl_resource_name
        self.acl_resource_pattern_type = acl_resource_pattern_type
        self.username = username

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.acl_resource_type is not None:
            result['AclResourceType'] = self.acl_resource_type
        if self.host is not None:
            result['Host'] = self.host
        if self.acl_operation_type is not None:
            result['AclOperationType'] = self.acl_operation_type
        if self.acl_resource_name is not None:
            result['AclResourceName'] = self.acl_resource_name
        if self.acl_resource_pattern_type is not None:
            result['AclResourcePatternType'] = self.acl_resource_pattern_type
        if self.username is not None:
            result['Username'] = self.username
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AclResourceType') is not None:
            self.acl_resource_type = m.get('AclResourceType')
        if m.get('Host') is not None:
            self.host = m.get('Host')
        if m.get('AclOperationType') is not None:
            self.acl_operation_type = m.get('AclOperationType')
        if m.get('AclResourceName') is not None:
            self.acl_resource_name = m.get('AclResourceName')
        if m.get('AclResourcePatternType') is not None:
            self.acl_resource_pattern_type = m.get('AclResourcePatternType')
        if m.get('Username') is not None:
            self.username = m.get('Username')
        return self


class DescribeAclsResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        code: int = None,
        success: bool = None,
        kafka_acl_list: List[DescribeAclsResponseBodyKafkaAclList] = None,
    ):
        self.message = message
        self.request_id = request_id
        self.code = code
        self.success = success
        self.kafka_acl_list = kafka_acl_list

    def validate(self):
        if self.kafka_acl_list:
            for k in self.kafka_acl_list:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        result['KafkaAclList'] = []
        if self.kafka_acl_list is not None:
            for k in self.kafka_acl_list:
                result['KafkaAclList'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        self.kafka_acl_list = []
        if m.get('KafkaAclList') is not None:
            for k in m.get('KafkaAclList'):
                temp_model = DescribeAclsResponseBodyKafkaAclList()
                self.kafka_acl_list.append(temp_model.from_map(k))
        return self


class DescribeAclsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeAclsResponseBody = None,
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
            temp_model = DescribeAclsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeNodeStatusRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        instance_id: str = None,
    ):
        self.region_id = region_id
        self.instance_id = instance_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        return self


class DescribeNodeStatusResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        status_list: List[str] = None,
        code: int = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.status_list = status_list
        self.code = code
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.status_list is not None:
            result['StatusList'] = self.status_list
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('StatusList') is not None:
            self.status_list = m.get('StatusList')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DescribeNodeStatusResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeNodeStatusResponseBody = None,
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
            temp_model = DescribeNodeStatusResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeSaslUsersRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        instance_id: str = None,
    ):
        self.region_id = region_id
        self.instance_id = instance_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        return self


class DescribeSaslUsersResponseBodySaslUserList(TeaModel):
    def __init__(
        self,
        type: str = None,
        password: str = None,
        username: str = None,
    ):
        self.type = type
        self.password = password
        self.username = username

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.type is not None:
            result['Type'] = self.type
        if self.password is not None:
            result['Password'] = self.password
        if self.username is not None:
            result['Username'] = self.username
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('Password') is not None:
            self.password = m.get('Password')
        if m.get('Username') is not None:
            self.username = m.get('Username')
        return self


class DescribeSaslUsersResponseBody(TeaModel):
    def __init__(
        self,
        sasl_user_list: List[DescribeSaslUsersResponseBodySaslUserList] = None,
        message: str = None,
        request_id: str = None,
        code: int = None,
        success: bool = None,
    ):
        self.sasl_user_list = sasl_user_list
        self.message = message
        self.request_id = request_id
        self.code = code
        self.success = success

    def validate(self):
        if self.sasl_user_list:
            for k in self.sasl_user_list:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['SaslUserList'] = []
        if self.sasl_user_list is not None:
            for k in self.sasl_user_list:
                result['SaslUserList'].append(k.to_map() if k else None)
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.sasl_user_list = []
        if m.get('SaslUserList') is not None:
            for k in m.get('SaslUserList'):
                temp_model = DescribeSaslUsersResponseBodySaslUserList()
                self.sasl_user_list.append(temp_model.from_map(k))
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DescribeSaslUsersResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeSaslUsersResponseBody = None,
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
            temp_model = DescribeSaslUsersResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetAllowedIpListRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        instance_id: str = None,
    ):
        self.region_id = region_id
        self.instance_id = instance_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        return self


class GetAllowedIpListResponseBodyAllowedListInternetList(TeaModel):
    def __init__(
        self,
        port_range: str = None,
        allowed_ip_list: List[str] = None,
    ):
        self.port_range = port_range
        self.allowed_ip_list = allowed_ip_list

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.port_range is not None:
            result['PortRange'] = self.port_range
        if self.allowed_ip_list is not None:
            result['AllowedIpList'] = self.allowed_ip_list
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('PortRange') is not None:
            self.port_range = m.get('PortRange')
        if m.get('AllowedIpList') is not None:
            self.allowed_ip_list = m.get('AllowedIpList')
        return self


class GetAllowedIpListResponseBodyAllowedListVpcList(TeaModel):
    def __init__(
        self,
        port_range: str = None,
        allowed_ip_list: List[str] = None,
    ):
        self.port_range = port_range
        self.allowed_ip_list = allowed_ip_list

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.port_range is not None:
            result['PortRange'] = self.port_range
        if self.allowed_ip_list is not None:
            result['AllowedIpList'] = self.allowed_ip_list
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('PortRange') is not None:
            self.port_range = m.get('PortRange')
        if m.get('AllowedIpList') is not None:
            self.allowed_ip_list = m.get('AllowedIpList')
        return self


class GetAllowedIpListResponseBodyAllowedList(TeaModel):
    def __init__(
        self,
        deploy_type: int = None,
        internet_list: List[GetAllowedIpListResponseBodyAllowedListInternetList] = None,
        vpc_list: List[GetAllowedIpListResponseBodyAllowedListVpcList] = None,
    ):
        self.deploy_type = deploy_type
        self.internet_list = internet_list
        self.vpc_list = vpc_list

    def validate(self):
        if self.internet_list:
            for k in self.internet_list:
                if k:
                    k.validate()
        if self.vpc_list:
            for k in self.vpc_list:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.deploy_type is not None:
            result['DeployType'] = self.deploy_type
        result['InternetList'] = []
        if self.internet_list is not None:
            for k in self.internet_list:
                result['InternetList'].append(k.to_map() if k else None)
        result['VpcList'] = []
        if self.vpc_list is not None:
            for k in self.vpc_list:
                result['VpcList'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DeployType') is not None:
            self.deploy_type = m.get('DeployType')
        self.internet_list = []
        if m.get('InternetList') is not None:
            for k in m.get('InternetList'):
                temp_model = GetAllowedIpListResponseBodyAllowedListInternetList()
                self.internet_list.append(temp_model.from_map(k))
        self.vpc_list = []
        if m.get('VpcList') is not None:
            for k in m.get('VpcList'):
                temp_model = GetAllowedIpListResponseBodyAllowedListVpcList()
                self.vpc_list.append(temp_model.from_map(k))
        return self


class GetAllowedIpListResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        allowed_list: GetAllowedIpListResponseBodyAllowedList = None,
        code: int = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.allowed_list = allowed_list
        self.code = code
        self.success = success

    def validate(self):
        if self.allowed_list:
            self.allowed_list.validate()

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.allowed_list is not None:
            result['AllowedList'] = self.allowed_list.to_map()
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('AllowedList') is not None:
            temp_model = GetAllowedIpListResponseBodyAllowedList()
            self.allowed_list = temp_model.from_map(m['AllowedList'])
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class GetAllowedIpListResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: GetAllowedIpListResponseBody = None,
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
            temp_model = GetAllowedIpListResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetConsumerListRequest(TeaModel):
    def __init__(
        self,
        instance_id: str = None,
        region_id: str = None,
        current_page: int = None,
        page_size: int = None,
    ):
        self.instance_id = instance_id
        self.region_id = region_id
        self.current_page = current_page
        self.page_size = page_size

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.current_page is not None:
            result['CurrentPage'] = self.current_page
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('CurrentPage') is not None:
            self.current_page = m.get('CurrentPage')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        return self


class GetConsumerListResponseBodyConsumerListTags(TeaModel):
    def __init__(
        self,
        key: str = None,
        value: str = None,
    ):
        self.key = key
        self.value = value

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.key is not None:
            result['Key'] = self.key
        if self.value is not None:
            result['Value'] = self.value
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Key') is not None:
            self.key = m.get('Key')
        if m.get('Value') is not None:
            self.value = m.get('Value')
        return self


class GetConsumerListResponseBodyConsumerList(TeaModel):
    def __init__(
        self,
        remark: str = None,
        tags: List[GetConsumerListResponseBodyConsumerListTags] = None,
        consumer_id: str = None,
        instance_id: str = None,
        region_id: str = None,
    ):
        self.remark = remark
        self.tags = tags
        self.consumer_id = consumer_id
        self.instance_id = instance_id
        self.region_id = region_id

    def validate(self):
        if self.tags:
            for k in self.tags:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.remark is not None:
            result['Remark'] = self.remark
        result['Tags'] = []
        if self.tags is not None:
            for k in self.tags:
                result['Tags'].append(k.to_map() if k else None)
        if self.consumer_id is not None:
            result['ConsumerId'] = self.consumer_id
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Remark') is not None:
            self.remark = m.get('Remark')
        self.tags = []
        if m.get('Tags') is not None:
            for k in m.get('Tags'):
                temp_model = GetConsumerListResponseBodyConsumerListTags()
                self.tags.append(temp_model.from_map(k))
        if m.get('ConsumerId') is not None:
            self.consumer_id = m.get('ConsumerId')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        return self


class GetConsumerListResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        code: int = None,
        consumer_list: List[GetConsumerListResponseBodyConsumerList] = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.code = code
        self.consumer_list = consumer_list
        self.success = success

    def validate(self):
        if self.consumer_list:
            for k in self.consumer_list:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        result['ConsumerList'] = []
        if self.consumer_list is not None:
            for k in self.consumer_list:
                result['ConsumerList'].append(k.to_map() if k else None)
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        self.consumer_list = []
        if m.get('ConsumerList') is not None:
            for k in m.get('ConsumerList'):
                temp_model = GetConsumerListResponseBodyConsumerList()
                self.consumer_list.append(temp_model.from_map(k))
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class GetConsumerListResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: GetConsumerListResponseBody = None,
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
            temp_model = GetConsumerListResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetConsumerProgressRequest(TeaModel):
    def __init__(
        self,
        instance_id: str = None,
        consumer_id: str = None,
        region_id: str = None,
    ):
        self.instance_id = instance_id
        self.consumer_id = consumer_id
        self.region_id = region_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.consumer_id is not None:
            result['ConsumerId'] = self.consumer_id
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('ConsumerId') is not None:
            self.consumer_id = m.get('ConsumerId')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        return self


class GetConsumerProgressResponseBodyConsumerProgressTopicListOffsetList(TeaModel):
    def __init__(
        self,
        broker_offset: int = None,
        consumer_offset: int = None,
        last_timestamp: int = None,
        partition: int = None,
    ):
        self.broker_offset = broker_offset
        self.consumer_offset = consumer_offset
        self.last_timestamp = last_timestamp
        self.partition = partition

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.broker_offset is not None:
            result['BrokerOffset'] = self.broker_offset
        if self.consumer_offset is not None:
            result['ConsumerOffset'] = self.consumer_offset
        if self.last_timestamp is not None:
            result['LastTimestamp'] = self.last_timestamp
        if self.partition is not None:
            result['Partition'] = self.partition
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('BrokerOffset') is not None:
            self.broker_offset = m.get('BrokerOffset')
        if m.get('ConsumerOffset') is not None:
            self.consumer_offset = m.get('ConsumerOffset')
        if m.get('LastTimestamp') is not None:
            self.last_timestamp = m.get('LastTimestamp')
        if m.get('Partition') is not None:
            self.partition = m.get('Partition')
        return self


class GetConsumerProgressResponseBodyConsumerProgressTopicList(TeaModel):
    def __init__(
        self,
        total_diff: int = None,
        last_timestamp: int = None,
        topic: str = None,
        offset_list: List[GetConsumerProgressResponseBodyConsumerProgressTopicListOffsetList] = None,
    ):
        self.total_diff = total_diff
        self.last_timestamp = last_timestamp
        self.topic = topic
        self.offset_list = offset_list

    def validate(self):
        if self.offset_list:
            for k in self.offset_list:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.total_diff is not None:
            result['TotalDiff'] = self.total_diff
        if self.last_timestamp is not None:
            result['LastTimestamp'] = self.last_timestamp
        if self.topic is not None:
            result['Topic'] = self.topic
        result['OffsetList'] = []
        if self.offset_list is not None:
            for k in self.offset_list:
                result['OffsetList'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TotalDiff') is not None:
            self.total_diff = m.get('TotalDiff')
        if m.get('LastTimestamp') is not None:
            self.last_timestamp = m.get('LastTimestamp')
        if m.get('Topic') is not None:
            self.topic = m.get('Topic')
        self.offset_list = []
        if m.get('OffsetList') is not None:
            for k in m.get('OffsetList'):
                temp_model = GetConsumerProgressResponseBodyConsumerProgressTopicListOffsetList()
                self.offset_list.append(temp_model.from_map(k))
        return self


class GetConsumerProgressResponseBodyConsumerProgress(TeaModel):
    def __init__(
        self,
        topic_list: List[GetConsumerProgressResponseBodyConsumerProgressTopicList] = None,
        last_timestamp: int = None,
        total_diff: int = None,
    ):
        self.topic_list = topic_list
        self.last_timestamp = last_timestamp
        self.total_diff = total_diff

    def validate(self):
        if self.topic_list:
            for k in self.topic_list:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['TopicList'] = []
        if self.topic_list is not None:
            for k in self.topic_list:
                result['TopicList'].append(k.to_map() if k else None)
        if self.last_timestamp is not None:
            result['LastTimestamp'] = self.last_timestamp
        if self.total_diff is not None:
            result['TotalDiff'] = self.total_diff
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.topic_list = []
        if m.get('TopicList') is not None:
            for k in m.get('TopicList'):
                temp_model = GetConsumerProgressResponseBodyConsumerProgressTopicList()
                self.topic_list.append(temp_model.from_map(k))
        if m.get('LastTimestamp') is not None:
            self.last_timestamp = m.get('LastTimestamp')
        if m.get('TotalDiff') is not None:
            self.total_diff = m.get('TotalDiff')
        return self


class GetConsumerProgressResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        consumer_progress: GetConsumerProgressResponseBodyConsumerProgress = None,
        code: int = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.consumer_progress = consumer_progress
        self.code = code
        self.success = success

    def validate(self):
        if self.consumer_progress:
            self.consumer_progress.validate()

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.consumer_progress is not None:
            result['ConsumerProgress'] = self.consumer_progress.to_map()
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('ConsumerProgress') is not None:
            temp_model = GetConsumerProgressResponseBodyConsumerProgress()
            self.consumer_progress = temp_model.from_map(m['ConsumerProgress'])
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class GetConsumerProgressResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: GetConsumerProgressResponseBody = None,
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
            temp_model = GetConsumerProgressResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetInstanceListRequestTag(TeaModel):
    def __init__(
        self,
        key: str = None,
        value: str = None,
    ):
        self.key = key
        self.value = value

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.key is not None:
            result['Key'] = self.key
        if self.value is not None:
            result['Value'] = self.value
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Key') is not None:
            self.key = m.get('Key')
        if m.get('Value') is not None:
            self.value = m.get('Value')
        return self


class GetInstanceListRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        order_id: str = None,
        instance_id: List[str] = None,
        tag: List[GetInstanceListRequestTag] = None,
    ):
        self.region_id = region_id
        self.order_id = order_id
        self.instance_id = instance_id
        self.tag = tag

    def validate(self):
        if self.tag:
            for k in self.tag:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.order_id is not None:
            result['OrderId'] = self.order_id
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        result['Tag'] = []
        if self.tag is not None:
            for k in self.tag:
                result['Tag'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('OrderId') is not None:
            self.order_id = m.get('OrderId')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        self.tag = []
        if m.get('Tag') is not None:
            for k in m.get('Tag'):
                temp_model = GetInstanceListRequestTag()
                self.tag.append(temp_model.from_map(k))
        return self


class GetInstanceListResponseBodyInstanceListUpgradeServiceDetailInfo(TeaModel):
    def __init__(
        self,
        current_2open_source_version: str = None,
    ):
        self.current_2open_source_version = current_2open_source_version

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.current_2open_source_version is not None:
            result['Current2OpenSourceVersion'] = self.current_2open_source_version
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Current2OpenSourceVersion') is not None:
            self.current_2open_source_version = m.get('Current2OpenSourceVersion')
        return self


class GetInstanceListResponseBodyInstanceListTags(TeaModel):
    def __init__(
        self,
        key: str = None,
        value: str = None,
    ):
        self.key = key
        self.value = value

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.key is not None:
            result['Key'] = self.key
        if self.value is not None:
            result['Value'] = self.value
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Key') is not None:
            self.key = m.get('Key')
        if m.get('Value') is not None:
            self.value = m.get('Value')
        return self


class GetInstanceListResponseBodyInstanceList(TeaModel):
    def __init__(
        self,
        vpc_id: str = None,
        upgrade_service_detail_info: List[GetInstanceListResponseBodyInstanceListUpgradeServiceDetailInfo] = None,
        spec_type: str = None,
        create_time: int = None,
        deploy_type: int = None,
        disk_size: int = None,
        tags: List[GetInstanceListResponseBodyInstanceListTags] = None,
        disk_type: int = None,
        instance_id: str = None,
        ssl_end_point: str = None,
        security_group: str = None,
        service_status: int = None,
        eip_max: int = None,
        region_id: str = None,
        msg_retain: int = None,
        v_switch_id: str = None,
        expired_time: int = None,
        topic_num_limit: int = None,
        zone_id: str = None,
        io_max: int = None,
        paid_type: int = None,
        name: str = None,
        end_point: str = None,
    ):
        self.vpc_id = vpc_id
        self.upgrade_service_detail_info = upgrade_service_detail_info
        self.spec_type = spec_type
        self.create_time = create_time
        self.deploy_type = deploy_type
        self.disk_size = disk_size
        self.tags = tags
        self.disk_type = disk_type
        self.instance_id = instance_id
        self.ssl_end_point = ssl_end_point
        self.security_group = security_group
        self.service_status = service_status
        self.eip_max = eip_max
        self.region_id = region_id
        self.msg_retain = msg_retain
        self.v_switch_id = v_switch_id
        self.expired_time = expired_time
        self.topic_num_limit = topic_num_limit
        self.zone_id = zone_id
        self.io_max = io_max
        self.paid_type = paid_type
        self.name = name
        self.end_point = end_point

    def validate(self):
        if self.upgrade_service_detail_info:
            for k in self.upgrade_service_detail_info:
                if k:
                    k.validate()
        if self.tags:
            for k in self.tags:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.vpc_id is not None:
            result['VpcId'] = self.vpc_id
        result['UpgradeServiceDetailInfo'] = []
        if self.upgrade_service_detail_info is not None:
            for k in self.upgrade_service_detail_info:
                result['UpgradeServiceDetailInfo'].append(k.to_map() if k else None)
        if self.spec_type is not None:
            result['SpecType'] = self.spec_type
        if self.create_time is not None:
            result['CreateTime'] = self.create_time
        if self.deploy_type is not None:
            result['DeployType'] = self.deploy_type
        if self.disk_size is not None:
            result['DiskSize'] = self.disk_size
        result['Tags'] = []
        if self.tags is not None:
            for k in self.tags:
                result['Tags'].append(k.to_map() if k else None)
        if self.disk_type is not None:
            result['DiskType'] = self.disk_type
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.ssl_end_point is not None:
            result['SslEndPoint'] = self.ssl_end_point
        if self.security_group is not None:
            result['SecurityGroup'] = self.security_group
        if self.service_status is not None:
            result['ServiceStatus'] = self.service_status
        if self.eip_max is not None:
            result['EipMax'] = self.eip_max
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.msg_retain is not None:
            result['MsgRetain'] = self.msg_retain
        if self.v_switch_id is not None:
            result['VSwitchId'] = self.v_switch_id
        if self.expired_time is not None:
            result['ExpiredTime'] = self.expired_time
        if self.topic_num_limit is not None:
            result['TopicNumLimit'] = self.topic_num_limit
        if self.zone_id is not None:
            result['ZoneId'] = self.zone_id
        if self.io_max is not None:
            result['IoMax'] = self.io_max
        if self.paid_type is not None:
            result['PaidType'] = self.paid_type
        if self.name is not None:
            result['Name'] = self.name
        if self.end_point is not None:
            result['EndPoint'] = self.end_point
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('VpcId') is not None:
            self.vpc_id = m.get('VpcId')
        self.upgrade_service_detail_info = []
        if m.get('UpgradeServiceDetailInfo') is not None:
            for k in m.get('UpgradeServiceDetailInfo'):
                temp_model = GetInstanceListResponseBodyInstanceListUpgradeServiceDetailInfo()
                self.upgrade_service_detail_info.append(temp_model.from_map(k))
        if m.get('SpecType') is not None:
            self.spec_type = m.get('SpecType')
        if m.get('CreateTime') is not None:
            self.create_time = m.get('CreateTime')
        if m.get('DeployType') is not None:
            self.deploy_type = m.get('DeployType')
        if m.get('DiskSize') is not None:
            self.disk_size = m.get('DiskSize')
        self.tags = []
        if m.get('Tags') is not None:
            for k in m.get('Tags'):
                temp_model = GetInstanceListResponseBodyInstanceListTags()
                self.tags.append(temp_model.from_map(k))
        if m.get('DiskType') is not None:
            self.disk_type = m.get('DiskType')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('SslEndPoint') is not None:
            self.ssl_end_point = m.get('SslEndPoint')
        if m.get('SecurityGroup') is not None:
            self.security_group = m.get('SecurityGroup')
        if m.get('ServiceStatus') is not None:
            self.service_status = m.get('ServiceStatus')
        if m.get('EipMax') is not None:
            self.eip_max = m.get('EipMax')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('MsgRetain') is not None:
            self.msg_retain = m.get('MsgRetain')
        if m.get('VSwitchId') is not None:
            self.v_switch_id = m.get('VSwitchId')
        if m.get('ExpiredTime') is not None:
            self.expired_time = m.get('ExpiredTime')
        if m.get('TopicNumLimit') is not None:
            self.topic_num_limit = m.get('TopicNumLimit')
        if m.get('ZoneId') is not None:
            self.zone_id = m.get('ZoneId')
        if m.get('IoMax') is not None:
            self.io_max = m.get('IoMax')
        if m.get('PaidType') is not None:
            self.paid_type = m.get('PaidType')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('EndPoint') is not None:
            self.end_point = m.get('EndPoint')
        return self


class GetInstanceListResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        instance_list: List[GetInstanceListResponseBodyInstanceList] = None,
        code: int = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.instance_list = instance_list
        self.code = code
        self.success = success

    def validate(self):
        if self.instance_list:
            for k in self.instance_list:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        result['InstanceList'] = []
        if self.instance_list is not None:
            for k in self.instance_list:
                result['InstanceList'].append(k.to_map() if k else None)
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        self.instance_list = []
        if m.get('InstanceList') is not None:
            for k in m.get('InstanceList'):
                temp_model = GetInstanceListResponseBodyInstanceList()
                self.instance_list.append(temp_model.from_map(k))
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class GetInstanceListResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: GetInstanceListResponseBody = None,
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
            temp_model = GetInstanceListResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetMetaProductListRequest(TeaModel):
    def __init__(
        self,
        list_normal: str = None,
        region_id: str = None,
    ):
        self.list_normal = list_normal
        self.region_id = region_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.list_normal is not None:
            result['ListNormal'] = self.list_normal
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ListNormal') is not None:
            self.list_normal = m.get('ListNormal')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        return self


class GetMetaProductListResponseBodyMetaDataProductsNormal(TeaModel):
    def __init__(
        self,
        topic_quota: str = None,
        spec_type: str = None,
        deploy_type: str = None,
        disk_size: str = None,
        io_max: int = None,
        disk_type: str = None,
        region_id: str = None,
    ):
        self.topic_quota = topic_quota
        self.spec_type = spec_type
        self.deploy_type = deploy_type
        self.disk_size = disk_size
        self.io_max = io_max
        self.disk_type = disk_type
        self.region_id = region_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.topic_quota is not None:
            result['TopicQuota'] = self.topic_quota
        if self.spec_type is not None:
            result['SpecType'] = self.spec_type
        if self.deploy_type is not None:
            result['DeployType'] = self.deploy_type
        if self.disk_size is not None:
            result['DiskSize'] = self.disk_size
        if self.io_max is not None:
            result['IoMax'] = self.io_max
        if self.disk_type is not None:
            result['DiskType'] = self.disk_type
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TopicQuota') is not None:
            self.topic_quota = m.get('TopicQuota')
        if m.get('SpecType') is not None:
            self.spec_type = m.get('SpecType')
        if m.get('DeployType') is not None:
            self.deploy_type = m.get('DeployType')
        if m.get('DiskSize') is not None:
            self.disk_size = m.get('DiskSize')
        if m.get('IoMax') is not None:
            self.io_max = m.get('IoMax')
        if m.get('DiskType') is not None:
            self.disk_type = m.get('DiskType')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        return self


class GetMetaProductListResponseBodyMetaDataProductsProfessional(TeaModel):
    def __init__(
        self,
        topic_quota: str = None,
        spec_type: str = None,
        deploy_type: str = None,
        disk_size: str = None,
        io_max: int = None,
        disk_type: str = None,
        region_id: str = None,
    ):
        self.topic_quota = topic_quota
        self.spec_type = spec_type
        self.deploy_type = deploy_type
        self.disk_size = disk_size
        self.io_max = io_max
        self.disk_type = disk_type
        self.region_id = region_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.topic_quota is not None:
            result['TopicQuota'] = self.topic_quota
        if self.spec_type is not None:
            result['SpecType'] = self.spec_type
        if self.deploy_type is not None:
            result['DeployType'] = self.deploy_type
        if self.disk_size is not None:
            result['DiskSize'] = self.disk_size
        if self.io_max is not None:
            result['IoMax'] = self.io_max
        if self.disk_type is not None:
            result['DiskType'] = self.disk_type
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TopicQuota') is not None:
            self.topic_quota = m.get('TopicQuota')
        if m.get('SpecType') is not None:
            self.spec_type = m.get('SpecType')
        if m.get('DeployType') is not None:
            self.deploy_type = m.get('DeployType')
        if m.get('DiskSize') is not None:
            self.disk_size = m.get('DiskSize')
        if m.get('IoMax') is not None:
            self.io_max = m.get('IoMax')
        if m.get('DiskType') is not None:
            self.disk_type = m.get('DiskType')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        return self


class GetMetaProductListResponseBodyMetaData(TeaModel):
    def __init__(
        self,
        products_normal: List[GetMetaProductListResponseBodyMetaDataProductsNormal] = None,
        products_professional: List[GetMetaProductListResponseBodyMetaDataProductsProfessional] = None,
        names: Dict[str, Any] = None,
    ):
        self.products_normal = products_normal
        self.products_professional = products_professional
        self.names = names

    def validate(self):
        if self.products_normal:
            for k in self.products_normal:
                if k:
                    k.validate()
        if self.products_professional:
            for k in self.products_professional:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['ProductsNormal'] = []
        if self.products_normal is not None:
            for k in self.products_normal:
                result['ProductsNormal'].append(k.to_map() if k else None)
        result['ProductsProfessional'] = []
        if self.products_professional is not None:
            for k in self.products_professional:
                result['ProductsProfessional'].append(k.to_map() if k else None)
        if self.names is not None:
            result['Names'] = self.names
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.products_normal = []
        if m.get('ProductsNormal') is not None:
            for k in m.get('ProductsNormal'):
                temp_model = GetMetaProductListResponseBodyMetaDataProductsNormal()
                self.products_normal.append(temp_model.from_map(k))
        self.products_professional = []
        if m.get('ProductsProfessional') is not None:
            for k in m.get('ProductsProfessional'):
                temp_model = GetMetaProductListResponseBodyMetaDataProductsProfessional()
                self.products_professional.append(temp_model.from_map(k))
        if m.get('Names') is not None:
            self.names = m.get('Names')
        return self


class GetMetaProductListResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        meta_data: GetMetaProductListResponseBodyMetaData = None,
        code: int = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.meta_data = meta_data
        self.code = code
        self.success = success

    def validate(self):
        if self.meta_data:
            self.meta_data.validate()

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.meta_data is not None:
            result['MetaData'] = self.meta_data.to_map()
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('MetaData') is not None:
            temp_model = GetMetaProductListResponseBodyMetaData()
            self.meta_data = temp_model.from_map(m['MetaData'])
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class GetMetaProductListResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: GetMetaProductListResponseBody = None,
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
            temp_model = GetMetaProductListResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetTopicListRequest(TeaModel):
    def __init__(
        self,
        instance_id: str = None,
        current_page: str = None,
        page_size: str = None,
        region_id: str = None,
    ):
        self.instance_id = instance_id
        self.current_page = current_page
        self.page_size = page_size
        self.region_id = region_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.current_page is not None:
            result['CurrentPage'] = self.current_page
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('CurrentPage') is not None:
            self.current_page = m.get('CurrentPage')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        return self


class GetTopicListResponseBodyTopicListTags(TeaModel):
    def __init__(
        self,
        key: str = None,
        value: str = None,
    ):
        self.key = key
        self.value = value

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.key is not None:
            result['Key'] = self.key
        if self.value is not None:
            result['Value'] = self.value
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Key') is not None:
            self.key = m.get('Key')
        if m.get('Value') is not None:
            self.value = m.get('Value')
        return self


class GetTopicListResponseBodyTopicList(TeaModel):
    def __init__(
        self,
        status: int = None,
        remark: str = None,
        create_time: int = None,
        topic: str = None,
        status_name: str = None,
        tags: List[GetTopicListResponseBodyTopicListTags] = None,
        instance_id: str = None,
        region_id: str = None,
    ):
        self.status = status
        self.remark = remark
        self.create_time = create_time
        self.topic = topic
        self.status_name = status_name
        self.tags = tags
        self.instance_id = instance_id
        self.region_id = region_id

    def validate(self):
        if self.tags:
            for k in self.tags:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.status is not None:
            result['Status'] = self.status
        if self.remark is not None:
            result['Remark'] = self.remark
        if self.create_time is not None:
            result['CreateTime'] = self.create_time
        if self.topic is not None:
            result['Topic'] = self.topic
        if self.status_name is not None:
            result['StatusName'] = self.status_name
        result['Tags'] = []
        if self.tags is not None:
            for k in self.tags:
                result['Tags'].append(k.to_map() if k else None)
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('Remark') is not None:
            self.remark = m.get('Remark')
        if m.get('CreateTime') is not None:
            self.create_time = m.get('CreateTime')
        if m.get('Topic') is not None:
            self.topic = m.get('Topic')
        if m.get('StatusName') is not None:
            self.status_name = m.get('StatusName')
        self.tags = []
        if m.get('Tags') is not None:
            for k in m.get('Tags'):
                temp_model = GetTopicListResponseBodyTopicListTags()
                self.tags.append(temp_model.from_map(k))
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        return self


class GetTopicListResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        message: str = None,
        page_size: int = None,
        current_page: int = None,
        total: int = None,
        topic_list: List[GetTopicListResponseBodyTopicList] = None,
        code: int = None,
        success: bool = None,
    ):
        self.request_id = request_id
        self.message = message
        self.page_size = page_size
        self.current_page = current_page
        self.total = total
        self.topic_list = topic_list
        self.code = code
        self.success = success

    def validate(self):
        if self.topic_list:
            for k in self.topic_list:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.message is not None:
            result['Message'] = self.message
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.current_page is not None:
            result['CurrentPage'] = self.current_page
        if self.total is not None:
            result['Total'] = self.total
        result['TopicList'] = []
        if self.topic_list is not None:
            for k in self.topic_list:
                result['TopicList'].append(k.to_map() if k else None)
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('CurrentPage') is not None:
            self.current_page = m.get('CurrentPage')
        if m.get('Total') is not None:
            self.total = m.get('Total')
        self.topic_list = []
        if m.get('TopicList') is not None:
            for k in m.get('TopicList'):
                temp_model = GetTopicListResponseBodyTopicList()
                self.topic_list.append(temp_model.from_map(k))
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class GetTopicListResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: GetTopicListResponseBody = None,
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
            temp_model = GetTopicListResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetTopicStatusRequest(TeaModel):
    def __init__(
        self,
        instance_id: str = None,
        topic: str = None,
        region_id: str = None,
    ):
        self.instance_id = instance_id
        self.topic = topic
        self.region_id = region_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.topic is not None:
            result['Topic'] = self.topic
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('Topic') is not None:
            self.topic = m.get('Topic')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        return self


class GetTopicStatusResponseBodyTopicStatusOffsetTable(TeaModel):
    def __init__(
        self,
        min_offset: int = None,
        topic: str = None,
        partition: int = None,
        last_update_timestamp: int = None,
        max_offset: int = None,
    ):
        self.min_offset = min_offset
        self.topic = topic
        self.partition = partition
        self.last_update_timestamp = last_update_timestamp
        self.max_offset = max_offset

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.min_offset is not None:
            result['MinOffset'] = self.min_offset
        if self.topic is not None:
            result['Topic'] = self.topic
        if self.partition is not None:
            result['Partition'] = self.partition
        if self.last_update_timestamp is not None:
            result['LastUpdateTimestamp'] = self.last_update_timestamp
        if self.max_offset is not None:
            result['MaxOffset'] = self.max_offset
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('MinOffset') is not None:
            self.min_offset = m.get('MinOffset')
        if m.get('Topic') is not None:
            self.topic = m.get('Topic')
        if m.get('Partition') is not None:
            self.partition = m.get('Partition')
        if m.get('LastUpdateTimestamp') is not None:
            self.last_update_timestamp = m.get('LastUpdateTimestamp')
        if m.get('MaxOffset') is not None:
            self.max_offset = m.get('MaxOffset')
        return self


class GetTopicStatusResponseBodyTopicStatus(TeaModel):
    def __init__(
        self,
        last_time_stamp: int = None,
        total_count: int = None,
        offset_table: List[GetTopicStatusResponseBodyTopicStatusOffsetTable] = None,
    ):
        self.last_time_stamp = last_time_stamp
        self.total_count = total_count
        self.offset_table = offset_table

    def validate(self):
        if self.offset_table:
            for k in self.offset_table:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.last_time_stamp is not None:
            result['LastTimeStamp'] = self.last_time_stamp
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        result['OffsetTable'] = []
        if self.offset_table is not None:
            for k in self.offset_table:
                result['OffsetTable'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('LastTimeStamp') is not None:
            self.last_time_stamp = m.get('LastTimeStamp')
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        self.offset_table = []
        if m.get('OffsetTable') is not None:
            for k in m.get('OffsetTable'):
                temp_model = GetTopicStatusResponseBodyTopicStatusOffsetTable()
                self.offset_table.append(temp_model.from_map(k))
        return self


class GetTopicStatusResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        topic_status: GetTopicStatusResponseBodyTopicStatus = None,
        code: int = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.topic_status = topic_status
        self.code = code
        self.success = success

    def validate(self):
        if self.topic_status:
            self.topic_status.validate()

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.topic_status is not None:
            result['TopicStatus'] = self.topic_status.to_map()
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('TopicStatus') is not None:
            temp_model = GetTopicStatusResponseBodyTopicStatus()
            self.topic_status = temp_model.from_map(m['TopicStatus'])
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class GetTopicStatusResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: GetTopicStatusResponseBody = None,
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
            temp_model = GetTopicStatusResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListTagResourcesRequestTag(TeaModel):
    def __init__(
        self,
        key: str = None,
        value: str = None,
    ):
        self.key = key
        self.value = value

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.key is not None:
            result['Key'] = self.key
        if self.value is not None:
            result['Value'] = self.value
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Key') is not None:
            self.key = m.get('Key')
        if m.get('Value') is not None:
            self.value = m.get('Value')
        return self


class ListTagResourcesRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        resource_type: str = None,
        next_token: str = None,
        resource_id: List[str] = None,
        tag: List[ListTagResourcesRequestTag] = None,
    ):
        self.region_id = region_id
        self.resource_type = resource_type
        self.next_token = next_token
        self.resource_id = resource_id
        self.tag = tag

    def validate(self):
        if self.tag:
            for k in self.tag:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.resource_type is not None:
            result['ResourceType'] = self.resource_type
        if self.next_token is not None:
            result['NextToken'] = self.next_token
        if self.resource_id is not None:
            result['ResourceId'] = self.resource_id
        result['Tag'] = []
        if self.tag is not None:
            for k in self.tag:
                result['Tag'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('ResourceType') is not None:
            self.resource_type = m.get('ResourceType')
        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')
        if m.get('ResourceId') is not None:
            self.resource_id = m.get('ResourceId')
        self.tag = []
        if m.get('Tag') is not None:
            for k in m.get('Tag'):
                temp_model = ListTagResourcesRequestTag()
                self.tag.append(temp_model.from_map(k))
        return self


class ListTagResourcesResponseBodyTagResources(TeaModel):
    def __init__(
        self,
        resource_type: str = None,
        tag_value: str = None,
        resource_id: str = None,
        tag_key: str = None,
    ):
        self.resource_type = resource_type
        self.tag_value = tag_value
        self.resource_id = resource_id
        self.tag_key = tag_key

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.resource_type is not None:
            result['ResourceType'] = self.resource_type
        if self.tag_value is not None:
            result['TagValue'] = self.tag_value
        if self.resource_id is not None:
            result['ResourceId'] = self.resource_id
        if self.tag_key is not None:
            result['TagKey'] = self.tag_key
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ResourceType') is not None:
            self.resource_type = m.get('ResourceType')
        if m.get('TagValue') is not None:
            self.tag_value = m.get('TagValue')
        if m.get('ResourceId') is not None:
            self.resource_id = m.get('ResourceId')
        if m.get('TagKey') is not None:
            self.tag_key = m.get('TagKey')
        return self


class ListTagResourcesResponseBody(TeaModel):
    def __init__(
        self,
        next_token: str = None,
        request_id: str = None,
        tag_resources: List[ListTagResourcesResponseBodyTagResources] = None,
    ):
        self.next_token = next_token
        self.request_id = request_id
        self.tag_resources = tag_resources

    def validate(self):
        if self.tag_resources:
            for k in self.tag_resources:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.next_token is not None:
            result['NextToken'] = self.next_token
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        result['TagResources'] = []
        if self.tag_resources is not None:
            for k in self.tag_resources:
                result['TagResources'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        self.tag_resources = []
        if m.get('TagResources') is not None:
            for k in m.get('TagResources'):
                temp_model = ListTagResourcesResponseBodyTagResources()
                self.tag_resources.append(temp_model.from_map(k))
        return self


class ListTagResourcesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ListTagResourcesResponseBody = None,
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
            temp_model = ListTagResourcesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ModifyInstanceNameRequest(TeaModel):
    def __init__(
        self,
        instance_id: str = None,
        region_id: str = None,
        instance_name: str = None,
    ):
        self.instance_id = instance_id
        self.region_id = region_id
        self.instance_name = instance_name

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.instance_name is not None:
            result['InstanceName'] = self.instance_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('InstanceName') is not None:
            self.instance_name = m.get('InstanceName')
        return self


class ModifyInstanceNameResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        code: int = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.code = code
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class ModifyInstanceNameResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ModifyInstanceNameResponseBody = None,
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
            temp_model = ModifyInstanceNameResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ModifyPartitionNumRequest(TeaModel):
    def __init__(
        self,
        instance_id: str = None,
        topic: str = None,
        region_id: str = None,
        add_partition_num: int = None,
    ):
        self.instance_id = instance_id
        self.topic = topic
        self.region_id = region_id
        self.add_partition_num = add_partition_num

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.topic is not None:
            result['Topic'] = self.topic
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.add_partition_num is not None:
            result['AddPartitionNum'] = self.add_partition_num
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('Topic') is not None:
            self.topic = m.get('Topic')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('AddPartitionNum') is not None:
            self.add_partition_num = m.get('AddPartitionNum')
        return self


class ModifyPartitionNumResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        code: int = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.code = code
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class ModifyPartitionNumResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ModifyPartitionNumResponseBody = None,
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
            temp_model = ModifyPartitionNumResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ModifyTopicRemarkRequest(TeaModel):
    def __init__(
        self,
        instance_id: str = None,
        topic: str = None,
        region_id: str = None,
        remark: str = None,
    ):
        self.instance_id = instance_id
        self.topic = topic
        self.region_id = region_id
        self.remark = remark

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.topic is not None:
            result['Topic'] = self.topic
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.remark is not None:
            result['Remark'] = self.remark
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('Topic') is not None:
            self.topic = m.get('Topic')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('Remark') is not None:
            self.remark = m.get('Remark')
        return self


class ModifyTopicRemarkResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        code: int = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.code = code
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class ModifyTopicRemarkResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ModifyTopicRemarkResponseBody = None,
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
            temp_model = ModifyTopicRemarkResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ReleaseInstanceRequest(TeaModel):
    def __init__(
        self,
        instance_id: str = None,
        region_id: str = None,
        release_ignore_time: bool = None,
        force_delete_instance: bool = None,
    ):
        self.instance_id = instance_id
        self.region_id = region_id
        self.release_ignore_time = release_ignore_time
        self.force_delete_instance = force_delete_instance

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.release_ignore_time is not None:
            result['ReleaseIgnoreTime'] = self.release_ignore_time
        if self.force_delete_instance is not None:
            result['ForceDeleteInstance'] = self.force_delete_instance
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('ReleaseIgnoreTime') is not None:
            self.release_ignore_time = m.get('ReleaseIgnoreTime')
        if m.get('ForceDeleteInstance') is not None:
            self.force_delete_instance = m.get('ForceDeleteInstance')
        return self


class ReleaseInstanceResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        code: int = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.code = code
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class ReleaseInstanceResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ReleaseInstanceResponseBody = None,
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
            temp_model = ReleaseInstanceResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class StartInstanceRequest(TeaModel):
    def __init__(
        self,
        instance_id: str = None,
        region_id: str = None,
        vpc_id: str = None,
        v_switch_id: str = None,
        deploy_module: str = None,
        zone_id: str = None,
        is_eip_inner: bool = None,
        is_set_user_and_password: bool = None,
        username: str = None,
        password: str = None,
        name: str = None,
        cross_zone: bool = None,
        security_group: str = None,
    ):
        self.instance_id = instance_id
        self.region_id = region_id
        self.vpc_id = vpc_id
        self.v_switch_id = v_switch_id
        self.deploy_module = deploy_module
        self.zone_id = zone_id
        self.is_eip_inner = is_eip_inner
        self.is_set_user_and_password = is_set_user_and_password
        self.username = username
        self.password = password
        self.name = name
        self.cross_zone = cross_zone
        self.security_group = security_group

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.vpc_id is not None:
            result['VpcId'] = self.vpc_id
        if self.v_switch_id is not None:
            result['VSwitchId'] = self.v_switch_id
        if self.deploy_module is not None:
            result['DeployModule'] = self.deploy_module
        if self.zone_id is not None:
            result['ZoneId'] = self.zone_id
        if self.is_eip_inner is not None:
            result['IsEipInner'] = self.is_eip_inner
        if self.is_set_user_and_password is not None:
            result['IsSetUserAndPassword'] = self.is_set_user_and_password
        if self.username is not None:
            result['Username'] = self.username
        if self.password is not None:
            result['Password'] = self.password
        if self.name is not None:
            result['Name'] = self.name
        if self.cross_zone is not None:
            result['CrossZone'] = self.cross_zone
        if self.security_group is not None:
            result['SecurityGroup'] = self.security_group
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('VpcId') is not None:
            self.vpc_id = m.get('VpcId')
        if m.get('VSwitchId') is not None:
            self.v_switch_id = m.get('VSwitchId')
        if m.get('DeployModule') is not None:
            self.deploy_module = m.get('DeployModule')
        if m.get('ZoneId') is not None:
            self.zone_id = m.get('ZoneId')
        if m.get('IsEipInner') is not None:
            self.is_eip_inner = m.get('IsEipInner')
        if m.get('IsSetUserAndPassword') is not None:
            self.is_set_user_and_password = m.get('IsSetUserAndPassword')
        if m.get('Username') is not None:
            self.username = m.get('Username')
        if m.get('Password') is not None:
            self.password = m.get('Password')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('CrossZone') is not None:
            self.cross_zone = m.get('CrossZone')
        if m.get('SecurityGroup') is not None:
            self.security_group = m.get('SecurityGroup')
        return self


class StartInstanceResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        code: int = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.code = code
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class StartInstanceResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: StartInstanceResponseBody = None,
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
            temp_model = StartInstanceResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class TagResourcesRequestTag(TeaModel):
    def __init__(
        self,
        key: str = None,
        value: str = None,
    ):
        self.key = key
        self.value = value

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.key is not None:
            result['Key'] = self.key
        if self.value is not None:
            result['Value'] = self.value
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Key') is not None:
            self.key = m.get('Key')
        if m.get('Value') is not None:
            self.value = m.get('Value')
        return self


class TagResourcesRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        resource_type: str = None,
        resource_id: List[str] = None,
        tag: List[TagResourcesRequestTag] = None,
    ):
        self.region_id = region_id
        self.resource_type = resource_type
        self.resource_id = resource_id
        self.tag = tag

    def validate(self):
        if self.tag:
            for k in self.tag:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.resource_type is not None:
            result['ResourceType'] = self.resource_type
        if self.resource_id is not None:
            result['ResourceId'] = self.resource_id
        result['Tag'] = []
        if self.tag is not None:
            for k in self.tag:
                result['Tag'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('ResourceType') is not None:
            self.resource_type = m.get('ResourceType')
        if m.get('ResourceId') is not None:
            self.resource_id = m.get('ResourceId')
        self.tag = []
        if m.get('Tag') is not None:
            for k in m.get('Tag'):
                temp_model = TagResourcesRequestTag()
                self.tag.append(temp_model.from_map(k))
        return self


class TagResourcesResponseBody(TeaModel):
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


class TagResourcesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: TagResourcesResponseBody = None,
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
            temp_model = TagResourcesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UntagResourcesRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        resource_type: str = None,
        all: bool = None,
        resource_id: List[str] = None,
        tag_key: List[str] = None,
    ):
        self.region_id = region_id
        self.resource_type = resource_type
        self.all = all
        self.resource_id = resource_id
        self.tag_key = tag_key

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.resource_type is not None:
            result['ResourceType'] = self.resource_type
        if self.all is not None:
            result['All'] = self.all
        if self.resource_id is not None:
            result['ResourceId'] = self.resource_id
        if self.tag_key is not None:
            result['TagKey'] = self.tag_key
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('ResourceType') is not None:
            self.resource_type = m.get('ResourceType')
        if m.get('All') is not None:
            self.all = m.get('All')
        if m.get('ResourceId') is not None:
            self.resource_id = m.get('ResourceId')
        if m.get('TagKey') is not None:
            self.tag_key = m.get('TagKey')
        return self


class UntagResourcesResponseBody(TeaModel):
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


class UntagResourcesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: UntagResourcesResponseBody = None,
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
            temp_model = UntagResourcesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdateAllowedIpRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        update_type: str = None,
        port_range: str = None,
        allowed_list_type: str = None,
        allowed_list_ip: str = None,
        instance_id: str = None,
    ):
        self.region_id = region_id
        self.update_type = update_type
        self.port_range = port_range
        self.allowed_list_type = allowed_list_type
        self.allowed_list_ip = allowed_list_ip
        self.instance_id = instance_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.update_type is not None:
            result['UpdateType'] = self.update_type
        if self.port_range is not None:
            result['PortRange'] = self.port_range
        if self.allowed_list_type is not None:
            result['AllowedListType'] = self.allowed_list_type
        if self.allowed_list_ip is not None:
            result['AllowedListIp'] = self.allowed_list_ip
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('UpdateType') is not None:
            self.update_type = m.get('UpdateType')
        if m.get('PortRange') is not None:
            self.port_range = m.get('PortRange')
        if m.get('AllowedListType') is not None:
            self.allowed_list_type = m.get('AllowedListType')
        if m.get('AllowedListIp') is not None:
            self.allowed_list_ip = m.get('AllowedListIp')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        return self


class UpdateAllowedIpResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        code: int = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.code = code
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class UpdateAllowedIpResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: UpdateAllowedIpResponseBody = None,
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
            temp_model = UpdateAllowedIpResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpgradePostPayOrderRequest(TeaModel):
    def __init__(
        self,
        instance_id: str = None,
        topic_quota: int = None,
        disk_size: int = None,
        region_id: str = None,
        io_max: int = None,
        spec_type: str = None,
        eip_max: int = None,
        io_max_spec: str = None,
    ):
        self.instance_id = instance_id
        self.topic_quota = topic_quota
        self.disk_size = disk_size
        self.region_id = region_id
        self.io_max = io_max
        self.spec_type = spec_type
        self.eip_max = eip_max
        self.io_max_spec = io_max_spec

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.topic_quota is not None:
            result['TopicQuota'] = self.topic_quota
        if self.disk_size is not None:
            result['DiskSize'] = self.disk_size
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.io_max is not None:
            result['IoMax'] = self.io_max
        if self.spec_type is not None:
            result['SpecType'] = self.spec_type
        if self.eip_max is not None:
            result['EipMax'] = self.eip_max
        if self.io_max_spec is not None:
            result['IoMaxSpec'] = self.io_max_spec
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('TopicQuota') is not None:
            self.topic_quota = m.get('TopicQuota')
        if m.get('DiskSize') is not None:
            self.disk_size = m.get('DiskSize')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('IoMax') is not None:
            self.io_max = m.get('IoMax')
        if m.get('SpecType') is not None:
            self.spec_type = m.get('SpecType')
        if m.get('EipMax') is not None:
            self.eip_max = m.get('EipMax')
        if m.get('IoMaxSpec') is not None:
            self.io_max_spec = m.get('IoMaxSpec')
        return self


class UpgradePostPayOrderResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        code: int = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.code = code
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class UpgradePostPayOrderResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: UpgradePostPayOrderResponseBody = None,
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
            temp_model = UpgradePostPayOrderResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpgradePrePayOrderRequest(TeaModel):
    def __init__(
        self,
        instance_id: str = None,
        topic_quota: int = None,
        disk_size: int = None,
        region_id: str = None,
        io_max: int = None,
        spec_type: str = None,
        eip_max: int = None,
        io_max_spec: str = None,
    ):
        self.instance_id = instance_id
        self.topic_quota = topic_quota
        self.disk_size = disk_size
        self.region_id = region_id
        self.io_max = io_max
        self.spec_type = spec_type
        self.eip_max = eip_max
        self.io_max_spec = io_max_spec

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        if self.topic_quota is not None:
            result['TopicQuota'] = self.topic_quota
        if self.disk_size is not None:
            result['DiskSize'] = self.disk_size
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.io_max is not None:
            result['IoMax'] = self.io_max
        if self.spec_type is not None:
            result['SpecType'] = self.spec_type
        if self.eip_max is not None:
            result['EipMax'] = self.eip_max
        if self.io_max_spec is not None:
            result['IoMaxSpec'] = self.io_max_spec
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        if m.get('TopicQuota') is not None:
            self.topic_quota = m.get('TopicQuota')
        if m.get('DiskSize') is not None:
            self.disk_size = m.get('DiskSize')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('IoMax') is not None:
            self.io_max = m.get('IoMax')
        if m.get('SpecType') is not None:
            self.spec_type = m.get('SpecType')
        if m.get('EipMax') is not None:
            self.eip_max = m.get('EipMax')
        if m.get('IoMaxSpec') is not None:
            self.io_max_spec = m.get('IoMaxSpec')
        return self


class UpgradePrePayOrderResponseBody(TeaModel):
    def __init__(
        self,
        message: str = None,
        request_id: str = None,
        code: int = None,
        success: bool = None,
    ):
        self.message = message
        self.request_id = request_id
        self.code = code
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class UpgradePrePayOrderResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: UpgradePrePayOrderResponseBody = None,
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
            temp_model = UpgradePrePayOrderResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


