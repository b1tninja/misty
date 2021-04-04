import json
import os.path
import requests
from datetime import date, timedelta

from misty.utils import mkdir


def grantees(names):
    return [n[4:] for n in names if n.startswith('(E)')]


def grantors(names):
    return [n[4:] for n in names if n.startswith('(R)')]


def grantees_of_search_by_filing_code(search, filing_code):
    return [grantees(result['Names'].split('<br/>')) for result in search['SearchResults'] if
            result['FilingCode'] == filing_code]


def clerk_search(**kwargs):
    cookies = {
        'Fit': 'Width',
        'HideDetails': '0',
        'SelectedTool': 'FitToWidth',
    }

    headers = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
        'DNT': '1',
        'EncryptedKey': '/9QfnIc4QJV1Btrg3S9YyLFFhAYqzxX7783Q7ThF0EPngIemjulDxfAr5tWuJjEBVGBQc3U3XTKiYUlIWCEwoTGelARoCGx2Oix9OFe8j/tSBC0Nr0ET5A2Cgc4H/YBW',
        'sec-ch-ua-mobile': '?0',
        'Authorization': 'Bearer',
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
        'Password': 'MTM1NDc0NzI2NQ==',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://recordersdocumentindex.saccounty.net/',
        'Accept-Language': 'en-US,en;q=0.9,ro;q=0.8,ru;q=0.7,bs;q=0.6,zh-CN;q=0.5,zh-TW;q=0.4,zh;q=0.3,be;q=0.2',
    }

    base_params = dict([
        ('APN', ''),
        ('Acres', ''),
        ('AddressLineOne', ''),
        ('AddressLineTwo', ''),
        ('AreaCode', ''),
        ('Block', ''),
        ('BookNo', ''),
        ('BookType', ''),
        ('Building', ''),
        ('BuildingHigh', ''),
        ('BuildingLow', ''),
        ('ChildDocumentGlobalID', ''),
        ('City', ''),
        ('CityArea', ''),
        ('CityPhase', ''),
        ('CityVillageCode', ''),
        ('Code', ''),
        ('CornerLetter', ''),
        ('CornerNumber', ''),
        ('CountryCode', ''),
        ('County', ''),
        ('CountyCode', ''),
        ('Division', ''),
        ('DocNumberFrom', ''),
        ('DocNumberTo', ''),
        ('DocumentClass', 'OfficialRecords'),
        ('EventDateFrom', ''),
        ('EventDateTo', ''),
        # ('FilingCode', '685'),  # GRANT DEED
        ('FilingCodeGroupID', ''),
        ('FilingCodeRefiners', ''),
        ('FirstName', ''),
        ('FirstQtrSect', ''),
        ('FrameNumberFrom', ''),
        ('FrameNumberThrough', ''),
        ('GarageHigh', ''),
        ('GarageLow', ''),
        ('GovernmentUnit', ''),
        ('HighLot', ''),
        ('Info', ''),
        ('IsBasicSearch', 'false'),
        ('IsExactMatch', ''),
        ('LastName', ''),
        ('LegalDescription', ''),
        ('LotTract', ''),
        ('LotType', ''),
        ('LowLot', ''),
        ('MaxRecordedDate', '03/28/2021'),
        ('MiddleName', ''),
        ('MinRecordedDate', '01/01/1980'),
        ('Name', ''),
        ('NameRefiners', ''),
        ('NameTypeID', 'Primary'),
        ('NotInSidwellFl', ''),
        ('NumAcres', ''),
        ('OneHalfCode', ''),
        ('PageNo', ''),
        ('PageNumberFrom', ''),
        ('PageNumberThrough', ''),
        ('ParentDocumentGlobalID', ''),
        ('PartOneCode', ''),
        ('PartTwoCode', ''),
        ('Pin', ''),
        ('PlatName', ''),
        ('PrimaryFirstName', ''),
        ('PrimaryLastName', ''),
        ('PrimaryMiddleName', ''),
        ('ProfileID', 'Public'),
        ('PropertyID', ''),
        ('PropertyPhase', ''),
        ('PropertyUnit', ''),
        ('Range', ''),
        ('RangeDirection', ''),
        ('RefinementTokens', ''),
        ('RollNumber', ''),
        ('RollType', ''),
        ('Rows', '10'),
        ('SearchText', ''),
        ('SecDocNumberFrom', ''),
        ('SecDocNumberTo', ''),
        ('SecondQtrSect', ''),
        ('SecondaryFirstName', ''),
        ('SecondaryLastName', ''),
        ('SecondaryMiddleName', ''),
        ('Section', ''),
        ('SectionHalf', ''),
        ('SectionLot', ''),
        ('SectionQuarters', ''),
        ('SheetNumberFrom', ''),
        ('SheetNumberThrough', ''),
        ('SortFields', 'SPrimaryDocNumber'),
        ('SortOrders', 'ASC'),
        ('SplitUnit', ''),
        ('StartRow', '0'),
        ('State', ''),
        ('Suffix', ''),
        ('TertiaryFirstName', ''),
        ('TertiaryLastName', ''),
        ('TertiaryMiddleName', ''),
        ('ThirdQtrSect', ''),
        ('TownCode', ''),
        ('TownDirection', ''),
        ('TownhomeID', ''),
        ('Township', ''),
        ('UnderPin', ''),
        ('YearRefiners', ''),
        ('ZipCode', ''),
        ('ZipCodeFour', ''),
    ])
    p = dict(base_params)
    p.update(**kwargs)
    response = requests.get('https://recordersdocumentindex.saccounty.net/SearchServiceAPI/api/Search/GetSearchResults',
                            headers=headers, params=p, cookies=cookies)
    return response.json()


if __name__ == '__main__':
    basedir = "sacrec"
    mkdir(basedir)
    today = date.today()
    current_year = today.year
    n = 0
    min_record_date = '01/01/%d' % 1980
    max_record_date = (today + timedelta(days=-7)).strftime('%m/%d/%Y')

    while n == 0 or n < j['ResultCount']:
        j = clerk_search(MinRecordedDate=min_record_date,
                         MaxRecordedDate=max_record_date,
                         Rows='10000',
                         StartRow=n)

        if j['SearchResults'] is None:
            break

        jsonp_path = os.path.join(basedir, "%d.json" % n)

        with open(jsonp_path, 'w') as fh:
            json.dump(j, fh)

        n += len(j['SearchResults'])

# TODO: json incremental encoder

