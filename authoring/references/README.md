# References

Reference material that shapes how the agents write this world. Nothing here is canon and nothing here is copied source text.

## The chain

When a role works, it reads, in this order (the loader reports which levels exist):

1. `roles/<role-id>.md`: cards written for that one role (the nine roles that most shape the world should have one)
2. `categories/<category-id>.md`: cards shared by the roles in a category (for example description and exposition)
3. `../../voice.md`: the world's own voice, the fallback every role has

A role without its own file inherits the category cards and the voice. You do not need a reference for every role.

## What goes in a file

- **Technique cards** in the shape of `CARD-TEMPLATE.md`: the desired effect, the mechanism that produces it, how it would look in this world, and what to avoid. A card describes a technique in your own words. It is not a summary of the work and quotes at most a few words.
- **Evidence notes**: which edition or episode was actually read, where, what was not read, spoiler ceiling.

## Exemplars

`exemplars/` holds two or three short original passages per prose role that the user approved as "this is the voice". They are the strongest style signal. Each starts with `status: proposed` until the user changes it to `approved`. They must be original text written for this world.

## Rules

- Source material stays outside this repository. Record a title, edition, a locator and your own notes.
- Unread or unavailable material is marked unreviewed, never summarized from memory as if read.
- Author influence means transferable mechanisms, not signature phrasing, names, scenes or plot.
