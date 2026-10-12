# oslo-ld-kit

The knowledge behind the OSLO SSN/SOSA data examples (Flanders), packaged for reuse in any project:
a modelling guide, workflows as Claude Code skills, and the enforceable rules as SHACL shapes.
Born in the OSLOthema-SSNSOSA-VL project; the validation server is
[ld-mcp](https://github.com/milieuinfo/ld-mcp) (`ld-vocab`).

## Contents

| Path | What |
|---|---|
| `guide/` | the modelling guide: linked data rules, SSN/SOSA rules R1–R17, recurring patterns, discussion document, exercise, diagrams ([`guide/README.md`](guide/README.md)) |
| `skills/` | workflows: `new-example`, `revise-mapping`, `alternative-mapping`, `map-source-data`, `decision-document`, `design-ontology`, `align-ontologies` |
| `rules/ssn-sosa-rules.ttl` | the enforceable rules (R2, R3, R5, R7, R9, R11, R12, R13, R15, R16) as SHACL, for `validate_file` |
| `registers/alignments.ttl` | known alignment modules between vocabularies (e.g. SOSA–SAREF), with the namespaces they connect; read by R17 and by `vocabulary_profile` of ld-mcp (`--alignments`) |
| `sync.py` | copies the skills into a project's `.claude/skills/` (see below) |
| `.claude-plugin/` | plugin manifest (`oslo-ld`) and a marketplace manifest, for using the skills outside a project |

## Using it in a project

The kit goes into the project as plain files, so that users of the project need nothing but
`git clone` or `git pull` (no submodules, no plugin installation, no symbolic links). Only the
maintainer of the project deals with the kit.

1. **Add the kit as a git subtree** in `oslo-ld-kit/`, which pins the version the project follows:

   ```bash
   git subtree add --prefix oslo-ld-kit https://github.com/milieuinfo/oslo-ld-kit.git main --squash
   ```

   `git subtree` creates a commit of its own and needs a working tree without uncommitted changes.

2. **Copy the skills into the project**, as project skills in `.claude/skills/` (available as
   `/new-example` and so on), and commit them:

   ```bash
   python oslo-ld-kit/sync.py
   ```

   The script rewrites the skills' links to the guide and writes `.claude/skills/.oslo-ld-kit.json`
   (kit version, copied skills). Skills of the project's own in `.claude/skills/` are left alone.

3. **Load the guide in every session** by importing it from the project's `CLAUDE.md` (paths
   relative to the project), so that the rules are in context also outside the skills:

   ```markdown
   @oslo-ld-kit/guide/linked-data.md
   @oslo-ld-kit/guide/ssn-sosa.md
   ```

   Add the other guide files as needed.

4. **Declare a project profile** in `CLAUDE.md`: examples directory, file names, document language,
   local time zone, unit registry, extra prefixes, validation (see
   [`guide/README.md`](guide/README.md#project-profile)).

5. **Configure validation** with [ld-mcp](https://github.com/milieuinfo/ld-mcp) (`ld-vocab`). Users
   need Java 21 and the jar, downloaded from
   [the latest release](https://github.com/milieuinfo/ld-mcp/releases/latest/download/ld-mcp-vocab.jar)
   into `tools/` in the project (add `tools/` to `.gitignore`); no Maven. In the project's
   `.mcp.json`, with paths relative to the project and the jar from an environment variable
   (developers of ld-mcp point `LD_MCP_JAR` at their own build):

   ```json
   {
     "mcpServers": {
       "ld-vocab": {
         "command": "java",
         "args": [
           "-jar", "${LD_MCP_JAR:-tools/ld-mcp-vocab.jar}",
           "--ontologies", "src/main/resources",
           "--generate-shapes",
           "--shapes", "oslo-ld-kit/rules/ssn-sosa-rules.ttl",
           "--prefix-registry", "src/main/cc/prefix/prefix.cc.ttl"
         ]
       }
     }
   }
   ```

   `--prefix-registry` is optional: a download of
   [prefix.cc/popular/all.file.ttl](http://prefix.cc/popular/all.file.ttl), kept outside the
   ontology directory, so that `validate_file` can tell a known but unloaded vocabulary from a typo.
   Add `--rules <file>` for a Jena rules file if the project has one (see the
   [ld-mcp README](https://github.com/milieuinfo/ld-mcp#ld-mcp-vocab)).

## Keeping it up to date

Change the kit in its own repository, never in a project's copy: a change made in
`oslo-ld-kit/` or `.claude/skills/` of a project conflicts with, or is overwritten by, the next
update.

**Releasing a change** (maintainer of the kit): raise `version` in `.claude-plugin/plugin.json`
(patch for a correction, minor for a new rule or skill), check with
`claude plugin validate --strict .`, commit and push.

**Updating a project** (maintainer of the project), with a clean working tree:

```bash
git subtree pull --prefix oslo-ld-kit https://github.com/milieuinfo/oslo-ld-kit.git main --squash
python oslo-ld-kit/sync.py
git add .claude/skills && git commit -m "oslo-ld-kit <version>"
```

Review the changes to the guide and the rules (`git show` of the squash commit), and validate the
project's examples again. Users of the project receive the update with `git pull`; `ld-vocab` reloads
changed rules by itself on the next tool call.

**Without a project:** the repository is also a Claude Code plugin (`oslo-ld`), for using the
skills elsewhere: `claude plugin marketplace add milieuinfo/oslo-ld-kit` and
`claude plugin install oslo-ld@oslo-ld-kit`. The plugin is updated only when its `version` changes
(`claude plugin marketplace update oslo-ld-kit`, or auto-update in `/plugin` → Marketplaces). Do
not enable it in a project that has the kit as a subtree: the skills would then exist twice, with
possibly different versions.

## Contributing

A lesson learnt in a project goes here, not into a project's private notes: a rule into the guide
(next free R-number), a checkable rule also into `rules/`, a recurring pattern into
`guide/patterns.md`, a workflow into a skill. Check with `claude plugin validate --strict .` and run
the rules against the examples of OSLOthema-SSNSOSA-VL before publishing a change.

British English throughout. The guide is project-neutral: anything specific to one project belongs
in that project's profile.
