Useful utils for [gist.cafe](https://gist.cafe) Python Apps.

## Usage

Simple usage example:

```python
import requests
import operator

from dataclasses import dataclass, field
from dataclasses_json import config, dataclass_json, Undefined
from typing import Optional
from gistcafe import inspect

@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class GithubRepo:
    name: str
    description: Optional[str] = None
    homepage: Optional[str] = None
    lang: Optional[str] = field(metadata=config(field_name="language"),default=None)
    watchers: Optional[int] = 0
    forks: Optional[int] = 0

orgName = "python"
response = requests.get(f'https://api.github.com/orgs/{orgName}/repos')
orgRepos = GithubRepo.schema().loads(response.text, many=True)
orgRepos.sort(key=operator.attrgetter('watchers'), reverse=True)

inspect.printdump(orgRepos[0:3])
print('')
inspect.printdumptable(orgRepos[0:10],headers=['name','lang','watchers','forks'])

inspect.vars({ 'orgRepos': orgRepos })
```

Which outputs:

```
[
    {
        name: mypy,
        description: Optional static typing for Python 3 and 2 (PEP 484),
        homepage: http://www.mypy-lang.org/,
        lang: Python,
        watchers: 9637,
        forks: 1564
    },
    {
        name: peps,
        description: Python Enhancement Proposals,
        homepage: https://www.python.org/dev/peps/,
        lang: Python,
        watchers: 2458,
        forks: 921
    },
    {
        name: typeshed,
        description: Collection of library stubs for Python, with static types,
        homepage: ,
        lang: Python,
        watchers: 1942,
        forks: 972
    }
]

| name         | lang      |   watchers |   forks |
|--------------|-----------|------------|---------|
| mypy         | Python    |       9637 |    1564 |
| peps         | Python    |       2458 |     921 |
| typeshed     | Python    |       1942 |     972 |
| pythondotorg | Python    |       1038 |     432 |
| asyncio      |           |        945 |     178 |
| typing       | Python    |        840 |     130 |
| raspberryio  | Python    |        217 |      38 |
| typed_ast    | C         |        171 |      43 |
| planet       | Python    |        100 |     145 |
| psf-salt     | SaltStack |         87 |      50 |
```

## Features and bugs

Please file feature requests and bugs at the [issue tracker](https://github.com/ServiceStack/gistcafe-pyhon/issues).