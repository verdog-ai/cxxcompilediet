<!-- This file is intended to be tool-verified by Verdog in a future release. -->

`MUST` and `MUST NOT` are verifier requirements; `MAY` grants permission. If
the verifier cannot prove a requirement, it MUST report a violation.

An **authored file** has `ownership: "user"` in `project.json`. An **entity
scope** is a package, workflow, subroutine, profile, feature, node, or visit
directory identified by `project.json`. A **production consumer** is an
authored file below the package that statically imports, calls, loads, or
includes a declaration or resource; generated files and tests are excluded.
The **owner scope** is the deepest entity scope containing every production
consumer. A declaration or prompt resource with no production consumer MUST
be removed, except the package-root `Payload`.

# State placement rules

A **payload** is data transported through `Input`, `Output`, `Success.output`,
or a call. **Node-local state** is the authored `class State` in a non-Feature
node's `impl.py`. **Feature state** is the runtime `FeatureState` passed to a
Feature-node visit. A **graph invocation** runs one workflow or subroutine from
enter to exit or failure; invoking a child starts another graph invocation.
Runtime `WorkflowState` aggregates node and Feature slots for transition
validation; authored code MUST NOT import, construct, or transport it.

- A value created by `visit_impl` and not needed after that call returns MUST
  remain a local variable.
- A value needed by later visits to the same node, but by no non-Feature visit to
  another node, MUST be in that node's `State`.
- A value needed by a visit to another node MUST travel through the
  producer's `Output` and the consumer's generated `Input`.
- A call node's `State` MAY retain data across revisits to that call node during
  one parent graph invocation. Data needed by sibling parent nodes or separate
  call nodes MUST travel in the parent payload.
- Node-local state is initialized once per graph invocation. Non-Feature visits
  receive only their target node's state. Feature visits MUST call
  `FeatureState.get` and `FeatureState.replace` only with Feature definitions;
  they MUST NOT read node-local state.
- A Feature MUST have type `bool`, `int`, `float`, or `str` and MUST occur in at
  least one edge condition or effect. Feature declarations belong in
  `project.json`; features have no authored module or initializer callback.
- Feature values start as `None` at each subroutine invocation. Only
  Feature-node visits MAY initialize or update them, using
  `state.replace(FEATURE, value)` and returning `FeatureSuccess`.
  Conditions read the state before the source visit, so initialization MUST
  precede any node whose outgoing conditions read that feature.
- A shared payload or state type MUST be declared at its owner scope. It MAY be
  in package-root `impl.py` only when it is `Payload` or appears, directly or
  transitively, in `Payload`'s annotations.

# Prompt placement rules

A **prompt sink** is the prompt argument of `context.invoke` in an Agent-node
visit. A **primary template** is the `.md.j2` file rendered for that argument.
A **reference resource** is an authored file read only as data and never
imported or executed.
The consumers of a prompt resource are the Agent visits whose prompts contain
it, including through templates or reference resources. Paths beginning with
`nodes/` below are relative to the consuming subroutine.

- Repository-authored text reaching a prompt sink MUST originate in a primary
  template or a non-executable reference resource. It MUST NOT originate in a
  Python literal, f-string, concatenation, or other executable source.
- Runtime values from `Input`, `State`, `Context`, agent replies, or tool output
  MAY be supplied to a template. Repository-authored fallback text supplied as
  a template value is prompt text and MUST instead be in the template.
- Unresolved prompt provenance MUST be reported as a violation.
- A visit with one primary template MUST store it as
  `nodes/<target-id>/visit/<edge-id>/prompt.md.j2`.
- Multiple primary templates used only by one visit MUST be stored as
  `nodes/<target-id>/visit/<edge-id>/prompts/<name>.md.j2`.
- A non-primary resource used by one visit MUST be stored as
  `nodes/<target-id>/visit/<edge-id>/prompts/<name>.<extension>`.
- A resource used by multiple visits MUST be stored as
  `<owner-scope>/prompts/<name>.<extension>`.
- Shared fragments and reference resources follow the same consumer and owner
  calculation. Prompt-rendering Python helpers follow the code rules below.
- `<name>` MUST match `[a-z][a-z0-9_]*`; `<extension>` is the complete nonempty
  suffix after that name, such as `md.j2` or `tex`.

# Code placement rules

Authored declarations MUST use these paths. `<subroutine>` denotes its complete
nested `subroutines/<id>/subroutines/<id>/...` directory. `<workflow>` denotes
the complete root or nested `workflows/<id>` directory.

| Declaration | Required path |
| --- | --- |
| `Payload` and its annotation types | `<package>/impl.py` |
| Subroutine `Input`, `Output`, `Params` | `<subroutine>/impl.py` |
| Non-Feature node `Output`, `State` | `<subroutine>/nodes/<node-id>/impl.py` |
| Edge-selected `visit_impl` | `<subroutine>/nodes/<target-id>/visit/<edge-id>/impl.py` |
| Workflow dependencies | `<workflow>/requirements.txt` |

- Workflow profiles, sessions, and bindings MUST be configured in
  `project.json`. Their Python declarations are generated; workflows and
  profiles have no authored configuration callback.
- An authored helper is a top-level declaration not listed above and not
  `Payload` or one of its annotation types. A helper with one production
  consumer MUST be defined in that consumer's module; a helper with multiple
  consumers MUST be in a module at their owner scope.
- Authored helper modules MUST NOT be named `runtime.py` or `utils.py`.
- Authored Python MUST NOT occur below `edges/` or `bindings/`; edge-selected
  behavior belongs to the target visit.
- Graph structure MUST be represented in `project.json`. Every file marked
  `generated` there MUST match its recorded size and SHA-256 hash; generated
  Python and generated `pyproject.toml` MUST NOT be edited.
