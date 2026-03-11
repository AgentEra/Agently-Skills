# Built-In Tools

Agently currently ships three main built-in tool families that are worth treating as first-class options.

## 1. Search

Use `Search(...)` when the request needs:

- web search
- news search
- Wikipedia-only search
- arXiv search

Important knobs:

- `proxy`
- `timeout`
- `backend`, `search_backend`, `news_backend`
- `region`
- `options`

The main async methods are:

- `search(...)`
- `search_news(...)`
- `search_wikipedia(...)`
- `search_arxiv(...)`

## 2. Browse

Use `Browse(...)` when the request needs web-page reading rather than just search hits.

Important knobs:

- `proxy`
- `timeout`
- `response_mode`
- fallback chain controls for `pyautogui`, `playwright`, and `bs4`

The main method is:

- `browse(url)`

Use Browse when the model needs actual page content, not just search-result snippets.

## 3. Cmd

Use `Cmd(...)` only when the request should run guarded shell commands.

Important knobs:

- `allowed_cmd_prefixes`
- `allowed_workdir_roots`
- `timeout`
- `env`

The main method is:

- `run(cmd, workdir=None, allow_unsafe=False)`

`Cmd` is designed around allowlist checks. It is not a general unrestricted shell tool.

## 4. Selection Rule

- need public information discovery -> Search
- need page content extraction -> Browse
- need bounded local shell access -> Cmd
