from typing import Iterator

import black
import click
import pyperclip
from pygments import highlight
from pygments.formatters import get_formatter_by_name
from pygments.lexers import get_all_lexers, get_lexer_by_name
from pygments.styles import get_all_styles, get_style_by_name


def get_short_lexers() -> Iterator[str]:
    for lex in get_all_lexers():
        if len(lex[1]) > 0:
            yield lex[1][0]


@click.command()
@click.option(
    "--language",
    "-l",
    type=click.Choice(list(get_short_lexers()) + ["auto"]),
    help="Programming language to highlight",
    default="python",
)
@click.option("--fontsize", "-f", type=click.INT, help="Fontsize of resulting text", default=60)
@click.option(
    "--style",
    "-s",
    type=click.Choice(list(get_all_styles())),
    help="Theme of resulting text",
    default="solarized-dark",
)
@click.option(
    "--inp",
    "-i",
    type=click.Choice(["clipboard", "editor"]),
    default="clipboard",
    help="What is the source of code",
)
@click.option(
    "--line-width", "-w", type=click.INT, default=100, help="python only. Format code to fit width"
)
def make_highlight(language, fontsize, style, inp, line_width) -> None:
    """
    Highlight code for keynote.app from clipboard and save result to clipboard.

    STYLE Style for code

    FONTSIZE Font size to use

    LANGUAGE Programming language of source code

    INP What is the source of code

    LINE-WIDTH python only. Format code to fit width
    """
    lexer = get_lexer_by_name(language)
    click.echo(f"Using lexer {lexer}")
    code = (
        pyperclip.paste()
        if inp == "clipboard"
        else click.edit(text=pyperclip.paste(), extension=lexer.filenames[0][1:])
    )
    if language == "python":
        code = black.format_str(code, mode=black.Mode(line_length=line_width))
    click.echo(f"Got code from clipboard that starts with {click.style(code[:20], fg='blue')}...")
    res = highlight(
        code,
        lexer,
        get_formatter_by_name("rtf", style=get_style_by_name(style), fontsize=fontsize),
    )
    click.echo("Highlighted")
    pyperclip.copy(res)
    click.echo("Done!")


def main():
    return make_highlight()


if __name__ == "__main__":
    main()
