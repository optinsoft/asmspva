import aiohttp
import ssl
import certifi
import json
from urllib.parse import urlencode

class AsyncSmsPvaException(Exception):
    pass

class NoSMSException(AsyncSmsPvaException):
    pass

class AsyncSmsPva:
    def __init__(self, apiKey: str, apiUrl: str = 'https://smspva.com/priemnik.php'):
        self.apiKey = apiKey
        self.apiUrl = apiUrl

    def checkResponse(self, respJson: dict, successResponseCode: str, noSmsCode: str):
        if len(successResponseCode) > 0:
            if "response" in respJson:            
                code = respJson["response"]
                if code != successResponseCode:
                    if len(noSmsCode) > 0 and code == noSmsCode:
                        raise NoSMSException("No SMS")
                    if "error_msg" in respJson:
                        msg = respJson["error_msg"]
                        raise AsyncSmsPvaException(f'Error "{code}": {msg}')
                    raise AsyncSmsPvaException(f'Error "{code}": {str(respJson)}')
            else:
                raise AsyncSmsPvaException(f"Bad response: {str(respJson)}")
        return respJson

    async def doRequest(self, url: str, successResponseCode: str = '1', noSmsCode: str = ''):
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        conn = aiohttp.TCPConnector(ssl=ssl_context)
        async with aiohttp.ClientSession(connector=conn, raise_for_status=False) as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    respText = await resp.text()
                    raise AsyncSmsPvaException(f"Request failed:\nStatus Code: {resp.status}\nText: {respText}")
                try:
                    respText = await resp.text()
                    respJson = json.loads(respText)
                except ValueError as e:
                    raise AsyncSmsPvaException(f"Request failed: {str(e)}")
                return self.checkResponse(respJson, successResponseCode, noSmsCode)

    async def getBalance(self, service: str):
        url = self.apiUrl + '?' + urlencode({'metod':'get_balance','service':service,'apikey':self.apiKey})
        return await self.doRequest(url)
    
    async def getUserInfo(self, service: str):
        url = self.apiUrl + '?' + urlencode({'metod':'get_userinfo','service':service,'apikey':self.apiKey})
        return await self.doRequest(url)

    async def getCountNew(self, service: str, country: str):
        url = self.apiUrl + '?' + urlencode({'metod':'get_count_new','service':service,'apikey':self.apiKey,'country':country})
        return await self.doRequest(url, successResponseCode='')

    async def getServicePrice(self, service: str, country: str):
        url = self.apiUrl + '?' + urlencode({'metod':'get_service_price','service':service,'apikey':self.apiKey,'country':country})
        return await self.doRequest(url)
    
    async def getNumber(self, service: str, country: str):
        url = self.apiUrl + '?' + urlencode({'metod':'get_number','service':service,'apikey':self.apiKey,'country':country})
        return await self.doRequest(url)

    async def ban(self, service: str, id: str):
        url = self.apiUrl + '?' + urlencode({'metod':'ban','service':service,'apikey':self.apiKey,'id':id})
        return await self.doRequest(url)
    
    async def getSMS(self, service: str, country: str, id: str):
        url = self.apiUrl + '?' + urlencode({'metod':'get_sms','service':service,'apikey':self.apiKey,'country':country,'id':id})
        return await self.doRequest(url, '1', '2')

    async def denial(self, service: str, country: str, id: str):
        url = self.apiUrl + '?' + urlencode({'metod':'denial','service':service,'apikey':self.apiKey,'country':country,'id':id})
        return await self.doRequest(url)

    async def getClearSMS(self, service: str, id: str):
        url = self.apiUrl + '?' + urlencode({'metod':'get_clearsms','service':service,'apikey':self.apiKey,'id':id})
        return await self.doRequest(url)

    async def getProverka(self, service: str, number: str):
        url = self.apiUrl + '?' + urlencode({'metod':'get_proverka','service':service,'apikey':self.apiKey,'number':number})
        return await self.doRequest(url, 'ok')

    async def balanceSIM(self, service: str, id: str):
        url = self.apiUrl + '?' + urlencode({'metod':'balance_sim','service':service,'apikey':self.apiKey,'id':id})
        return await self.doRequest(url)

    async def get2FA(self, secret: str):
        url = self.apiUrl + '?' + urlencode({'metod':'get_2fa','apikey':self.apiKey,'secret':secret})
        return await self.doRequest(url)
