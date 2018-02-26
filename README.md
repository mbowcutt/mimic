# Mimic

Mimic is an interface for bot creation. Utilizing [markovify](https://github.com/jsvine/markovify), a markov-chain text imitation engine. Users can create personas and aliases that link the engine to a profile's markov model, which is iteratively generated from a collection of text files stored as gists.

## Installation

Mimic can be installed locally via `pip`. To get started, clone the repository into a new directory.

```shell
git clone https://github.com/mbowcutt/mimic.git mimic
cd mimic
pip install --editable .
```

Before we run our application, we must set some environment variables.

```shell
export FLASK_APP=mimic/__init__.py
export FLASK_DEBUG=true
```

Finally, start flask and open http://127.0.0.1:5000.

```shell
flask run
```