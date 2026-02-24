# ERG Topic Forum — Claude Project Context

## Project overview

This is the **Earthquake Research Group (ERG) Topic Forum** — a Quarto website hosted on GitHub Pages for the University of Melbourne's earthquake science group. It is used to share paper discussions, methods demos, work-in-progress updates, and earthquake science topics.

Live site: https://earthquake-research-group.github.io/erg-topic-forum/
Repo: https://github.com/earthquake-research-group/erg-topic-forum

## Audience

PhD students and academic researchers in earthquake science (seismology, tectonics, geodesy). Content should be technically accurate and appropriately concise — session pages are structured summaries, not full papers.

## Standing instructions

- **Never commit or push without explicit instruction.** Always stage and show diffs; wait for the user to confirm before committing.
- Keep content concise. Bullet points over paragraphs where appropriate.
- Follow Quarto conventions: `.qmd` files, YAML front matter, callout blocks (`::: {.callout-note}`), etc.

## Project structure

```
sessions/          Each session is a subdirectory with index.qmd, paper.bib, assets/
templates/session/ Template to copy when creating a new session
topics/            Glossary, reading list
bibliography/      Central references.bib (shared BibTeX)
docs/              How-to and documentation pages
_quarto.yml        Site config (navbar, theme, Giscus comments, MathJax)
styles/            SCSS theme (erg-theme.scss)
scripts/           Helper utilities
```

## Creating a new session

1. Copy `templates/session/` to `sessions/<slug>/` where slug is `topic-name` or `author_topic`
2. Edit `sessions/<slug>/index.qmd` — fill in YAML front matter (title, author, date, categories)
3. Add paper BibTeX entry to `sessions/<slug>/paper.bib`
4. Place paper PDF at `sessions/<slug>/assets/paper.pdf` if available
5. Add the session to `sessions/index.qmd` listing

Session page sections (from template):
- Paper details (citation, abstract)
- Presentation summary (takeaway, key points, why it matters for ERG)
- Session resources (BibTeX/PDF buttons)
- Group discussion (proposed questions + Giscus comments)

## Quarto notes

- Build/preview: `quarto preview` or `quarto render`
- Output goes to `_site/` (git-ignored for local builds; CI deploys via GitHub Actions)
- Comments use Giscus (GitHub Discussions), configured in `_quarto.yml`
- Math via MathJax; theme is Cosmo + custom SCSS
