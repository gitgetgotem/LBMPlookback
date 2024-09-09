import pymysql
from variables import curve

zone_dict = {
    'CAPITL': 'f',
    'CENTRL': 'c',
    'DUNWOD': 'i',
    'GENESE': 'b',
    'H Q': 'hq',
    'HUD VL': 'g',
    'LONGIL': 'k',
    'MHK VL': 'e',
    'MILLWD': 'h',
    'N.Y.C.': 'j',
    'NORTH': 'd',
    'NPX': 'npx',
    'O H': 'oh',
    'PJM': 'pjm',
    'WEST': 'a'
}

reverse_zone_dict = {
    'f':'CAPITL',
    'c':'CENTRL',
    'i':'DUNWOD',
    'b':'GENESE',
    'hq':'H Q',
    'g':'HUD VL',
    'k':'LONGIL',
    'e':'MHK VL',
    'h':'MILLWD',
    'j':'N.Y.C.',
    'd':'NORTH',
    'npx':'NPX',
    'oh':'O H',
    'pjm':'PJM',
    'a':'WEST'
}




# query_zone = reverse_zone_dict[zone]

selected_curve = curve

# lbmp_query = f"SELECT Time_Stamp, Year, Month, Day, Hour, Name, LBMP FROM nyiso.lbmp WHERE Name='{query_zone}'"
#
# curve_query = f"SELECT Month, Day, Hour, {selected_curve} AS Production FROM nyiso.curves;"

# icap_query = f"SELECT Year, Month, {utility}_ICAP AS ICAP FROM nyiso.icap;"
#
# drv_query = f"SELECT Month, Day, Hour, {utility} AS DRV FROM nyiso.drv;"

connection = pymysql.connect(
        user='admin',
        password='Malanga.92',
        database='nyiso',
        host='drs.cwx3jbukkn5u.us-east-1.rds.amazonaws.com'
    )


utility_line_loss = {
'NYSEG':1.0728,
'NG':1.084,
'CHUD':1.042,
'ORU':1.0789
}

icap_line_loss = {
    'NYSEG': 1.0738,
    'NG': 1.084,
    'CHUD': 1.0264,
    'ORU': 1.098
}


drv_by_utility = {
    'NYSEG': 0.08870,
    'ORU': 0.22180,
    'NG': 0.21080
}

