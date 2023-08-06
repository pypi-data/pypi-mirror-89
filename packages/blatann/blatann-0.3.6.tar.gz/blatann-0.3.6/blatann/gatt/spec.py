from typing import List
from blatann.uuid import Uuid


class Attribute:
    def __init__(self, uuid: Uuid):
        pass


class Characteristic:
    def __init__(self, uuid: Uuid):
        pass


class Service:
    def __init__(self, uuid: Uuid, characteristics: List[Characteristic] = None):
        self.uuid = uuid
        self.characteristics = characteristics or []

import yaml

class Database(yaml.YAMLObject):
    yaml_tag = "!Database"
    def __init__(self, services: List[Service] = None):
        self.services = services or []


if __name__ == '__main__':
    doc = """
!Database
services:
  - uuid: "deadbeef-0011-2345-6679-ab12ccd4f550"
    characteristics:
      - uuid: "deadbeea-0011-2345-6679-ab12ccd4f550"
        properties: [read, write, notify, indicate, variable_length]
        max_len: 20
        security_level: OPEN
        string_encoding: utf8
      - uuid: "deadbeeb-0011-2345-6679-ab12ccd4f550"
        properties: [read, notify]
        max_len: 23
  - uuid: "ceaf"
    characteristics:
      - uuid: "cddf"
    """
    d = yaml.load(doc)
    print(d)