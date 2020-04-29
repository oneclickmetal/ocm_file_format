from os import path

import pytest
from ocm_file_format import OCMFile, PartNotFoundException

TEST_PACKAGE = path.join(path.dirname(__file__), 'test.ocm')

def test_read_all_top_level_relationships():
    with OCMFile(TEST_PACKAGE) as package:
        relationships = package.read_relationships('/')

    assert len(relationships) == 2


def test_read_gcode_top_level_relationships():
    with OCMFile(TEST_PACKAGE) as package:
        relationships = package.read_relationships(
            '/',
            'http://schemas.oneclickmetal.com/package/2020/relationships/mprint/gcode'
        )

    assert len(relationships) == 1
    assert relationships[0].Type == 'http://schemas.oneclickmetal.com/package/2020/relationships/mprint/gcode'
    assert relationships[0].Target == '/3D/model.gcode'


def test_read_thumbnail_top_level_relationships():
    with OCMFile(TEST_PACKAGE) as package:
        relationships = package.read_relationships(
            '/',
            'http://schemas.openxmlformats.org/package/2006/relationships/metadata/thumbnail'
        )

    assert len(relationships) == 1
    assert relationships[0].Type == 'http://schemas.openxmlformats.org/package/2006/relationships/metadata/thumbnail'
    assert relationships[0].Target == '/Metadata/thumbnail.png'

def test_read_existing_part_relationships():
    with OCMFile(TEST_PACKAGE) as package:
        relationships = package.read_relationships('/3D/model.gcode')

    assert len(relationships) == 3


def test_read_existing_part_without_relationships():
    with OCMFile(TEST_PACKAGE) as package:
        relationships = package.read_relationships('/Metadata/thumbnail.png')

    assert relationships == []


def test_read_non_existing_part_relationships():
    with OCMFile(TEST_PACKAGE) as package:
        with pytest.raises(PartNotFoundException):
            relationships = package.read_relationships('/3D/doesnt.exist')

