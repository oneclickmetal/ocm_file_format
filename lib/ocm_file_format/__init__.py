from zipfile import ZipFile
from os.path import basename, dirname, join
import xml.etree.ElementTree as ElementTree

XML_ID_RELATIONSHIP = '{http://schemas.openxmlformats.org/package/2006/relationships}Relationship'

GCODE_RELATION_TYPE = 'http://schemas.oneclickmetal.com/package/2020/relationships/mprint/gcode'
THUMBNAIL_RELATION_TYPE = 'http://schemas.openxmlformats.org/package/2006/relationships/metadata/thumbnail'
JOB_PARAMETERS_RELATION_TYPE = 'http://schemas.oneclickmetal.com/package/2020/relationships/mprint/job_parameters'
JOB_DESCRIPTION_RELATION_TYPE = 'http://schemas.oneclickmetal.com/package/2020/relationships/mprint/job_description'


class PartNotFoundException(Exception):
    pass


class FromDict:
    def __init__(self, dict):
        self.__dict__ = dict

    def __repr__(self):
        return self.__class__.__name__ + ': ' +  self.__dict__.__repr__()


class Relationship(FromDict):
    pass


class JobParameters(FromDict):
    pass


class JobDescription(FromDict):
    pass


class OCMFile:
    def __init__(self, filename):
        self.filename = filename

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, *args):
        self.close()

    def open(self):
        self.file = ZipFile(self.filename)

    def close(self):
        self.file.close()

    def read_relationships(self, part, type=None):
        if part[:1] != '/':
            raise NotImplementedError('relative part paths are not supported')
        # Strip the leading slash as this is how zipfile module handles paths
        part = part[1:]

        # and there is only one special case for
        # non part related relationships -> the package
        # otherwise check if file exists
        if part != '':
            try:
                part_info = self.file.getinfo(part)
                if part_info.is_dir():
                    raise PartNotFoundException(f'Part "/{part}" is a directory, no file.')
            except KeyError:
                raise PartNotFoundException(f'Part "/{part}" does not exist in package')

        relationships_file = join(dirname(part), '_rels', f'{basename(part)}.rels')
        if relationships_file not in self.file.namelist():
            return []

        relationships_file_content = self.file.read(relationships_file)
        relationships_xml = ElementTree.fromstring(relationships_file_content)
        relationships_for_file = [
            Relationship(element.attrib) for element in relationships_xml.findall(XML_ID_RELATIONSHIP)
        ]

        return [
            relation for relation in relationships_for_file
            if type is None or relation.Type == type
        ]


    def read_job_parameters(self, part_path):
        # TODO Check file ending + mimetype
        part_path = part_path[1:]

        try:
            parameters_xml_string = self.file.read(part_path)
        except KeyError:
            raise PartNotFoundException(f'Part "/{part_path}" does not exist in package')

        parameter_dict = {}

        parameters = ElementTree.fromstring(parameters_xml_string)
        for param in parameters:
            _, _, tag_without_namespace = param.tag.rpartition('}')
            parameter_dict[tag_without_namespace] = param.text

        return JobParameters(parameter_dict)


    def read_job_description(self, part_path):
        # TODO Check file ending + mimetype
        part_path = part_path[1:]

        try:
            parameters_xml_string = self.file.read(part_path)
        except KeyError:
            raise PartNotFoundException(f'Part "/{part_path}" does not exist in package')

        parameter_dict = {}

        parameters = ElementTree.fromstring(parameters_xml_string)
        for param in parameters:
            _, _, tag_without_namespace = param.tag.rpartition('}')
            parameter_dict[tag_without_namespace] = param.text

        return JobDescription(parameter_dict)

