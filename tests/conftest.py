"""Shared pytest configuration for Task 4, written by Amna Wahab.

1. Registers the markers (test groups).
2. Sets the execution order: first by group, then by an optional
   @pytest.mark.case_order(n) number inside a group.
"""

# Execution order of the groups (first item runs first).
GROUP_ORDER = ["group_between", "group_length", "group_email", "group_csv"]

# All markers used by the test files.
MARKERS = GROUP_ORDER + ["bva", "ecp", "negative", "smoke", "case_order(n): explicit run order inside a group"]

def pytest_configure(config):
    """Register the markers so pytest knows them."""
    for marker in MARKERS:
        if ":" not in marker:
            marker = f"{marker}: test group or technique label"
        config.addinivalue_line("markers", marker)


def pytest_collection_modifyitems(items):
    """Sort tests by group, then by case_order. Other tests keep their order."""

    def sort_key(item):
        group_rank = len(GROUP_ORDER)  # tests without a group run last
        for rank, name in enumerate(GROUP_ORDER):
            if item.get_closest_marker(name):
                group_rank = rank
                break
        order_marker = item.get_closest_marker("case_order")
        case_rank = order_marker.args[0] if order_marker else 999
        return (group_rank, case_rank)

    items.sort(key=sort_key)  # sort is stable, so equal keys keep their order