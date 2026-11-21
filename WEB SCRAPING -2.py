import requests
from bs4 import BeautifulSoup
import pandas as pd

# Website URL
url = "https://books.toscrape.com/"

# Send request
response = requests.get(url)

# Check response
if response.status_code == 200:

    soup = BeautifulSoup(response.text, "html.parser")

    # Extract book details
    books = soup.find_all("article", class_="product_pod")

    data = []

    for book in books:
        title = book.h3.a["title"]
        price = book.find("p", class_="price_color").text
        availability = book.find(
            "p", class_="instock availability"
        ).text.strip()

        data.append({
            "Book Name": title,
            "Price": price,
            "Availability": availability
        })

    # Store data in CSV
    df = pd.DataFrame(data)
    df.to_csv("books_data.csv", index=False)

    print("Data scraped successfully!")
    print(df)

else:
    print("Failed to access website")