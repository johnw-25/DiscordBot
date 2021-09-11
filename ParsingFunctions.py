import re


def get_quote(input_string):
    quote = re.findall('"([^"]*)"', input_string)
    return quote


def get_author(input_string):
    author = input_string.split("-")
    if len(author) > 1:
        author = author[1]
        return author
    else:
        return ''
