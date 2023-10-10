from dataclasses import dataclass
import requests
import json
from pprint import pprint

# Importing the relevant functions and classes from schema_converter.py
from schema_converter import generate_grammar, SchemaConverter

# Assuming to_json_schema function is imported or defined here
from llm_core.schema import to_json_schema

# Assuming generate_grammar function is imported or defined here
# from your_schema_converter_module import generate_grammar

@dataclass
class Book:
    title: str
    summary: str
    author: str
    published_year: int

    @classmethod
    def schema(cls):
        return to_json_schema(cls)


def parse(text, schema):
    url = "http://localhost:8080/completion"
    headers = {"Content-Type": "application/json"}
    grammar = generate_grammar(schema)  # Make sure generate_grammar is available
    
    prompt = f"""<s>[INST]
    {text}
    [/INST]
    """
    
    data = {
        "prompt": prompt,
        "n_predict": 512,
        "temperature": 0.1,
        "grammar": grammar,
    }
    response = requests.post(url, headers=headers, json=data)
    return json.loads(response.json()["content"])


# Test code
if __name__ == "__main__":
    text = """Foundation is a science fiction novel by American writer
    Isaac Asimov. It is the first published in his Foundation Trilogy (later
    expanded into the Foundation series). Foundation is a cycle of five
    interrelated short stories, first published as a single book by Gnome Press
    in 1951. Collectively they tell the early story of the Foundation,
    an institute founded by psychohistorian Hari Seldon to preserve the best
    of galactic civilization after the collapse of the Galactic Empire.
    """
    
    data = parse(text, Book.schema())
    pprint(data)
