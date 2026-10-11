---
name: world-mode
description: Set the task mode for this session (explore, extend, edit or lock), or turn it off. Only the user can run it; the write guard then enforces it.
argument-hint: explore | extend | edit | lock | off
disable-model-invocation: true
---

The user ran `/world-mode $ARGUMENTS`. If the argument was `off`, a hook has removed the mode: nothing is enforced any more, so say so in one line and go on (the ordinary rules still apply, and you still ask the user for the task mode). Otherwise a hook has recorded the mode, and the write guard now enforces it for this session:

<!-- modes:start -->
- `explore`: ideas only; no existing world page may be changed (new drafts and designs are fine).
- `extend`: add new pages, sections and links; every original line of an existing page must survive.
- `edit`: change existing pages with a change record; protected pages still need the user's authorization.
- `lock`: read-only; nothing may be written.
<!-- modes:end -->

Confirm the mode (or that it is off) in one line and continue with the task under it. If the guard blocks a write, do not look for a way around it: tell the user what you wanted to write and that they can switch the mode with `/world-mode`.
