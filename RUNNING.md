# Bookstore inventory

The inventory starts with Jane Austen, Neil Gaiman, Terry Pratchett, and five
books. `bookstore.js` adds Ursula K. Le Guin, *The Left Hand of Darkness*
and *The Dispossessed*. Author biographies are embedded documents. Books
reference one or more authors through `author_ids`.

Set `MONGODB_ATLAS_URL`, `MONGODB_ATLAS_USER`, and `MONGODB_ATLAS_PWD` in your
shell. Keep the connection URL separate from the username and password.
If these variables are stored in a private `.env` file, load them with
`set -a; source .env; set +a`. This file is excluded from Git.

Run these commands from the repository root:

```bash
uv sync
mongosh "$MONGODB_ATLAS_URL" --apiVersion 1 --username "$MONGODB_ATLAS_USER" --file bookstore.js
uv run python src/nosql_lab/bookstore_report.py
```

mongosh prompts for the database password. The shell script replaces the
`bookstore.authors` and `bookstore.books` collections with the inventory.

The Python report queries Neil Gaiman, Terry Pratchett, and Ursula K. Le Guin.
It resolves books from their stored `author_ids`, so *Good Omens* appears
under both of its authors. The report contains three authors and six book
entries, representing five distinct books.
