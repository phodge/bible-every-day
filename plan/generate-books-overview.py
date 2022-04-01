from collections import defaultdict

import MySQLdb
import yaml

# king james version
T = 2
SKIP = {
  'TOB',
  'JDT',
  'ESG',
  'WIS',
  'SIR',
  'BAR',
  'LJE',
  'S3Y',
  'SUS',
  'BEL',
  '1MA',
  '2MA',
  '1ES',
  'MAN',
  '2ES',
}

db = MySQLdb.connect(
    host="127.0.0.1",
    user="root",
    passwd="coolroot",
    db="bible_api",
)
c = db.cursor()
c.execute(f"SELECT DISTINCT(book_id), book_num, book FROM verses WHERE translation_id = {T} ORDER BY book_num")
books = {}
for row in c.fetchall():
    book_id, _, book_name = row
    if book_id not in SKIP:
        books[book_id] = book_name

# now get verse counts
c.execute(f"SELECT book_id, chapter, COUNT(*) FROM verses WHERE translation_id = {T} GROUP BY book_id, chapter ORDER BY book_id, chapter")
totalverses = 0
bookinfo = {}
versecount = {}
chapter_versecount = defaultdict(dict)
book_versecount = defaultdict(int)
for row in c.fetchall():
    book_id, chapter, versecount = row
    if book_id not in SKIP:
        book_versecount[book_id] += versecount
        chapter_versecount[book_id][chapter] = versecount

with open('bookinfo.yml', 'w') as f:
    # write these to the yaml file
    yaml.dump({
        'book-names': books,
        'verse-count-by-book': dict(book_versecount),
        'verse-count-by-chapter': dict(chapter_versecount),
    }, f, sort_keys=False)
