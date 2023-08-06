# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['deltalake']

package_data = \
{'': ['*']}

install_requires = \
['azure-storage-blob>=12.6.0,<13.0.0', 'pyarrow>=2.0.0,<3.0.0']

setup_kwargs = {
    'name': 'delta-lake-reader',
    'version': '0.1.0',
    'description': '',
    'long_description': '![Build package](https://github.com/jeppe742/DeltaLakeReader/workflows/Build%20python%20package/badge.svg)\n# Delta Lake Reader\nThe [Delta](https://github.com/delta-io/delta) format, developed by Databricks, is often used to build data lakes.\n\nWhile it tries to solve many issues with data lakes, one of the downsides is that delta tables rely on Spark to read the data. If you only need to read a small table, this can introduce a lot of unnecessary overhead.\n\nThis package tries to fix this, by providing a lightweight python wrapper around the delta file format.\n\n\n\n# Usage\nPackage currently only support local file system, and azure blob storage, but should be easily extended to AWS and GCP in the future.\nThe main entry point should be the `DeltaReader` class. This will try to derrive the underlying file system, based on the input URL.\n\nWhen the class is instantiated, it will try to parse the transaction log files, to find the files in the newest table version. It will, however, not read any data before you run the `to_pyarrow` or `to_pandas` functions.\n## Local file system\n\n```python\nfrom deltalake import DeltaReader\n\n# native file path\ntable_path = "somepath/mytable"\n# Get table as pyarrow table\ndf = DeltaReader(table_path).to_pyarrow()\n# Get table as pandas dataframe\ndf = DeltaReader(table_path).to_pandas()\n\n\n# file url\ntable_path = "file://somepath/mytable"\ndf = DeltaReader(table_path).to_pandas()\n```\n## Azure\nThe Azure integration is based on the [Azure python SDK](https://docs.microsoft.com/en-us/azure/developer/python/azure-sdk-overview). The `credential` used to authenticate against the storage account, can be either a SAS token, Access Keys or one of the `azure.identity` classes ([read more](https://docs.microsoft.com/en-us/python/api/azure-identity/azure.identity?view=azure-python)).\n\nThe input path can either be the https or abfss protocol (will be converted to https under the hood). Note that the current implementation doesn\'t support the `dfs.core.windows.net` api. But you should simply be able to replace dfs with blob.\n```python\nfrom deltalake import DeltaReader\n\ncredential = "..." #SAS-token, Access keys or an azure.identity class\n\n#abfss\ntable_url = "abfss://mycontainer@mystorage.blob.core.windows.net/mytable"\ndf = DeltaReader(table_url, credential).to_pandas()\n\n#https\ntable_url = "https://mystorage.blob.core.windows.net/mycontainer/mytable"\ndf = DeltaReader(table_url, credential).to_pandas()\n```\n\n## Time travel\nOne of the features of the Delta format, is the ability to do timetravel.\n\nThis can be done using the `as_version` property. Note that this currenly only support specific version, and not timestamp.\n```python\nfrom deltalake import DeltaReader\n\ntable_url = "https://mystorage.blob.core.windows.net/mycontainer/mytable"\ncredential = "..."\ndf = DeltaReader(table_url, credential).as_version(5).to_pandas()\n```\n\n\n## Disclaimer\nDatabricks recently announced a stand alone reader for Delta tables in a [blogpost](https://databricks.com/blog/2020/12/22/natively-query-your-delta-lake-with-scala-java-and-python.html)\nThe python bindings mentioned, however, requires you to install the rust library which might sound scary for a python developer.\n\n# Read more\n[Delta transaction log](https://databricks.com/blog/2019/08/21/diving-into-delta-lake-unpacking-the-transaction-log.html)\n',
    'author': 'Jeppe Johan Waarkjær Olsen',
    'author_email': 'jeppe742@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jeppe742/DeltaLakeReader/actions',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
