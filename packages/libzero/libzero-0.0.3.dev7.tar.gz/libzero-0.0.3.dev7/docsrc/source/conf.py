import sys
from pathlib import Path

# Add the repository root to PYTHONPATH
zero_path = Path.cwd()
while not (zero_path.name == 'zero' and zero_path.parent.name != 'zero'):
    zero_path = zero_path.parent
sys.path.append(str(zero_path))
import zero  # noqa

# Project information
author = 'Yura52'
copyright = '2020, Yura52'
project = 'Zero'
release = zero.__version__
version = zero.__version__

# General configuration
default_role = 'py:obj'
templates_path = ['_templates']

# Extensions
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinxcontrib.spelling',
]

autodoc_member_order = 'bysource'
autodoc_typehints = 'description'

autosummary_generate = True

doctest_global_setup = '''
import numpy as np
import torch
from zero import *
'''

intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'numpy': ('https://numpy.org/doc/stable', None),
    'torch': ('https://pytorch.org/docs/stable', None),
    'ignite': ('https://pytorch.org/ignite', None)
}

napoleon_numpy_docstring = False
napoleon_use_admonition_for_examples = False

spelling_show_suggestions = True

# Options for HTML output
pygments_style = 'default'
repo_url = 'https://github.com/Yura52/zero'

# html_theme = 'alabaster'
# html_theme_options = {
#     'fixed_sidebar': True,
#     'github_type': 'star',
#     'github_user': 'Yura52',
#     'github_repo': 'zero',
#     'page_width': '65%',
#     'sidebar_width': '250px'
# }

import sphinx_material  # noqa
html_theme = 'sphinx_material'
html_theme_options = {
    # Full list of options: https://github.com/bashtage/sphinx-material/blob/master/sphinx_material/sphinx_material/theme.conf
    'base_url': repo_url,
    # Full list of colors (not all of them are available in sphinx-material, see theme.conf above):
    # https://squidfunk.github.io/mkdocs-material/setup/changing-the-colors/#primary-color
    'color_primary': 'white',
    'globaltoc_depth': 2,
    # search here for logo icons: https://www.compart.com/en/unicode
    'logo_icon': '&#127968;',
    'nav_links': [],
    'nav_title': project,
    'repo_name': project,
    'repo_url': repo_url,
    'repo_type': 'github',
    'master_doc': False,
    'version_dropdown': True,
    'version_info': {f'{zero.__version__}': ''}
}
html_sidebars = {
    '**': ['logo-text.html', 'globaltoc.html', 'searchbox.html'],
}

# import sphinx_rtd_theme  # noqa
# extensions.append('sphinx_rtd_theme')
# html_theme = 'sphinx_rtd_theme'
# html_theme_options = {
#     'canonical_url': '',
#     'collapse_navigation': False,
#     'prev_next_buttons_location': None,
#     'navigation_depth': -1,
#     'style_nav_header_background': '#343131',  # default sidebar color
# }

# html_theme = 'pydata_sphinx_theme'
# html_theme_options = {
#     'external_links': [],
#     'github_url': repo_url,
#     'navigation_with_keys': False,
#     'show_prev_next': False,
# }
