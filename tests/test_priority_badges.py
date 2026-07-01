"""Rendering tests for the priority-badge Markdown extension."""

import markdown

from markdown_priority_badges import PriorityBadgesExtension


def render(text: str, **cfg: object) -> str:
    ext = PriorityBadgesExtension(**cfg)
    return markdown.markdown(text, extensions=["pymdownx.tasklist", ext])


# --- Task-list shorthand (! / !!) -----------------------------------------


def test_single_bang_is_high():
    html = render("- [ ] ! Call vendor")
    assert 'class="task-prio task-prio--high"' in html
    assert "background-color:#ef6c00" in html
    assert ">high<" in html
    assert "Call vendor" in html
    assert "! Call vendor" not in html  # marker stripped


def test_double_bang_is_critical():
    html = render("- [ ] !! Prod is down")
    assert 'class="task-prio task-prio--critical"' in html
    assert "background-color:#d32f2f" in html
    assert "Prod is down" in html


def test_triple_bang_degrades_to_critical():
    html = render("- [ ] !!! Meltdown")
    assert "task-prio--critical" in html


def test_plain_item_has_no_badge():
    html = render("- [ ] Normal task")
    assert "task-prio" not in html


def test_bang_without_space_is_not_shorthand():
    # No space after the bang -> not the list shorthand, and "important" is not
    # a configured level -> no badge at all.
    html = render("- [ ] !important CSS flag")
    assert "task-prio" not in html
    assert "!important CSS flag" in html


def test_done_item_keeps_badge():
    html = render("- [x] !! Rotated keys")
    assert "task-prio--critical" in html
    assert "checked" in html


def test_loose_list_item():
    html = render("- [ ] !! Prod down\n\n- [ ] second\n")
    assert "task-prio--critical" in html


def test_code_block_is_untouched():
    html = render("```\n- [ ] !! not a task\n```\n")
    assert "task-prio" not in html
    assert "!! not a task" in html


# --- Inline keyword (!low / !medium / !high / !critical) -------------------


def test_inline_critical_in_prose():
    html = render("This migration is !critical and blocks the release.")
    assert 'class="task-prio task-prio--critical"' in html
    assert "background-color:#d32f2f" in html
    assert "blocks the release" in html
    assert "!critical" not in html  # keyword consumed


def test_inline_high_in_heading():
    html = render("# !high Rotate the keys")
    assert "<h1" in html
    assert "task-prio--high" in html
    assert "Rotate the keys" in html


def test_inline_all_default_levels():
    html = render("!low !medium !high !critical")
    for level, color in (
        ("low", "#2e7d32"),
        ("medium", "#f9a825"),
        ("high", "#ef6c00"),
        ("critical", "#d32f2f"),
    ):
        assert f"task-prio--{level}" in html
        assert f"background-color:{color}" in html


def test_inline_requires_a_known_keyword():
    # A bare bang, an exclamation, and an unknown word are all left alone.
    html = render("Watch out! Also !important and !blocker are not levels.")
    assert "task-prio" not in html


def test_inline_respects_word_boundaries():
    # Preceded by a word char, or not ending on a boundary -> no match.
    html = render("foo!high and !highest priority")
    assert "task-prio" not in html


def test_inline_not_in_code_span():
    html = render("Use `!critical` verbatim in code.")
    assert "task-prio" not in html
    assert "!critical" in html  # survives inside the code span


def test_badge_text_color_is_auto_contrasted():
    # White on dark red (critical), black on light amber (medium).
    assert "color:#fff" in render("!critical")
    assert "color:#000" in render("!medium")


def test_three_digit_hex_color_is_contrasted():
    html = render("!low !high", levels={"low": "#eee", "high": "#003"})
    assert "background-color:#eee;color:#000" in html  # light -> black
    assert "background-color:#003;color:#fff" in html  # dark -> white


def test_named_color_is_contrasted():
    html = render("!low", levels={"low": "yellow"})
    assert "background-color:yellow;color:#000" in html  # yellow is light


def test_unresolvable_color_falls_back_to_white_text():
    html = render("!low", levels={"low": "rgb(10,10,10)"})
    assert "background-color:rgb(10,10,10);color:#fff" in html


def test_badge_has_title_for_accessibility():
    assert 'title="critical priority"' in render("!critical")
    assert 'title="high priority"' in render("- [ ] ! do it")


# --- Configurable levels ---------------------------------------------------


def test_custom_level_can_be_added():
    html = render("Ship blocker: !blocker now", levels={"blocker": "#7b1fa2"})
    assert 'class="task-prio task-prio--blocker"' in html
    assert "background-color:#7b1fa2" in html
    # Built-in levels still work alongside the custom one.
    assert "task-prio--high" in render("!high", levels={"blocker": "#7b1fa2"})


def test_custom_config_can_override_a_builtin_color():
    html = render("- [ ] ! urgent", levels={"high": "#000000"})
    assert "task-prio--high" in html
    assert "background-color:#000000" in html


def test_unconfigured_keyword_is_not_matched():
    # Without config, "blocker" is not a level, so it is left as plain text.
    html = render("!blocker here")
    assert "task-prio" not in html
    assert "!blocker here" in html
