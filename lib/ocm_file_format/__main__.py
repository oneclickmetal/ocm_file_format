import sys
from . import OCMFile, GCODE_RELATION_TYPE, THUMBNAIL_RELATION_TYPE, JOB_PARAMETERS_RELATION_TYPE, JOB_DESCRIPTION_RELATION_TYPE

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Please provide the file path to the .ocm file as argument")
        exit(1)\

    with OCMFile(sys.argv[1]) as ocmfile:
        gcode_part = ocmfile.read_relationships('/', type=GCODE_RELATION_TYPE)[0].Target

        parameters_part = ocmfile.read_relationships(gcode_part, JOB_PARAMETERS_RELATION_TYPE)[0].Target
        description_part = ocmfile.read_relationships(gcode_part, JOB_DESCRIPTION_RELATION_TYPE)[0].Target
        thumbnail_part = ocmfile.read_relationships(gcode_part, THUMBNAIL_RELATION_TYPE)[0].Target

        parameters = ocmfile.read_job_parameters(parameters_part)
        description = ocmfile.read_job_description(description_part)

        print("Gcode path: ", gcode_part)
        print("Thumbnail path: ", thumbnail_part)
        print("Parameters: ", parameters)
        print("Description: ", description)