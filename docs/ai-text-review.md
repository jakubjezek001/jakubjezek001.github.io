# Review: does this post read as AI-written?

Run this on the current text of one post before it can be published. Read the post in full first. Read Jakub's voice guide (`/Users/jakub/CODE/job-agent-ats/knowledge/memory/voice.md`) and, for comparison, his published posts in `content/posts/` that were written before 2025 (`hidden-cost-of-digital-delivery`, `studio-funding`).

Report, in this order: the verdict, the blocking problems, then the notes. Quote the exact sentence for each problem. Do not rewrite the post.

## Blocking (any one means FAIL)

1. **Leftovers:** `[ADD`, `TODO`, `lorem`, "as an AI", "I hope this helps", "Here is", or text that talks to the reader of a chat.
2. **No hand of the author:** no specific detail only Jakub could know (a named studio, a number, a mistake he made, a date, a tool he used). A post with no such detail is generic.
3. **Invented facts:** a number, quote, date, name or claim that is not in Jakub's notes or sources. Ask Jakub for the source. Do not guess.
4. **Hype and stock words (three or more together; one stray word is only a note):** delve, leverage, unlock, game-changer, revolutionary, seamless, robust, landscape, tapestry, testament, navigate (figurative), "in today's fast-paced world", "it's important to note", "in conclusion", "ever-evolving".
5. **Pattern tells, more than twice:**
   - "It's not just X, it's Y" and "not only … but also" constructions.
   - Rhetorical-question openers and answers ("The result? …").
   - Lists of exactly three adjectives or three examples as a habit.
   - A bold lead-in on every bullet.
   - A tidy summary paragraph that repeats the post, or a closing line like "The future is bright".
   - Em dashes used for rhythm in most paragraphs (his own 2025 posts have about 1 per 100 words; well above 2 per 100 is a tell).
6. **Voice mismatch:** perfect, even, polished prose with no hedging ("it seems", "in my experience", "I am not sure"), when his real voice is plain, direct and slightly non-native.

## Notes (do not block alone, but report)

- Paragraph and sentence lengths all similar.
- Headings that are generic ("Key takeaways", "Why it matters").
- Examples that could belong to any studio.
- A closing question that is empty ("Thoughts?").
- Claims stated with more certainty than the evidence gives.

## Output

```
Verdict: PASS | FAIL
Post: <slug>   Version reviewed: <git commit or "working tree">   Date: <YYYY-MM-DD>

Blocking
- "<quoted sentence>" — <rule number and why>

Notes
- ...

What Jakub should do next: <one or two lines>
```

PASS needs zero blocking items and Jakub's own sign-off after he reads the text. The review is advice. It is never a reason to publish by itself, and a PASS does not allow an agent to change `draft`, merge or push.
