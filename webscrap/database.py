import sqlite3

conn = sqlite3.connect('mycars.db')

curr = conn.cursor()

curr.execute("""create table Cars_DB(
                car_make text,
                car_model text,
                car_price text,
                car_link text,
                car_mileage text,
                car_year text,
                car_transmission text,
                car_status text,
                car_image_link text
                )""")

conn.commit()
conn.close()