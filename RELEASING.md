# Releasing the PHOIBLE clld app

```shell
git clone https://github.com/cldf-datasets/phoible phoible-cldf
git -C phoible-cldf checkout v2.0.1
git clone https://github.com/clld/phoible
cd phoible
pip install -e .[test]
```

```shell
clld initdb development.ini --cldf ../phoible-cldf/cldf/StructureDataset-metadata.json --glottolog ../../glottolog/glottolog
```

```shell
pytest
```

Store the tested requirements:
```shell
pip freeze > requirements.txt
```

Store a db dump:
```shell
pg_dump -xO phoible > phoible.sql
zip phoible.sql.zip phoible.sql
rm phoible.sql
```
