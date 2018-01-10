# Mimic

Mimic is a simple UI for bot profile creation. At the moment, mimic features [markovify](https://github.com/jsvine/markovify), a markov-chain text imitation engine. Users can create personas and aliases that link the engine to a profile's markov model, which is iteratively generated from a collection of text files.

## Installation

Mimic can be installed locally via `pip`. To get started, clone the repository into a new directory.

```shell
git clone https://github.com/mbowcutt/mimic.git mimic
cd mimic
```

From here, enter your [virtualenv](#using-virtual-environments) environment and install.

```shell
source VENV_DIRECTORY/bin/activate
pip install .
```

Before we run our application, we must set some environment variables.

```shell
export FLASK_APP=mimic/__init__.py
export FLASK_DEBUG=true
```

Finally, run

```shell
flask run
```

Then head over to http://127.0.0.1:5000.

## Contributing

There's many things Mimic needs at the moment, the biggest of which is a stable frontend, but also:

- Account creation could use pictures and additional metainformation.
- Database overhaul
- Complete PyPi/Pip packaging
- Option for alternative text generation engines other than Markovify
- Enrollment for User Profiles/Text Generation Engines
- Engines for alternative media types (images, audio, etc)
- Implement ReactXP
- Implement IPFS
- Implement HTTPS

## Using Virtual Environments

It is recommended to develop under a virtual environment. Make sure you have `virtualenv` installed.

```shell
pip install virtualenv
```

Then create a new environment. By default, the git repository will ignore the venv/ directory, but this can be conifigured in .gitignore

```shell
virtualenv venv
source venv/bin/activate
```

To exit the virtual environment, issue the `deactivate` command. TO re-enter, issue `source venv/bin/activate`

## Contact

Let me know if you have burning questions or ideas! I'd love to hear them. Email me at mbowcutt@case.edu.