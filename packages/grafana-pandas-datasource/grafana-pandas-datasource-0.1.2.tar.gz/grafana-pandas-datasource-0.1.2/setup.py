# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['grafana_pandas_datasource']

package_data = \
{'': ['*']}

install_requires = \
['flask-cors>=3.0.9,<4.0.0',
 'flask>=1.1.2,<2.0.0',
 'numpy>=1.19.2,<2.0.0',
 'pandas>=1.1.2,<2.0.0']

setup_kwargs = {
    'name': 'grafana-pandas-datasource',
    'version': '0.1.2',
    'description': 'Serve Pandas dataframes to Grafana',
    'long_description': '#########################\nGrafana Pandas Datasource\n#########################\n\n\n*****\nAbout\n*****\nA REST API based on Flask for serving Pandas Dataframes to Grafana.\n\nThis way, a native Python application can be used to directly supply\ndata to Grafana both easily and powerfully.\n\nIt was inspired by and is compatible with the simple json datasource.\n\nhttps://gist.github.com/linar-jether/95ff412f9d19fdf5e51293eb0c09b850\n\nSetup\n=====\n::\n\n    pip install grafana-pandas-datasource\n\nResources\n=========\n- https://github.com/grafana/grafana\n- https://grafana.com/grafana/plugins/grafana-simple-json-datasource\n\n\n*******\nExample\n*******\nThis is a demo program which generates a sine wave for data and\nannotations for designating midnight times. For both, we are using NumPy.\n\n.. figure:: https://user-images.githubusercontent.com/453543/103137119-78dab480-46c6-11eb-829f-6aa957239804.png\n\n    Image: Sinewave data and midnights annotations, both generated using NumPy.\n\n\nAcquire example files\n=====================\n::\n\n    export EXAMPLES_BASEURL=https://raw.githubusercontent.com/panodata/grafana-pandas-datasource/0.1.0/examples\n\n    wget ${EXAMPLES_BASEURL}/sinewave-midnights/demo.py \\\n        --output-document=sinewave-midnights-demo.py\n\n    wget ${EXAMPLES_BASEURL}/sinewave-midnights/datasource.json \\\n        --output-document=sinewave-midnights-datasource.json\n\n    wget ${EXAMPLES_BASEURL}/sinewave-midnights/dashboard.json \\\n        --output-document=sinewave-midnights-dashboard.json\n\n\nInvoke\n======\n::\n\n    # Run Grafana.\n    docker run --rm -it \\\n        --publish=3000:3000 --volume="$(pwd)/var/lib/grafana":/var/lib/grafana \\\n        --env=\'GF_SECURITY_ADMIN_PASSWORD=admin\' --env=\'GF_INSTALL_PLUGINS=grafana-simple-json-datasource\' \\\n        grafana/grafana:7.3.6\n\n    # Run Grafana Pandas Datasource demo.\n    python sinewave-midnights-demo.py\n\n\nConfigure\n=========\n.. note::\n\n    The host where the datasource service is running can be accessed from the\n    Grafana Docker container using the hostname ``host.docker.internal``.\n\nYou can have a quickstart by putting ``examples/sinewave-midnights/datasource.json``\nand ``examples/sinewave-midnights/dashboard.json`` into Grafana::\n\n    # Login to Grafana.\n    export GRAFANA_URL=http://localhost:3000\n    http --session=grafana ${GRAFANA_URL} --auth=admin:admin\n\n    # Create datasource.\n    cat sinewave-midnights-datasource.json | \\\n        http --session=grafana POST ${GRAFANA_URL}/api/datasources\n\n    # Create dashboard.\n    cat sinewave-midnights-dashboard.json | \\\n        http --session=grafana POST ${GRAFANA_URL}/api/dashboards/db\n\n    open ${GRAFANA_URL}\n',
    'author': 'Andreas Motl',
    'author_email': 'andreas.motl@panodata.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://community.panodata.org/t/grafana-python-datasource-using-pandas-for-timeseries-and-table-data/148',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
