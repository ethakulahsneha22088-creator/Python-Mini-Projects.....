import pandas as pd
import requests
from bs4 import BeautifulSoup

response = requests.get("https://www.flipkart.com/search?q=samsung%20mobiles&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off")
print(response)

soup = BeautifulSoup(response.content,'html.parser')
# raw HTML received from a website and convert it into a structure that Python can easily search and extract data from.
# A parser converts raw HTML code into a structured format so that Python can understand, navigate, and extract information from it.
# print(soup)

names = soup.find_all("div",class_ = "RG5Slk")
# print(names)
name = []
for i in names[0:10]:
    d = i.get_text()
    name.append(d)
# print(name)


ratings = soup.find_all("div", class_="MKiFS6")
# print(ratings)
rate = []
for i in ratings[0:10]:
    d = i.get_text()
    rate.append(float(d))
# print(rate)

prices = soup.find_all("div",class_ = "hZ3P6w DeU9vF")
# print(prices)
price = []
for i in prices[0:10]:
    d = i.get_text()
    price.append(d)
# print(price)
result = [i.replace("₹","") for i in price]
# print(result)


images = soup.find_all("img",class_ = "UCc1lI")
# print(images)
image = []
for i in images[0:10]:
    data = i.get("src")
    image.append(data)
# print(image)


df = pd.DataFrame()
df["names"] = name
df["prices"] = result
df["ratings"] = rate
df["images"] = image
print(df)
df.to_csv("mobiles.csv")