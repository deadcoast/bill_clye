# CLISPEC:MRDR - The Visual Syntax CLI
<!--
  THIS IS A LIVING DOCUMENT THAT IS BEING UPDATED AS DEVELOPMENT PROGRESSES. IT WILL EVENTUALLY BE UTILIZED AS THE ABSOLUTE SOURCE OF TRUTH FOR THE DATABASE DURING DEVELOPMENT. ALL DATA IN THIS DOCUMENT MUST BE COHERENT, AND CONSISTENT.
-->

_MRDR The Syntax CLI is a(nod, and homage to `Doctor Jekl and Mister Hyde`) CLI database that allows you to display and render different example of common codebases._

> [!IMPORTANT]
> `MRDR` initial design should focus on comprehensive, future proof, documented, modular codebase.

## INTRODUCTION
`MRDR` CLI output features (pulled from the designed database) in the initial design will be minimal, but that does not mean the DEVELOPMENT and SPEC will be minimal.
> command: `mrdr`

- (1).SPEC_DESIGN_PURPOSE: To maximize initial CLI design depth, the first spec will focus on full scope foundational modular cli development, if done correctly `database_display_integration` should be much easier.
  - `database_display_integration`: The CLI pulling data from the database, and displaying them in the CLI, such as the (currently planned) integration 'docstrings'.
- (2).DESIGN_IMPLICATIONS: The implications of the future support and design spec, indicate that this codebase design must be comprehensive from its foundations.
- (3) The modular design should be created full scope, with weighted attention focused on developing user quality of life, database integration, CLI design and inclusivity.
- (4) The foundations should be so in deopth and comprehensiove, that the `docstring` display format functions and modules should be an easy, modular injection / integration.
- (5) After the initial design is completed, shipped, stabilized and launched, the `future_roadmap` will be considered. The `future_roadmap` will be a list of features that will be implemented in the future, and will be considered in the development of the `MRDR` CLI.
- (6).FUTURE_ROADMAP: a list of features that will be implemented in the future, and will be considered in the development of the quality of life, and modular foundations `MRDR` CLI **BUT** additional output display modules will not be integrated past the `docstrings`.

**The weighted focus will stay on the comprehensive foundational development and expansion.**

DEVELOPMENT_STAGE: `PLANNING`

## CLI DESIGN
LANGUAGE: `Python`
CLI_ECOSYSTEM: `Rich`

### REQUIREMENTS
_Below you will find mandatory requirements for the initial, foundational design for `MRDR`_

### COMPREHENSIVE MODULAR CLI DESIGN FOCUS
- The cli should be modular, meaning that it should be able to be used in different ways.
- The initial design will be to display and render different examples of docstrings, once that is completed, shipped, stabilized and launched, `future_roadmap` will be considered.

### `current_roadmap`
- `MRDR` docstrings, once that is completed, shipped, stabilized and launched, `future_roadmap` will be considered.
- `database`: definitions, examples, very basic statistic definitions that can be `objectively_accepted`[] by most.
- Syntax highlighting for all input docstrings

#### `future_roadmap`

SEE [SHELVED FEATURES](/.shelved_features/)

---

## CLI SPECIFICATIONS

[!NOTE]
> MRDR documents, categorizes and collects data from syntax and languages for future database usage, all predetermined essential data should be entered into the MRDR documents. [TODO-03]
> All official supported languages data must be documented for the database

- _This section contains a global dictionary of all the terms and their definitions that are used in the documentation._
- _If any definitions have exact duplicates in other languages, identiy the additional utilization with tag `[+LANG_USE]` but always keep the more widely accepted or pupular nametype for these documents_

### MRDR THE SYNTAX GUY SPEC

_This section contains commands, definitions, and other information that are used in the documentation._
_The design has not been finalized yet, so the differential of commands have not been specified and defined yet._

#### MAIN CLI COMMAND CALL

- `mrdr` - _This tag is used to identify the CLI command, it launches the CLI menu._

#### CLI COMMANDS

- `docstring` - _This tag is used to identify the CLI command._
- `CLI_COMMAND` - _This tag is used to identify the CLI command._

#### MRDR COMMANDS

- `docstring` - _identifies docstrings for the CLI._
- `fix` - _native fix command to refresh syntax highlighting or CLI UI display_

#### MRDR COMMAND OPTIONS

- `-s`, `--show` - _This tag is used to display the output of the CLI command._
- `-n`, `--no` - _Hides the CLI display output of any correspondig command._
- `-ui`, `--ui` - _Identifies the UI option for a corresponding CLI command._

#### CLI CLASSIC COMMAND OPTION

- `-h`, `--help` - _This tag is used to display help for the CLI Commands and Options._
- `-v`, `--version` - _Displays version control, current intalled version._
- `-d`, `--debug` - _Automated Debug process for the CLI visual UI and common errors._
- `-f`, `--format` - _This tag is used to identify the CLI command option._
- `-p`, `--purpose` - _This tag is used to identify the CLI command option._
- `-r`, `--restrictions` - _This tag is used to identify the CLI command option._
- `-s`, `--styling` - _This tag is used to identify the CLI command option._
- `-u`, `--user` - _This tag is used to identify the CLI command option._
- `-n`, `--notes` - _This tag is used to identify the CLI command option._
- `-q`, `--quit` - _This tag is used to quit the cli._

### INTER-DOCUMENT (doc) DEFINITIONS

- `github_flavor` - The flavor of the documentation that is used to define the documentation.

## DATABASE EXAMPLE FORMATS

### Standard Language Docstrings

SEE [Docstring Example File](database/docstrings/docstring_examples.md)

### User Defined Docstrings

SEE [Docstring UDL Template](/templates/udl_template.md)

## FOOTER REMOVALLOG METADATA - A CHANGELOG EXPLICITLY FOR REMOVED DATA, INLINE

<!--
  THIS AREA IS RESERVED FOR AI TO DOCUMENT REMOVED DATA.
    param: 
      REMOVED_DATA: "DATA REMOVED FROM THIS FILE MUST BE PASTED HERE AS IS"
    
  THE USER WILL REMOVE IT MANUALLY ONCE EDITS ARE ACCEPTED AFTER REVIEW.
-->