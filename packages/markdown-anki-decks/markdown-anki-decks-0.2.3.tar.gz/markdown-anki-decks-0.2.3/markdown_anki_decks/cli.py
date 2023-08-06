import hashlib
import itertools
import os
from pathlib import Path

import frontmatter
import genanki
import markdown
import typer
from bs4 import BeautifulSoup
from genanki.deck import Deck

from markdown_anki_decks.sync import sync_deck
from markdown_anki_decks.utils import print_success

app = typer.Typer()


@app.command("convert")
def convertMarkdown(
    input_dir: Path = typer.Argument(...),
    output_dir: Path = typer.Argument(...),
    sync: bool = typer.Argument(False),
    deck_title_prefix: str = typer.Argument(""),
    delete_cards: bool = typer.Argument(False),
):

    # iterate over the source directory
    for root, _, files in os.walk(input_dir):
        for file in files:
            if is_markdown_file(file):
                deck = parse_markdown(os.path.join(root, file), deck_title_prefix)
                package = genanki.Package(deck)
                # add all image files to the package
                package.media_files = image_files(input_dir)
                path_to_pkg_file = os.path.join(output_dir, f"{Path(file).stem}.apkg")
                package.write_to_file(path_to_pkg_file)
                print_success(f"created apkg for deck {deck.name}")
                if sync:
                    sync_deck(deck, Path(path_to_pkg_file), delete_cards)


def parse_markdown(file: str, deck_title_prefix: str) -> Deck:
    markdown_string = frontmatter.loads(read_file(file)).content
    html = markdown.markdown(
        markdown_string, extensions=["fenced_code", "sane_lists", "tables"]
    )
    soup = BeautifulSoup(html, "html.parser")

    # model for an anki deck
    model = genanki.Model(
        model_id=integer_hash("Simple Model"),
        name="Simple Model",
        fields=[{"name": "Question"}, {"name": "Answer"}, {"name": "Guid"}],
        templates=[
            {
                "name": "Card 1",
                "qfmt": '<div class="card">{{Question}}</div>',
                "afmt": '<div class="card">{{FrontSide}}<hr id="answer">{{Answer}}</div>',
            },
        ],
        css=read_css(),
    )

    # get the deck title
    deck_title = Path(file).stem
    h1 = soup.h1
    if h1 is not None and h1.text:
        deck_title = h1.text
    deck_title = deck_title_prefix + deck_title

    # create the deck
    deck_id = integer_hash(deck_title)
    deck = genanki.Deck(deck_id=deck_id, name=deck_title)

    # add model to deeck
    deck.add_model(model)

    # get the notes
    note_headers = soup.find_all("h2")
    for header in note_headers:
        # the question is the header
        question = header

        # the contents are everything until the next header
        contents = list(
            itertools.takewhile(lambda el: el.name != "h2", header.next_siblings)
        )

        # wrap the contents in a section tag. the section is the answer.
        answer = soup.new_tag("section")
        contents[0].wrap(answer)
        for content in contents[1:]:
            answer.append(content)

        # create the note using the simple model
        note = FrontIdentifierNote(
            deck_id,
            model=model,
            fields=[soup_to_html_string(question), soup_to_html_string(answer)],
        )
        deck.add_note(note)

    return deck


# genanki Note which has a unique id based on the deck and the question
# also has a field for the guid so the guid can be accessed in queries
class FrontIdentifierNote(genanki.Note):
    def __init__(self, deck_id, model=None, fields=None, sort_field=None, tags=None):
        guid = genanki.guid_for(fields[0], deck_id)
        if fields is not None:
            fields.append(guid)
        super().__init__(
            model=model, fields=fields, sort_field=sort_field, tags=tags, guid=guid
        )


# convert beautiful soup object to a string
def soup_to_html_string(soup):
    return soup.prettify(formatter="html5")


# convert a file to a string
def read_file(file):
    with open(file, "r", encoding="utf-8") as f:
        markdown_string = f.read()
    return markdown_string


# check if a file is a markdown file
def is_markdown_file(file):
    # TODO(lukemurray): parameterize markdown extensions?
    return file.endswith(".md")


# convert a string into a random integer from 0 to 1<<31 exclusive
# used to create model and deck ids
# from https://stackoverflow.com/a/42089311/11499360
def integer_hash(s: str):
    return int(hashlib.sha256(s.encode("utf-8")).hexdigest(), 16) % (1 << 31)


# get all the image files in a directory
def image_files(source: Path):
    return list(
        str(p)
        for p in itertools.chain(
            source.rglob("*.jpg"),
            source.rglob("*.jpeg"),
            source.rglob("*.png"),
            source.rglob("*.gif"),
        )
    )


def read_css():
    path = Path(__file__).parent / "./styles/markdown.css"
    return path.read_text("utf-8")


def main():
    app()
