// Step 2: select the bookstore database.
db = db.getSiblingDB("bookstore");

// Step 3: reload authors with stable IDs used by the books.
db.authors.drop();
db.authors.insertMany(JSON.parse(fs.readFileSync("authors.json", "utf8")));

// Step 4: reload the starter books.
db.books.drop();
db.books.insertMany(JSON.parse(fs.readFileSync("books.json", "utf8")));

// Step 5: list the starter inventory.
print("Starter authors:");
db.authors.find().sort({ _id: 1 }).forEach(author => printjson(author));
print("Starter books:");
db.books.find().sort({ published_year: 1, title: 1 }).forEach(book => printjson(book));

// Step 6: add two books that reference a new author.
db.books.insertMany([
  { title: "The Left Hand of Darkness", published_year: 1969, author_ids: ["author_004"] },
  { title: "The Dispossessed", published_year: 1974, author_ids: ["author_004"] }
]);

// Step 7: add the missing author with an embedded biography.
db.authors.insertOne({
  _id: "author_004",
  name: "Ursula K. Le Guin",
  nationality: "American",
  bio: {
    short: "American author of science fiction and fantasy.",
    long: "Ursula K. Le Guin wrote science fiction and fantasy that explored cultures, social institutions, and individual choices. Her novels include The Left Hand of Darkness and The Dispossessed."
  }
});

// Step 8: include starter authors and the new author in the filter.
const authorIds = ["author_002", "author_003", "author_004"];
print("Books matching the selected authors:");
db.books.find({ author_ids: { $in: authorIds } })
  .sort({ published_year: 1, title: 1 })
  .forEach(book => printjson(book));
