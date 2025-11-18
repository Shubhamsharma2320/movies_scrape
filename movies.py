import requests
from bs4 import BeautifulSoup
import csv

# URL for IMDb Top 250
URL = "https://www.imdb.com/chart/top"
save_path = r"C:\Users\JK TECH COMPUTER\Desktop\ws portfolio\imdb_top250.csv"

# Send HTTP request
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(URL, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# Find all movie rows
movies = soup.select("li.ipc-metadata-list-summary-item")

data = []
for i, movie in enumerate(movies, start=1):
    try:
        title_tag = movie.select_one("h3.ipc-title__text")
        rating_tag = movie.select_one("span.ipc-rating-star--imdb")
        link_tag = movie.select_one("a.ipc-title-link-wrapper")

        title = title_tag.text if title_tag else "N/A"
        rating = rating_tag.text.strip("IMDb Rating:") if rating_tag else "N/A"
        link = "https://www.imdb.com" + link_tag["href"] if link_tag else "N/A"

        # Extract year from text (inside parentheses)
        year = "N/A"
        if "(" in title and ")" in title:
            year = title.split("(")[-1].strip(")")
            title = title.split("(")[0].strip()

        data.append([i, title, year, rating, link])

    except Exception as e:
        print(f"Error parsing movie {i}: {e}")

# Save data to CSV
with open(save_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Rank", "Title", "Year", "Rating", "Link"])
    writer.writerows(data)

print(f"✅ Scraping complete! {len(data)} movies saved to {save_path}")
