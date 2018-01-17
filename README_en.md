[![Build Status](https://travis-ci.org/AgenciaImplementacion/Asistente-LADM_COL.svg?branch=master)](https://travis-ci.org/AgenciaImplementacion/Asistente-LADM_COL)

# LADM_COL Assistant
[QGIS](http://qgis.org) plugin to capture and maintain data compliant with [LADM_COL](https://github.com/AgenciaImplementacion/LADM_COL) as well as generate [INTERLIS](http://www.interlis.ch/index_e.htm) interchange files (.XTF).

License: [GNU General Public License v3.0](https://github.com/AgenciaImplementacion/Asistente-LADM_COL/blob/master/LICENSE)


A project of: [Agencia de Implementación](https://www.proadmintierra.info/) ([BSF-Swissphoto AG](http://bsf-swissphoto.com/) - [INCIGE SAS](http://www.incige.com/))


## Functionalities

The current version (0.0.2) of the LADM_COL Assistant allows to:

 - Capture data for the LADM_COL v2.2.0 model.
 - Add points to the `Boundary Point` layer from CSV files.
   - Validate and avoid insertion of overlapping points.
 - Define `Boundaries` by digitizing on the map.
   - Aids for digitization:
     - Automatic snapping configuration and default field values.
     - Explode selected lines (split per segment).
     - Merge selected lines.
 - Create `Plot`:
   - From selected boundaries.
   - From a source layer with the same field structure as the `Plot` layer.
 - Fill topology tables automatically:
   - `BFS Points` (relates `Boundary Points` to `Boundary`)
   - `More BFS` (relates `Boundaries` to `Plot`)

## Testing

Unit tests are automatically executed after every commit made to the repository. Results are available for:

- Linux: https://travis-ci.org/AgenciaImplementacion/Asistente-LADM_COL
- Windows: http://portal.proadmintierra.info:18000/

To run the tests locally you need to have *docker* and *docker-compose* installed.
- The version of *docker* that we use can be downloaded from [official site](https://www.docker.com/community-edition#/download), for the development we use Ubuntu / Linux_Mint so we follow steps from
[Install using the convenience script](https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu/#install-using-the-convenience-script).
- The version of *docker-compose* that we use can be installed using the [binaries](https://github.com/docker/compose/releases/tag/1.18.0).

The command to execute unit tests is:
`` `sh
docker-compose run --rm qgis
`` `