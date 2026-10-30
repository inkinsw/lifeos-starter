# private/

Sensitive originals live here: health records, bank statements, documents about other people, and a
roster of the people in your life (`people.md`). **Git ignores everything in this folder except this
README**, so none of it reaches a remote. `scripts/wrap.py` blocks a commit if anything here gets tracked.

The wiki keeps a bland one-line pointer to a file here ("lab results from 2026-11, in private/health/"),
so the agent knows it exists and can open it when asked, without the content ever being committed.

Back this folder up yourself (an encrypted drive or a cloud folder you trust). Git does not.
