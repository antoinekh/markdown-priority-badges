# Changelog

All notable changes are documented here. This project follows [Keep a Changelog](https://keepachangelog.com/) and [Semantic Versioning](https://semver.org/).

## Unreleased

### Added

- Task-list shorthand: a leading `!` (high) / `!!` (critical) after a checkbox renders a priority badge, via a Treeprocessor running just before `pymdownx.tasklist`.
- Inline keywords: `!low` / `!medium` / `!high` / `!critical` (and any custom level) render a badge anywhere in prose, headings, or table cells.
- Configurable `levels` map (name -> color), merged over the built-in `low` / `medium` / `high` / `critical`, so levels can be recolored or added from config.
- Self-contained styling: badges ship inline styles (no external CSS), with the text color auto-contrasted (black or white) against each background.
- Colors accept 3- or 6-digit hex and common CSS names.
