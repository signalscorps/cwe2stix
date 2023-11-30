import logging
import os

from uuid import UUID
from stix2 import FileSystemStore
import xml.etree.ElementTree as ET

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s",  # noqa D100 E501
    datefmt="%Y-%m-%d - %H:%M:%S",
)

namespace = UUID("762246cb-c8a1-53a7-94b3-eafe3ed511c9")

file_system = "stix2_objects"
if not os.path.exists(file_system):
    os.makedirs(file_system)
fs = FileSystemStore("stix2_objects")

raw_data_xml = "data/raw_xml/"
raw_data_json = "data/raw_json/"
cwe2stix_version_filename = "CWE_VERSION"
filename = "cwec_v4.13.xml"
root = None
tree = None
cwe2stix_version = ""

DEFAULT_OBJECT_URL = [
    "https://raw.githubusercontent.com/signalscorps/stix4signalscorps/main/objects/identity/identity--762246cb-c8a1-53a7-94b3-eafe3ed511c9.json",
    "https://raw.githubusercontent.com/signalscorps/stix4signalscorps/main/objects/marking-definition/marking-definition--762246cb-c8a1-53a7-94b3-eafe3ed511c9.json",
    "https://raw.githubusercontent.com/signalscorps/stix4signalscorps/main/objects/extension-definition/extension-definition--51650285-49b2-50ee-916c-20836485532d.json",
]

IDENTITY = "https://raw.githubusercontent.com/signalscorps/stix4signalscorps/main/objects/identity/identity--762246cb-c8a1-53a7-94b3-eafe3ed511c9.json"
MD = "https://raw.githubusercontent.com/signalscorps/stix4signalscorps/main/objects/marking-definition/marking-definition--762246cb-c8a1-53a7-94b3-eafe3ed511c9.json"

EXTENSION_DEFINITION_URL="https://raw.githubusercontent.com/signalscorps/stix4signalscorps/main/objects/extension-definition/extension-definition--51650285-49b2-50ee-916c-20836485532d.json"
default_md_ref= "marking-definition--613f2e26-407d-48c7-9eca-b8e91df99dc9"
# try:
#     with open(cwe2stix_version_filename, 'r') as file:
#         cwe2stix_version = file.read()
# except FileNotFoundError:
#     logging.error(f"File not found: '{cwe2stix_version_filename}'")
# except IOError:
#     logging.error(f"Error reading file: '{cwe2stix_version_filename}'")
#


def read_file(filename):
    try:
        with open(filename) as file:
            content = file.read()
    except FileNotFoundError:
        logging.error(f"File not found: '{filename}'")
    except OSError:
        logging.error(f"Error reading file: '{filename}'")

    # return content


def get_update_file_root():
    if filename and os.path.exists(raw_data_xml):
        tree = ET.parse(raw_data_xml + filename)
    return tree


cwe2stix_version = read_file(cwe2stix_version_filename)
