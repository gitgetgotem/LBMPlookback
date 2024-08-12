import pymysql
from variables import zone, curve

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


selected_curve = curve

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



