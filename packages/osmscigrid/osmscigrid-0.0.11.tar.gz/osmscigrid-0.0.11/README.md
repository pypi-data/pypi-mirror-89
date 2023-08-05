# osmscigrid

`osmscigrid` is a Python library to read and filter [OpenStreetMap](https://www.openstreetmap.org) data files in the [Protocol
Buffers (PBF)](https://developers.google.com/protocol-buffers/) format for gas pipelines and export them to a the scigrid_gas class and further  to geojson.

## Install

```console
foo@bar:~$ pip install osmscigrind
```

## Usage

In the following example the prefilter of esy-osmfilter is used to extract all pipelines from Liechtenstein.
The easiest way to run esy-osmfilter is to download the sample.py 
from https://gitlab.com/dlr-ve-esy/esy-osmfilter and run it.
It is quite similar to the more detailed desription below.


In this example, we start by importing all necessary libraries and methods. 

```python

>>> import configparser, contextlib
>>> import os, sys
>>> from esy.osmfilter import osm_colors as CC
>>> from esy.osmfilter import run_filter 
>>> from esy.osmfilter import Node, Way, Relation

```
Thereafter, the IO filepaths are defined, assuming the osm-pbf file is already downloaded.

```python
>>> PBF_inputfile = os.path.join(os.getcwd(),
...                              'tests/input/liechtenstein-191101.osm.pbf')
>>> JSON_outputfile = os.path.join(os.getcwd(),
...                              'tests/output/LI/liechtenstein-191101.json')

```

Alternatively, you could also make use of urllib library to retrieve a OSM file:

```python

>>> import urllib.request
>>> if not os.path.exists('tests/input/liechtenstein-191101.osm.pbf'):
...    filename, headers = urllib.request.urlretrieve(
...        'https://download.geofabrik.de/europe/liechtenstein-191101.osm.pbf',
...        filename='liechtenstein-191101.osm.pbf'
...    )
...    PBF_inputfile = filename

```



In the next step, a prefilter for all pipeline objects is defined.
With the prefilter, we accept all way-items that have "man_made" as key and "pipeline" as value in their taglist.
The white and black filter are left empty for the moment.

```python

>>> prefilter   = {Node: {}, Way: {"man_made":["pipeline",],}, Relation: {}}
>>> whitefilter = []
>>> blackfilter = []

```

The run_filter function will allow to filter for OSM items from a pbf-file. 
We confirm the prefilter phase by setting the boolean variable NewPreFilterData=True. 

```python
>>> [Data,_]=run_filter('noname',
...                     PBF_inputfile, 
...                     JSON_outputfile, 
...                     prefilter,
...                     whitefilter, 
...                     blackfilter, 
...                     NewPreFilterData=True, 
...                     CreateElements=False, 
...                     LoadElements=False,
...                     verbose=True)

```
The prefilter returns the filter results to the `Data` dictionary.
This means all OSM way-items with the tag "man_made"="pipeline" are stored there.
But not enough, additionally, all referenced node items of these pipelines are stored there too.

```python
>>> len(Data['Node'])
13
>>> len(Data['Relation'])
0
>>> len(Data['Way'])
2

```
In this example, we have only found two pipelines and their correspondent 13 nodes.


***PLEASE NOTICE:***  
You can also set *"man_made":True* to accept items independently of a key value.


In the next step we use run_filter to load the `Data` dictionary and specify the main filtering results.
In this example, we use the blackfilter to exclude possible pipelines substations from our prefiltering results.

```python
>>> blackfilter = [("pipeline","substation"),]

```
We further only accept the drain pipelines that have the really great name "Wäschgräbli".

```python
>>> whitefilter =[(("waterway","drain"),("name","Wäschgräble")), ]

```

We initiate the mainfilter phase by setting CreateElements=True.


```python
>>> [_,Elements]=run_filter('funny-waterway-pipelines',
...                            PBF_inputfile, 
...                            JSON_outputfile, 
...                            prefilter,
...                            whitefilter, 
...                            blackfilter, 
...                            NewPreFilterData=False, 
...                            CreateElements=True, 
...                            LoadElements=False,
...                            verbose=True)
>>> len(Elements['funny-waterway-pipelines']['Node'])
0
>>> len(Elements['funny-waterway-pipelines']['Relation'])
0
>>> len(Elements['funny-waterway-pipelines']['Way'])
1

```
We see, that there is only one way-item left in the `Elements` dictionary, the other has been filtered out.
There are no referenced nodes (or relation members) of the remaining way-item passed to the `Elements` dictionary.

However, these are still accessible in the `Data` dictionary.


Esy-osmfilter comes with an export function for GeoJSON files (not implemented for relations yet) which will 
make thinks a lot easier:

```python
>>> from esy.osmfilter import export_geojson
>>> export_geojson(Elements['funny-waterway-pipelines']['Way'],Data,
... filename='test.geojson',jsontype='Line')

```

To visualize the output-file just open http://geojson.io and drag it on the screen.

![image](images/graeble2.png)

For more details, jump to the
[documentation](https://dlr-ve-esy.gitlab.io/esy-osmfilter/).
