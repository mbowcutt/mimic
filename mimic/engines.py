import markovify

def markovize(file):
        text=file.stream.read()
        model = markovify.Text(text.decode("utf-8"))
        return model