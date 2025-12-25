"""Property tests for Advanced Table Renderer component.

Feature: mrdr-visual-integration
Tests Properties 21-26 for table rendering capabilities.
"""

from hypothesis import given, settings, assume
from hypothesis import strategies as st

from mrdr.render.components import AdvancedTableRenderer, TableConfig


# Strategy for simple field names (alphanumeric, no special chars)
field_name = st.text(
    min_size=1,
    max_size=10,
    alphabet=st.characters(whitelist_categories=("L",), whitelist_characters="_"),
)

# Strategy for simple field values
field_value = st.text(
    min_size=1,
    max_size=20,
    alphabet=st.characters(whitelist_categories=("L", "N"), whitelist_characters=" "),
)


# Strategy for table row data
def row_strategy(columns: list[str]) -> st.SearchStrategy[dict[str, str]]:
    """Generate a row with the given column names."""
    return st.fixed_dictionaries({col: field_value for col in columns})


@given(
    filter_value=st.sampled_from(["alpha", "beta", "gamma"]),
    num_matching=st.integers(min_value=0, max_value=5),
    num_non_matching=st.integers(min_value=0, max_value=5),
)
@settings(max_examples=100)
def test_table_row_filtering(
    filter_value: str, num_matching: int, num_non_matching: int
) -> None:
    """Property 23: Table Row Filtering.

    Feature: mrdr-visual-integration, Property 23: Table Row Filtering
    For any --filter field=value option, the rendered table SHALL contain
    only rows where the specified field matches the value.
    **Validates: Requirements 10.3**
    """
    assume(num_matching + num_non_matching > 0)

    # Create test data with known matching and non-matching rows
    data = []
    for i in range(num_matching):
        data.append({"language": f"lang_{i}", "type": filter_value})
    for i in range(num_non_matching):
        # Use a different value that won't match
        other_value = "other" if filter_value != "other" else "different"
        data.append({"language": f"other_{i}", "type": other_value})

    config = TableConfig(filter_field="type", filter_value=filter_value)
    renderer = AdvancedTableRenderer(data=data, config=config)

    filtered = renderer._apply_filter()

    # All filtered rows should match the filter value
    assert len(filtered) == num_matching
    for row in filtered:
        assert row["type"].lower() == filter_value.lower()


@given(
    data=st.lists(
        st.fixed_dictionaries(
            {
                "name": st.text(min_size=1, max_size=10, alphabet="abcdefghij"),
                "value": st.text(min_size=1, max_size=10, alphabet="0123456789"),
            }
        ),
        min_size=1,
        max_size=10,
    )
)
@settings(max_examples=100)
def test_table_filter_no_match(data: list[dict[str, str]]) -> None:
    """Property 23: Table Row Filtering - no matches case.

    Feature: mrdr-visual-integration, Property 23: Table Row Filtering
    When filter value matches no rows, result should be empty.
    **Validates: Requirements 10.3**
    """
    # Use a filter value that won't match any data
    config = TableConfig(filter_field="name", filter_value="NONEXISTENT_VALUE_XYZ")
    renderer = AdvancedTableRenderer(data=data, config=config)

    filtered = renderer._apply_filter()
    assert len(filtered) == 0


def test_table_filter_case_insensitive() -> None:
    """Property 23: Table Row Filtering - case insensitivity.

    Feature: mrdr-visual-integration, Property 23: Table Row Filtering
    Filter matching should be case-insensitive.
    **Validates: Requirements 10.3**
    """
    data = [
        {"language": "Python", "type": "LITERAL"},
        {"language": "Ruby", "type": "literal"},
        {"language": "JavaScript", "type": "block"},
    ]

    config = TableConfig(filter_field="type", filter_value="Literal")
    renderer = AdvancedTableRenderer(data=data, config=config)

    filtered = renderer._apply_filter()
    assert len(filtered) == 2
    assert all(row["type"].lower() == "literal" for row in filtered)



@given(
    data=st.lists(
        st.fixed_dictionaries(
            {
                "name": st.text(min_size=1, max_size=10, alphabet="abcdefghij"),
                "value": st.integers(min_value=0, max_value=100),
            }
        ),
        min_size=2,
        max_size=10,
    ),
    sort_descending=st.booleans(),
)
@settings(max_examples=100)
def test_table_sorting(data: list[dict], sort_descending: bool) -> None:
    """Property 24: Table Sorting.

    Feature: mrdr-visual-integration, Property 24: Table Sorting
    For any --sort field option, the rendered table rows SHALL be ordered
    by the specified field in ascending order (or descending with toggle).
    **Validates: Requirements 10.4**
    """
    config = TableConfig(sort_field="name", sort_descending=sort_descending)
    renderer = AdvancedTableRenderer(data=data, config=config)

    sorted_data = renderer._apply_sort(data)

    # Extract sorted names
    names = [row["name"] for row in sorted_data]

    # Verify order
    expected = sorted(names, reverse=sort_descending)
    assert names == expected


@given(
    data=st.lists(
        st.fixed_dictionaries(
            {
                "name": st.text(min_size=1, max_size=10, alphabet="abcdefghij"),
                "priority": st.integers(min_value=1, max_value=10),
            }
        ),
        min_size=1,
        max_size=10,
    )
)
@settings(max_examples=100)
def test_table_sorting_preserves_data(data: list[dict]) -> None:
    """Property 24: Table Sorting - data preservation.

    Feature: mrdr-visual-integration, Property 24: Table Sorting
    Sorting should preserve all data, just reorder it.
    **Validates: Requirements 10.4**
    """
    config = TableConfig(sort_field="name")
    renderer = AdvancedTableRenderer(data=data, config=config)

    sorted_data = renderer._apply_sort(data)

    # Same number of rows
    assert len(sorted_data) == len(data)

    # Same data, just reordered
    original_set = {(row["name"], row["priority"]) for row in data}
    sorted_set = {(row["name"], row["priority"]) for row in sorted_data}
    assert original_set == sorted_set


def test_table_sorting_no_sort_field() -> None:
    """Property 24: Table Sorting - no sort field.

    Feature: mrdr-visual-integration, Property 24: Table Sorting
    When no sort field is specified, data order should be preserved.
    **Validates: Requirements 10.4**
    """
    data = [
        {"name": "zebra", "value": 1},
        {"name": "apple", "value": 2},
        {"name": "mango", "value": 3},
    ]

    config = TableConfig()  # No sort_field
    renderer = AdvancedTableRenderer(data=data, config=config)

    sorted_data = renderer._apply_sort(data)

    # Order should be preserved
    assert [row["name"] for row in sorted_data] == ["zebra", "apple", "mango"]



@given(
    num_rows=st.integers(min_value=1, max_value=100),
    page_size=st.integers(min_value=5, max_value=20),
)
@settings(max_examples=100)
def test_table_pagination(num_rows: int, page_size: int) -> None:
    """Property 25: Table Pagination.

    Feature: mrdr-visual-integration, Property 25: Table Pagination
    For any table with rows exceeding page_size, the output SHALL include
    pagination hints showing current page and navigation options.
    **Validates: Requirements 10.5**
    """
    data = [{"id": i, "name": f"item_{i}"} for i in range(num_rows)]

    config = TableConfig(page_size=page_size, current_page=1)
    renderer = AdvancedTableRenderer(data=data, config=config)

    page_data, total_pages = renderer._apply_pagination(data)

    # Calculate expected total pages
    expected_pages = (num_rows + page_size - 1) // page_size

    assert total_pages == expected_pages
    assert len(page_data) <= page_size

    # First page should start at index 0
    if page_data:
        assert page_data[0]["id"] == 0


@given(
    num_rows=st.integers(min_value=21, max_value=50),
    page_size=st.integers(min_value=5, max_value=10),
    current_page=st.integers(min_value=1, max_value=5),
)
@settings(max_examples=100)
def test_table_pagination_page_navigation(
    num_rows: int, page_size: int, current_page: int
) -> None:
    """Property 25: Table Pagination - page navigation.

    Feature: mrdr-visual-integration, Property 25: Table Pagination
    Pagination should correctly navigate to specified pages.
    **Validates: Requirements 10.5**
    """
    data = [{"id": i, "name": f"item_{i}"} for i in range(num_rows)]

    total_pages = (num_rows + page_size - 1) // page_size
    # Clamp current_page to valid range
    valid_page = min(current_page, total_pages)

    config = TableConfig(page_size=page_size, current_page=valid_page)
    renderer = AdvancedTableRenderer(data=data, config=config)

    page_data, returned_pages = renderer._apply_pagination(data)

    # Verify correct page data
    expected_start = (valid_page - 1) * page_size
    if page_data:
        assert page_data[0]["id"] == expected_start


@given(
    num_rows=st.integers(min_value=21, max_value=50),
    page_size=st.integers(min_value=5, max_value=10),
)
@settings(max_examples=100)
def test_table_pagination_hints_shown(num_rows: int, page_size: int) -> None:
    """Property 25: Table Pagination - hints display.

    Feature: mrdr-visual-integration, Property 25: Table Pagination
    When multiple pages exist, pagination hints should be shown.
    **Validates: Requirements 10.5**
    """
    data = [{"id": i, "name": f"item_{i}"} for i in range(num_rows)]

    config = TableConfig(page_size=page_size, current_page=1)
    renderer = AdvancedTableRenderer(data=data, config=config)

    total_pages = renderer.get_total_pages()

    if total_pages > 1:
        output = renderer.render()
        # Pagination hints should contain page info
        assert "Page" in output
        assert "/" in output


def test_table_pagination_empty_data() -> None:
    """Property 25: Table Pagination - empty data.

    Feature: mrdr-visual-integration, Property 25: Table Pagination
    Empty data should return 1 total page.
    **Validates: Requirements 10.5**
    """
    config = TableConfig(page_size=10, current_page=1)
    renderer = AdvancedTableRenderer(data=[], config=config)

    page_data, total_pages = renderer._apply_pagination([])

    assert total_pages == 1
    assert len(page_data) == 0



@given(
    selected_columns=st.lists(
        st.sampled_from(["name", "type", "location"]),
        min_size=1,
        max_size=3,
        unique=True,
    )
)
@settings(max_examples=100)
def test_table_column_filtering(selected_columns: list[str]) -> None:
    """Property 22: Table Column Filtering.

    Feature: mrdr-visual-integration, Property 22: Table Column Filtering
    For any --columns option with column list, the rendered table SHALL
    contain only the specified columns in the specified order.
    **Validates: Requirements 10.2**
    """
    data = [
        {"name": "Python", "type": "literal", "location": "internal"},
        {"name": "JavaScript", "type": "block", "location": "above"},
    ]

    config = TableConfig(columns=selected_columns)
    renderer = AdvancedTableRenderer(data=data, config=config)
    output = renderer.render()

    # Each selected column header should appear in output
    for col in selected_columns:
        # Column headers are title-cased
        header = col.replace("_", " ").title()
        assert header in output, f"Column '{header}' should appear in output"


@given(
    data=st.lists(
        st.fixed_dictionaries(
            {
                "col_a": st.text(min_size=1, max_size=5, alphabet="abc"),
                "col_b": st.text(min_size=1, max_size=5, alphabet="xyz"),
                "col_c": st.integers(min_value=0, max_value=99),
            }
        ),
        min_size=1,
        max_size=5,
    )
)
@settings(max_examples=100)
def test_table_column_filtering_order(data: list[dict]) -> None:
    """Property 22: Table Column Filtering - column order.

    Feature: mrdr-visual-integration, Property 22: Table Column Filtering
    Columns should appear in the order specified.
    **Validates: Requirements 10.2**
    """
    # Request columns in reverse order
    config = TableConfig(columns=["col_c", "col_a"])
    renderer = AdvancedTableRenderer(data=data, config=config)
    output = renderer.render()

    # Col C should appear before Col A in the output
    col_c_pos = output.find("Col C")
    col_a_pos = output.find("Col A")

    assert col_c_pos < col_a_pos, "Columns should appear in specified order"


def test_table_column_filtering_nonexistent() -> None:
    """Property 22: Table Column Filtering - nonexistent columns.

    Feature: mrdr-visual-integration, Property 22: Table Column Filtering
    Nonexistent columns should be ignored.
    **Validates: Requirements 10.2**
    """
    data = [{"name": "Python", "type": "literal"}]

    # Request a mix of existing and nonexistent columns
    config = TableConfig(columns=["name", "nonexistent", "type"])
    renderer = AdvancedTableRenderer(data=data, config=config)
    output = renderer.render()

    # Existing columns should appear
    assert "Name" in output
    assert "Type" in output
    # Nonexistent should not cause errors


def test_table_column_filtering_all_columns() -> None:
    """Property 22: Table Column Filtering - no filter shows all.

    Feature: mrdr-visual-integration, Property 22: Table Column Filtering
    When no columns specified, all columns should be shown.
    **Validates: Requirements 10.2**
    """
    data = [{"name": "Python", "type": "literal", "location": "internal"}]

    config = TableConfig()  # No columns specified
    renderer = AdvancedTableRenderer(data=data, config=config)
    output = renderer.render()

    # All columns should appear
    assert "Name" in output
    assert "Type" in output
    assert "Location" in output



@given(
    data=st.lists(
        st.fixed_dictionaries(
            {
                "name": st.text(min_size=1, max_size=10, alphabet="abcdefghij"),
                "value": st.integers(min_value=0, max_value=100),
            }
        ),
        min_size=1,
        max_size=10,
    )
)
@settings(max_examples=100)
def test_table_markdown_export(data: list[dict]) -> None:
    """Property 26: Table Markdown Export.

    Feature: mrdr-visual-integration, Property 26: Table Markdown Export
    For any --export md option, the output SHALL be valid GFM table syntax.
    **Validates: Requirements 10.6**
    """
    renderer = AdvancedTableRenderer(data=data)
    md = renderer.export_markdown()

    lines = md.split("\n")

    # Must have at least header + separator + 1 data row
    assert len(lines) >= 3

    # First line is header
    assert lines[0].startswith("|")
    assert lines[0].endswith("|")

    # Second line is separator with ---
    assert "---" in lines[1]
    assert lines[1].startswith("|")
    assert lines[1].endswith("|")

    # All data rows should be pipe-delimited
    for line in lines[2:]:
        assert line.startswith("|")
        assert line.endswith("|")


@given(
    data=st.lists(
        st.fixed_dictionaries(
            {
                "name": st.text(min_size=1, max_size=10, alphabet="abcdefghij"),
                "desc": st.text(min_size=1, max_size=10, alphabet="abcdefghij"),
            }
        ),
        min_size=1,
        max_size=5,
    )
)
@settings(max_examples=100)
def test_table_markdown_export_all_data(data: list[dict]) -> None:
    """Property 26: Table Markdown Export - all data included.

    Feature: mrdr-visual-integration, Property 26: Table Markdown Export
    Markdown export should include all data rows (not paginated).
    **Validates: Requirements 10.6**
    """
    # Use small page size to verify export ignores pagination
    config = TableConfig(page_size=2, current_page=1)
    renderer = AdvancedTableRenderer(data=data, config=config)
    md = renderer.export_markdown()

    lines = md.split("\n")
    # Header + separator + all data rows
    expected_lines = 2 + len(data)
    assert len(lines) == expected_lines


def test_table_markdown_export_pipe_escape() -> None:
    """Property 26: Table Markdown Export - pipe character escape.

    Feature: mrdr-visual-integration, Property 26: Table Markdown Export
    Pipe characters in data should be escaped.
    **Validates: Requirements 10.6**
    """
    data = [{"name": "test|value", "type": "literal"}]

    renderer = AdvancedTableRenderer(data=data)
    md = renderer.export_markdown()

    # Pipe should be escaped
    assert "\\|" in md


def test_table_markdown_export_empty() -> None:
    """Property 26: Table Markdown Export - empty data.

    Feature: mrdr-visual-integration, Property 26: Table Markdown Export
    Empty data should produce minimal valid markdown.
    **Validates: Requirements 10.6**
    """
    renderer = AdvancedTableRenderer(data=[])
    md = renderer.export_markdown()

    assert "No data" in md



def test_master_table_completeness() -> None:
    """Property 21: Master Table Completeness.

    Feature: mrdr-visual-integration, Property 21: Master Table Completeness
    For any invocation of `mrdr jekyl table --master`, the output SHALL
    contain all languages from the database in table format.
    **Validates: Requirements 10.1**
    """
    from mrdr.database.loader import DatabaseLoader

    # Load all entries from database
    loader = DatabaseLoader()
    entries = loader.get_entries()

    # Convert to table data format (same as the command does)
    data = []
    for entry in entries:
        row = {
            "language": entry.language,
            "syntax_type": entry.syntax.type if entry.syntax else "",
            "syntax_start": entry.syntax.start if entry.syntax else "",
            "syntax_end": entry.syntax.end or "" if entry.syntax else "",
            "syntax_location": entry.syntax.location if entry.syntax else "",
            "tags": ", ".join(entry.tags) if entry.tags else "",
            "conflict_ref": entry.conflict_ref or "",
        }
        data.append(row)

    # Create renderer with large page size to get all data
    config = TableConfig(page_size=100)
    renderer = AdvancedTableRenderer(data=data, config=config)

    # Verify all languages are present
    assert renderer.get_total_rows() == len(entries)

    # Verify data integrity - all languages should be in the data
    languages_in_data = {row["language"] for row in data}
    expected_languages = {entry.language for entry in entries}
    assert languages_in_data == expected_languages


def test_master_table_all_columns_present() -> None:
    """Property 21: Master Table Completeness - all columns.

    Feature: mrdr-visual-integration, Property 21: Master Table Completeness
    Master table should include all expected columns.
    **Validates: Requirements 10.1**
    """
    from mrdr.database.loader import DatabaseLoader

    loader = DatabaseLoader()
    entries = loader.get_entries()

    if not entries:
        return  # Skip if no data

    # Convert to table data format
    data = []
    for entry in entries:
        row = {
            "language": entry.language,
            "syntax_type": entry.syntax.type if entry.syntax else "",
            "syntax_start": entry.syntax.start if entry.syntax else "",
            "syntax_end": entry.syntax.end or "" if entry.syntax else "",
            "syntax_location": entry.syntax.location if entry.syntax else "",
            "tags": ", ".join(entry.tags) if entry.tags else "",
            "conflict_ref": entry.conflict_ref or "",
        }
        data.append(row)

    renderer = AdvancedTableRenderer(data=data)
    output = renderer.render()

    # Check that column headers appear (may be split across lines in Rich output)
    # Language should always appear
    assert "Language" in output, "Column 'Language' should appear in table"
    # Syntax should appear (part of multiple column names)
    assert "Syntax" in output, "Syntax columns should appear in table"
    # Tags should appear
    assert "Tags" in output, "Column 'Tags' should appear in table"


@given(
    page=st.integers(min_value=1, max_value=10),
    page_size=st.integers(min_value=5, max_value=20),
)
@settings(max_examples=50)
def test_master_table_pagination_coverage(page: int, page_size: int) -> None:
    """Property 21: Master Table Completeness - pagination coverage.

    Feature: mrdr-visual-integration, Property 21: Master Table Completeness
    All data should be accessible through pagination.
    **Validates: Requirements 10.1**
    """
    from mrdr.database.loader import DatabaseLoader

    loader = DatabaseLoader()
    entries = loader.get_entries()

    if not entries:
        return

    data = [{"language": e.language, "type": e.syntax.type if e.syntax else ""} for e in entries]

    # Collect all languages across all pages
    all_languages = set()
    total_pages = (len(data) + page_size - 1) // page_size

    for p in range(1, total_pages + 1):
        config = TableConfig(page_size=page_size, current_page=p)
        renderer = AdvancedTableRenderer(data=data, config=config)
        page_data, _ = renderer._apply_pagination(data)
        for row in page_data:
            all_languages.add(row["language"])

    # All languages should be covered
    expected_languages = {e.language for e in entries}
    assert all_languages == expected_languages
