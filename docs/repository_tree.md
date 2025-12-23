# REPOSITORY TREE
[MRDR:doc:spec=doctags](/docs/doctags.md)
<!--
TREE01:spec
  [1] MONITORSTATUS: true,
  [2] MONITOR: 'depreciation',
    [2.1] IFTRUE: 'notify_user'
  [3]  
-->

## TREE SPEC
<!-- NOTE: THIS IS ALIVING DOCUMENT , THE REPOSITORY TREE SHOULD BE MONITORED, IF OUT OF SYNC OR DEPRECIATED, NOTIFY THE USER TO GENERATE ANOTHER UPDATED VERSION. -->

```
.
├── .gitignore
├── .markdownlint.json
├── .python-version
├── .shelved_features
│   ├── advanced_udl_docstring.md
│   └── docstring_deepdive.md
├── AGENTS.md
├── README.md
├── main.py
├── pyproject.toml
├── uv.lock
├── database
│   ├── delimeters
│   │   └── delimeters.md
│   ├── docstrings
│   │   ├── docstring_database.json
│   │   ├── docstring_database.md
│   │   └── docstring_examples.md
│   ├── languages
│   │   ├── javascript
│   │   ├── python
│   │   │   └── docstring_styles.md
│   │   └── udl
│   │       ├── udl_example.md
│   │       └── udl_template.md
│   ├── operators
│   │   └── operators.md
│   └── tables
│       ├── table_database.md
│       └── table_references.md
├── docs
│   ├── dictionary.md
│   ├── doc_specs
│   │   ├── cli_spec.md
│   │   ├── metadata_spec.md
│   │   ├── newline_spec.md
│   │   └── todo_spec.md
│   ├── doctags.md
│   ├── repository_tree.md
│   ├── resources
│   │   ├── academic_adv_markdown.md
│   │   ├── github_adv_markdown.md
│   │   ├── python_trends_2025.md
│   │   └── uv_cheatsheet.md
│   └── TODO.md
├── src
└── templates
    ├── docstring_template.md
    └── todo_template.md
```
