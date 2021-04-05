import logging
import json
import os.path
import requests
from datetime import date, timedelta

from misty.utils import mkdir

import tqdm

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

    min_record_date = '01/01/%d' % 1980
    max_record_date = (today + timedelta(days=-7)).strftime('%m/%d/%Y')

    base_params = dict([
        # ('APN', ''),
        # ('Acres', ''),
        # ('AddressLineOne', ''),
        # ('AddressLineTwo', ''),
        # ('AreaCode', ''),
        # ('Block', ''),
        # ('BookNo', ''),
        # ('BookType', ''),
        # ('Building', ''),
        # ('BuildingHigh', ''),
        # ('BuildingLow', ''),
        # ('ChildDocumentGlobalID', ''),
        # ('City', ''),
        # ('CityArea', ''),
        # ('CityPhase', ''),
        # ('CityVillageCode', ''),
        # ('Code', ''),
        # ('CornerLetter', ''),
        # ('CornerNumber', ''),
        # ('CountryCode', ''),
        # ('County', ''),
        # ('CountyCode', ''),
        # ('Division', ''),
        # ('DocNumberFrom', ''),
        # ('DocNumberTo', ''),
        ('DocumentClass', 'OfficialRecords'),
        # ('EventDateFrom', ''),
        # ('EventDateTo', ''),
        # ('FilingCode', ''),
        # ('FilingCodeGroupID', ''),
        # ('FilingCodeRefiners', ''),
        # ('FirstName', ''),
        # ('FirstQtrSect', ''),
        # ('FrameNumberFrom', ''),
        # ('FrameNumberThrough', ''),
        # ('GarageHigh', ''),
        # ('GarageLow', ''),
        # ('GovernmentUnit', ''),
        # ('HighLot', ''),
        # ('Info', ''),
        ('IsBasicSearch', 'false'),
        # ('IsExactMatch', ''),
        # ('LastName', ''),
        # ('LegalDescription', ''),
        # ('LotTract', ''),
        # ('LotType', ''),
        # ('LowLot', ''),
        ('MaxRecordedDate', max_record_date),
        # ('MiddleName', ''),
        ('MinRecordedDate', min_record_date),
        # ('Name', ''),
        # ('NameRefiners', ''),
        ('NameTypeID', 'Primary'),
        # ('NotInSidwellFl', ''),
        # ('NumAcres', ''),
        # ('OneHalfCode', ''),
        # ('PageNo', ''),
        # ('PageNumberFrom', ''),
        # ('PageNumberThrough', ''),
        # ('ParentDocumentGlobalID', ''),
        # ('PartOneCode', ''),
        # ('PartTwoCode', ''),
        # ('Pin', ''),
        # ('PlatName', ''),
        # ('PrimaryFirstName', ''),
        # ('PrimaryLastName', ''),
        # ('PrimaryMiddleName', ''),
        ('ProfileID', 'Public'),
        # ('PropertyID', ''),
        # ('PropertyPhase', ''),
        # ('PropertyUnit', ''),
        # ('Range', ''),
        # ('RangeDirection', ''),
        # ('RefinementTokens', ''),
        # ('RollNumber', ''),
        # ('RollType', ''),
        # ('Rows', '10'),
        # ('SearchText', ''),
        # ('SecDocNumberFrom', ''),
        # ('SecDocNumberTo', ''),
        # ('SecondQtrSect', ''),
        # ('SecondaryFirstName', ''),
        # ('SecondaryLastName', ''),
        # ('SecondaryMiddleName', ''),
        # ('Section', ''),
        # ('SectionHalf', ''),
        # ('SectionLot', ''),
        # ('SectionQuarters', ''),
        # ('SheetNumberFrom', ''),
        # ('SheetNumberThrough', ''),
        # ('SortFields', 'SPrimaryDocNumber'),
        ('SortOrders', 'ASC'),
        # ('SplitUnit', ''),
        ('StartRow', '0'),
        # ('State', ''),
        # ('Suffix', ''),
        # ('TertiaryFirstName', ''),
        # ('TertiaryLastName', ''),
        # ('TertiaryMiddleName', ''),
        # ('ThirdQtrSect', ''),
        # ('TownCode', ''),
        # ('TownDirection', ''),
        # ('TownhomeID', ''),
        # ('Township', ''),
        # ('UnderPin', ''),
        # ('YearRefiners', ''),
        # ('ZipCode', ''),
        # ('ZipCodeFour', ''),
    ])
    p = dict(base_params)
    p.update(**kwargs)
    response = requests.get('https://recordersdocumentindex.saccounty.net/SearchServiceAPI/api/Search/GetSearchResults',
                            headers=headers, params=p, cookies=cookies)
    return response.json()


# TODO: convert to ints?
filing_codes = {'151': 'AFFIDAVIT', '153': 'AFFIDAVIT OF DEATH', '155': 'AFFIDAVIT TERMINATING HOMESTEAD INTEREST', '156': 'AFFIDAVIT TERMINATING JOINT TENANCY', '157': 'AFFIDAVIT TERMINATING LIFE ESTATE', '158': 'AGREEMENT FOR DEED ESTOPPEL AND SOLVENCY AFFIDAVIT', '159': 'ESTOPPEL AFFIDAVIT', '160': 'ESTOPPEL CERTIFICATE AND AMENDMENT TO LEASE', '161': 'CERTIFICATE', '162': 'DECLARATION', '180': 'ADDITIONAL ADVANCE AGREEMENT', '181': 'AGREEMENT', '182': 'AGREEMENT CONCERNING LICENSE TO TAKE WATER', '183': 'AGREEMENT TO REIMBURSE', '186': 'BILL OF SALE', '187': 'CONTRACT', '188': 'COVENANT AND AGREEMENT', '189': 'DEPOSIT RECEIPT AGREEMENT', '190': 'EASEMENT', '193': 'JOINT VENTURE', '195': 'AGREEMENT TO SELL', '196': 'NON DISTURBANCE AGREEMENT', '197': 'NOTICE OF NON RENEWAL', '199': 'PARTNERSHIP', '201': 'PRENUPTIAL AGREEMENT', '202': 'PURCHASE AGREEMENT', '205': 'RECIPROCAL AGREEMENT', '206': 'SECURITY AGREEMENT', '208': 'SUBORDINATION AGREEMENT', '210': 'CONTRACT AGREEMENT', '213': 'MAINTENANCE AGREEMENT', '214': 'SIGN RELOCATION AGREEMENT', '215': 'CONSERVATION EASEMENT', '219': 'SUPPLEMENT NOTICE OF SPECIAL TAX LIEN', '220': 'AMENDED RESTRICTION', '221': 'AMENDED DECLARATION OF TRUST', '222': 'AMENDED DEED OF TRUST', '223': 'AMENDED NOTICE OF ACTION LIS PENDENS', '224': 'AMENDED PARTNERSHIP', '225': 'AMENDMENT', '226': 'APPOINTMENT OF TRUSTEE', '227': 'ASSIGNMENT OF DEED OF TRUST', '228': 'ASSUMPTION OF DEED OF TRUST', '229': 'CONSTRUCTION DEED OF TRUST', '230': 'DEED OF TRUST', '232': 'EXTENSION MECHANICS LIEN', '233': 'EXTENSION TAX LIEN', '235': 'MODIFICATION AGREEMENT', '236': 'MORTGAGE', '238': 'RECONVEYANCE', '239': 'SUBSTITUTION OF TRUSTEE', '240': 'AMENDMENT TO CONDO PLAN', '242': 'AMENDED LEASE', '243': 'AMENDED TAX LIEN', '244': 'AMENDED ORDER', '245': 'AMENDED NOTICE TO CREDITORS OF BULK TRANSFER', '246': 'AMENDED ABSTRACT OF JUDGMENT', '247': 'AMENDED OPTION AGREEMENT', '248': 'AMENDED OIL AND GAS LEASE', '249': 'AMENDED NOTICE OF ASSESSMENT LIEN', '250': 'ASSIGNMENT', '251': 'ASSIGNMENT OF JUDGMENT', '252': 'ASSIGNMENT OF LEASE', '253': 'ASSIGNMENT OF LIEN', '254': 'ASSIGNMENT OF VENDEE INTEREST IN LAND CONTRACT', '257': 'ASSIGNMENT OF RENTS', '258': 'ASSIGNMENT OF REAL PROPERTY LEASE', '261': 'ASSIGNMENT OF CONSENT AND WAIVER', '262': 'MODIFIED ASSIGNMENT', '265': 'CONTRACT BOND', '266': 'NOTARY BOND', '267': 'OFFICIAL BOND', '268': 'PERFORMANCE BOND', '269': 'RELEASE OF LIEN BOND', '270': 'BONDS TO GUARANTEE MECHANIC LIEN', '272': 'BOND', '273': 'PAYMENT BOND', '274': 'PAYMENT OF CONTRACTUAL ASSESSMENT REQUIRED', '280': 'ACCEPTANCE OF OFFER OF DEDICATION', '281': 'CERTIFICATE OF ACKNOWLEDGEMENT', '283': 'CERTIFICATE OF COMPLETION', '284': 'CERTIFICATE OF COMPLIANCE', '285': 'CERTIFICATE OF CORRECTION', '287': 'CERTIFICATE OF DISCHARGE PROPERTY', '290': 'CERTIFICATE OF JUDGMENT CREDITOR AND DEBTOR', '291': 'CERTIFICATE OF PARTIAL DISCHARGE OF NOTICE OF PENDING ACTION', '293': 'CERTIFICATE OF REDEMPTION', '294': 'CERTIFICATE OF REGISTRY', '295': 'CERTIFICATE OF SUBORDINATION FEDERAL TAX LIEN', '298': 'DISTRICT FORMATION', '299': 'REORGANIZATION', '300': 'BUILDING CONTRACT', '301': 'CONDOMINIUM PLAN', '302': 'CONSTRUCTION PERMIT', '304': 'NOTICE OF AWARD', '305': 'NOTICE OF CESSATION', '306': 'NOTICE OF COMPLETION', '320': 'DECLARATION OF ANNEXATION', '324': 'DECLARATION OF RESTRICTION', '327': 'DECLARATION OF TRUST', '337': 'DECREE FORECLOSURE AND APPOINTMENT OF COMMISSIONER', '339': 'DECREE OF DISTRIBUTION', '342': 'DECREE QUIETING TITLE', '355': 'FICTITIOUS DEED OF TRUST', '365': 'UCC AMENDMENT', '366': 'UCC ASSIGNMENT', '367': 'UCC CONTINUATION', '368': 'UCC FINANCING STATEMENT', '370': 'UCC PARTIAL RELEASE', '371': 'UCC RELEASE', '372': 'UCC TERMINATION', '373': 'BUILDING SAFETY LIEN', '374': 'NOTICE OF CANNABIS PENALTY LIEN', '375': 'ABATEMENT OF NUISANCE', '376': 'ABSTRACT OF JUDGMENT', '378': 'CERTIFICATE OF DELINQUENT PERSONAL PROPERTY TAX', '379': 'CERTIFICATE OF FEDERAL TAX LIEN', '380': 'CERTIFICATE OF SALE', '381': 'CERTIFICATE OF TAX COLLECTORS LIEN', '383': 'INTERLOCUTORY DIVORCE', '384': 'LIEN', '385': 'NOTICE OF ACTION', '386': 'NOTICE OF ASSOCIATION LIEN', '387': 'NOTICE OF ASSESSMENT', '388': 'NOTICE OF ATTACHMENT', '389': 'NOTICE OF CLAIM OR MECHANICS LIEN', '391': 'POSTPONED PROPERTY TAX LIEN', '392': 'ORDER FOR SUPPORT PAYMENT', '395': 'DISSOLUTION OF MARRIAGE', '398': 'SUBSTANDARD BUILDING', '400': 'STATE TAX LIEN', '401': 'UTILITY BILLING LIEN', '405': 'ABSTRACT OF JUDGEMENT - UNSECURED', '406': 'NOTICE OF SUPPORT JUDGMENT', '407': 'NOTICE OF SPECIAL TAX LIEN', '425': 'AGRICULTURAL PRESERVE MAP', '426': 'AMENDED ASSESSMENT MAP', '427': 'ASSESSMENT MAP', '428': 'CEMETERY MAP', '430': 'DESIGNATED FLOODWAY MAP', '431': 'HIGHWAY MAP', '433': 'PARCEL MAP', '434': 'RELINQUISHMENT MAP', '435': 'SUBDIVISION MAP', '436': 'SURVEY MAP', '438': 'AMENDED PARCEL MAP', '439': 'AMENDED HIGHWAY MAP', '440': 'AMENDED SUBDIVISION MAP', '441': 'AMENDED SURVEY MAP', '446': 'ARTICLES OF INCORPORATION', '451': 'CHARTER', '452': 'CONSENT', '455': 'FINAL ORDER OF CONDEMNATION', '456': 'FLOOD PLAN', '457': 'DECLARATION OF HOMESTEAD', '458': 'IRREVOCABLE OFFER OF DEDICATION', '460': 'LOT LINE ADJUSTMENT', '461': 'MERGER', '462': 'MILITARY DISCHARGE', '464': 'MOBILEHOME INSTALLATION OF FOUNDATION SYSTEM', '465': 'PATENT', '466': 'POWER OF ATTORNEY', '467': 'PROOF OF LABOR', '473': 'DEED OF NON ACCEPTANCE', '476': 'RESOLUTION', '478': 'RESTRICTIVE COVENANT', '479': 'RIGHT OF REDEMPTION', '480': 'DELINQUENT TAX NOTICE', '484': 'ORDINANCE', '485': 'RIGHT OF WAY', '486': 'FIRST RIGHT OF REFUSAL', '487': 'CONSENT TO REMOVAL OF PERSONAL PROPERTY', '488': 'DISCLAIMER', '489': 'PERMIT', '490': 'SUBORDINATION OF JUDGMENT', '491': 'SUBORDINATION OF DEED OF TRUST', '492': 'JUDGMENT SETTLING FINAL ACCOUNT', '493': 'JUDGMENT OF DISMISSAL', '494': 'BY LAWS', '495': 'PETITION', '497': 'ARTICLES OF ORGANIZATION', '498': 'ENVIRONMENTAL RESTRICTION', '499': 'RESTRICTIVE COVENANT MODIFICATION', '500': 'STATEMENT OF REDEVELOPMENT PLAN', '501': 'PAYMENT OF TRANSFER FEE REQUIRED', '529': 'NOTICE OF PENDING ENFORCEMENT ACTION', '530': 'NON ATTACHMENT OF FEDERAL TAX LIEN', '531': 'NOTICE OF DEFAULT', '532': 'NOTICE OF HOME IMPROVEMENT LOAN AGREEMENT', '533': 'NOTICE OF FINAL DESCRIPTION', '535': 'NOTICE OF INTENDED BULK TRANSFER', '537': 'NOTICE OF LOCATION', '538': 'NOTICE OF NON COMPLIANCE', '539': 'NOTICE OF NON RESPONSIBILITY', '541': 'NOTICE OF RELEASE OF EASEMENT', '542': 'NOTICE OF INTENDED SALE', '543': 'NOTICE OF TRUSTEES SALE', '544': 'NOTICE OF VIOLATION', '546': 'REQUEST FOR NOTICE', '549': 'NOTICE', '551': 'NOTICE OF CONSERVATION EASEMENT', '552': 'NOTICE OF AFFORDABILITY RESTRICTIONS ON TRANSFER OF PROPERTY', '553': 'NOTICE OF REINTERNMENT OF NATIVE AMERICAN REMAINS', '555': 'LETTERS OF ADMINISTRATION', '556': 'LETTERS OF CONSERVATORSHIP', '557': 'LETTERS OF GUARDIANSHIP', '558': 'LETTERS OF TESTAMENTARY', '559': 'ORDER', '584': 'ORIGINAL PETITION UNDER CHAPTER XI', '585': 'TRUSTEES REPORT OF EXEMPT PROPERTY', '587': 'VOLUNTARY PETITION', '591': 'ORDER FINAL ACCOUNT', '596': 'CONSERVATORSHIP REGISTRATION', '600': 'ABANDONMENT OF HOMESTEAD', '602': 'CANCELLATION OF PARTNERSHIP', '604': 'CANCELLATION OF RESTRICTIONS', '607': 'CANCELLATION OF TAX DEED', '612': 'LANDLORDS WAIVER', '613': 'PARTIAL RECONVEYANCE', '614': 'PARTIAL RELEASE', '615': 'QUITCLAIM GAS & OIL LEASE', '619': 'RELEASE', '620': 'RELEASE AGREEMENT', '621': 'RELEASE AGREEMENT NOT TO SELL', '623': 'RELEASE OF JUDGMENT', '624': 'RELEASE OF LIEN', '626': 'RELEASE MORTGAGE', '628': 'RELEASE OF ASSIGNMENT', '629': 'RELEASE OF EQUITY', '631': 'RELEASE OF FEDERAL TAX LIEN', '632': 'RELEASE OF INHERITANCE TAX LIEN', '633': 'RELEASE OF LEVY', '635': 'RELEASE OF MECHANICS LIEN', '636': 'RELEASE OF IMPROVEMENT LIEN', '637': 'RELEASE OF REAL PROPERTY', '638': 'RELEASE OF REAL PROPERTY FROM GIFT TAX LIEN', '639': 'RELEASE OF RIGHT OF REDEMPTION', '640': 'REVOCATION OF POWER OF ATTORNEY', '642': 'SURRENDER OF LIFE ESTATE', '644': 'TERMINATION OF DELINQUENT UTILITY', '645': 'WAIVER', '651': 'WITHDRAWAL OF LIS PENDENS', '654': 'RELEASE OF WEED ABATEMENT', '655': 'RELEASE OF ASSESSMENT OF ASSOCIATION LIEN', '657': 'SURRENDER OF OIL AND GAS LEASE', '658': 'RELEASE OF ASSIGNMENT OF RENTS', '661': 'REVOCATION', '662': 'CANCELLATION', '663': 'REVOCATION OF DEED', '664': 'CANCELLATION OF BOND', '670': 'LIEN RELEASE RECORDED IN ERROR', '680': 'DEED', '681': 'EASEMENT DEED', '685': 'GRANT DEED', '689': 'QUITCLAIM DEED', '692': 'TAX DEED', '694': 'TRUSTEES DEED', '697': 'REVOCABLE TRANSFER ON DEATH DEED', '698': 'REVOCATION OF REVOCABLE TRANSFER ON DEATH DEED', '711': 'LEASE AGREEMENT', '712': 'OPTION', '714': 'SUBORDINATION  OF LEASE', '715': 'OIL AND GAS LEASE', '716': 'JUDGMENT', '718': 'APPLICATION FOR AND RENEWAL OF JUDGMENT', '720': 'RESCISSION', '721': 'WITHDRAWAL OF FEDERAL TAX LIEN', '800': 'NOTICE OF LEVY', '801': 'DEED IN LIEU OF FORECLOSURE', '802': 'NOTICE OF POWER TO SELL TAX-DEFAULTED PROPERTY', '803': 'RELEASE OF LIEN POSTPONED PROPERTY TAXES', '804': 'NOTICE OF SUPPORT SUBSTITUTION OF PAYEE', '805': 'AMENDMENT TO NOTICE OF SPECIAL TAX LIEN', '806': 'CERTIFICATE OF WATER LIEN', '999': 'Official Outcard'}

if __name__ == '__main__':
    # TODO: argparse
    root_dir = 'sac'
    mkdir(root_dir)
    today = date.today()
    for filing_code_id, filing_code_desc in tqdm.tqdm(filing_codes.items(), position=0, leave=True):
        logging.info("Fetching %s - %s", filing_code_id, filing_code_desc)

        basedir = os.path.join(root_dir, filing_code_desc)
        mkdir(basedir)

        n = 0
        r = 10000
        retries = 2

        # TODO: resume from last record synched

        while n == 0 or n < j['ResultCount']:
            j = clerk_search(FilingCode=filing_code_id,
                             Rows='%d' % r,
                             StartRow=n)

            if j is None:
                if retries:
                    logger.warning("Failed to get chunk! (%d retries left)", retries)
                    retries -= 1
                    continue
                else:
                    break

            if j['SearchResults'] is None:
                break

            n += len(j['SearchResults'])
            logger.info("%d/%d", n, j['ResultCount'])

            jsonp_path = os.path.join(basedir, "%d.json" % n)

            with open(jsonp_path, 'w') as fh:
                json.dump(j, fh)

    # TODO: json incremental encoder
    # jq '[.[]]' grantdeeds_*.json
