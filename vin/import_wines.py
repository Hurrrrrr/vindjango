import os
import django
import sqlite3
import sys
# import pdb
from django.core.wsgi import get_wsgi_application

# Ensure the path includes your project
sys.path.append('/home/jp/repos/vindjango')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vin.settings')

django.setup()

from vinapp.models import Wine

# pdb.set_trace()

def import_wines():
    conn = sqlite3.connect('catalog.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM wines')

    for row in cursor.fetchall():
        wine = Wine(
            id=row[0],
            scope=row[1],
            style=row[2],
            label_color=row[3],
            country=row[4],
            region=row[5],
            appellation=row[6],
            grapes=row[7],
            vintage=row[8],
            producer=row[9],
            bottling=row[10],
            clarity=row[11],
            appearance_red=row[12],
            appearance_green=row[13],
            appearance_blue=row[14],
            appearance_other=row[15],
            condition=row[16],
            nose_intensity=row[17],
            development=row[18],
            petillance=row[19],
            sweetness=row[20],
            acidity=row[21],
            alcohol=row[22],
            body=row[23],
            tannin_or_bitterness=row[24],
            finish=row[25],
            fruit_color=row[26],
            fruit_family=row[27],
            fruit_ripeness=row[28],
            fruit_subcondition=row[29],
            floral=row[30],
            herbaceous=row[31],
            herbal=row[32],
            earth_organic=row[33],
            earth_inorganic=row[34],
            grape_spice=row[35],
            oak_aroma=row[36],
            oak_intensity=row[37],
            aroma_other=row[38]
        )
        wine.save()

if __name__ == "__main__":
    import_wines()