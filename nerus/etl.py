
import subprocess
import zipfile
import gzip
import bz2
import csv
import json
import xml.etree.ElementTree as ET

from .log import log
from .path import rm, exists


def load_text(path):
    with open(path) as file:
        return file.read()


def dump_text(text, path):
    with open(path, 'w') as file:
        file.write(text)


def load_lines(path):
    with open(path) as file:
        for line in file:
            yield line.rstrip('\n')


def dump_lines(lines, path):
    with open(path, 'w') as file:
        for line in lines:
            file.write(line + '\n')


def parse_xml(content):
    return ET.fromstring(content)


def download(url, path):
    log('Download %s -> %s', url, path)
    try:
        subprocess.run(
            ['wget', '--force-directories', '-O', path, url],
            check=True
        )
    except subprocess.CalledProcessError:
        if exists(path):
            rm(path)
        raise


def unzip(path, dir):
    log('Unzip %s -> %s', path, dir)
    with zipfile.open(path) as zip:
        zip.extractall(dir)


def load_gz_lines(path, encoding='utf8', gzip=gzip):
    with gzip.open(path, mode='rt', encoding=encoding) as file:
        for line in file:
            yield line.rstrip()


def load_bz2_lines(path, encoding='utf8'):
    return load_gz_lines(path, encoding=encoding, gzip=bz2)


def parse_csv(lines, header=True):
    if header:
        next(lines)
    return csv.reader(lines)


def serialize_jsonl(items):
    for item in items:
        yield json.dumps(item, ensure_ascii=False)


def parse_jsonl(lines):
    for line in lines:
        yield json.loads(line)


def dump_gz_lines(lines, path):
    with gzip.open(path, 'wt') as file:
        for line in lines:
            file.write(line + '\n')
