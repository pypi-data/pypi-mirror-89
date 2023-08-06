# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['beet', 'beet.contrib', 'beet.core', 'beet.library', 'beet.toolchain']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=2.11.2,<3.0.0',
 'Pillow>=8.0.1,<9.0.0',
 'click-help-colors>=0.9,<0.10',
 'click>=7.1.2,<8.0.0',
 'nbtlib>=1.8.2,<2.0.0',
 'pathspec>=0.8.1,<0.9.0',
 'pydantic>=1.7.3,<2.0.0']

extras_require = \
{':sys_platform == "win32"': ['colorama']}

entry_points = \
{'console_scripts': ['beet = beet.toolchain.cli:main']}

setup_kwargs = {
    'name': 'beet',
    'version': '0.2.1',
    'description': 'The Minecraft pack development kit',
    'long_description': '# <img src="https://github.com/vberlier/beet/blob/main/docs/assets/logo.svg" alt="beet logo" width="30"> beet\n\n[![GitHub Actions](https://github.com/vberlier/beet/workflows/CI/badge.svg)](https://github.com/vberlier/beet/actions)\n[![PyPI](https://img.shields.io/pypi/v/beet.svg)](https://pypi.org/project/beet/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/beet.svg)](https://pypi.org/project/beet/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n\n> The Minecraft pack development kit.\n\n## Introduction\n\nMinecraft [resource packs](https://minecraft.gamepedia.com/Resource_Pack) and [data packs](https://minecraft.gamepedia.com/Data_Pack) work well as _distribution_ formats but can be pretty limiting as _authoring_ formats. Without the ability to parametrize or create abstractions over assets and data pack resources, the reusability and interoperability of community-created projects and libraries is greatly limited.\n\nThe community is tackling the problem by building independent tooling left and right, from command pre-processors to frameworks of all kinds and full-blown programming languages. However, there\'s no silver bullet and in situations where a combination of these tools could actually provide the most effective workflow, the separate toolchains and the poor interoperability make it difficult for them to coexist.\n\nThe `beet` project is meant to serve as a platform for building a cooperative tooling ecosystem by providing a flexible composition model and a unified, user-friendly development workflow. Higher-level projects should be able to leverage the toolchain and `beet` primitives to reduce their internal complexity and become more interoperable.\n\n### Library\n\n> [Documentation]()\n\n```python\nfrom beet import ResourcePack, Texture\n\nwith ResourcePack(path="stone.zip") as assets:\n    assets["minecraft:block/stone"] = Texture(source_path="custom.png")\n```\n\nThe `beet` library provides carefully crafted primitives for working with Minecraft resource packs and data packs.\n\n- Create, read, edit and merge resource packs and data packs\n- Handle zipped and unzipped packs\n- Fast and lazy by default, files are transparently loaded when needed\n- Statically typed API enabling rich intellisense and autocompletion\n\n### Toolchain\n\n> [Documentation]()\n\n```python\nfrom beet import Context, Function\n\ndef greet(ctx: Context):\n    ctx.data["greet:hello"] = Function(["say hello"], tags=["minecraft:load"])\n```\n\nThe `beet` toolchain is designed to support a wide range of use-cases. The most basic pipeline will let you create configurable resource packs and data packs, but plugins make it easy to implement arbitrarily advanced workflows and tools like linters, asset generators and function pre-processors.\n\n- Compose plugins that can inspect and edit the generated resource pack and data pack\n- Configure flexible build systems for development and creating releases\n- Cache expensive computations and heavy files with a versatile caching API\n- Automatically rebuild the project on file changes with watch mode\n- Link the generated resource pack and data pack to Minecraft\n- First-class template integration approachable without prior Python knowledge\n\n## Installation\n\nThe package can be installed with `pip`.\n\n```bash\n$ pip install beet\n```\n\nYou can make sure that `beet` was successfully installed by trying to use the toolchain from the command-line.\n\n```bash\n$ beet --help\nUsage: beet [OPTIONS] COMMAND [ARGS]...\n\n  The beet toolchain.\n\nOptions:\n  -d, --directory DIRECTORY  Use the specified project directory.\n  -c, --config FILE          Use the specified config file.\n  -v, --version              Show the version and exit.\n  -h, --help                 Show this message and exit.\n\nCommands:\n  build  Build the current project.\n  cache  Inspect or clear the cache.\n  link   Link the generated resource pack and data pack to Minecraft.\n  watch  Watch the project directory and build on file changes.\n```\n\n## Status\n\nYou can expect current releases to be pretty stable, but the project as a whole should still be considered alpha.\n\nThe main reason is that resource pack and data pack coverage is currently lacking in certain areas. Exposing a consistent interface for every data pack and resource pack feature can involve design decisions that aren\'t immediately obvious. You\'re welcome to open an issue to discuss the implementation of currently unsupported resources. And feel free to ask questions, report bugs, and share your thoughts and impressions.\n\n## Contributing\n\nContributions are welcome. Make sure to first open an issue discussing the problem or the new feature before creating a pull request. The project uses [`poetry`](https://python-poetry.org).\n\n```bash\n$ poetry install\n```\n\nYou can run the tests with `poetry run pytest`. We use [`pytest-minecraft`](https://github.com/vberlier/pytest-minecraft) to run tests against actual Minecraft releases.\n\n```bash\n$ poetry run pytest\n$ poetry run pytest --minecraft-latest\n```\n\nWe also use [`pytest-insta`](https://github.com/vberlier/pytest-minecraft) for snapshot testing. Data pack and resource pack snapshots make it easy to monitor and review changes.\n\n```bash\n$ poetry run pytest --insta review\n```\n\nThe project must type-check with [`pyright`](https://github.com/microsoft/pyright). If you\'re using VSCode the [`pylance`](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) extension should report diagnostics automatically. You can also install the type-checker locally with `npm install` and run it from the command-line.\n\n```bash\n$ npm run watch\n$ npm run check\n```\n\nThe code follows the [`black`](https://github.com/psf/black) code style. Import statements are sorted with [`isort`](https://pycqa.github.io/isort/).\n\n```bash\n$ poetry run isort beet tests\n$ poetry run black beet tests\n$ poetry run black --check beet tests\n```\n\n---\n\nLicense - [MIT](https://github.com/vberlier/beet/blob/main/LICENSE)\n',
    'author': 'Valentin Berlier',
    'author_email': 'berlier.v@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vberlier/beet',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
