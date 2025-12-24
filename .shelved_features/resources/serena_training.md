# The Project Workflow

Serena uses a project-based workflow.
A **project** is simply a directory on your filesystem that contains code and other files
that you want Serena to work with.

Assuming that you have project you want to work with (which may initially be empty),
setting up a project with Serena typically involves the following steps:

1. **Project creation**: Configuring project settings for Serena (and indexing the project, if desired)
2. **Project activation**: Making Serena aware of the project you want to work with
3. **Onboarding**: Getting Serena familiar with the project (creating memories)
4. **Working on coding tasks**: Using Serena to help you with actual coding tasks in the project

(project-creation-indexing)=
## Project Creation & Indexing

You can create a project either  
- implicitly, by just activating a directory as a project while already in a conversation; this will use default settings for your project (skip to the next section).
- explicitly, using the project creation command, or

### Explicit Project Creation

To explicitly create a project, use the following command while in the project directory:

    <serena> project create [options]

For instance, when using `uvx`, run

    uvx --from git+https://github.com/oraios/serena serena project create [options]

- For an empty project, you will need to specify the programming language
   (e.g., `--language python`).
- For an existing project, the main programming language will be detected automatically,
   but you can choose to explicitly specify multiple languages by passing the `--language` parameter
   multiple times (e.g. `--language python --language typescript`).
- You can optionally specify a custom project name with `--name "My Project"`.
- You can immediately index the project after creation with `--index`.

After creation, you can adjust the project settings in the generated `.serena/project.yml` file.

(indexing)=
### Indexing

Especially for larger project, it is advisable to index the project after creation (in order to avoid
delays during MCP server startup or the first tool application):

While in the project directory, run this command:

    <serena> project index

Indexing has to be called only once. During regular usage, Serena will automatically update the index whenever files change.

## Project Activation

Project activation makes Serena aware of the project you want to work with.
You can either choose to do this
- while in a conversation, by telling the model to activate a project, e.g.,

  - "Activate the project /path/to/my_project" (for first-time activation with auto-creation)
  - "Activate the project my_project"

   Note that this option requires the `activate_project` tool to be active,
   which it isn't in the (default version) of context `ide-assistant` if a project is provided at startup.
   (The tool is deactivated because we assume that in the ide-assistant context the user will only work on the open project and have
   no need to switch it.)

- when the MCP server starts, by passing the project path or name as a command-line argument
   (e.g. when working on a fixed project in `ide-assistant` mode): `--project <path|name>`

## Onboarding & Memories

By default, Serena will perform an **onboarding process** when
it is started for the first time for a project.
The goal of the onboarding is for Serena to get familiar with the project
and to store memories, which it can then draw upon in future interactions.
If an LLM should fail to complete the onboarding and does not actually write the
respective memories to disk, you may need to ask it to do so explicitly.

The onboarding will usually read a lot of content from the project, thus filling
up the context. It can therefore be advisable to switch to another conversation
once the onboarding is complete.
After the onboarding, we recommend that you have a quick look at the memories and,
if necessary, edit them or add additional ones.

**Memories** are files stored in `.serena/memories/` in the project directory,
which the agent can choose to read in subsequent interactions.
Feel free to read and adjust them as needed; you can also add new ones manually.
Every file in the `.serena/memories/` directory is a memory file.
Whenever Serena starts working on a project, the list of memories is
provided, and the agent can decide to read them.
We found that memories can significantly improve the user experience with Serena.

## Preparing Your Project

When using Serena to work on your project, it can be helpful to follow a few best practices.

### Structure Your Codebase

Serena uses the code structure for finding, reading and editing code. This means that it will
work well with well-structured code but may perform poorly on fully unstructured one (like a "God class"
with enormous, non-modular functions).

Furthermore, for languages that are not statically typed, the use of type annotations (if supported)
are highly beneficial.

### Start from a Clean State

It is best to start a code generation task from a clean git state. Not only will
this make it easier for you to inspect the changes, but also the model itself will
have a chance of seeing what it has changed by calling `git diff` and thereby
correct itself or continue working in a followup conversation if needed.

### Use Platform-Native Line Endings

**Important**: since Serena will write to files using the system-native line endings
and it might want to look at the git diff, it is important to
set `git config core.autocrlf` to `true` on Windows.
With `git config core.autocrlf` set to `false` on Windows, you may end up with huge diffs
due to line endings only.
It is generally a good idea to globally enable this git setting on Windows:

    ```shell
    git config --global core.autocrlf true
    ```

### Logging, Linting, and Automated Tests

Serena can successfully complete tasks in an _agent loop_, where it iteratively
acquires information, performs actions, and reflects on the results.
However, Serena cannot use a debugger; it must rely on the results of program executions,
linting results, and test results to assess the correctness of its actions.
Therefore, software that is designed to meaningful interpretable outputs (e.g. log messages)
and that has a good test coverage is much easier to work with for Serena.

We generally recommend to start an editing task from a state where all linting checks and tests pass.

## Configuration

Serena is very flexible in terms of configuration. While for most users, the default configurations will work,
you can fully adjust it to your needs by editing a few yaml files. You can disable tools, change Serena's instructions
(what we denote as the `system_prompt`), adjust the output of tools that just provide a prompt, and even adjust tool descriptions.

Serena is configured in four places:

1. The `serena_config.yml` for general settings that apply to all clients and projects.
   It is located in your user directory under `.serena/serena_config.yml`.
   If you do not explicitly create the file, it will be auto-generated when you first run Serena.
   You can edit it directly or use

   ```shell
   uvx --from git+https://github.com/oraios/serena serena config edit
   ```

   (or use the `--directory` command version).
2. In the arguments passed to the `start-mcp-server` in your client's config (see below),
   which will apply to all sessions started by the respective client. In particular, the [context](contexts) parameter
   should be set appropriately for Serena to be best adjusted to existing tools and capabilities of your client.
   See for a detailed explanation. You can override all entries from the `serena_config.yml` through command line arguments.
3. In the `.serena/project.yml` file within your project. This will hold project-level configuration that is used whenever
   that project is activated. This file will be autogenerated when you first use Serena on that project, but you can also
   create it explicitly with `serena project create [options]` (see the [](project-creation-indexing)
   for details on available options).
4. Through the context and modes (see below).

After the initial setup, continue with one of the sections below, depending on how you
want to use Serena.

## Modes and Contexts

Serena's behavior and toolset can be adjusted using contexts and modes.
These allow for a high degree of customization to best suit your workflow and the environment Serena is operating in.

(contexts)=
### Contexts

A **context** defines the general environment in which Serena is operating.
It influences the initial system prompt and the set of available tools.
A context is set at startup when launching Serena (e.g., via CLI options for an MCP server or in the agent script) and cannot be changed during an active session.

Serena comes with pre-defined contexts:

- `desktop-app`: Tailored for use with desktop applications like Claude Desktop. This is the default.
  The full set of Serena's tools is provided, as the application is assumed to have no prior coding-specific capabilities.
- `claude-code`: Optimized for use with Claude Code, it disables tools that would duplicate Claude Code's built-in capabilities.
- `codex`: Optimized for use with OpenAI Codex.
- `ide`: Generic context for IDE assistants/coding agents, e.g. VSCode, Cursor, or Cline, focusing on augmenting existing capabilities.
  Basic file operations and shell execution are assumed to be handled by the assistant's own capabilities.
- `agent`: Designed for scenarios where Serena acts as a more autonomous agent, for example, when used with Agno.

Choose the context that best matches the type of integration you are using.

Find the concrete definitions of the above contexts [at the github repo](https://github.com/oraios/serena/tree/main/src/serena/resources/config/contexts).

When launching Serena, specify the context using `--context <context-name>`.
Note that for cases where parameter lists are specified (e.g. Claude Desktop), you must add two parameters to the list.

If you are using a local server (such as Llama.cpp) which requires you to use OpenAI-compatible tool descriptions, use context `oaicompat-agent` instead of `agent`.

You can manage contexts using the `context` command,

    <serena> context --help
    <serena> context list
    <serena> context create <context-name>
    <serena> context edit <context-name>
    <serena> context delete <context-name>

where `<serena>` is [your way of running Serena](020_running).

(modes)=
### Modes

Modes further refine Serena's behavior for specific types of tasks or interaction styles. Multiple modes can be active simultaneously, allowing you to combine their effects. Modes influence the system prompt and can also alter the set of available tools by excluding certain ones.

Examples of built-in modes include:

- `planning`: Focuses Serena on planning and analysis tasks.
- `editing`: Optimizes Serena for direct code modification tasks.
- `interactive`: Suitable for a conversational, back-and-forth interaction style.
- `one-shot`: Configures Serena for tasks that should be completed in a single response, often used with `planning` for generating reports or initial plans.
- `no-onboarding`: Skips the initial onboarding process if it's not needed for a particular session but retains the memory tools (assuming initial memories were created externally).
- `onboarding`: Focuses on the project onboarding process.
- `no-memories`: Disables all memory tools (and tools building on memories such as onboarding tools)  

Find the concrete definitions of these modes [config modes](https://github.com/oraios/serena/tree/main/src/serena/resources/config/modes).

:::{important}
By default, Serena activates the two modes `interactive` and `editing`.  

As soon as you start to specify modes, only the modes you explicitly specify will be active, however.
Therefore, if you want to keep the default modes, you must specify them as well.  
For example, to add mode `no-memories` to the default behaviour, specify
```shell
--mode interactive --mode editing --mode no-memories
```
:::

Modes can be set at startup (similar to contexts) but can also be _switched dynamically_ during a session.
You can instruct the LLM to use the `switch_modes` tool to activate a different set of modes (e.g., "Switch to planning and one-shot modes").

When launching Serena, specify modes using `--mode <mode-name>`; multiple modes can be specified, e.g. `--mode planning --mode no-onboarding`.

:::{note}
**Mode Compatibility**: While you can combine modes, some may be semantically incompatible (e.g., `interactive` and `one-shot`).
Serena currently does not prevent incompatible combinations; it is up to the user to choose sensible mode configurations.
:::

You can manage modes using the `mode` command,

    <serena> mode --help
    <serena> mode list
    <serena> mode create <mode-name>
    <serena> mode edit <mode-name>
    <serena> mode delete <mode-name>

where `<serena>` is [your way of running Serena](020_running).

## Advanced Configuration

For advanced users, Serena's configuration can be further customized.

### Serena Data Directory

The Serena user data directory (where configuration, language server files, logs, etc. are stored) defaults to `~/.serena`.
You can change this location by setting the `SERENA_HOME` environment variable to your desired path.

### Custom Prompts

All of Serena's prompts can be fully customized.
We define prompt as jinja templates in yaml files, and you can inspect our default prompts [prompt templates](https://github.com/oraios/serena/tree/main/src/serena/resources/config/prompt_templates).

To override a prompt, simply add a .yml file to the `prompt_templates` folder in your Serena data directory
which defines the prompt with the same name as the default prompt you want to override.
For example, to override the `system_prompt`, you could create a file `~/.serena/prompt_templates/system_prompt.yml` (assuming default Serena data folder location)
with content like:

```yaml
prompts:
  system_prompt: |
    Whatever you want ...
```

It is advisable to use the default prompt as a starting point and modify it to suit your needs.

## Additional Usage Pointers

## Prompting Strategies

We found that it is often a good idea to spend some time conceptualizing and planning a task
before actually implementing it, especially for non-trivial task. This helps both in achieving
better results and in increasing the feeling of control and staying in the loop. You can
make a detailed plan in one session, where Serena may read a lot of your code to build up the context,
and then continue with the implementation in another (potentially after creating suitable memories).

## Running Out of Context

For long and complicated tasks, or tasks where Serena has read a lot of content, you
may come close to the limits of context tokens. In that case, it is often a good idea to continue
in a new conversation. Serena has a dedicated tool to create a summary of the current state
of the progress and all relevant info for continuing it. You can request to create this summary and
write it to a memory. Then, in a new conversation, you can just ask Serena to read the memory and
continue with the task. In our experience, this worked really well. On the up-side, since in a
single session there is no summarization involved, Serena does not usually get lost (unlike some
other agents that summarize under the hood), and it is also instructed to occasionally check whether
it's on the right track.

Serena instructs the LLM to be economical in general, so the problem of running out of context
should not occur too often, unless the task is very large or complicated.

## Serena and Git Worktrees

[git-worktree](https://git-scm.com/docs/git-worktree) can be an excellent way to parallelize your work. More on this in [Anthropic: Run parallel Claude Code sessions with Git worktrees](https://docs.claude.com/en/docs/claude-code/common-workflows#run-parallel-claude-code-sessions-with-git-worktrees).

When it comes to serena AND git-worktree AND larger projects (that take longer to index),
the recommended way is to COPY your `$ORIG_PROJECT/.serena/cache` to `$GIT_WORKTREE/.serena/cache`.
Perform [pre-indexing of your project](indexing) to avoid having to re-index per each worktree you create.
