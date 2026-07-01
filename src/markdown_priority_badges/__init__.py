"""Priority badges for Markdown, two ways.

- **Task lists (shorthand):** a leading ``!`` / ``!!`` right after the
  checkbox renders a HIGH / CRITICAL badge. A Treeprocessor runs just before
  ``pymdownx.tasklist`` (priority 26 > 25), so it sees pristine ``[ ] !!
  text`` list-item text; it strips the marker and prepends a stashed raw-HTML
  badge span, leaving the ``[ ]`` checkbox intact for tasklist.
- **Anywhere (inline keyword):** ``!low`` / ``!medium`` / ``!high`` /
  ``!critical`` (and any custom level) in ordinary prose, headings, table
  cells, etc. render the same badge inline. An InlineProcessor matches only
  the configured level keywords, so ordinary ``!`` in text is untouched.

Levels are a name->color map, configurable via the ``levels`` option (merged
over the built-ins). The badge carries its own inline styles, so the extension
is self-contained: no external stylesheet is needed. Badge text color (black
or white) is chosen automatically for legibility against each background.
"""

import re
import xml.etree.ElementTree as etree
from typing import Any

from markdown import Extension
from markdown.inlinepatterns import InlineProcessor
from markdown.treeprocessors import Treeprocessor

# Built-in level -> badge background color. Config `levels` merges over this.
DEFAULT_LEVELS = {
    "low": "#2e7d32",       # green
    "medium": "#f9a825",    # amber
    "high": "#ef6c00",      # orange
    "critical": "#d32f2f",  # red
}

# Task-list shorthand: checkbox prefix, a leading run of `!`, then required
# whitespace. The checkbox part mirrors pymdownx.tasklist's own pattern so the
# same items match. One `!` maps to "high", two or more to "critical".
MARKER_RE = re.compile(
    r"^(?P<checkbox> *\[(?:x|X| )\] +)(?P<bangs>!+)\s+(?P<rest>.*)", re.DOTALL
)

# Shared pill geometry; per-badge background and (auto) text color are appended.
_BADGE_STYLE = (
    "display:inline-block;padding:0.05em 0.45em;margin-right:0.15em;"
    "border-radius:0.35em;font-size:0.62em;font-weight:700;line-height:1.5;"
    "letter-spacing:0.04em;text-transform:uppercase;vertical-align:middle;"
    "-webkit-user-select:none;user-select:none;"
)


def _text_color(bg: str) -> str:
    """Black or white, whichever has the higher WCAG contrast against `bg`
    (a ``#rrggbb`` string). Falls back to white for anything unparseable."""
    if not (len(bg) == 7 and bg.startswith("#")):
        return "#fff"
    try:
        r, g, b = (int(bg[i : i + 2], 16) / 255 for i in (1, 3, 5))
    except ValueError:
        return "#fff"

    def lin(c: float) -> float:
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    lum = 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)
    contrast_black = (lum + 0.05) / 0.05
    contrast_white = 1.05 / (lum + 0.05)
    return "#000" if contrast_black >= contrast_white else "#fff"


def _shorthand_level(bangs: str) -> str:
    """One bang is 'high'; two or more collapse to 'critical'."""
    return "high" if len(bangs) == 1 else "critical"


def _badge_element(level: str, color: str) -> etree.Element:
    """A styled inline badge <span> for `level` on background `color`."""
    el = etree.Element("span")
    el.set("class", f"task-prio task-prio--{level}")
    el.set("style", f"{_BADGE_STYLE}background-color:{color};color:{_text_color(color)};")
    el.text = level
    return el


def _badge_html(level: str, color: str) -> str:
    """The badge as an HTML string with a trailing space (used by the task-list
    treeprocessor via the HTML stash)."""
    return etree.tostring(_badge_element(level, color), encoding="unicode") + " "


class TasklistShorthandTreeprocessor(Treeprocessor):
    """Rewrite task-list items flagged with a leading `!` run into a badge."""

    def __init__(self, md: Any, levels: dict[str, str]) -> None:
        super().__init__(md)
        self.levels = levels

    def _rewrite(self, holder: Any) -> bool:
        m = MARKER_RE.match(holder.text or "")
        if m is None:
            return False
        level = _shorthand_level(m.group("bangs"))
        badge = self.md.htmlStash.store(_badge_html(level, self.levels[level]))
        holder.text = m.group("checkbox") + badge + m.group("rest")
        return True

    def run(self, root: Any) -> None:
        for li in root.iter("li"):
            if self._rewrite(li):
                continue
            # Loose lists wrap the checkbox text in a child <p>.
            if len(li):
                first = next(iter(li))
                if first.tag == "p":
                    self._rewrite(first)


class PriorityInlineProcessor(InlineProcessor):
    """Render an inline `!<level>` keyword as a badge span."""

    def __init__(self, pattern: str, md: Any, levels: dict[str, str]) -> None:
        super().__init__(pattern, md)
        self.levels = levels

    def handleMatch(self, m: Any, data: Any) -> tuple[etree.Element, int, int]:
        level = m.group(1)
        return _badge_element(level, self.levels[level]), m.start(0), m.end(0)


def _inline_re(names: list[str]) -> str:
    """`!<name>` inline-keyword regex for the configured level names: not
    preceded by a word char or another `!`, ending on a word boundary. Longer
    names are tried first so no name shadows a longer one."""
    alts = "|".join(re.escape(n) for n in sorted(names, key=len, reverse=True))
    return rf"(?<![\w!])!({alts})\b"


class PriorityBadgesExtension(Extension):
    def __init__(self, **kwargs: Any) -> None:
        self.config = {
            "levels": [{}, "Level->color map, merged over the built-in defaults"],
        }
        super().__init__(**kwargs)

    def extendMarkdown(self, md: Any) -> None:
        levels = {**DEFAULT_LEVELS, **(self.getConfig("levels", {}) or {})}
        md.treeprocessors.register(
            TasklistShorthandTreeprocessor(md, levels), "priority-badge-tasklist", 26
        )
        md.inlinePatterns.register(
            PriorityInlineProcessor(_inline_re(list(levels)), md, levels),
            "priority-badge-inline",
            185,
        )


def makeExtension(**kwargs: Any) -> PriorityBadgesExtension:
    return PriorityBadgesExtension(**kwargs)
