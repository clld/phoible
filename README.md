PHOIBLE Online
==============

Cite
----

PHOIBLE Online is licensed under a Creative Commons Attribution-ShareAlike 3.0 Unported License. Cite as

  Moran, Steven & McCloy, Daniel & Wright, Richard (eds.) 2014.
  PHOIBLE Online.
  Leipzig: Max Planck Institute for Evolutionary Anthropology.
  (Available online at http://phoible.org) 
  [![DOI](https://zenodo.org/badge/doi/10.5281/zenodo.11706.png)](http://dx.doi.org/10.5281/zenodo.11706)


Install
-------

To get PHOIBLE Online running locally, you need python 2.7 and have to run your system's equivalent to the following bash commands:

```bash
virtualenv --no-site-packages phoible
cd phoible/
. bin/activate
curl -O http://zenodo.org/record/11706/files/phoible-v2014.zip
unzip phoible-v2014.zip
python clld-phoible-8ee231f/fromdump.py
cd phoible/
pip install -r requirements.txt
python setup.py develop
python phoible/scripts/unfreeze.py sqlite.ini
pserve sqlite.ini
```

Then you should be able to access the application by visiting http://localhost:6543 in your browser. Note that you still need an internet connection for the application to download external resources like the map tiles or javascript libraries.




