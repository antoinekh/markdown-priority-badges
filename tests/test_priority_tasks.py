"""Rendering tests for the task-list priority-badge extension."""

import markdown

from zensical_tasklist_priority import PriorityTasksExtension


def render(text: str) -> str:
    return markdown.markdown(
        text, extensions=["pymdownx.tasklist", PriorityTasksExtension()]
    )


def test_single_bang_is_high():
    html = render("- [ ] ! Call vendor")
    assert 'class="task-prio task-prio--high"' in html
    assert ">high<" in html
    assert "Call vendor" in html
    assert "! Call vendor" not in html  # marker stripped


def test_double_bang_is_critical():
    html = render("- [ ] !! Prod is down")
    assert 'class="task-prio task-prio--critical"' in html
    assert "Prod is down" in html


def test_triple_bang_degrades_to_critical():
    html = render("- [ ] !!! Meltdown")
    assert "task-prio--critical" in html


def test_plain_item_has_no_badge():
    html = render("- [ ] Normal task")
    assert "task-prio" not in html


def test_bang_without_space_is_not_a_marker():
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
