"""Module setuptools script based off sc2client-proto."""

import os
import subprocess
import sys
from pathlib import Path
from setuptools import setup
from setuptools.command.install import install
from setuptools.command.develop import develop
from setuptools.command.egg_info import egg_info
from shutil import which


SETUP_DIR = Path(__file__).parent
PROTO_DIR = SETUP_DIR / "w3dclientprotocol"

try:
    protoc = os.environ["PROTOC"]
except KeyError:
    protoc = which("protoc")
if protoc is None or not Path(protoc).exists():
    raise RuntimeError(
        "protoc executable not found! Try debugging your protoc installation, or " \
        "run ./install_protoc.sh or apt-get install -y protobuf-compiler"
    )


def compile_proto(source: str, python_out: str, proto_path: str):
    """Invoke Protocol Compiler to generate python from given source .proto."""
    if not protoc:
        sys.exit('protoc not found. Is the protobuf-compiler installed?\n')

    protoc_command = [
        protoc,
        '--proto_path', proto_path,
        '--python_out', python_out,
        source,
    ]
    
    if subprocess.call(protoc_command) != 0:
        sys.exit(
            "protoc protobuf compilation failed. Ensure protoc is version >= 2.6. " \
            "You can use a custom protoc by setting the PROTOC environment variable."
        )

def build_proto():
    for proto_file in PROTO_DIR.rglob("*.proto"):
        compile_proto(str(proto_file), str(SETUP_DIR), str(SETUP_DIR))
    (PROTO_DIR / "__init__.py").touch()

class ProtoInstallCommand(install):
    def run(self):
        build_proto()
        install.run(self)


class ProtoDevelopCommand(develop):
    def run(self):
        build_proto()
        develop.run(self)


class ProtoEggInfoCommand(egg_info):
    def run(self):
        build_proto()
        egg_info.run(self)

setup(
    name="w3dclientprotocol",
    version="0.0.1",
    description="Warcraft III API - client protocol",
    license="MIT",
    url="https://github.com/W3Droid/w3droid",
    packages=["w3dclientprotocol"],
    install_requires=["protobuf"],
    cmdclass={
        'install': ProtoInstallCommand,
        'develop': ProtoDevelopCommand,
        'egg_info': ProtoEggInfoCommand,
    },
)