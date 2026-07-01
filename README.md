# zensical-tasklist-priority

A Python-Markdown / Zensical extension that turns a leading `!` / `!!` on a task-list item into a priority badge.

## Syntax

```markdown
- [ ] ! Call the vendor back      <!-- HIGH badge -->
- [ ] !! Prod is down             <!-- CRITICAL badge -->
- [x] !! Rotated the keys         <!-- CRITICAL badge on a done item -->
- [ ] Normal task                 <!-- no badge -->
```

One `!` is HIGH, two or more is CRITICAL. The marker must come first (right after the checkbox) and be followed by a space, so `- [ ] !important note` is left untouched. Works with `-`, `*`, `+` bullets and both `[ ]` / `[x]` states.

It renders `<span class="task-prio task-prio--high|critical">...</span>` right after the checkbox; style `.task-prio` in your site CSS.

## Install & enable

```bash
uv pip install -e /path/to/zensical-tasklist-priority
```

Zensical (`zensical.toml`):

```toml
[project.markdown_extensions.zensical_tasklist_priority]
```

Plain Python-Markdown:

```python
markdown.markdown(text, extensions=["pymdownx.tasklist", "zensical_tasklist_priority"])
```
