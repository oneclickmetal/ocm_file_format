1. GCode - required
    - The gcode that should be executed by the machine. No further transformation will happen.
    - ContentType: text/x-gcode
    - Relation Type: http://schemas.oneclickmetal.com/package/2020/relationships/mprint/gcode
2. Thumbnail - optional
    - A preview image to be displayed by the machine
    - ContentType: image/png
    - Relation Type: http://schemas.openxmlformats.org/package/2006/relationships/metadata/thumbnail
3. Job Parameters - optional (defaults will be used)
    - The process parameters used for the job. E.g. oxygen level.
    - ContentType: application/oneclickmetal.mprint.job_parameters+xml
    - Relation Type: http://schemas.oneclickmetal.com/package/2020/relationships/mprint/job_parameters
4. Job Description - optional
    - Additional information that can be shown to the user or used to calculate job progress.
    - ContentType: application/oneclickmetal.mprint.job_description+xml
    - Relation Type: http://schemas.oneclickmetal.com/package/2020/relationships/mprint/job_description
