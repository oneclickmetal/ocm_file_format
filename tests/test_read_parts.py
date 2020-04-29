from os import path

import pytest
from ocm_file_format import OCMFile, PartNotFoundException

TEST_PACKAGE = path.join(path.dirname(__file__), 'test.mprint')

def test_read_gcode():
    with OCMFile(TEST_PACKAGE) as package:
        gcode = package.read_part(package.gcode_part)

    assert gcode == b'G28 X Y\nG1 X1 Y1 F9000'
