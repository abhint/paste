"""Syntax highlighting helpers (Pygments)."""
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.util import ClassNotFound


def _lexer(paste):
    if paste["lang"] != "auto":
        try:
            return get_lexer_by_name(paste["lang"])
        except ClassNotFound:
            pass
    try:
        if len(paste["content"]) < 100_000:
            return guess_lexer(paste["content"])
    except ClassNotFound:
        pass
    return get_lexer_by_name("text")


def render(paste):
    """Returns (html, language name)."""
    lexer = _lexer(paste)
    return highlight(paste["content"], lexer, HtmlFormatter()), lexer.name


def theme_css():
    """Light colours by default, dark colours when the page is in dark mode."""
    light = HtmlFormatter(style="default").get_style_defs(".highlight")
    dark = HtmlFormatter(style="monokai")
    auto = dark.get_style_defs(':root:not([data-theme="light"]) .highlight')
    forced = dark.get_style_defs(':root[data-theme="dark"] .highlight')
    return f"{light}\n@media (prefers-color-scheme: dark){{\n{auto}\n}}\n{forced}"
