#!/usr/bin/env python3
"""Print the books associated with selected bookstore authors."""

import logging
import os

from pymongo import MongoClient
from pymongo.errors import PyMongoError
from pymongo.server_api import ServerApi

MONGODB_ATLAS_URL = os.environ.get("MONGODB_ATLAS_URL")
MONGODB_ATLAS_USER = os.environ.get("MONGODB_ATLAS_USER")
MONGODB_ATLAS_PWD = os.environ.get("MONGODB_ATLAS_PWD")
AUTHOR_IDS = ["author_002", "author_003", "author_004"]
LOGGER = logging.getLogger(__name__)


def main():
    """Connect to Atlas and print each selected author's linked books."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    client = None
    try:
        if not all((MONGODB_ATLAS_URL, MONGODB_ATLAS_USER, MONGODB_ATLAS_PWD)):
            raise ValueError("Set MONGODB_ATLAS_URL, MONGODB_ATLAS_USER, and MONGODB_ATLAS_PWD")
        client = MongoClient(
            MONGODB_ATLAS_URL,
            username=MONGODB_ATLAS_USER,
            password=MONGODB_ATLAS_PWD,
            server_api=ServerApi("1"),
            serverSelectionTimeoutMS=10000,
        )
        client.admin.command("ping")
        LOGGER.info("Connected to MongoDB Atlas")
        database = client["bookstore"]
        authors = database["authors"]
        books = database["books"]
        selected_authors = {"_id": {"$in": AUTHOR_IDS}}
        count = authors.count_documents(selected_authors)
        if count != len(AUTHOR_IDS):
            raise ValueError("Selected authors are missing; run bookstore.js first")
        print(f"Authors: {count}")
        for author in authors.find(selected_authors).sort("_id", 1):
            print(f"\n{author['name']}")
            # Resolve the many-to-many references from the stored documents.
            linked_books = books.find({"author_ids": author["_id"]}).sort(
                [("published_year", 1), ("title", 1)]
            )
            for book in linked_books:
                print(f"  {book['title']} ({book['published_year']})")
        return 0
    except (PyMongoError, ValueError) as error:
        # Avoid logging connection strings or credentials from driver errors.
        if isinstance(error, ValueError):
            LOGGER.error("%s", error)
        else:
            LOGGER.error("MongoDB report failed (%s)", type(error).__name__)
        return 1
    finally:
        if client is not None:
            client.close()


if __name__ == "__main__":
    raise SystemExit(main())
