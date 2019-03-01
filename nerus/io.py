

import xml.etree.ElementTree as ET


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
