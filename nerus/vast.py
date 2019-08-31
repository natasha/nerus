
from time import sleep
import json
import subprocess

from nerus.path import (
    join_path,
    get_dir
)
from nerus.utils import Record


class VastError(Exception):
    pass


def call_vast(*args):
    vast = join_path(get_dir(__file__), 'third', 'vast.py')
    output = subprocess.check_output(('python', vast) + args + ('--raw',))
    return json.loads(output.decode('utf8'))


#########
#
#   SEARCH
#
######


class Offer(Record):
    __attributes__ = ['id', 'cores', 'ram', 'gpu_count', 'gpu_name',
                      'download', 'upload', 'price']

    def __init__(self, id, cores, ram, gpu_count, gpu_name, download, upload, price):
        self.id = id
        self.cores = cores
        self.ram = ram
        self.gpu_count = gpu_count
        self.gpu_name = gpu_name
        self.download = download
        self.upload = upload
        self.price = price


def parse_offers(data):
    #     [{'bundle_id': 87814654,
    #   'bundled_results': 1,
    #   'compute_cap': 750,
    #   'cpu_cores': 16,
    #   'cpu_cores_effective': 16.0,
    #   'cpu_name': 'AMD Ryzen Threadripper 1900X 8-Core Processor',
    #   'cpu_ram': 32103,
    #   'cuda_max_good': 10.0,
    #   'disk_bw': 3133.06342500836,
    #   'disk_name': None,
    #   'disk_space': 198.6,
    #   'dlperf': 77.477698,
    #   'dlperf_per_dphtotal': 96.8471225,
    #   'dph_base': 0.8,
    #   'dph_total': 0.8,
    #   'duration': 730407.148319483,
    #   'end_date': 1567884955.0,
    #   'external': False,
    #   'flops_per_dphtotal': 94.9824,
    #   'gpu_display_active': False,
    #   'gpu_frac': 1.0,
    #   'gpu_lanes': 8,
    #   'gpu_mem_bw': 467.7,
    #   'gpu_name': 'RTX 2080 Ti',
    #   'gpu_ram': 10989,
    #   'has_avx': 1,
    #   'host_id': 82,
    #   'id': 379168,
    #   'inet_down': 416.9,
    #   'inet_down_billed': None,
    #   'inet_down_cost': 0.02,
    #   'inet_up': 38.5,
    #   'inet_up_billed': None,
    #   'inet_up_cost': 0.02,
    #   'is_bid': False,
    #   'logo': '/static/logos/vastai_small2.png',
    #   'machine_id': 335,
    #   'min_bid': 0.6055556,
    #   'mobo_name': 'X399 DESIGNARE EX',
    #   'num_gpus': 4,
    #   'pci_gen': 3.0,
    #   'pcie_bw': 6.1,
    #   'pending_count': 0,
    #   'reliability2': 0.9977864,
    #   'rentable': True,
    #   'rented': False,
    #   'start_date': 1567154462.75266,
    #   'storage_cost': 0.5,
    #   'storage_total_cost': 0.0,
    #   'total_flops': 75.98592,
    #   'webpage': None},
    for item in data:
        yield Offer(
            id=item['id'],
            cores=item['cpu_cores'],
            ram=item['cpu_ram'],
            gpu_count=item['num_gpus'],
            gpu_name=item['gpu_name'],
            download=item['inet_down'],
            upload=item['inet_up'],
            price=item['dph_base']
        )


def list_offers():
    data = call_vast('search offers')
    return parse_offers(data)


def has_one_1080(offer):
    return offer.gpu_count == 1 and 'GTX 1080' in offer.gpu_name


def download_key(offer):
    return -offer.download


def preset_offers(offers):
    offers = filter(has_one_1080, offers)
    return sorted(offers, key=download_key)


GB = 1024


def show_offers(offers):
    pattern = (
        '{id: <8}{cores: >5}{ram: >5}   {gpu: <20}'
        '{download: >5}{upload: >5}{price: >10} {index: <3}'
    )
    print(pattern.format(
        index='', id='id', cores='cpu', ram='ram', gpu='gpu',
        download='down', upload='up', price='$/h')
    )
    for index, offer in enumerate(offers):
        print(pattern.format(
            index=index,
            id=offer.id,
            cores=offer.cores,
            ram=offer.ram // GB,
            gpu='%d x %s' % (offer.gpu_count, offer.gpu_name),
            download='%d' % offer.download,
            upload='%d' % offer.upload,
            price='%.2f' % offer.price
        ))


#######
#
#   CREATE
#
######


LOADING = 'loading'
RUNNING = 'running'


class Instance(Record):
    __attributes__ = ['id', 'status', 'host', 'port', 'label']

    def __init__(self, id, status, host, port, label):
        self.id = id
        self.status = status
        self.host = host
        self.port = port
        self.label = label


def create_instance_async(id, image, disk, label):
    data = call_vast(
        'create instance', str(id),
        '--image', image,
        '--disk', str(disk),
        '--label', label
    )
    if not data.get('success'):
        raise VastError(data)


def parse_instances(data):
    # [{'actual_status': 'loading',
    #   'bundle_id': 87816783,
    #   'compute_cap': 610,
    #   'cpu_cores': 8,
    #   'cpu_cores_effective': 1.0,
    #   'cpu_name': 'Core™ i7-7700K ',
    #   'cpu_ram': 15970,
    #   'cuda_max_good': 10.0,
    #   'cur_state': 'running',
    #   'disk_bw': 537.159689194533,
    #   'disk_name': 'Western WDC',
    #   'disk_space': 15.1,
    #   'dlperf': 8.495015,
    #   'dlperf_per_dphtotal': 82.3592647949908,
    #   'dph_base': 0.1,
    #   'dph_total': 0.103145833333333,
    #   'driver_version': '418.56',
    #   'duration': None,
    #   'end_date': None,
    #   'external': False,
    #   'flops_per_dphtotal': 132.802727529792,
    #   'gpu_display_active': False,
    #   'gpu_frac': 0.125,
    #   'gpu_lanes': 1,
    #   'gpu_mem_bw': 337.6,
    #   'gpu_name': 'GTX 1080 Ti',
    #   'gpu_ram': 11178,
    #   'gpu_temp': None,
    #   'gpu_util': None,
    #   'has_avx': 1,
    #   'host_id': 1276,
    #   'id': 379501,
    #   'image_args': [],
    #   'image_runtype': 'ssh',
    #   'image_uuid': 'natasha/deeppavlov-ner-ru-bert',
    #   'inet_down': 400.1,
    #   'inet_down_billed': None,
    #   'inet_down_cost': 0.02,
    #   'inet_up': 329.3,
    #   'inet_up_billed': None,
    #   'inet_up_cost': 0.02,
    #   'intended_status': 'running',
    #   'is_bid': False,
    #   'jupyter_token': 'dea16c0c970c51657567f59e81187836f27d719cedbf64264923c73a2c2aaf48',
    #   'label': 'nerus',
    #   'logo': '/static/logos/vastai_small2.png',
    #   'machine_id': 838,
    #   'min_bid': 0.1031458,
    #   'mobo_name': 'TB250',
    #   'next_state': 'running',
    #   'num_gpus': 1,
    #   'pci_gen': 2.0,
    #   'pcie_bw': 0.3,
    #   'reliability2': 0.996485,
    #   'rentable': True,
    #   'ssh_host': 'ssh4.vast.ai',
    #   'ssh_idx': '4',
    #   'ssh_port': 19501,
    #   'start_date': 1567157375.79946,
    #   'status_msg': 'ce0014457fab: Download complete\n',
    #   'storage_cost': 0.15,
    #   'storage_total_cost': 0.00314583333333333,
    #   'total_flops': 13.698048,
    #   'webpage': None}]
    for item in data:
        yield Instance(
            id=item['id'],
            status=item['actual_status'],
            host=item['ssh_host'],
            port=item['ssh_port'],
            label=item['label']
        )


def list_instances():
    data = call_vast('show instances')
    return parse_instances(data)


def find_label(instances, label):
    for instance in instances:
        if instance.label == label:
            return instance


def wait_label(label, retries=60, delay=3, callback=None):
    for _ in range(retries):
        instance = find_label(list_instances(), label)
        if instance and instance.status == RUNNING:
            break
        if callback:
            callback()
        sleep(delay)


#########
#
#    REMOVE
#
############


def remove_instance(id):
    data = call_vast('destroy instance', str(id))
    if not data.get('success'):
        raise VastError(data)
