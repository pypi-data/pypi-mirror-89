# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['readsql']

package_data = \
{'': ['*']}

install_requires = \
['argparse>=1.4.0,<2.0.0']

entry_points = \
{'console_scripts': ['readsql = readsql.__main__:command_line']}

setup_kwargs = {
    'name': 'readsql',
    'version': '0.1.1',
    'description': 'Convert SQL to most human readable format',
    'long_description': '# readsql\n\nConvert SQL to most human readable format. For the time being it upper cases SQL keywords, it might prettify of even suggest improvements of SQL code in the future. It converts SQL code and even SQL-strings in programming languages (only Python at the moment).\n\nSo if we write\n\n```sql\nselect sushi, avg(price) from tokyo where ocean = \'pacific\' group by sushi\n```\n\nreadsql will help us read it as\n\n```sql\nSELECT sushi, AVG(price) FROM tokyo WHERE ocean = \'pacific\' GROUP BY sushi\n```\n\n# Installation\n\n`pip install readsql`\n\n# Usage\n\n1. Format SQL code provided in command line\n    - `readsql <SQL_STRING> -s`\n2. Format an SQL file or folder\n    - as in a folder, it will look for files ending with .sql or .py\n    - `readsql <FILE_OR_FOLDER_PATH>`\n    \nIt supports multiple strings and files or folders as well\n\n1.\n```bash\nreadsql <SQL_STRING1> <SQL_STRING2> -s\n```\n\n2. In Python files it looks for `query` strings and formats them\n```bash\nreadsql <FILE_OR_FOLDER_PATH1> <FILE_OR_FOLDER_PATH2>\n```\n\nWe can look for different strings in Python files with a `-py` arguments\n```bash\nreadsql <FILE_OR_FOLDER_PATH> -py <PY_VAR1> <PY_VAR2>\n```\n    \n# Usage examples\n\n1. `readsql \'select sushi from tokyo\' -s` command returns\n    - `SELECT sushi FROM tokyo`\n\n2. a. `readsql sql_example.sql` command, while `sql_example.sql` is a SQL file with code as below,\n```sql\nselect max(height), avg(mass), min(age) from jungle group by forest where animal=elephant;\n```\nreplaces the file with this code\n```sql\nSELECT MAX(height), AVG(mass), MIN(age) FROM jungle GROUP BY forest WHERE animal=elephant;\n```\n\n2.c. `readsql sql_in_python_variable_example.py` command, while `sql_in_python_variable_example.py` is a Python file with code as below,\n```python\ndef get_query():\n    limit = 6\n    sql = f"SELEct speed from world where animal=\'dolphin\' limit {limit}"\n    return sql\n```\nreplaces the file with this code\n```python\ndef get_query():\n    limit = 6\n    sql = f"SELECT speed FROM world WHERE animal=\'dolphin\' LIMIT {limit}"\n    return sql\n```\n\n2.c. `readsql sql_in_python_variable_example.py -py sql` command, while `sql_in_python_variable_example.py` is a Python file with code as below,\n```python\ndef get_query():\n    limit = 6\n    sql = f"SELEct speed from world where animal=\'dolphin\' limit {limit}"\n    return sql\n```\nreplaces the file with this code\n```python\ndef get_query():\n    limit = 6\n    sql = f"SELECT speed FROM world WHERE animal=\'dolphin\' LIMIT {limit}"\n    return sql\n```\n\n2.d. `readsql tests -n` command outputs all of the formated SQL code in `tests` folder, files are not replaced by the formatted version (`-n` argument stand for not-replace)\n\n# Add a pre-commit hook\nHow to add a [pre-commit](https://pre-commit.com/) hook of readsql?\n```yaml\nrepos:\n-   repo: https://github.com/AzisK/readsql\n    rev: 0.0.5-alpha # Replace by any tag/version: https://github.com/azisk/readsql/tags\n    hooks:\n    -   id: readsql\n```\n\n# Development\nHaving the repo cloned dig into\n\n- `python -m readsql "select sushi from tokyo" -s` takes the `"select sushi from tokyo"` string as input and outputs it formatted\n- `python -m readsql tests/sql_example.sql` converts example SQL code to easier readable format\n- `python -m readsql tests/sql_in_python_example.py` converts example SQL code in Python (it looks for variables `query`)\n- we can change the SQL variable with `-py` option `python -m readsql tests/sql_in_python_variable_example.py -py sql`\n- `python -m readsql tests` formats all Python and SQL files in `tests` folder\n\n# Testing\n\nHave `pytest` installed and run `pytest -v` (-v stands for verbose)\n',
    'author': 'Azis',
    'author_email': 'azuolas.krusna@yahoo.com',
    'maintainer': 'Azis',
    'maintainer_email': 'azuolas.krusna@yahoo.com',
    'url': 'https://github.com/AzisK/readsql/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
