# Writing posts in OpenKnowledge

OpenKnowledge (OK) edits the markdown files of this repo directly. Hugo builds the site from the same files, so nothing is exported or converted.

## Setup on a new machine

```bash
cd /Users/jakub/CODE/__BLOG/jakubjezek001.github.io
ok init          # registers the MCP server and agent skills on this machine
ok start --open  # or open the folder in OpenKnowledge.app
```

The project config is committed: `.ok/config.yml`, `.okignore` and the front matter schema in `.ok/schemas/`. `ok init` only adds what is machine-local (`.ok/local/`, which git ignores). The `open-knowledge` skill folders under `.claude/`, `.codex/`, `.github/skills/`, `.opencode/` and `.pi/` were written by `ok init` for each agent. You can delete the ones for agents you don't use.

## What the settings do

| Setting | Why |
|---|---|
| `content.attachmentFolderPath: ./` | A pasted or dropped image lands next to the post's `index.md`. Hugo serves it from there as part of the page bundle. |
| `autoSync.default: "off"` | OK never commits or pushes by itself. A post goes to `develop` only after the AI-text review (AGENTS.md, Rule 1). Do not switch this to `full`. |
| `contentRules.frontmatter` | Checks every `content/posts/*/index.md` against `.ok/schemas/post.frontmatter.schema.json`: required fields, kebab-case slug, description length, `draft` is a boolean. The warnings are advisory. They never block a save. |
| `contentRules.okf.generate.index: false` | Keep it off. OK would write an `index.md` into every folder. In Hugo, an `index.md` in `content/posts/` turns the whole blog section into a single page. |
| `.okignore` | Hides Hugo internals (`themes/`, `layouts/`, `public/`, `resources/` and so on) so search and agents only see hand-written markdown. |

## Writing conventions that work in both OK and Hugo

- One folder per post: `content/posts/<slug>/index.md`, with its images next to it.
- Front matter follows the format in `AGENTS.md`. `draft: true` stays until Jakub publishes.
- Links between posts are relative: `[text](../other-slug/index.md)`, optionally with `#heading-anchor`. Hugo's link render hook turns them into `/posts/<slug>/`. The same link resolves in OK and on GitHub.
- Images are relative: `![what the image shows](./diagram.png)`. Hugo adds the size, lazy loading and scaling (see `layouts/_default/_markup/render-image.html`).
- Avoid Hugo shortcodes (`{{</* */>}}`) in posts. OK does not know them. Plain markdown and a little raw HTML are fine.
- Wiki links (`[[...]]`) don't work in Hugo. Use normal markdown links.

## Projects

`content/projects/` still holds placeholder pages from an old theme. The cascade in `hugo.toml` keeps that section out of the build. When real projects are written there, delete the placeholders and remove that cascade block. The menu entry for Projects is commented out in `hugo.toml`.
