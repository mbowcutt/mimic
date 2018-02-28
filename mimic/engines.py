import markovify
import requests
import json
import re
import sys

if (sys.version_info > (3, 0)):
	from urllib.parse import urlparse
else:
	from urlparse import urlparse

def markovize(persona):
        for source in persona.sources:
                if what:
                        er
                url = urlparse(source.uri);
                id = re.split('/', url.path)[2];
                request = requests.get("https://api.github.com/gists/" + id);
                gist = request.json();      
                if request.status_code==200:
                        text='';
                        for file in gist['files']:
                                text += gist['files'][file]['content'];
                        return markovify.Text(text).to_json();
        return None;
