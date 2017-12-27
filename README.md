# Mimic

Text Imitation Engine

## About

Mimic is an identity imitation engine. Select a profile and utter phrases. Upload a collection of text and give it a name to create a profile. Pending frontend development, it will soon be served on [jekyll island](https://jekyll.is/land).

## Developer Installation

Mimic is under active development, so there's no user installer. It will soon be deployed to the WWW, but until then you can build the source via `pip`. To get started, clone the repository.

```shell
git clone https://github.com/mbowcutt/mimic.git mimic
cd mimic
```

It is recommended to develop under a virtual environment. Make sure you have `virtualenv` installed and enter it.

```shell
pip install virtualenv
virtualenv venv
source venv/bin/activate
```

To exit the virtual environment, issue the `deactivate` command. TO re-enter, issue `source venv/bin/activate`

Now install the dependencies.

```shell
pip install flask markovify
```

To run, type

```shell
export FLASK_APP=__init__.py
export FLASK_DEBUG=true
flask run
```

Alternatively, you can use

```shell
python __init__.pyo
```

Then head over to http://127.0.0.1:5000

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

## Contact

Let me know if you have burning questions or ideas! I'd love to hear them. Email me at mbowcutt@case.edu.