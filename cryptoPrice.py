import urllib.request as request

def prices(curs: list):
    out={}
    for currency in curs:
        with request.urlopen(f"https://coinmarketcap.com/currencies/{currency}") as cmc:
            # open coin market cap page -- you may want to recode this for yourself if there is an exchange page with lower latency to your server
            page=cmc.read().decode() # decodes from bin

        idx=page.find("<div class=\"priceValue \">") # indexes the price value
        curStr=page[idx:idx+48].split(">")[1] # grabs the part of the page containing the exact price
        txtPrice=curStr[1:-5] # extracts the exact price--without a '$'
        out[currency]=txtPrice
    
    return out

# debugging and testing
if __name__=="__main__":

    lookup=["dogecoin","bitcoin","ethereum","polkadot","solana"]
    
    print(prices(lookup))
