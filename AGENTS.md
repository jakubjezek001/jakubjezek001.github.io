# Blog repo: instructions for coding agents

This is Jakub Ježek's personal blog (thestreamlighter.com), a Hugo site. Posts are in `content/posts/<slug>/index.md`. Work on the `develop` branch; `main` and `gh-pages` are what gets published. This file is the main instruction file. `CLAUDE.md` only imports it, so edit this file, not that one.

## How posts get here

1. Research, planning and the first draft happen in the private job-search workspace (`/Users/jakub/CODE/job-agent-ats`, folder `publishing/blog/`). Drafts arrive here as `draft: true` posts with only a basic structure.
2. Jakub rewrites each post himself by typing.
3. He cross-reviews it with an agent for AI-sounding text (see `docs/ai-text-review.md`).
4. The job-search workspace controls this repo with three skills (`.agents/skills/` there): `blog-post-develop` (worktree and branch from `develop`), `blog-post-review-merge` (review, then merge to `develop`, push, remove the worktree) and `blog-post-publish` (`draft: false`, merge to `main`, deploy). Each asks Jakub before anything leaves his machine.

The path of this repo is `BLOG_REPO_PATH` in the job-search workspace's `.env` (currently `/Users/jakub/CODE/__BLOG/jakubjezek001.github.io`).

## Rule 1: nothing that feels AI-written gets published

A post may only go live (`draft: false`, merged to `main`) when all of these are true:

- Jakub has rewritten it by hand. A post that is still the agent's first-draft structure is not publishable.
- The review in `docs/ai-text-review.md` has been run on the current text and the verdict is **PASS**. A review of an older version does not count.
- Jakub has read the final text and said it is fine to publish.

Agents must:

- Push and merge only through the three skills above, and only after the step's own conditions and Jakub's explicit yes. Pushing to `develop` needs a PASS review of the exact text (`blog-post-review-merge`). Setting `draft: false`, merging to `main` and deploying need a PASS review, a matching text hash and Jakub's yes in the same message (`blog-post-publish`). Any other way of publishing is not allowed. If asked to "publish" without all of that, run the review, report the verdict and stop.
- Never write or rewrite a whole post for publication. Agents may point at passages that read as AI-generated and say why. They may suggest a plainer wording for one sentence at a time. Jakub decides.
- Treat a FAIL or a "not sure" as a block. When in doubt, the post stays a draft.
- Never remove AI-text signals by adding tricks (random typos, odd punctuation, noise) to fool a detector. The goal is text that is in his voice and carries his own facts, not text that passes a tool.

## Other guard rails

- **Voice:** Jakub's voice guide is `/Users/jakub/CODE/job-agent-ats/knowledge/memory/voice.md`. Plain, slightly non-native English, first sentence says the thing, hedged guesses, one dry line at most, no hype words.
- **No unsourced facts:** every number, date, name and quote must come from Jakub or from a source he can show. `[ADD: …]` markers must be filled or deleted before publishing. A post with a leftover `[ADD` is a FAIL.
- **Confidentiality:** the biggest AYON client studios may be named, but never SN4. Check anything about Ynput's internals, unreleased features or client data with Jakub first.
- **Secrets:** never put passwords, tokens or keys in a post, a front matter field or a commit. `python/.env` is git-ignored; keep it that way.
- **Drafts are drafts:** new posts start with `draft: true`. A scheduled `date` in the future does not publish them, but `draft: true` must stay until Jakub changes it.
- **Don't touch what isn't asked:** leave `themes/`, `public/` and `resources/` alone (generated or vendored). Keep each commit to one post or one change.
- **Git:** no force push, no history rewriting. Work on posts in a worktree (`BLOG_REPO_PATH-worktrees/<slug>`), not in the main checkout. Commit to `main` only through `blog-post-publish`. Don't commit unless a skill or Jakub says to.

## Post file format

```yaml
---
title: "Plain title"
slug: kebab-case-slug
description: "One sentence."
tags:
  - AYON
date: 2026-11-10T09:00:00+01:00
draft: true
---
```

The body starts with `# Title`, then `##` headings. Images sit next to `index.md` in the post folder.

- The site shows the front matter `title` as the page heading and hides the body's `# Title`. If the `# Title` line says more than `title`, the extra part becomes a subtitle.
- `description` is the search and social-preview text: one sentence, about 150 to 160 characters.
- Link to another post with a relative path, `[text](../other-slug/index.md)`, and to an image with `![alt text](./picture.png)`. Hugo turns these into the published URLs, and they also work in OpenKnowledge and on GitHub. Always write alt text.
- Without an `image` in the front matter, a social card with the title is generated at build time.
- Never change the `slug` of a published post. If it must change, add the old URL to `aliases`.
- Posts are edited in OpenKnowledge. See `docs/openknowledge.md` for the setup and its guard rails.
