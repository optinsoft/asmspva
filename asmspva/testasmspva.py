from .asyncsmspva import AsyncSmsPva, AsyncSmsPvaException, NoSMSException
from typing import Coroutine

async def testApi(apiName: str, apiRoutine: Coroutine):
    print(apiName)
    try:
        response = await apiRoutine
        print(response)
        return response
    except NoSMSException:
        print("No SMS")
    except AsyncSmsPvaException as e:
        print("AsyncSmsPvaException:", e)
    return None

async def testAsyncSmsPva(apiKey: str):
    asmspva = AsyncSmsPva(apiKey)

    print('--- asmspva test ---')

    await testApi('getBalance', asmspva.getBalance('opt4'))
    await testApi('getUserInfo:', asmspva.getUserInfo('opt4'))
    await testApi('getCountNew:', asmspva.getCountNew('opt4','US'))
    await testApi('getServicePrice', asmspva.getServicePrice('opt4','US'))
    number = await testApi('getNumber', asmspva.getNumber('opt4','US'))
    if number:
        await testApi('getSMS', asmspva.getSMS('opt4','US',number['id']))
        await testApi('getClearSMS', asmspva.getClearSMS('opt4',number['id']))
        await testApi('getProverka', asmspva.getProverka('opt4',number['number']))
        await testApi('balanceSIM', asmspva.balanceSIM('opt4',number['id']))    
        await testApi('denial', asmspva.denial('opt4','US',number['id']))
        await testApi('ban', asmspva.denial('opt4','US',number['id']))
    await testApi('get2FA', asmspva.get2FA('1234567890'))

    print('--- asmspva test completed ---')