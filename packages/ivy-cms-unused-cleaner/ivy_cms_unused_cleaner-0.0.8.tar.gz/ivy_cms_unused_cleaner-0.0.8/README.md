# Ivy Used CMS Scanner

## About
Large AxonIvy projects usually have huge number amount of CMSs, and overtime, after countless times
of adding, updating and removing the CMSs, there will be `zoombie` CMSs in your code base.

The idea of this tool is pretty simple:

>In each project:
>  - List out all *.data and co.meta files
>  - Group the *.data files with their corresponding co.meta file
>  - Search the CMS in [*.java, *.drl, *.xhtml, *.mod] files using >  - CMS's path (example: /fintech/soba/authentication/message/accessdenied)
>  - If no result found -> CMS is not being used

_**WARNING:** If the CMS is not hard-coded, it will be `deleted`._

## Installation
`pip install rich`

`pip install ivy_cms_unused_cleaner`

## Usage

Create a Python script

```python
from ivy_cms_unused_cleaner import cms_cleaner
from rich.prompt import Prompt
import os

if __name__ == '__main__':
    path = Prompt.ask("Please enter the absolute path to your project")
    console.print("Process [bold purple]" + path)
    # move to the project folder
    os.chdir(path)
    cleaner = cms_cleaner()
    cleaner.get_all_cms()
    cleaner.get_unused_cms()
```

Run the script

`python cms_scanner.py`

Example output:

![Failed](./images/delete_cms_failed.jpg)

![Success](./images/delete_cms_success.jpg)
