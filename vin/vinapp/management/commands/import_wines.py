from django.core.management.base import BaseCommand
from vinapp.models import Wine
import sqlite3

class Command(BaseCommand):
    help = 'Imports wines from the SQLite database'

    def handle(self, *args, **options):
        # Connect to the SQLite database
        conn = sqlite3.connect('catalog.db')
        cursor = conn.cursor()

        # Execute a query to get all wines
        cursor.execute('SELECT * FROM wines')
        rows = cursor.fetchall()

        # For each row in the result, create a Wine object
        for row in rows:
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

        conn.close()