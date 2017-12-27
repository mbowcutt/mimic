# Mimic Me

Text Imitation Engine

## About

Mimic is an identity imitation engine. Select a profile and utter phrases. Upload a collection of text and give it a name to create a profile. Pending frontend development, it will soon be served on [jekyll island](https://jekyll.is/land).

## Installation

Mimic is under active development, so there's no installer. It will soon be deployed to the WWW, but until then you can install it via `pip`. To get started, clone the repository and init the repository.

```shell
git clone https://github.com/mbowcutt/mimmic.git mimic
cd mimic
python __init__.py
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

## Development

To get started developing, set the following variables and start the app:

```shell
export FLASK_APP=__init__.py
export FLASK_DEBUG=true
flask run
```

Navigate over to http://127.0.0.1:5000. Flask will compile the changes in realtime, just `f5` a browser refresh!

## Contact

Let me know if you have burning questions or ideas! I'd love to hear them. Email me at mbowcutt@case.edu.