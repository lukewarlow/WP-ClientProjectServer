from flask import Flask, request
import sqlite3 as sql
import os
import json
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)
DATABASE = APP_ROOT + "/database.db"

pincode = "1506"


@app.route('/', methods=['GET'])
def index():
    return app.send_static_file("index.html")


@app.route('/addpharmacy', methods=['POST', 'GET'])
def add_pharmacy():
    if request.method == "GET":
        return app.send_static_file("addPharmacy.html")
    else:
        name = request.form.get('name', default="Error")
        lat = request.form.get('lat', default="Error")
        long = request.form.get('long', default="Error")
        phoneNumber = request.form.get('phoneNumber', default="Error")
        openingTimes = request.form.get('openingTimes', default="Error")
        services = request.form.get('services', default="Error")
        pin = request.form.get('pincode', default="Error")
        if (pin == pincode):
            msg = insert_into_database_table("INSERT INTO tblPharmacy ('name', 'lat', 'long', 'openingTimes', 'phoneNumber', 'services') VALUES (?,?,?,?,?,?)", (name, lat, long, openingTimes, phoneNumber, services))
        else:
            msg = "Invalid pin code"
        return msg


@app.route('/deletepharmacy', methods=['POST', 'GET'])
def remove_pharmacy():
    if request.method == "GET":
        return app.send_static_file("deletePharmacy.html")
    else:
        name = request.form.get('name', default="Error")
        phoneNumber = request.form.get('phoneNumber', default="Error")
        pin = request.form.get('pincode', default="Error")
        if (pin == pincode):
            msg = delete_from_table("DELETE FROM tblPharmacy WHERE name=? AND phoneNumber=?", (name, phoneNumber))
        else:
            msg = "Invalid pin code"
        return msg


@app.route('/pharmacyjson', methods=['GET'])
def get_json():
    pharmacyData = select_from_database_table("SELECT * FROM tblPharmacy", "", True)
    data = {}
    for i in range(0, len(pharmacyData)):
        name = pharmacyData[i][1]
        lat = pharmacyData[i][2]
        long = pharmacyData[i][3]
        openingTimes = pharmacyData[i][4]
        phoneNumber = pharmacyData[i][5]
        services = pharmacyData[i][6]

        pharmacyObject = {}
        pharmacyObject['name'] = name
        pharmacyObject['lat'] = lat
        pharmacyObject['long'] = long
        pharmacyObject['phoneNumber'] = phoneNumber
        openingTimesObject = []
        openingTimesData = openingTimes.split(':')
        for j in range(0, len(openingTimesData)):
            open = int(openingTimesData[j].split(',')[0])
            close = int(openingTimesData[j].split(',')[1])
            openingTimesObject.append({"open" : open, "close": close})

        pharmacyObject['openingTimes'] = openingTimesObject

        servicesObject = []
        servicesData = services.split(':')
        for j in range(0, len(servicesData)):
            service = servicesData[j].split(',')[0]
            welshAvailablity = servicesData[j].split(',')[1]
            servicesObject.append({service: welshAvailablity})

        pharmacyObject['services'] = servicesObject

        data['pharmacy' + str(i)] = pharmacyObject

    json_data = json.dumps(data)
    return json_data


def select_from_database_table(sql_statement, array_of_terms=None, all=False):
    data = "Error"
    try:
        conn = sql.connect(DATABASE)
        cur = conn.cursor()
        cur.execute(sql_statement, array_of_terms)
        if (all):
            data = cur.fetchall()
        else:
            data = cur.fetchone()
    except sql.ProgrammingError as e:
        print("Error in select operation," + str(e))
    except sql.OperationalError as e:
        print(str(e))
    finally:
        conn.close()
        return data


def insert_into_database_table(sql_statement, tuple_of_terms):
    msg = "Error"
    try:
        conn = sql.connect(DATABASE)
        cur = conn.cursor()
        cur.execute(sql_statement, tuple_of_terms)
        conn.commit()
        msg = "Record successfully added."
    except sql.ProgrammingError as e:
        conn.rollback()
        msg = "Error in insert operation: " + str(e)
    except Exception as e:
        msg = str(e)
    finally:
        conn.close()
        print(msg)
        return msg


def update_table(sql_statement, array_of_terms):
    try:
        conn = sql.connect(DATABASE)
        cur = conn.cursor()
        cur.execute(sql_statement, array_of_terms)
        conn.commit()
        msg = "Record successfully updated."
    except sql.ProgrammingError as e:
        conn.rollback()
        msg = "Error in update operation" + str(e)
        print(msg)
    finally:
        conn.close()
        return msg


def delete_from_table(sql_statement, array_of_terms):
    try:
        conn = sql.connect(DATABASE)
        cur = conn.cursor()
        cur.execute(sql_statement, array_of_terms);
        conn.commit()
        msg = "Record successfully deleted."
    except sql.ProgrammingError as e:
        conn.rollback()
        msg = "Error in delete operation" + str(e)
        print(msg)
    finally:
        conn.close()
        return msg


if __name__ == '__main__':
    app.run()
