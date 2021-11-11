import urllib.request as request


def addrRes(addr:str,currency:str):
    url=f"https://blockchair.com/{currency}/address/{addr}"
    with request.urlopen(url) as blkchr:
        page=blkchr.read().decode()

    idx=page.find("<span v-update:raw=\"value !== defaultValue ? value : undefined \" v-mount:raw=\"value !== defaultValue ? value : undefined \" v-tooltip=\"''\" class=\"wb-ba\">")
    return (page)
    curStr=page[idx:idx+40].split(">")[1]
    txtPrice=curStr[1:-5]
    return txtPrice

if __name__=="__main__":
    eth="0xaae8b51a07140c5ab749cbe4a3f56d32969ac4e8"
    cur="ethereum"
    print(addrRes(eth,cur))

# ignore this:
"""
def BTCRes(addr: str):
    url="https://www.blockchain.com/btc/address/"

def ETHRes(addr: str):
    url="https://www.blockchain.com/eth/address/"

def XDGRes(addr: str):
    pass

def DOTRes(addr: str):
    pass

def SOLRes(addr:str):
    pass

def ADARes(addr: str):
    pass

#"""