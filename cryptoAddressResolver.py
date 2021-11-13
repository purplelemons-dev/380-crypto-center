import urllib.request as request
from bs4 import BeautifulSoup as bs4

def addrRes(addr:str,currency:str):
    """Returns a string of the value of the wallet given currency and address."""
    url=f"https://blockchair.com/{currency}/address/{addr}/"

    with request.urlopen(url) as blkchr:
        page=blkchr.read().decode()
    
    soup=bs4(page,"html.parser")

    one=soup.find_all("span", class_="value-wrapper d-iflex ai-center",attrs={":value":"data ? data.balance_usd : null"})[0].find_all("span",class_="wb-ba")[0]

    return one.string

def priceToInt(price:str):
    return float(price.strip().replace(",",""))
    
if __name__=="__main__":
    eth="0xaae8b51a07140c5ab749cbe4a3f56d32969ac4e8"
    dot="14i9mu3spoub2gi29W6ngemNoN4NcJVyPKCjwuMRKR8cto41"
    cur="ethereum"
    price=addrRes(eth,cur)
    print(f"${price}", priceToInt(price))
