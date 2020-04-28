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
        self.gcode_part = self.__locate_gcode_file()
        self.thumbnail_part = self.__locate_thumbnail(self.gcode_part)
        self.job_description = self.__read_job_description(self.gcode_part)
        self.job_parameters = self.__read_job_parameters(self.gcode_part)

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


    def __read_xml_to_dict(self, part_path):
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

        return parameter_dict


    def __read_job_parameters(self, gcode_part):
        parameter_parts = self.read_relationships(gcode_part, JOB_PARAMETERS_RELATION_TYPE)
        if not parameter_parts:
            return None

        parameter_dict = self.__read_xml_to_dict(parameter_parts[0].Target)

        return JobParameters(parameter_dict)


    def __read_job_description(self, gcode_part):

        parameter_parts = self.read_relationships(gcode_part, JOB_DESCRIPTION_RELATION_TYPE)
        if not parameter_parts:
            return None

        parameter_dict = self.__read_xml_to_dict(parameter_parts[0].Target)

        return JobDescription(parameter_dict)

    def __locate_gcode_file(self):
        gcode_parts = self.read_relationships('/', GCODE_RELATION_TYPE)
        if not gcode_parts:
            raise PartNotFoundException('No toplevel gcode file found')
        if len(gcode_parts) > 1:
            raise NotImplementedError('Multiple toplevel gcode files are not supported')

        return gcode_parts[0].Target

    def __locate_thumbnail(self, gcode_part):
        gcode_thumbnails = self.read_relationships(gcode_part, THUMBNAIL_RELATION_TYPE)
        # Try toplevel if no thumbnail relationship is found for the gcode part
        if not gcode_thumbnails:
            gcode_thumbnails = self.read_relationships('/', THUMBNAIL_RELATION_TYPE)

        return next((part.Target for part in gcode_thumbnails), None)