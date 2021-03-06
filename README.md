# Mimic

Mimic is an interface for bot creation. Utilizing [markovify](https://github.com/jsvine/markovify), a markov-chain text imitation engine. Users can create personas and aliases that link the engine to a profile's markov model, which is iteratively generated from a collection of text files stored as gists.

## Installation

Mimic can be installed locally via `pip`. To get started, clone the repository into a new directory.

```shell
git clone https://github.com/mbowcutt/mimic.git mimic
cd mimic
pip install --editable .
```

This will install the required dependencies. To run the program, start the init file.

```shell
python mimic/__init__.py
```

By default, Mimic will open on http://localhost:5000. If you wish to run mimic at another address or enable other flask developer options, configure them and call flask run:

```shell
export FLASK_APP=mimic/__init__.py
export FLASK_DEBUG=true
flask run --host 0.0.0.0 --port 8080
```