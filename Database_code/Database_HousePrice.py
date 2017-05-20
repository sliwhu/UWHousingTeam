import csv
import sqlite3

conn = sqlite3.connect('housePrices.db')
c = conn.cursor()

# Drop Table if it already exists
housePrices_tb_exists = "SELECT name FROM sqlite_master WHERE type='table' AND name='housePrices'"
if conn.execute(housePrices_tb_exists).fetchone():
    c.execute('''DROP TABLE housePrices''')

# Create table
c.execute(
    '''CREATE TABLE housePrices (id integer, date text, price integer, bedrooms integer, bathrooms numeric, sqft_living integer, sqft_lot integer, floors numeric,	waterfront integer,	view integer, condition integer, grade integer, sqft_above integer, sqft_basement integer, yr_built integer, yr_renovated integer, zipcode integer,	lat numeric, long numeric, sqft_living15 integer, sqft_lot15 integer, List price integer)''')

with open('Merged_Data.csv', 'r') as inputFile:
    next(inputFile)
    csv_inputFile = csv.reader(inputFile)
    for row in csv_inputFile:
        id = int(row[0])
        date = row[1]
        price = int(row[2])
        bedrooms = int(row[3])
        bathrooms = float(row[4])
        sqft_living = int(row[5])
        sqft_lot = int(row[6])
        floors = float(row[7])
        waterfront = int(row[8])
        view = int(row[9])
        condition = int(row[10])
        grade = int(row[11])
        sqft_above = int(row[12])
        sqft_basement = int(row[13])
        yr_built = int(row[14])
        yr_renovated = int(row[15])
        zipcode = int(row[16])
        lat = float(row[17])
        long = float(row[18])
        sqft_living15 = int(row[19])
        sqft_lot15 = int(row[20])
        List_price = int(row[21])

        query = format(
            "INSERT INTO housePrices VALUES (%s,'%s',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" % (
                str(id), date, str(price), str(bedrooms), str(bathrooms), str(sqft_living),
                str(sqft_lot), str(floors), str(waterfront), str(view), str(condition),
                str(grade), str(sqft_above), str(sqft_basement), str(yr_built), str(yr_renovated),
                str(zipcode), str(lat), str(long), str(sqft_living15), str(sqft_lot15),
                str(List_price)))
        c.execute(query)

 # For testing if the correct number of rows loaded in table
 #   with open('count_hoursePrice_entries.csv', 'w') as target:
 #       target.truncate()
 #       target.write("%s" % ('Number of Entries'))
 #       target.write("\n")
 #       rows = c.execute(
 #           'SELECT count(*) as count FROM housePrices')
 #       for row in rows:
 #           target.write("%s" % (row[0]))
 #           target.write("\n")

c.close()