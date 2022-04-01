from collections import defaultdict

import yaml

# you need to maintain about 85.21 verses per day to complete the bible in one
# year
VERSES_PER_DAY = 85.21
MAX_BEHIND = 30
DAYS = 365


with open('bookinfo.yml') as f:
    bookinfo = yaml.safe_load(f)


total_verses = 0
for book_id, versecount in bookinfo['verse-count-by-book'].items():
    total_verses += versecount


def next_reading_info():
    for book_id in bookinfo['book-names']:
        chapters = bookinfo['verse-count-by-chapter'][book_id]
        for chapter, versecount in chapters.items():
            yield book_id, chapter, versecount


# generate a plan for one year
gen = next_reading_info()
consumed = 0.0
day_target = 0.0
plan = defaultdict(list)
for day_num in range(1, 366):
    day_target += VERSES_PER_DAY
    min_goal = day_target - MAX_BEHIND
    while consumed < min_goal:
        book_id, chapter, verses = next(gen)
        plan[day_num].append((book_id, chapter, verses))
        consumed += verses

for day_num, day_readings in plan.items():
    total_verses = sum([r[2] for r in day_readings])
    print(f"Day {day_num} ({total_verses} verses):")
    for book_id, chapter, verses in day_readings:
        print(f"  {bookinfo['book-names'][book_id]} {chapter} ({verses} verses)")
