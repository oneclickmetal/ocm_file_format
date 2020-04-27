from . import OCMFile

if __name__ == '__main__':
    with OCMFile('tests/test.ocm') as ocmfile:
        params = ocmfile.read_job_description('/3D/model.mprint_job_description')
        print(params)