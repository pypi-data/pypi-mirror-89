# Football CLI

## Installation

### Build from source

```bash
    shell> git clone https://github.com/amunger3/fb-cli.git
    shell> cd soccer-cli
    shell> python setup.py install
```

### API Token Setup

An API key from [football-data.org](http://api.football-data.org/) will be required and you can register for one [here](http://api.football-data.org/client/register).

You can set the API key using an environment variable or create a file `.fb-cli.ini` in your home folder (`~/.fb-cli.ini`) that contains only your API token, such that:

```bash
    shell> cat ~/.fb-cli.ini
    <API_TOKEN>
```
