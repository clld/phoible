# Releasing the PHOIBLE clld app

```shell
git clone --branch v2.0.1 --depth 1 https://github.com/cldf-datasets/phoible phoible-cldf
git clone --branch v5.3 --depth 1 https://github.com/glottolog/glottolog
git clone https://github.com/clld/phoible
cd phoible
pip install -e .[test]
```

```shell
clld initdb development.ini --cldf ../phoible-cldf/cldf/StructureDataset-metadata.json --glottolog ../glottolog
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
pg_dump -xO --compress gzip:9 phoible > phoible.sql.gz
```

