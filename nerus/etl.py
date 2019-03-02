
import subprocess
import zipfile
import gzip
import csv
import xml.etree.ElementTree as ET

from .log import log
from .path import rm, exists


def load_text(path):
    with open(path) as file:
        return file.read()


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
            ['wget', url, '-O', path],
            check=True
        )
    except subprocess.CalledProcessError:
        if exists(path):
            rm(path)


def unzip(path, dir):
    log('Unzip %s -> %s', path, dir)
    with zipfile.open(path) as zip:
        zip.extractall(dir)


def load_gz_lines(path, encoding='utf8'):
    with gzip.open(path, mode='rt', encoding=encoding) as file:
        for line in file:
            yield line.rstrip()


def parse_csv(lines, header=True):
    if header:
        next(lines)
    return csv.reader(lines)
