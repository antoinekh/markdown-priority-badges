"""Priority badges for Markdown task-list items.

A leading ``!`` / ``!!`` right after the checkbox in a task item renders a
HIGH / CRITICAL badge. One Treeprocessor runs just before
``pymdownx.tasklist`` (priority 26 > 25), so it sees pristine
``[ ] !! text`` list-item text. It strips the marker and prepends a stashed
raw-HTML badge span, leaving the ``[ ]`` checkbox prefix intact for tasklist
to render the checkbox afterwards.
"""

import re
from typing import Any

from markdown import Extension
from markdown.treeprocessors import Treeprocessor

# Checkbox prefix, then a leading run of `!`, then required whitespace. The
# checkbox part mirrors pymdownx.tasklist's own pattern so the same items match.
MARKER_RE = re.compile(
    r"^(?P<checkbox> *\[(?:x|X| )\] +)(?P<bangs>!+)\s+(?P<rest>.*)", re.DOTALL
)

HIGH = "high"
CRITICAL = "critical"


def _level_for(bangs: str) -> str:
    """One bang is HIGH; two or more collapse to CRITICAL."""
    return HIGH if len(bangs) == 1 else CRITICAL


def _badge_html(level: str) -> str:
    return f'<span class="task-prio task-prio--{level}">{level}</span> '


class PriorityTasksTreeprocessor(Treeprocessor):
    """Rewrite task-list items flagged with a leading `!` run into a badge."""

    def _rewrite(self, holder: Any) -> bool:
        m = MARKER_RE.match(holder.text or "")
        if m is None:
            return False
        badge = self.md.htmlStash.store(_badge_html(_level_for(m.group("bangs"))))
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


class PriorityTasksExtension(Extension):
    def extendMarkdown(self, md: Any) -> None:
        md.treeprocessors.register(
            PriorityTasksTreeprocessor(md), "task-list-priority", 26
        )


def makeExtension(**kwargs: Any) -> PriorityTasksExtension:
    return PriorityTasksExtension(**kwargs)
