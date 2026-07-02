# Changelog


## Unreleased

## 0.2.0 - 2026-07-01

### Added

- Public parsing API: `LEVELS`, `level_rank(level, levels=LEVELS)`, and `priority_of(text, levels=LEVELS)` for tools that aggregate or filter task items by priority.

## 0.1.0 - 2026-07-01

### Added

- Inline keywords: `!low` / `!medium` / `!high` / `!critical` (and any custom level) render a badge anywhere in prose, headings, or table cells. Only configured level keywords match, so an ordinary `!` in text is untouched.
- Task-list shorthand: a leading `!` (high) / `!!` (critical) after a checkbox renders a priority badge, via a Treeprocessor running just before `pymdownx.tasklist`.
- Configurable `levels` map (name -> color), merged over the built-in `low` / `medium` / `high` / `critical`, so levels can be recolored or added from config.
- Self-contained styling: badges ship inline styles (no external CSS), with the text color auto-contrasted (black or white) against each background.
- Colors accept 3- or 6-digit hex and common CSS names.
