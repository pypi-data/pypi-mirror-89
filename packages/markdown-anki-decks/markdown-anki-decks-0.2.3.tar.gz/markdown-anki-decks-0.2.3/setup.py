# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['markdown_anki_decks']

package_data = \
{'': ['*'], 'markdown_anki_decks': ['styles/*']}

install_requires = \
['Markdown>=3.3.3,<4.0.0',
 'beautifulsoup4>=4.9.3,<5.0.0',
 'colorama>=0.4.4,<0.5.0',
 'genanki>=0.10.1,<0.11.0',
 'python-frontmatter>=0.5.0,<0.6.0',
 'shellingham>=1.3.2,<2.0.0',
 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['mdankideck = markdown_anki_decks.cli:main']}

setup_kwargs = {
    'name': 'markdown-anki-decks',
    'version': '0.2.3',
    'description': 'A command line program to convert markdown files into anki decks.',
    'long_description': '# markdown-anki-decks\n\n![PyPI](https://img.shields.io/pypi/v/markdown-anki-decks)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/markdown-anki-decks)\n![PyPI - License](https://img.shields.io/pypi/l/markdown-anki-decks)\n\nMarkdown anki decks is a simple program to convert markdown files into anki decks.\n\n```md\n# The h1 tag is the deck title\n\n## The h2 tags are the questions\n\nThe markdown content between h2 tags are the answers.\n```\n\nMarkdown anki decks uses the question to uniquely identify the card.\nYou can change the card contents without losing your progress on the card.\nMarkdown anki decks can be reimported without creating duplicates.\n\n## Installation\n\nMake sure you have a python version of 3.7 or greater installed.\n\n`pip install markdown-anki-decks`\n\nThis will install the `mdankideck` cli tool.\n\n## Tutorial\n\nMarkdown anki decks converts all markdown files in an input directory to `apkg` files.\nThe `apkg` files are stored in an output directory.\n\n1. Create the input directory `mkdir input`.\n2. Create the output directory `mkdir output`.\n3. Create a markdown file in the input directory.\n\n   ```md\n   <!-- input/deck.md -->\n\n   # Deck Title\n\n   ## Card Title\n\n   card contents.\n\n   ## Second Card Title\n\n   card contents 2.\n   ```\n\n4. Run `mdankideck input output` to convert the markdown files in the input directory to `apkg` files in the output directory.\n5. Import `apkg` files as decks into anki.\n\n## Usage\n\nRun `mdankideck input output` to convert the markdown files in the input directory to `apkg` files in the output directory.\n\n```\nArguments:\n  INPUT_DIR            [required]           The input directory containing markdown files. Browsed recursively.\n  OUTPUT_DIR           [required]           The output directory for storing apkg files.\n  [SYNC]               [default: False]     Whether to sync the decks to anki\n  [DECK_TITLE_PREFIX]  [default: ]          A prefix added to every deck title\n  [DELETE_CARDS]       [default: False]     Whether to delete cards from anki during sync. If sync is false this has no effect.\n```\n\n### Syncing\n\nMarkdown anki decks can use [AnkiConnect](https://ankiweb.net/shared/info/2055492159) to sync the created decks immediately to anki.\nFirst you need to install AnkiConnect as an add on in Anki.\nThen you need to set the Sync Argument to true.\nBy default if you delete a question in markdown we do not delete the question in Anki during sync.\nHowever you can delete missing questions in Anki during sync by setting Delete cards to true.\n\nIf you see an error message `Unable to reach anki connect. Make sure anki is running and the Anki Connect addon is installed.`, make sure you have installed anki connect and that you are running anki.\n\n### Subdecks\n\nYou can use the Deck title prefix option to make all your markdown decks part of a single subdeck.\nAnki automatically creates subdecks based on deck names.\n\n> Decks can contain other decks, which allows you to organize decks into a tree. Anki uses “::” to show different levels. A deck called “Chinese::Hanzi” refers to a “Hanzi” deck, which is part of a “Chinese” deck. If you select “Hanzi” then only the Hanzi cards will be shown; if you select “Chinese” then all Chinese cards, including Hanzi cards, will be shown. [Source](https://docs.ankiweb.net/#/getting-started?id=decks)\n\nI use a prefix `md::` to store all my markdown decks in a subdeck called `md`.\n\n### Images\n\nMarkdown anki decks support images which are stored in the same folder as the markdown file they are referenced by.\n\n`![my-image](image.jpg)` will work because it is in the same folder as the markdown file.\n\n`![my-image](./images/image.jpg)` will not work because it is in a different folder than the markdown file.\n\nAll images must have unique filenames even if they are stored in different folders.\n\nThese are limitations of anki not Markdown anki decks.\n\n## Limitations\n\nMarkdown anki decks makes some assumptions to enable syncing.\nCards are uniquely identified by their deck name and question.\nIf you change the deck name or the question you will lose the card history.\nAll deck names must be unique.\nAll questions in a single deck must be unique.\nIdentical questions in separate decks are ok.\n\n## Design\n\nThe markdown files are parsed with [python-markdown](https://pypi.org/project/Markdown/). The resulting html is then parsed with [beautifulsoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/).\nFinally the cards are created with [genanki](https://github.com/kerrickstaley/genanki).\nThe cli is implemented using [typer](https://github.com/tiangolo/typer) and the program is packaged using [poetry](https://github.com/python-poetry/poetry).\n\n## Contributing\n\nHappy to discuss additional features if you open up an issue.\n\nWe use commitizen for commits.\nRun `poetry run cz commit` to make a commit.\n\nRun `poetry run mdankideck testData/input testData/output True "test::" True` to convert the test data into decks.\n\n### Releases\n\nRun `poetry run cz bump --check-consistency` to update the changelog and create a tag.\n\nRun `poetry publish --build` to publish the pack to pypi.\n\n`git push --tags && git push` to update github.\n',
    'author': 'Luke Murray',
    'author_email': 'lukepigeonmail@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/lukesmurray/markdown-anki-decks',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)
