# markdown-priority-badges

A Python-Markdown extension that renders **priority badges** two ways: `!level` keywords inline anywhere, and a `!` / `!!` shorthand on task-list items. Works in Zensical, MkDocs, or plain Python-Markdown. The badge ships its own inline styles, so no external CSS is required.

## Syntax

Inline keywords (`!low` / `!medium` / `!high` / `!critical`), anywhere (prose, headings, table cells):

```markdown
This migration is !critical and blocks the release.

## !high Rotate the keys
```

Only the configured level keywords match, so an ordinary `!`, `!important`, or `!highest` in text is never touched.

Task-list shorthand, a simplified form for checkbox items (one `!` = high, two or more = critical):

```markdown
- [ ] ! Call the vendor back      <!-- HIGH badge -->
- [ ] !! Prod is down             <!-- CRITICAL badge -->
- [x] !! Rotated the keys         <!-- CRITICAL badge on a done item -->
- [ ] Normal task                 <!-- no badge -->
```

The shorthand marker must come first (right after the checkbox) and be followed by a space, so `- [ ] !important note` is left untouched. Works with `-`, `*`, `+` bullets and both `[ ]` / `[x]` states.

## Levels

Built-in levels (name → background color):

| Level      | Color            |
| ---------- | ---------------- |
| `low`      | green `#2e7d32`  |
| `medium`   | amber `#f9a825`  |
| `high`     | orange `#ef6c00` |
| `critical` | red `#d32f2f`    |

The `!` / `!!` task-list shorthand always maps to `high` / `critical`; lower levels are used via their inline keyword (`!low`, `!medium`). Badge text color (black or white) is chosen automatically for legibility against each background.

### Custom / extra levels

The `levels` option is a name → color map that is **merged over** the built-ins, so you can recolor a level or add your own:

```toml
# zensical.toml
[project.markdown_extensions.markdown_priority_badges.levels]
blocker = "#7b1fa2"
low     = "#1b5e20"
```

```python
# plain Python-Markdown
from markdown_priority_badges import PriorityBadgesExtension
markdown.markdown(text, extensions=["pymdownx.tasklist", PriorityBadgesExtension(levels={"blocker": "#7b1fa2"})])
```

Colors may be 3- or 6-digit hex (`#7b1fa2`, `#eee`) or a common CSS name (`red`, `yellow`, `rebeccapurple`); the badge text color auto-contrasts against them.

## Install & enable

```bash
uv pip install -e /path/to/markdown-priority-badges
```

Zensical (`zensical.toml`):

```toml
[project.markdown_extensions.markdown_priority_badges]
```

Plain Python-Markdown:

```python
markdown.markdown(text, extensions=["pymdownx.tasklist", "markdown_priority_badges"])
```

The badge renders as `<span class="task-prio task-prio--<level>" style="...">...</span>`. The `task-prio` classes are kept for optional site-side overriding, but no CSS is needed by default.
