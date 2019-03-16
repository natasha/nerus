
import subprocess
from time import sleep

import yandexcloud

from yandex.cloud.resourcemanager.v1.folder_service_pb2 import ListFoldersRequest
from yandex.cloud.resourcemanager.v1.folder_service_pb2_grpc import FolderServiceStub

from yandex.cloud.vpc.v1.subnet_service_pb2 import ListSubnetsRequest
from yandex.cloud.vpc.v1.subnet_service_pb2_grpc import SubnetServiceStub

from yandex.cloud.compute.v1.image_service_pb2 import GetImageLatestByFamilyRequest
from yandex.cloud.compute.v1.image_service_pb2_grpc import ImageServiceStub

from yandex.cloud.compute.v1.instance_pb2 import (
    IPV4,
    SchedulingPolicy
)
from yandex.cloud.compute.v1.instance_service_pb2 import (
    CreateInstanceRequest,
    DeleteInstanceRequest,
    ListInstancesRequest,

    ResourcesSpec,
    AttachedDiskSpec,

    NetworkInterfaceSpec,
    PrimaryAddressSpec,
    OneToOneNatSpec
)
from yandex.cloud.compute.v1.instance_service_pb2_grpc import InstanceServiceStub

from .path import exists
from .etl import load_text
from .const import (
    YC_CLOUD,
    YC_TOKEN,
    YC_FOLDER,
    YC_PLATFORM,
    YC_SUBNET,
    YC_HDD,
    YC_UBUNTU_1604,

    SSH_USER,
    SSH_KEY
)


##########
#
#   SDK
#
########


def call_yc(*args):
    try:
        output = subprocess.check_output(('yc',) + args)
        return output.decode('utf8').strip()
    except subprocess.CalledProcessError:
        return


def yc_token():
    return call_yc('config', 'get', 'token')


def yc_cloud():
    return call_yc('config', 'get', 'cloud-id')


class YcError(Exception):
    pass


def find_token():
    token = YC_TOKEN or yc_token()
    if not token:
        raise YcError('not token')
    return token


def find_cloud():
    cloud = YC_CLOUD or yc_cloud()
    if not cloud:
        raise YcError('no cloud id')
    return cloud


def get_sdk():
    token = find_token()
    return yandexcloud.SDK(token=token)


def wait(sdk, operation, every=1, callback=None):
    waiter = sdk.waiter(operation.id)
    for _ in waiter:
        if callback:
            callback()
        sleep(every)
    return waiter.operation.response


########
#
#   LIST
#
#########


def find_name(records, name):
    for record in records:
        if record.name == name:
            return record


def list_folders(sdk):
    service = sdk.client(FolderServiceStub)
    cloud = find_cloud()
    return service.List(
        ListFoldersRequest(
            cloud_id=cloud
        )
    ).folders


def find_folder(sdk, name=YC_FOLDER):
    folders = list_folders(sdk)
    return find_name(folders, name)


def list_instances(sdk, folder):
    service = sdk.client(InstanceServiceStub)
    return service.List(
        ListInstancesRequest(
            folder_id=folder.id
        )
    ).instances


def find_instance(sdk, folder, name):
    instances = list_instances(sdk, folder)
    return find_name(instances, name)


def list_subnets(sdk, folder):
    service = sdk.client(SubnetServiceStub)
    return service.List(
        ListSubnetsRequest(
            folder_id=folder.id
        )
    ).subnets


def find_subnet(sdk, folder, name):
    subnets = list_subnets(sdk, folder)
    return find_name(subnets, name)


def find_image(sdk, folder, path):
    # standard-images/ubuntu-1604-lts
    folder, family = path.split('/')
    service = sdk.client(ImageServiceStub)
    return service.GetLatestByFamily(
        GetImageLatestByFamilyRequest(
            folder_id=folder,
            family=family
        )
    )


########
#
#   CREATE
#
#########


GB = 1024 * 1024 * 1024

SSH_KEYS = '{user}:{key}'

USER_DATA = '''#cloud-config
datasource:
 Ec2:
  strict_id: false
ssh_pwauth: no
users:
- name: {user}
  sudo: ALL=(ALL) NOPASSWD:ALL
  shell: /bin/bash
  ssh-authorized-keys:
  - {key}
'''


def generate_metadata(user, key):
    if not key or not exists(key):
        raise YcError('no ssh key: %r' % key)

    key = load_text(key)
    yield 'ssh-keys', SSH_KEYS.format(user=user, key=key)
    yield 'user-data', USER_DATA.format(user=user, key=key)


def create_instance_async(sdk, name, memory, cores, disk_size,
                          share=100, spot=True, disk_type=YC_HDD, image=YC_UBUNTU_1604,
                          subnet=YC_SUBNET, folder=YC_FOLDER, platform=YC_PLATFORM,
                          user=SSH_USER, key=SSH_KEY):

    folder = find_folder(sdk, folder)
    subnet = find_subnet(sdk, folder, subnet)
    image = find_image(sdk, folder, image)
    metadata = dict(generate_metadata(user, key))

    service = sdk.client(InstanceServiceStub)
    return service.Create(
        CreateInstanceRequest(
            folder_id=folder.id,
            name=name,
            zone_id=subnet.zone_id,
            platform_id=platform,

            resources_spec=ResourcesSpec(
                memory=memory * GB,
                cores=cores,
                core_fraction=share
            ),

            metadata=metadata,

            boot_disk_spec=AttachedDiskSpec(
                auto_delete=True,
                disk_spec=AttachedDiskSpec.DiskSpec(
                    type_id=disk_type,
                    size=disk_size * GB,
                    image_id=image.id
                )
            ),

            network_interface_specs=[
                NetworkInterfaceSpec(
                    subnet_id=subnet.id,
                    primary_v4_address_spec=PrimaryAddressSpec(
                        one_to_one_nat_spec=OneToOneNatSpec(
                            ip_version=IPV4,
                        )
                    )
                ),
            ],

            scheduling_policy=SchedulingPolicy(
                preemptible=spot
            )
        ))


def create_instance(sdk, *args, callback=None, **kwargs):
    operation = create_instance_async(sdk, *args, **kwargs)
    wait(sdk, operation, callback=callback)


def instance_ip(instance):
    for interface in instance.network_interfaces:
        return interface.primary_v4_address.one_to_one_nat.address


#######
#
#  REMOVE
#
########


def remove_instance_async(sdk, instance):
    service = sdk.client(InstanceServiceStub)
    return service.Delete(
        DeleteInstanceRequest(
            instance_id=instance.id
        )
    )


def remove_instance(sdk, instance, callback=None):
    operation = remove_instance_async(sdk, instance)
    wait(sdk, operation, callback=callback)
