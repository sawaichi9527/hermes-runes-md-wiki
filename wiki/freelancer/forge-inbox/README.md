# Forge Inbox

Status: runtime draft inbox / untrusted proposals only

This directory is the governed draft inbox for the `freelancer` workspace.

Allowed use:

- place draft memory proposals here before human review
- keep unreviewed agent-generated material isolated from trusted memory
- review, approve, reject, or promote proposals through governed tooling

Important boundaries:

- files in `forge-inbox/` are not trusted memory
- agent-generated drafts here must not be treated as reviewed knowledge
- real local proposal drafts are local working artifacts and should normally not be committed
- committed repository content should stay limited to this README and `.gitkeep`

Trusted memory belongs in reviewed workspace Markdown files outside `forge-inbox/`.
