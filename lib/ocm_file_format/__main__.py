import sys
from . import OCMFile, GCODE_RELATION_TYPE, THUMBNAIL_RELATION_TYPE, JOB_PARAMETERS_RELATION_TYPE, JOB_DESCRIPTION_RELATION_TYPE

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Please provide the file path to the .ocm file as argument")
        exit(1)\

    with OCMFile(sys.argv[1]) as ocmfile:
        print("Gcode path: ", ocmfile.gcode_part)
        print("Thumbnail path: ", ocmfile.thumbnail_part)
        print("Parameters: ", ocmfile.job_parameters)
        print("Description: ", ocmfile.job_description)