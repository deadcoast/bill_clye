"""Doctag schema definitions for MRDR.

This module defines the doctag data structures and the complete
doctag database as defined in docs/doctags.md.
"""

from dataclasses import dataclass
from enum import Enum

from pydantic import BaseModel, Field


class DoctagCategory(str, Enum):
    """Doctag category types."""

    DDL = "DDL"  # Delimiters
    GRM = "GRM"  # Grammar
    IDC = "IDC"  # Inter-Document Commands
    FMT = "FMT"  # Formatting
    DOC = "DOC"  # Document Spec

    # Legacy aliases for backward compatibility
    DELIMITER = "DDL"
    GRAMMAR = "GRM"
    INTER_DOC = "IDC"
    FORMATTING = "FMT"
    DOC_SPEC = "DOC"


class DoctagEntry(BaseModel):
    """Pydantic model for doctag database entry.

    Attributes:
        id: Tag identifier (e.g., "DDL01", "GRM05").
        symbol: The symbol or token (e.g., "+", "rstr").
        short_name: Short NLP identifier (e.g., "ADDTACH", "RESTRICTIONS").
        description: Full description of the tag.
        category: The doctag category (DDL, GRM, IDC, FMT, DOC).
        example: Optional usage example.
    """

    id: str = Field(..., pattern=r"^(DDL|GRM|IDC|FMT|DOC)\d{2}$")
    symbol: str = Field(..., description="The delimiter or symbol")
    short_name: str = Field(..., description="Short identifier (SCREAMINGSNAKE)")
    description: str = Field(..., description="Tag description")
    category: DoctagCategory = Field(..., description="Tag category")
    example: str | None = Field(None, description="Usage example")


class DoctagDatabase(BaseModel):
    """Complete doctag database model."""

    manifest: dict = Field(..., description="Database manifest")
    doctags: list[DoctagEntry] = Field(default_factory=list)


@dataclass
class DoctagDefinition:
    """A single doctag definition (legacy dataclass).

    Attributes:
        id: Tag identifier (e.g., "DDL01", "GRM05").
        symbol: The symbol or token (e.g., "+", "rstr").
        short_name: Short NLP identifier (e.g., "ADDTACH", "RESTRICTIONS").
        description: Full description of the tag.
        category: The doctag category (DDL, GRM, IDC, FMT, DOC).
        example: Optional usage example.
    """

    id: str
    symbol: str
    short_name: str
    description: str
    category: DoctagCategory
    example: str | None = None


# Complete doctag database from docs/doctags.md
DOCTAG_DATABASE: dict[str, DoctagDefinition] = {
    # Document Delimiters (DDL01-DDL10)
    "DDL01": DoctagDefinition(
        id="DDL01",
        symbol="+",
        short_name="ADDTACH",
        description="add, or attach an item or reference",
        category=DoctagCategory.DELIMITER,
        example="+item",
    ),
    "DDL02": DoctagDefinition(
        id="DDL02",
        symbol="-+",
        short_name="DELREM",
        description="remove, or delete an item or reference",
        category=DoctagCategory.DELIMITER,
        example="-+item",
    ),
    "DDL03": DoctagDefinition(
        id="DDL03",
        symbol="!>",
        short_name="EXCEPTFOR",
        description="Except for [x] ID, an exception to a rule",
        category=DoctagCategory.DELIMITER,
        example="!> lists",
    ),
    "DDL04": DoctagDefinition(
        id="DDL04",
        symbol=":",
        short_name="KEYVAL",
        description="key/value separator for tags and metadata",
        category=DoctagCategory.DELIMITER,
        example="key:value",
    ),
    "DDL05": DoctagDefinition(
        id="DDL05",
        symbol="|",
        short_name="DOCPIPE",
        description="file/header separator in doc links",
        category=DoctagCategory.DELIMITER,
        example="file|## header",
    ),
    "DDL06": DoctagDefinition(
        id="DDL06",
        symbol="=",
        short_name="ASSIGN",
        description="assignment operator for inline configs",
        category=DoctagCategory.DELIMITER,
        example="config=value",
    ),
    "DDL07": DoctagDefinition(
        id="DDL07",
        symbol=",",
        short_name="LISTSEP",
        description="inline list separator",
        category=DoctagCategory.DELIMITER,
        example="a, b, c",
    ),
    "DDL08": DoctagDefinition(
        id="DDL08",
        symbol=";",
        short_name="STMTSEP",
        description="statement separator for compact specs",
        category=DoctagCategory.DELIMITER,
        example="stmt1; stmt2",
    ),
    "DDL09": DoctagDefinition(
        id="DDL09",
        symbol="/",
        short_name="PATHSEP",
        description="path delimiter for repo-relative references",
        category=DoctagCategory.DELIMITER,
        example="/docs/file.md",
    ),
    "DDL10": DoctagDefinition(
        id="DDL10",
        symbol="#",
        short_name="HEADTAG",
        description="header identifier for anchor references",
        category=DoctagCategory.DELIMITER,
        example="#section",
    ),
    # Grammar definitions (GRM01-GRM10)
    "GRM01": DoctagDefinition(
        id="GRM01",
        symbol="rstr",
        short_name="RESTRICTIONS",
        description="Prohibited practise",
        category=DoctagCategory.GRAMMAR,
        example="rstr: no spaces",
    ),
    "GRM02": DoctagDefinition(
        id="GRM02",
        symbol="ntype",
        short_name="NAMETYPE",
        description="Grandparent Type",
        category=DoctagCategory.GRAMMAR,
        example="ntype: function",
    ),
    "GRM05": DoctagDefinition(
        id="GRM05",
        symbol="dlist",
        short_name="DASHLIST",
        description="a dash ordered list",
        category=DoctagCategory.GRAMMAR,
        example="- item1\n- item2",
    ),
    "GRM06": DoctagDefinition(
        id="GRM06",
        symbol="id",
        short_name="ID",
        description="Purpose Related Identifier",
        category=DoctagCategory.GRAMMAR,
        example="id: TAG01",
    ),
    "GRM07": DoctagDefinition(
        id="GRM07",
        symbol="glbl",
        short_name="GLOBAL",
        description="Applies Globally in the Repo",
        category=DoctagCategory.GRAMMAR,
        example="glbl: true",
    ),
    "GRM08": DoctagDefinition(
        id="GRM08",
        symbol="met",
        short_name="METADATA",
        description="References the docs Metadata",
        category=DoctagCategory.GRAMMAR,
        example="met: version",
    ),
    "GRM09": DoctagDefinition(
        id="GRM09",
        symbol="alias",
        short_name="ALIAS",
        description="Alternate name binding for the same command/tag",
        category=DoctagCategory.GRAMMAR,
        example="alias: alt_name",
    ),
    "GRM10": DoctagDefinition(
        id="GRM10",
        symbol="desc",
        short_name="DESCRIPTION",
        description="Descriptive text attached to an identifier",
        category=DoctagCategory.GRAMMAR,
        example="desc: A brief description",
    ),
    # Inter-Document Commands (IDC01-IDC10)
    "IDC01": DoctagDefinition(
        id="IDC01",
        symbol="LANGUSE",
        short_name="LANGUAGEUSAGE",
        description="Duplicated Usage",
        category=DoctagCategory.INTER_DOC,
        example="LANGUSE: python",
    ),
    "IDC02": DoctagDefinition(
        id="IDC02",
        symbol="DOCLINK",
        short_name="DOCREFERENCE",
        description="File+header reference using file|## header",
        category=DoctagCategory.INTER_DOC,
        example="DOCLINK: docs/spec.md|## Overview",
    ),
    "IDC03": DoctagDefinition(
        id="IDC03",
        symbol="FILELINK",
        short_name="FILEREF",
        description="File-only reference",
        category=DoctagCategory.INTER_DOC,
        example="FILELINK: /docs/readme.md",
    ),
    "IDC04": DoctagDefinition(
        id="IDC04",
        symbol="HEADRLINK",
        short_name="HEADERREF",
        description="Header-only reference within a file",
        category=DoctagCategory.INTER_DOC,
        example="HEADRLINK: ## Installation",
    ),
    "IDC05": DoctagDefinition(
        id="IDC05",
        symbol="REF",
        short_name="REFERENCE",
        description="General cross-doc reference marker",
        category=DoctagCategory.INTER_DOC,
        example="REF: related_doc",
    ),
    "IDC06": DoctagDefinition(
        id="IDC06",
        symbol="SPECREF",
        short_name="SPECREFERENCE",
        description="Spec pointer in docs",
        category=DoctagCategory.INTER_DOC,
        example="SPECREF: cli_spec.md",
    ),
    "IDC07": DoctagDefinition(
        id="IDC07",
        symbol="DBREF",
        short_name="DATABASEREF",
        description="Database reference pointer",
        category=DoctagCategory.INTER_DOC,
        example="DBREF: docstrings/python",
    ),
    "IDC08": DoctagDefinition(
        id="IDC08",
        symbol="TEMPRE",
        short_name="TEMPLATEREF",
        description="Template reference pointer",
        category=DoctagCategory.INTER_DOC,
        example="TEMPRE: docstring_template.md",
    ),
    "IDC09": DoctagDefinition(
        id="IDC09",
        symbol="RESREF",
        short_name="RESOURCEREF",
        description="Resource reference pointer",
        category=DoctagCategory.INTER_DOC,
        example="RESREF: assets/image.png",
    ),
    "IDC10": DoctagDefinition(
        id="IDC10",
        symbol="TODOLINK",
        short_name="TODOREF",
        description="TODO reference pointer",
        category=DoctagCategory.INTER_DOC,
        example="TODOLINK: TODO.md#TASK01",
    ),
    # Formatting rules (FMT01-FMT10)
    "FMT01": DoctagDefinition(
        id="FMT01",
        symbol="newline",
        short_name="NEWLINE",
        description="Newline formatting rule",
        category=DoctagCategory.FORMATTING,
        example="newline: above=true, below=false",
    ),
    "FMT02": DoctagDefinition(
        id="FMT02",
        symbol="nlrule",
        short_name="NEWLINERULE",
        description="newline rule marker",
        category=DoctagCategory.FORMATTING,
        example="nlrule: backslash",
    ),
    "FMT03": DoctagDefinition(
        id="FMT03",
        symbol="cfgdflt",
        short_name="CONFIGDEFAULT",
        description="default config marker",
        category=DoctagCategory.FORMATTING,
        example="cfgdflt: twospc",
    ),
    "FMT04": DoctagDefinition(
        id="FMT04",
        symbol="twospc",
        short_name="TWOSPACES",
        description="two-space newline variant (default)",
        category=DoctagCategory.FORMATTING,
        example="line1  \nline2",
    ),
    "FMT05": DoctagDefinition(
        id="FMT05",
        symbol="htmlbr",
        short_name="HTMLBR",
        description="HTML <br> line break method",
        category=DoctagCategory.FORMATTING,
        example="line1<br>line2",
    ),
    "FMT06": DoctagDefinition(
        id="FMT06",
        symbol="htmlpre",
        short_name="HTMLPRE",
        description="<pre> block newline method",
        category=DoctagCategory.FORMATTING,
        example="<pre>content</pre>",
    ),
    "FMT07": DoctagDefinition(
        id="FMT07",
        symbol="codeblk",
        short_name="CODEBLOCK",
        description="code block newline method",
        category=DoctagCategory.FORMATTING,
        example="```\ncode\n```",
    ),
    "FMT08": DoctagDefinition(
        id="FMT08",
        symbol="tblmtd",
        short_name="TABLEMETHOD",
        description="table-based newline method",
        category=DoctagCategory.FORMATTING,
        example="| col1 | col2 |",
    ),
    "FMT09": DoctagDefinition(
        id="FMT09",
        symbol="invtable",
        short_name="INVISIBLETABLE",
        description="invisible table variant",
        category=DoctagCategory.FORMATTING,
        example="<table><tr><td>content</td></tr></table>",
    ),
    "FMT10": DoctagDefinition(
        id="FMT10",
        symbol="bksmtd",
        short_name="BACKSLASHMETHOD",
        description="backslash newline method",
        category=DoctagCategory.FORMATTING,
        example="line1\\\nline2",
    ),
    # Document spec markers (DOC01-DOC05)
    "DOC01": DoctagDefinition(
        id="DOC01",
        symbol="MRDR:doc:spec=doctags",
        short_name="DOCSPEC_DOCTAGS",
        description="Required docspec marker for all documents",
        category=DoctagCategory.DOC_SPEC,
        example="[MRDR:doc:spec=doctags](/docs/doctags.md)",
    ),
    "DOC02": DoctagDefinition(
        id="DOC02",
        symbol="MRDR:doc:spec=metadata",
        short_name="DOCSPEC_METADATA",
        description="Metadata spec alignment",
        category=DoctagCategory.DOC_SPEC,
        example="[MRDR:doc:spec=metadata](/docs/docspecs/metadata_spec.md)",
    ),
    "DOC03": DoctagDefinition(
        id="DOC03",
        symbol="MRDR:doc:spec=visualdata",
        short_name="DOCSPEC_VISUALDATA",
        description="Visual data spec focus",
        category=DoctagCategory.DOC_SPEC,
        example="[MRDR:doc:spec=visualdata]",
    ),
    "DOC04": DoctagDefinition(
        id="DOC04",
        symbol="MRDR:doc:spec=output",
        short_name="DOCSPEC_OUTPUT",
        description="Output and display focus",
        category=DoctagCategory.DOC_SPEC,
        example="[MRDR:doc:spec=output]",
    ),
    "DOC05": DoctagDefinition(
        id="DOC05",
        symbol="MRDR:doc:spec=userexperience",
        short_name="DOCSPEC_UX",
        description="UX focus",
        category=DoctagCategory.DOC_SPEC,
        example="[MRDR:doc:spec=userexperience]",
    ),
}
