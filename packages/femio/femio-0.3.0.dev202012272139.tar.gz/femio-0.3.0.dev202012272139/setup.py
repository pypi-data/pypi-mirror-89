# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['femio',
 'femio.__main__',
 'femio.formats',
 'femio.formats.fistr',
 'femio.formats.obj',
 'femio.formats.stl',
 'femio.formats.ucd',
 'femio.util']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.1,<4.0',
 'meshio>=3.3,<4.0',
 'networkx>=2.4,<3.0',
 'numpy-stl>=2.10,<3.0',
 'numpy>=1.17,<2.0',
 'pandas>=1.0,<2.0',
 'scikit-learn>=0.22.0,<0.23.0',
 'scipy>=1.4,<2.0']

extras_require = \
{'PyQt5': ['PyQt5>=5.14.0,<6.0.0']}

entry_points = \
{'console_scripts': ['femconvert = femio.__main__.femconvert:main']}

setup_kwargs = {
    'name': 'femio',
    'version': '0.3.0.dev202012272139',
    'description': 'FEM I/O Tool',
    'long_description': "# Femio\nThe FEM I/O + mesh processing tool.\n\nFemio can:\n- Read FEM data including analysis results from various formats\n- Perform mesh processing\n- Write FEM data to various formats\n\n\n## How to install\n```bash\npip install femio\n```\n\n\n## How to use\nUsage could be something similar to this:\n\n```python\nimport femio\n\n# Read FEM data of files\nfem_data = femio.FEMData.read_files(file_type='ucd', file_names=['mesh.inp'])\n# Read FEM data in a directory\nfem_data = femio.FEMData.read_directory(file_type='ucd', 'directory/name')\n\n# Access FEM data\nprint(fem_data.nodes.ids, fem_data.entity.nodes.data)  # data means node position here\nprint(fem_data.elements.ids, fem_data.entity.elements.data)  # data means node ids here\nprint(fem_data.nodal_data['DISPLACEMENT'].ids, fem_data.entity.nodal_data['DISPLACEMENT']).data\n\n# Output FEM data to a file format different from the input\nfem_data.write(file_type='stl')\n```\n\nSupported file types:\n- 'fistr': FrontISTR file format\n- 'obj': Wavefront .obj file format\n- 'stl': STereoLithography file format\n- 'ucd': AVS UCD old format\n- 'vtk': VTK format\n\n\n## License\n\n[Apache License 2.0](./LICENSE).\n",
    'author': 'RICOS Co. Ltd.',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ricosjp/femio',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
