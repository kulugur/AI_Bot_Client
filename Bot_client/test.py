import requests
import json
cookies = {
    'cid': 'fB8RvZcu',
    'BNC-Location': 'BINANCE',
    'OptanonAlertBoxClosed': '2023-02-26T06:42:09.070Z',
    '_cq_duid': '1.1677745077.UYt4qdNrVkovfH0H',
    '_cq_suid': '1.1680706926.UpPXZjYCmzU38rCY',
    'cr00': '2E9C6C981F98B40AD9AA74BE6198FE66',
    'd1og': 'web.37049662.F14E54BA5D167D0E3B98E2223EC2C0A0',
    'r2o1': 'web.37049662.036E4222AB181027B2F4A41497CE2182',
    'f30l': 'web.37049662.52D6C905E5228E7453B4049C073A6259',
    'p20t': 'web.37049662.137F881F17F85C3DC801554F527F37A7',
    'fiat-prefer-currency': 'RUB',
    'userPreferredCurrency': 'USD_USD',
    '_ga': 'GA1.2.1441043278.1680802674',
    '_gid': 'GA1.2.445042184.1680802674',
    '_gcl_au': '1.1.367762232.1680802675',
    'bnc-uuid': 'bca6df2c-1eb3-490f-bde3-3a1ff955310c',
    'source': 'referral',
    'campaign': 'www.binance.com',
    'BNC_FV_KEY': '3313035d74b5a138825501563c034b386f0bab0d',
    'BNC_FV_KEY_EXPIRE': '1680823101930',
    'sajssdk_2015_cross_new_user': '1',
    'monitor-uuid': '46f159a4-db0f-4843-99f9-04a5339f9144',
    'lang': 'ru',
    'sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%2237049662%22%2C%22first_id%22%3A%2218757a589f1820-0050d6a1f52f206-42015718-567864-18757a589f283f%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTg3NTdhNTg5ZjE4MjAtMDA1MGQ2YTFmNTJmMjA2LTQyMDE1NzE4LTU2Nzg2NC0xODc1N2E1ODlmMjgzZiIsIiRpZGVudGl0eV9sb2dpbl9pZCI6IjM3MDQ5NjYyIn0%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%2237049662%22%7D%2C%22%24device_id%22%3A%2218757a589f1820-0050d6a1f52f206-42015718-567864-18757a589f283f%22%7D',
    'userQuoteAsset': 'BTC',
    '_gat_UA-162512367-1': '1',
    'OptanonConsent': 'isGpcEnabled=0&datestamp=Thu+Apr+06+2023+22%3A25%3A05+GMT%2B0300+(%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0%2C+%D1%81%D1%82%D0%B0%D0%BD%D0%B4%D0%B0%D1%80%D1%82%D0%BD%D0%BE%D0%B5+%D0%B2%D1%80%D0%B5%D0%BC%D1%8F)&version=202211.1.0&geolocation=RU%3BSAM&isIABGlobal=false&hosts=&consentId=ea1484a8-e548-4b0e-a9ad-880971eb589a&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A0%2CC0004%3A0%2CC0002%3A0&AwaitingReconsent=false',
    '_gat': '1',
}

headers = {
    'authority': 'www.binance.com',
    'accept': '*/*',
    'accept-language': 'ru,ru-RU;q=0.9,en-US;q=0.8,en;q=0.7',
    'bnc-uuid': 'bca6df2c-1eb3-490f-bde3-3a1ff955310c',
    'clienttype': 'web',
    'content-type': 'application/json',
    # 'cookie': 'cid=fB8RvZcu; BNC-Location=BINANCE; OptanonAlertBoxClosed=2023-02-26T06:42:09.070Z; _cq_duid=1.1677745077.UYt4qdNrVkovfH0H; _cq_suid=1.1680706926.UpPXZjYCmzU38rCY; cr00=2E9C6C981F98B40AD9AA74BE6198FE66; d1og=web.37049662.F14E54BA5D167D0E3B98E2223EC2C0A0; r2o1=web.37049662.036E4222AB181027B2F4A41497CE2182; f30l=web.37049662.52D6C905E5228E7453B4049C073A6259; p20t=web.37049662.137F881F17F85C3DC801554F527F37A7; fiat-prefer-currency=RUB; userPreferredCurrency=USD_USD; _ga=GA1.2.1441043278.1680802674; _gid=GA1.2.445042184.1680802674; _gcl_au=1.1.367762232.1680802675; bnc-uuid=bca6df2c-1eb3-490f-bde3-3a1ff955310c; source=referral; campaign=www.binance.com; BNC_FV_KEY=3313035d74b5a138825501563c034b386f0bab0d; BNC_FV_KEY_EXPIRE=1680823101930; sajssdk_2015_cross_new_user=1; monitor-uuid=46f159a4-db0f-4843-99f9-04a5339f9144; lang=ru; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2237049662%22%2C%22first_id%22%3A%2218757a589f1820-0050d6a1f52f206-42015718-567864-18757a589f283f%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTg3NTdhNTg5ZjE4MjAtMDA1MGQ2YTFmNTJmMjA2LTQyMDE1NzE4LTU2Nzg2NC0xODc1N2E1ODlmMjgzZiIsIiRpZGVudGl0eV9sb2dpbl9pZCI6IjM3MDQ5NjYyIn0%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%2237049662%22%7D%2C%22%24device_id%22%3A%2218757a589f1820-0050d6a1f52f206-42015718-567864-18757a589f283f%22%7D; userQuoteAsset=BTC; _gat_UA-162512367-1=1; OptanonConsent=isGpcEnabled=0&datestamp=Thu+Apr+06+2023+22%3A25%3A05+GMT%2B0300+(%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0%2C+%D1%81%D1%82%D0%B0%D0%BD%D0%B4%D0%B0%D1%80%D1%82%D0%BD%D0%BE%D0%B5+%D0%B2%D1%80%D0%B5%D0%BC%D1%8F)&version=202211.1.0&geolocation=RU%3BSAM&isIABGlobal=false&hosts=&consentId=ea1484a8-e548-4b0e-a9ad-880971eb589a&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A0%2CC0004%3A0%2CC0002%3A0&AwaitingReconsent=false; _gat=1',
    'csrftoken': '47a1c34155104a5a814f7db0026fcfb1',
    'device-info': 'eyJzY3JlZW5fcmVzb2x1dGlvbiI6IjE5MjAsMTA4MCIsImF2YWlsYWJsZV9zY3JlZW5fcmVzb2x1dGlvbiI6IjE5MjAsMTAzMiIsInN5c3RlbV92ZXJzaW9uIjoiV2luZG93cyAxMCIsImJyYW5kX21vZGVsIjoidW5rbm93biIsInN5c3RlbV9sYW5nIjoicnUiLCJ0aW1lem9uZSI6IkdNVCszIiwidGltZXpvbmVPZmZzZXQiOi0xODAsInVzZXJfYWdlbnQiOiJNb3ppbGxhLzUuMCAoV2luZG93cyBOVCAxMC4wOyBXaW42NDsgeDY0KSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBDaHJvbWUvMTEyLjAuMC4wIFNhZmFyaS81MzcuMzYiLCJsaXN0X3BsdWdpbiI6IlBERiBWaWV3ZXIsQ2hyb21lIFBERiBWaWV3ZXIsQ2hyb21pdW0gUERGIFZpZXdlcixNaWNyb3NvZnQgRWRnZSBQREYgVmlld2VyLFdlYktpdCBidWlsdC1pbiBQREYiLCJjYW52YXNfY29kZSI6IjFmYzUzNGVlIiwid2ViZ2xfdmVuZG9yIjoiR29vZ2xlIEluYy4gKEFNRCkiLCJ3ZWJnbF9yZW5kZXJlciI6IkFOR0xFIChBTUQsIEFNRCBSYWRlb24gUjUgR3JhcGhpY3MgRGlyZWN0M0QxMSB2c181XzAgcHNfNV8wLCBEM0QxMSkiLCJhdWRpbyI6IjEyNC4wNDM0NzUyNzUxNjA3NCIsInBsYXRmb3JtIjoiV2luMzIiLCJ3ZWJfdGltZXpvbmUiOiJFdXJvcGUvTW9zY293IiwiZGV2aWNlX25hbWUiOiJDaHJvbWUgVjExMi4wLjAuMCAoV2luZG93cykiLCJmaW5nZXJwcmludCI6ImMyYjc2N2ZkN2I4YWVhZDBjNDU5ZTRjMjhlODliNDRkIiwiZGV2aWNlX2lkIjoiIiwicmVsYXRlZF9kZXZpY2VfaWRzIjoiIn0=',
    'fvideo-id': '3313035d74b5a138825501563c034b386f0bab0d',
    'lang': 'en-NG',
    'origin': 'https://www.binance.com',
    'referer': 'https://www.binance.com/en-NG/my/wallet/account/payment/dashboard',
    'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36',
    'x-trace-id': '79206577-5188-4bd2-93ee-3b370a6811f4',
    'x-ui-request-trace': '79206577-5188-4bd2-93ee-3b370a6811f4',
}

json_data = {
    'startTime': 1680722705110,
    'endTime': 1680809105110,
    'size': 5,
}

response = requests.post(
    'https://www.binance.com/bapi/pay/v1/private/binance-pay/transaction/scroll-query',
    cookies=cookies,
    headers=headers,
    json=json_data,
)
res = json.loads(response.text)['data']['transactionVOList']
for i in res:
    print(i)