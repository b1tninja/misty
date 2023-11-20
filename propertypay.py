import json

import requests


def get_property(management, hoa, account):
    cookies = {
        'XSRF-TOKEN': 'fa9cef48-5cef-4fc0-82c4-a4d912c4eb31',
        'bm_mi': '566323A7950D3A5412E702080DC15E0C~YAAQpP4ZuJa4qnCJAQAA8jrLcxQYLOx0rQxezyhDa2HhQ82i4tiPAMvtEQVrShTBaWKTMX0b4RrVisa3VN3yqjZAIlI95CkX1sV1E4Asv67DZogrZAUfibndYrGhqXxUz50S+lfKho4MYCplcxmfaANm/dScldUSkRvR08DjzyOdDAUbDszz3PhJHKiUdxMuYPSY4GVVvmyduPo/IU5ijm2CgUtMSkEkPW1fCUv8RphupxjUL6T6EIcKw0sDY5z85HMNWYSZHYXmZiRi62jMo6TDs282yc1Z6HFKGk+gIhuJzvYTJk7ryVYXCTrGalyA4k8VlYDAjQkXqD2UPiq205tvF/Ai~1',
        'ak_bmsc': 'AEC0646B20F13C19F42CB5B9D6C34E2C~000000000000000000000000000000~YAAQpP4ZuGS5qnCJAQAAtknLcxTSUg0rbcaLgVbebQKl+E8N4e8cUCErsUlUf01bmib6hcfH4sVbmzFl7JRZ6Wn07GRDpwUbHEAPsxdlbAjezjapgG2bL202EqVFr+y8MSc2V+WmLIWOdEU2tXKAAPp5GS3qBFiAq2GiPJFj1g6Ph0DeLMyxPveLe8v/HPpRALN1DcAQ5NtEfZjHTyEpkJAS6dswiI7tu+77uLYKXKp3WF4sG/hpeYtihgiQFGsEZ4AqagZf9p8DRxrvKV8Cg8Ax7XD0q52VixyATjcw7McXy+ZEP5uxaK4deiCsQNhiYy89bhvL3FOUDW4kytPasqbhumHy5yGrIA2EI8oodEgVKJrv+mxI1HnAyn5x9ONP1kvXRkVNxSOJpzMbfduX9zJyVLkUu8nTKsPsDgJWPSNIagIrAB785HGNCwPzf/YuGn/RZzLNomDAV5S9qS8fGAsHr5YnkPS2UPMYb4Llql7BFfrW1x7cRw/1M2ek7hdmCyF2Hd8ITjYAwsq5+6MMqZRt1dJVjjY7IPre+meWP1eRP2+RNxOTRXIhX6Ff+suym/ffPhRHW2+PrTwrvYhc',
        '_gid': 'GA1.2.63031030.1689864851',
        '_ga_79WT08SVLR': 'GS1.1.1689864850.2.1.1689864855.0.0.0',
        '_ga': 'GA1.2.1519185546.1689654604',
        'bm_sv': 'D04EABCDEDBB8AA527B3992FC735803A~YAAQpP4ZuEXOqnCJAQAADMTMcxQFRA/hBnUtGpxbulTYINDNYeYk317lZO0KDy8hmYAohxEzXCt93+q2r5g1QLIpfl+Jaj+OBdttsCpynwxp0jzdMO1k+sQj5xkjqxsnwSSMa/DYJ54X/glzAqddT0F4mBSQHYKU8S/m+9LmijL6s31CesXweaws5lbcEcIpfwKNUcMALDL3sRTx0H7/8T+L/bz92SIvj1Jrj7G7bwlKQMDECFPUl/rGW9fz+rF7t8/SEq3fwg0=~1',
    }

    headers = {
        'authority': 'propertypay.firstcitizens.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'clientversion': '2.18.8',
        # 'cookie': 'XSRF-TOKEN=fa9cef48-5cef-4fc0-82c4-a4d912c4eb31; bm_mi=566323A7950D3A5412E702080DC15E0C~YAAQpP4ZuJa4qnCJAQAA8jrLcxQYLOx0rQxezyhDa2HhQ82i4tiPAMvtEQVrShTBaWKTMX0b4RrVisa3VN3yqjZAIlI95CkX1sV1E4Asv67DZogrZAUfibndYrGhqXxUz50S+lfKho4MYCplcxmfaANm/dScldUSkRvR08DjzyOdDAUbDszz3PhJHKiUdxMuYPSY4GVVvmyduPo/IU5ijm2CgUtMSkEkPW1fCUv8RphupxjUL6T6EIcKw0sDY5z85HMNWYSZHYXmZiRi62jMo6TDs282yc1Z6HFKGk+gIhuJzvYTJk7ryVYXCTrGalyA4k8VlYDAjQkXqD2UPiq205tvF/Ai~1; ak_bmsc=AEC0646B20F13C19F42CB5B9D6C34E2C~000000000000000000000000000000~YAAQpP4ZuGS5qnCJAQAAtknLcxTSUg0rbcaLgVbebQKl+E8N4e8cUCErsUlUf01bmib6hcfH4sVbmzFl7JRZ6Wn07GRDpwUbHEAPsxdlbAjezjapgG2bL202EqVFr+y8MSc2V+WmLIWOdEU2tXKAAPp5GS3qBFiAq2GiPJFj1g6Ph0DeLMyxPveLe8v/HPpRALN1DcAQ5NtEfZjHTyEpkJAS6dswiI7tu+77uLYKXKp3WF4sG/hpeYtihgiQFGsEZ4AqagZf9p8DRxrvKV8Cg8Ax7XD0q52VixyATjcw7McXy+ZEP5uxaK4deiCsQNhiYy89bhvL3FOUDW4kytPasqbhumHy5yGrIA2EI8oodEgVKJrv+mxI1HnAyn5x9ONP1kvXRkVNxSOJpzMbfduX9zJyVLkUu8nTKsPsDgJWPSNIagIrAB785HGNCwPzf/YuGn/RZzLNomDAV5S9qS8fGAsHr5YnkPS2UPMYb4Llql7BFfrW1x7cRw/1M2ek7hdmCyF2Hd8ITjYAwsq5+6MMqZRt1dJVjjY7IPre+meWP1eRP2+RNxOTRXIhX6Ff+suym/ffPhRHW2+PrTwrvYhc; _gid=GA1.2.63031030.1689864851; _ga_79WT08SVLR=GS1.1.1689864850.2.1.1689864855.0.0.0; _ga=GA1.2.1519185546.1689654604; bm_sv=D04EABCDEDBB8AA527B3992FC735803A~YAAQpP4ZuEXOqnCJAQAADMTMcxQFRA/hBnUtGpxbulTYINDNYeYk317lZO0KDy8hmYAohxEzXCt93+q2r5g1QLIpfl+Jaj+OBdttsCpynwxp0jzdMO1k+sQj5xkjqxsnwSSMa/DYJ54X/glzAqddT0F4mBSQHYKU8S/m+9LmijL6s31CesXweaws5lbcEcIpfwKNUcMALDL3sRTx0H7/8T+L/bz92SIvj1Jrj7G7bwlKQMDECFPUl/rGW9fz+rF7t8/SEq3fwg0=~1',
        'referer': 'https://propertypay.firstcitizens.com/guest/',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    }

    params = {
        'pmcCouponId': str(management),
        'hoaCouponId': str(hoa),
        'propertyCouponId': str(account)
    }

    try:

        response = requests.get('https://propertypay.firstcitizens.com/HOAPass/v1/registration/propertyAddress',
                                params=params,
                                cookies=cookies,
                                headers=headers)

        assert response.status_code == 200
        return response.json()
    except json.JSONDecodeError:
        pass
    return None


def get_manager(management):
    cookies = {
        # '_ga': 'GA1.2.1408066733.1671896896',
        # '_gcl_au': '1.1.302749453.1671994166',
        # '_gac_UA-8170919-1': '1.1671994166.CjwKCAiAhqCdBhB0EiwAH8M_Go5zwOudrHbzhYEtBmD4tG4r23J_6H6fEL0DpXWgyf2PN4t-Uc1JeRoCyu4QAvD_BwE',
        # '_gac_UA-395987-1': '1.1671994166.CjwKCAiAhqCdBhB0EiwAH8M_Go5zwOudrHbzhYEtBmD4tG4r23J_6H6fEL0DpXWgyf2PN4t-Uc1JeRoCyu4QAvD_BwE',
        # 'mbox': 'PC#cb8f7ed99f5945c88a1f87567b7a29a8.35_0#1735238965|session#2aae9ad65d864d55925d54af33bd21be#1673228557',
        # 'AMCV_13340C0F53DAAFAC0A490D45%40AdobeOrg': '-1124106680%7CMCIDTS%7C19367%7CMCMID%7C75901132945383408334286777747187177413%7CMCAAMLH-1673831496%7C9%7CMCAAMB-1673831496%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1673233896s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C5.2.0',
        # '_gac_UA-8170919-5': '1.1673226697.CjwKCAiA8OmdBhAgEiwAShr40yCC3up4m1dIwxriWp9Ych3Oqe9LTw2JCPY82jUuU_dfMsK0V0IQvRoCfAAQAvD_BwE',
        # '_gcl_aw': 'GCL.1673226697.CjwKCAiA8OmdBhAgEiwAShr40yCC3up4m1dIwxriWp9Ych3Oqe9LTw2JCPY82jUuU_dfMsK0V0IQvRoCfAAQAvD_BwE',
        # 'adcloud': '{%22_les_lsc%22:%221673226697185%2Ccit.com%2C1681085497%22%2C%22_les_v%22:%22y%2Ccit.com%2C1673228497%22}',
        # '_uetvid': '90ab9de08fba11eda54f37c88a91305d',
        # 'cjConsent': 'MHxOfDB8Tnww',
        # '_mkto_trk': 'id:151-FHS-046&token:_mch-cit.com-1671994166139-17786',
        # '_hjSessionUser_303460': 'eyJpZCI6IjM1MTcxYWQ2LTFhZWItNTc1OC1hMGNjLTI4M2FlODI2N2VjYyIsImNyZWF0ZWQiOjE2NzMyMjY2OTc1NTgsImV4aXN0aW5nIjpmYWxzZX0=',
        # 'RT': '"z=1&dm=cit.com&si=u7rn7ob72rl&ss=lco3z0sy&sl=0&tt=0"',
        # 'XSRF-TOKEN': '5d5787c1-60dd-4d60-9a84-7a24556b1e0c',
        # 'ak_bmsc': '51FED1DB830AA40D29CB610F5D32B387~000000000000000000000000000000~YAAQFdLfFw9GMbeFAQAAiNYVwRIDnmTIQFI548ac8ZfEBMhexNdnLY7bgqgOJhcH6ke44r55/e1B18hLvV7C1I8qwXbMyv3mrg38/F99vnYGFBkWA4Wy3Jtr1YDOVeKw9CHHR5Y+U9gvshbmdTpIEnnEY7+aPL7GmFO7lNwDIDnPACL7RhVJqM+B4wFFiXE6iBKDPoWcPCrLeGrVzlfJtvihzC4WDWNJrauYhIoxtzqNq6CcJCf7bcPXAqSr5NtCyLuw5hh7pcXKc786nthcq81n4vjOk5RCSZXFP4sN1eDUj2r1VBueUQG/u5x3unGRfwpXT8bF7jdZG/Ln+7OYtLRBF/sSYmP4crtP0fnYdr1SdKWIKechd96mCF4V/v1DZHuM9ypwEjSPUpQBb2mm6e/zJpnTekvFTj47TXeMfg5QtdWb40hY1j/gQhQLlWXbG9o/M7TaDYQi6Qi2cRuotvW/sCRO4gzsv2j4D9GAOl/nRP23Nhfd7OrBj1SaWrV0Jjn1weQ=',
        # '_gid': 'GA1.2.1161124.1673981713',
        # 'bm_mi': 'AD6930946F6D6F959539350ABDDBFA06~YAAQ5OkyF588X3GFAQAA/pAgwRIiPDqPmv7X7BxjMppuIK2a4fuoymzESFly6VsnbiYVRCV/JBk2A4u9Kflf0RUUlkMd5eGrUijVrKroxMGj4YFUpH4JOd8f0j8xowLbTChgxwwmwyENjb1xS6b6V2Op23Fp1xcOOdw/AtZuEzW0lr3IuaYQw8LxEBwWmW7KXTxcqiFaEcLcHo5Ejo3a7bBb7Uvfw9TIDNZoMkTmWjS90u+xtII/rxF/VbRo08nZKxwbaGdi+AtVFHDFyd7Av59NGiGg0lcALLmYkw5nbhgskUdlxl/mJHLm9Z8bvwHHGw==~1',
        # '_gat_gtag_UA_44397603_10': '1',
        # 'bm_sv': '8D25198E9460CDDDCEBF1BAEE7568D41~YAAQ5OkyF9c8X3GFAQAAaLIgwRJKslcVtgzPxszGPRLWmTSlvJM2Y7qZPOEVnMiohCiUAQJjVkNNs7j2phRLrcYxfmiDCxKbk+z4iGiPOuBS3phUOATh7/vCdauUJi368gO+kivxxEgS5eWWpf5flOe2mE1FakRFD7b9nf8gk8xxYtwk0HpV/Evy04qfHTRdgTWnCQb9IFxlQG70xECR57MlEA9DCYGVk0QIkCCMfE3xZcvZhy4w+/4fM9sL2g==~1',
    }

    headers = {
        'authority': 'propertypay.cit.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'clientversion': '2.14.1',
        # 'cookie': '_ga=GA1.2.1408066733.1671896896; _gcl_au=1.1.302749453.1671994166; _gac_UA-8170919-1=1.1671994166.CjwKCAiAhqCdBhB0EiwAH8M_Go5zwOudrHbzhYEtBmD4tG4r23J_6H6fEL0DpXWgyf2PN4t-Uc1JeRoCyu4QAvD_BwE; _gac_UA-395987-1=1.1671994166.CjwKCAiAhqCdBhB0EiwAH8M_Go5zwOudrHbzhYEtBmD4tG4r23J_6H6fEL0DpXWgyf2PN4t-Uc1JeRoCyu4QAvD_BwE; mbox=PC#cb8f7ed99f5945c88a1f87567b7a29a8.35_0#1735238965|session#2aae9ad65d864d55925d54af33bd21be#1673228557; AMCV_13340C0F53DAAFAC0A490D45%40AdobeOrg=-1124106680%7CMCIDTS%7C19367%7CMCMID%7C75901132945383408334286777747187177413%7CMCAAMLH-1673831496%7C9%7CMCAAMB-1673831496%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1673233896s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C5.2.0; _gac_UA-8170919-5=1.1673226697.CjwKCAiA8OmdBhAgEiwAShr40yCC3up4m1dIwxriWp9Ych3Oqe9LTw2JCPY82jUuU_dfMsK0V0IQvRoCfAAQAvD_BwE; _gcl_aw=GCL.1673226697.CjwKCAiA8OmdBhAgEiwAShr40yCC3up4m1dIwxriWp9Ych3Oqe9LTw2JCPY82jUuU_dfMsK0V0IQvRoCfAAQAvD_BwE; adcloud={%22_les_lsc%22:%221673226697185%2Ccit.com%2C1681085497%22%2C%22_les_v%22:%22y%2Ccit.com%2C1673228497%22}; _uetvid=90ab9de08fba11eda54f37c88a91305d; cjConsent=MHxOfDB8Tnww; _mkto_trk=id:151-FHS-046&token:_mch-cit.com-1671994166139-17786; _hjSessionUser_303460=eyJpZCI6IjM1MTcxYWQ2LTFhZWItNTc1OC1hMGNjLTI4M2FlODI2N2VjYyIsImNyZWF0ZWQiOjE2NzMyMjY2OTc1NTgsImV4aXN0aW5nIjpmYWxzZX0=; RT="z=1&dm=cit.com&si=u7rn7ob72rl&ss=lco3z0sy&sl=0&tt=0"; XSRF-TOKEN=5d5787c1-60dd-4d60-9a84-7a24556b1e0c; ak_bmsc=51FED1DB830AA40D29CB610F5D32B387~000000000000000000000000000000~YAAQFdLfFw9GMbeFAQAAiNYVwRIDnmTIQFI548ac8ZfEBMhexNdnLY7bgqgOJhcH6ke44r55/e1B18hLvV7C1I8qwXbMyv3mrg38/F99vnYGFBkWA4Wy3Jtr1YDOVeKw9CHHR5Y+U9gvshbmdTpIEnnEY7+aPL7GmFO7lNwDIDnPACL7RhVJqM+B4wFFiXE6iBKDPoWcPCrLeGrVzlfJtvihzC4WDWNJrauYhIoxtzqNq6CcJCf7bcPXAqSr5NtCyLuw5hh7pcXKc786nthcq81n4vjOk5RCSZXFP4sN1eDUj2r1VBueUQG/u5x3unGRfwpXT8bF7jdZG/Ln+7OYtLRBF/sSYmP4crtP0fnYdr1SdKWIKechd96mCF4V/v1DZHuM9ypwEjSPUpQBb2mm6e/zJpnTekvFTj47TXeMfg5QtdWb40hY1j/gQhQLlWXbG9o/M7TaDYQi6Qi2cRuotvW/sCRO4gzsv2j4D9GAOl/nRP23Nhfd7OrBj1SaWrV0Jjn1weQ=; _gid=GA1.2.1161124.1673981713; bm_mi=AD6930946F6D6F959539350ABDDBFA06~YAAQ5OkyF588X3GFAQAA/pAgwRIiPDqPmv7X7BxjMppuIK2a4fuoymzESFly6VsnbiYVRCV/JBk2A4u9Kflf0RUUlkMd5eGrUijVrKroxMGj4YFUpH4JOd8f0j8xowLbTChgxwwmwyENjb1xS6b6V2Op23Fp1xcOOdw/AtZuEzW0lr3IuaYQw8LxEBwWmW7KXTxcqiFaEcLcHo5Ejo3a7bBb7Uvfw9TIDNZoMkTmWjS90u+xtII/rxF/VbRo08nZKxwbaGdi+AtVFHDFyd7Av59NGiGg0lcALLmYkw5nbhgskUdlxl/mJHLm9Z8bvwHHGw==~1; _gat_gtag_UA_44397603_10=1; bm_sv=8D25198E9460CDDDCEBF1BAEE7568D41~YAAQ5OkyF9c8X3GFAQAAaLIgwRJKslcVtgzPxszGPRLWmTSlvJM2Y7qZPOEVnMiohCiUAQJjVkNNs7j2phRLrcYxfmiDCxKbk+z4iGiPOuBS3phUOATh7/vCdauUJi368gO+kivxxEgS5eWWpf5flOe2mE1FakRFD7b9nf8gk8xxYtwk0HpV/Evy04qfHTRdgTWnCQb9IFxlQG70xECR57MlEA9DCYGVk0QIkCCMfE3xZcvZhy4w+/4fM9sL2g==~1',
        'referer': 'https://propertypay.cit.com/guest/',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'x-xsrf-token': '5d5787c1-60dd-4d60-9a84-7a24556b1e0c',
    }

    params = {
        'pmcCouponId': str(management),
    }

    response = requests.get('https://propertypay.cit.com/organization/pmc', params=params, cookies=cookies,
                            headers=headers)

    return response.json()

def get_hoa(management, hoa):
    cookies = {
        'XSRF-TOKEN': 'fa9cef48-5cef-4fc0-82c4-a4d912c4eb31',
        'bm_mi': '566323A7950D3A5412E702080DC15E0C~YAAQpP4ZuJa4qnCJAQAA8jrLcxQYLOx0rQxezyhDa2HhQ82i4tiPAMvtEQVrShTBaWKTMX0b4RrVisa3VN3yqjZAIlI95CkX1sV1E4Asv67DZogrZAUfibndYrGhqXxUz50S+lfKho4MYCplcxmfaANm/dScldUSkRvR08DjzyOdDAUbDszz3PhJHKiUdxMuYPSY4GVVvmyduPo/IU5ijm2CgUtMSkEkPW1fCUv8RphupxjUL6T6EIcKw0sDY5z85HMNWYSZHYXmZiRi62jMo6TDs282yc1Z6HFKGk+gIhuJzvYTJk7ryVYXCTrGalyA4k8VlYDAjQkXqD2UPiq205tvF/Ai~1',
        'ak_bmsc': 'AEC0646B20F13C19F42CB5B9D6C34E2C~000000000000000000000000000000~YAAQpP4ZuGS5qnCJAQAAtknLcxTSUg0rbcaLgVbebQKl+E8N4e8cUCErsUlUf01bmib6hcfH4sVbmzFl7JRZ6Wn07GRDpwUbHEAPsxdlbAjezjapgG2bL202EqVFr+y8MSc2V+WmLIWOdEU2tXKAAPp5GS3qBFiAq2GiPJFj1g6Ph0DeLMyxPveLe8v/HPpRALN1DcAQ5NtEfZjHTyEpkJAS6dswiI7tu+77uLYKXKp3WF4sG/hpeYtihgiQFGsEZ4AqagZf9p8DRxrvKV8Cg8Ax7XD0q52VixyATjcw7McXy+ZEP5uxaK4deiCsQNhiYy89bhvL3FOUDW4kytPasqbhumHy5yGrIA2EI8oodEgVKJrv+mxI1HnAyn5x9ONP1kvXRkVNxSOJpzMbfduX9zJyVLkUu8nTKsPsDgJWPSNIagIrAB785HGNCwPzf/YuGn/RZzLNomDAV5S9qS8fGAsHr5YnkPS2UPMYb4Llql7BFfrW1x7cRw/1M2ek7hdmCyF2Hd8ITjYAwsq5+6MMqZRt1dJVjjY7IPre+meWP1eRP2+RNxOTRXIhX6Ff+suym/ffPhRHW2+PrTwrvYhc',
        '_gid': 'GA1.2.63031030.1689864851',
        '_ga_79WT08SVLR': 'GS1.1.1689864850.2.1.1689864855.0.0.0',
        '_ga': 'GA1.2.1519185546.1689654604',
        'bm_sv': 'D04EABCDEDBB8AA527B3992FC735803A~YAAQpP4ZuEXOqnCJAQAADMTMcxQFRA/hBnUtGpxbulTYINDNYeYk317lZO0KDy8hmYAohxEzXCt93+q2r5g1QLIpfl+Jaj+OBdttsCpynwxp0jzdMO1k+sQj5xkjqxsnwSSMa/DYJ54X/glzAqddT0F4mBSQHYKU8S/m+9LmijL6s31CesXweaws5lbcEcIpfwKNUcMALDL3sRTx0H7/8T+L/bz92SIvj1Jrj7G7bwlKQMDECFPUl/rGW9fz+rF7t8/SEq3fwg0=~1',
    }

    headers = {
        'authority': 'propertypay.firstcitizens.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'clientversion': '2.18.8',
        # 'cookie': 'XSRF-TOKEN=fa9cef48-5cef-4fc0-82c4-a4d912c4eb31; bm_mi=566323A7950D3A5412E702080DC15E0C~YAAQpP4ZuJa4qnCJAQAA8jrLcxQYLOx0rQxezyhDa2HhQ82i4tiPAMvtEQVrShTBaWKTMX0b4RrVisa3VN3yqjZAIlI95CkX1sV1E4Asv67DZogrZAUfibndYrGhqXxUz50S+lfKho4MYCplcxmfaANm/dScldUSkRvR08DjzyOdDAUbDszz3PhJHKiUdxMuYPSY4GVVvmyduPo/IU5ijm2CgUtMSkEkPW1fCUv8RphupxjUL6T6EIcKw0sDY5z85HMNWYSZHYXmZiRi62jMo6TDs282yc1Z6HFKGk+gIhuJzvYTJk7ryVYXCTrGalyA4k8VlYDAjQkXqD2UPiq205tvF/Ai~1; ak_bmsc=AEC0646B20F13C19F42CB5B9D6C34E2C~000000000000000000000000000000~YAAQpP4ZuGS5qnCJAQAAtknLcxTSUg0rbcaLgVbebQKl+E8N4e8cUCErsUlUf01bmib6hcfH4sVbmzFl7JRZ6Wn07GRDpwUbHEAPsxdlbAjezjapgG2bL202EqVFr+y8MSc2V+WmLIWOdEU2tXKAAPp5GS3qBFiAq2GiPJFj1g6Ph0DeLMyxPveLe8v/HPpRALN1DcAQ5NtEfZjHTyEpkJAS6dswiI7tu+77uLYKXKp3WF4sG/hpeYtihgiQFGsEZ4AqagZf9p8DRxrvKV8Cg8Ax7XD0q52VixyATjcw7McXy+ZEP5uxaK4deiCsQNhiYy89bhvL3FOUDW4kytPasqbhumHy5yGrIA2EI8oodEgVKJrv+mxI1HnAyn5x9ONP1kvXRkVNxSOJpzMbfduX9zJyVLkUu8nTKsPsDgJWPSNIagIrAB785HGNCwPzf/YuGn/RZzLNomDAV5S9qS8fGAsHr5YnkPS2UPMYb4Llql7BFfrW1x7cRw/1M2ek7hdmCyF2Hd8ITjYAwsq5+6MMqZRt1dJVjjY7IPre+meWP1eRP2+RNxOTRXIhX6Ff+suym/ffPhRHW2+PrTwrvYhc; _gid=GA1.2.63031030.1689864851; _ga_79WT08SVLR=GS1.1.1689864850.2.1.1689864855.0.0.0; _ga=GA1.2.1519185546.1689654604; bm_sv=D04EABCDEDBB8AA527B3992FC735803A~YAAQpP4ZuEXOqnCJAQAADMTMcxQFRA/hBnUtGpxbulTYINDNYeYk317lZO0KDy8hmYAohxEzXCt93+q2r5g1QLIpfl+Jaj+OBdttsCpynwxp0jzdMO1k+sQj5xkjqxsnwSSMa/DYJ54X/glzAqddT0F4mBSQHYKU8S/m+9LmijL6s31CesXweaws5lbcEcIpfwKNUcMALDL3sRTx0H7/8T+L/bz92SIvj1Jrj7G7bwlKQMDECFPUl/rGW9fz+rF7t8/SEq3fwg0=~1',
        'referer': 'https://propertypay.firstcitizens.com/guest/',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    }

    params = {
        'hoaCouponId': str(hoa),
        'pmcCouponId': str(management),
    }

    response = requests.get('https://propertypay.cit.com/organization/hoa',
                            params=params,
                            cookies=cookies,
                            headers=headers)

    return response.json()

if __name__ == '__main__':
    for account in range(75000, 76000):
        property = get_property(1513, 4483, account)
        if property:
            print("%s\t%s" %(account, property['addressLine1']))