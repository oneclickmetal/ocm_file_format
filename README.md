# OCM File Format
This is a file format for OneClickMetal 3D Printers based on the Open Packaging Conventions.
The `example_package` folder contains an unzipped example package. The expected fileending is `.mprint`.

# Contents
## Parts

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


## Relationships

In OPC relationships allow to dynamically find parts in a package even if filenames or locations change.
This is why they are more important than the names of the corresponding files.

A valid file must at least contain one top level relationship pointing to a gcode file.
It may also provide a relationship to a thumbnail for the package.

The G-Code file may have additional relationships to a thumbnail, job parameters or a job description file.

```
                                              +-----------------------+
                                              |                       |
                                              |     Package Root      |
                                              |                       |
                                              +--+-----------------+--+
                                                 |                 |
+-----------------------------------------------------------+      |   +----------------------------+
|                                                |          |      |   |                            |
|                   +----------------------+     |          |      |   |  +----------------------+  |
|                   |                      <-----+          |      +------>                      |  |
|                   |        G-Code        |                |          |  |   Thumbnail (png)    |  |
|                   |                      +------------------------------>                      |  |
|                   +-+----------------+---+                |          |  +----------------------+  |
|                     |                |                    |          |                            |
|                     |                |                    |          |                            |
|                     |                |                    |          |                            |
|  +------------------v---+        +---v------------------+ |          |                            |
|  |                      |        |                      | |          |                            |
|  |   Job Parameters     |        |   Job Description    | |          |                            |
|  |                      |        |                      | |          |                            |
|  +----------------------+        +----------------------+ |          |                            |
|                                                           |          |                            |
|                                                           |          |                            |
|/3D/                                                       |          |/Metadata/                  |
+-----------------------------------------------------------+          +----------------------------+
```

## Job Parameters

The job parameters file is a simple xml file providing process parameters to the machine.

```xml
<?xml version='1.0' encoding='utf-8'?>
<mprint_job_parameters version="0.1" xmlns="http://schemas.oneclickmetal.com/package/2020/relationships/mprint/job_parameters">
  <!--The target level for oxygen in the build chamber in percent, DEFAULT: 0.3-->
  <oxygen_level_target>0.3</oxygen_level_target>
  <!--The allowed offset between real and desired oxygen level. It might not completely reach the desired target DEFAULT: 0.01 -->
  <oxygen_allowed_offset>0.01</oxygen_allowed_offset>
  <!--Layer height-->
  <layer_height>0.05</layer_height>
  <!--Differential pressure for the circulation pump control (0-500)-->
  <circulation_differential_pressure>345</circulation_differential_pressure>
  <!--Oversupply factor for powder coating-->
  <oversupply_factor>2.5</oversupply_factor>
  <!--The material the job was sliced to be printed with-->
  <material>StainlessSteel</material>
</mprint_job_parameters>
```


## Job Description

The job description file is a simple xml file providing additional information for the job.
This information might be shown to the user in the UI.

```xml
<?xml version='1.0' encoding='utf-8'?>
<mprint_job_description version="0.1" xmlns="http://schemas.oneclickmetal.com/package/2020/relationships/mprint/job_description">
  <!--ISO8601 Timestamp specifying the date when the file was generated-->
  <creation_date>2009-01-01T12:00:00+01:00</creation_date>
  <!--Identifier for slicer and its version-->
  <slicer_id>mprep-v0.0.1+4b3e5bf</slicer_id>
  <!--Tracking id-->
  <job_id>9a14926b-9783-482f-ac2a-31d8e3901833</job_id>
  <!--Estimated print time in seconds-->
  <estimated_print_time_seconds>239232</estimated_print_time_seconds>
  <!--powder consumption for the parts in #cartridges -->
  <estimated_powder_consumption>2.7</estimated_powder_consumption>
  <!--Number of layers contained in the job-->
  <layer_count>2314</layer_count>
</mprint_job_description>
```
