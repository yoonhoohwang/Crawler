from urllib.request import Request, urlopen
from operator import eq
import json
import time
import logging.handlers
from threading import Thread
from datetime import datetime
import pandas as pd




Bithumb = ['BTC', 'ETH', 'ZEC', 'XMR', 'XRP', 'EOS']
Poloniex = []
Bittrex = []
Yobit = []

'''
Bithumb = ['BTC', 'ETH', 'ZEC', 'XMR', 'XRP', 'EOS']
Poloniex = ['ETH', 'ZEC', 'XMR', 'XRP']
Bittrex = ['ETH', 'ZEC', 'XMR', 'XRP']
Yobit = ['MAX']
'''


class Agent2:
    def __init__(self):
        
        self.l1 = ""
        self.l2 = ""
        self.l3 = ""
        self.l4 = ""
        self.l5 = ""
        self.l6 = ""
        self.Webpage = ""
        self.now = 0   
        
        self.data = {"TIME" : [], "MARKET" : [], "FROMSYMBOL" : [], "TOSYMBOL" : [], 
                     "PRICE" : [], "CHANGE24HOUR" : [], "CHANGEPCT24HOUR" : []}
        
        self.dataframe1 = pd.DataFrame(self.data, columns = ["TIME", "MARKET", "FROMSYMBOL", 
                                     "TOSYMBOL", "PRICE", "CHANGE24HOUR", "CHANGEPCT24HOUR"])

    def main(self):
        self.t1 = time.time()
        
        while True:
            time.sleep(2)          
            self.Monitor = 0
            self.workerSum = 0
            self.workerList = []
            self.Warning = 0
            self.switching = 0
            self.hashRate = 0            
            self.TG_refresh = 30
            self.ratio = 10
            self.concat = ""
            self.concat_1 = ""
            
            self.t2 = time.time()

            B = ["Bithumb", 'KRW']
            P = ["Poloniex", 'BTC']
            Yo = ["Yobit", 'BTC']
            BT = ["Bittrex", "BTC"]

            B.extend(Bithumb)
            P.extend(Poloniex)
            Yo.extend(Yobit)
            BT.extend(Bittrex)

            list = [B, P, Yo, BT]
            self.t3 = time.time()
            
            str_date = str(datetime.now())
            d_date = datetime.strptime(str_date , '%Y-%m-%d %H:%M:%S.%f')
            self.reg_format_date = str(d_date.strftime("%Y-%m-%d %H:%M:%S"))

            for exchange in list:
                time.sleep(1)      
                a = ""
                place = exchange[0]
                market = exchange[1]
                market = str(market)
                target_coin = exchange[2:]
                for coins in exchange[2:]:
                    a = a + str(coins) + ","
                a = a[:-1]
                Url = "https://min-api.cryptocompare.com/data/pricemultifull?fsyms=" + \
                      a + "&tsyms=" + market + "&e=" + str(place)

                Req = Request(Url, headers={'User-Agent': 'Mozilla/5.0'})
                self.Webpage = urlopen(Req).read()
                jsonToPython = json.loads(self.Webpage.decode('utf-8'))
                logger = logging.getLogger()
                logger.setLevel(logging.NOTSET)

                for i in target_coin:
                    self.l1 = (jsonToPython['RAW'][i][market]['MARKET'])
                    self.l2 = (jsonToPython['RAW'][i][market]['FROMSYMBOL'])
                    self.l3 = (jsonToPython['RAW'][i][market]['TOSYMBOL'])
                    self.l4 = (jsonToPython['RAW'][i][market]['PRICE'])
                    self.l5 = (jsonToPython['RAW'][i][market]['CHANGE24HOUR'])
                    self.l6 = (jsonToPython['RAW'][i][market]['CHANGEPCT24HOUR'])

                    data = {"TIME" : [self.reg_format_date], "MARKET" : [self.l1], 
                            "FROMSYMBOL" : [self.l2], "TOSYMBOL" : [self.l3],
                            "PRICE" : [self.l4], "CHANGE24HOUR" : [self.l5], 
                            "CHANGEPCT24HOUR" : [self.l6]}
                    print(data)
                    
            
                    dataframe = pd.DataFrame(data, columns = ["TIME", "MARKET", "FROMSYMBOL", "TOSYMBOL", 
                                                              "PRICE", "CHANGE24HOUR", "CHANGEPCT24HOUR"])
                
                    self.dataframe1 = self.dataframe1.append(dataframe)
                
                monitor = "userpath" #경로 작성
                self.dataframe1.to_csv(monitor, index = False)
                
                        
            
            
if __name__ == "__main__":
    agent = Agent2()
    Thread(target = agent.main()).start()