from flask import Flask, request, render_template
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


@app.route('/addpharmacy', methods=['GET', 'POST'])
def add_pharmacy():
    if request.method == "GET":
        services = get_enhanced_service_names()
        return render_template("addPharmacy.html", services=services)
    else:
        name = request.form.get('name', default="Error")
        lat = request.form.get('lat', default="Error")
        long = request.form.get('long', default="Error")
        phoneNumber = request.form.get('phoneNumber', default="Error")
        openingTimes = request.form.get('openingTimes', default="Error")
        welshAvailable = request.form.get('welshAvailable', default="Error")
        services = request.form.get('services', default="Error")
        core_services = get_core_service_names()
        for i in range(0, 4):
            services = services.insert(core_services[i] + ",")
        pin = request.form.get('pincode', default="Error")
        if (pin == pincode):
            msg = insert_into_database_table("INSERT INTO tblPharmacy ('name', 'lat', 'long', 'openingTimes', 'phoneNumber', 'welshAvailable', 'services') VALUES (?,?,?,?,?,?,?)", (name, lat, long, openingTimes, phoneNumber, welshAvailable, services))
        else:
            msg = "Invalid pin code"
        return msg

def get_core_service_names():
    serviceData = select_from_database_table("SELECT * FROM tblService", "", True)
    services = []
    for i in range(0, 4):
        name = serviceData[i][1]
        name = name.replace(" ", "_")
        services.append(name.lower())
    return services


def get_enhanced_service_names():
    serviceData = select_from_database_table("SELECT * FROM tblService", "", True)
    services = []
    for i in range(4, len(serviceData)):
        name = serviceData[i][1]
        name = name.replace(" ", "_")
        services.append(name.lower())
    return services


@app.route('/deletepharmacy', methods=['GET', 'DELETE'])
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


@app.route('/findpharmacy',methods=['POST'])
def findpharmacy():
    pharmPhone = request.form.get('phoneNumber')
    print (pharmPhone)
    try:
        conn = sql.connect(DATABASE)
        cur = conn.cursor()
        pharmacyData = select_from_database_table("SELECT * FROM tblPharmacy WHERE phoneNumber=?", [pharmPhone])
        data = {}
        name = pharmacyData[1]
        lat = pharmacyData[2]
        long = pharmacyData[3]
        openingTimes = pharmacyData[4]
        phoneNumber = pharmacyData[5]
        welshAvailable = pharmacyData[6]
        services = pharmacyData[7]
        pharmacyObject = {}
        pharmacyObject['name'] = name
        pharmacyObject['lat'] = lat
        pharmacyObject['long'] = long
        pharmacyObject['phoneNumber'] = phoneNumber
        openingTimesObject = []
        openingTimesData = openingTimes.split(',')
        for j in range(0, len(openingTimesData)):
            open = openingTimesData[j].split(':')[0]
            close = openingTimesData[j].split(':')[1]
            openingTimesObject.append({"open" : open, "close": close})
            pharmacyObject['openingTimes'] = openingTimesObject

        pharmacyObject['welshAvailable'] = welshAvailable
        pharmacyObject['services'] = services

        data['pharmacy0'] = pharmacyObject

        json_data = json.dumps(data)
        print(data)
    except Exception as e:
        print(e)
    finally:
        conn.close()
        return json_data


@app.route('/updatepharmacy', methods=['GET','PUT'])
def update_pharmacy():
    if request.method == "GET":
        return app.send_static_file("updatePharmacy.html")
    else:
        phoneNumber = request.form.get('phoneNumber')
        welshAvailable = request.form.get('welshAvailable')
        services = request.form.get('services')
        core_services = get_core_service_names()
        for i in range(0, 4):
            services = core_services[i] + "," + services
        return update_table("UPDATE tblPharmacy SET welshAvailable=?, services=? WHERE phoneNumber=?",[welshAvailable, services, phoneNumber])


@app.route('/pharmacies', methods=['GET'])
def get_pharmacies():
    pharmacyData = select_from_database_table("SELECT * FROM tblPharmacy", "", True)
    data = {}
    for i in range(0, len(pharmacyData)):
        name = pharmacyData[i][1]
        lat = pharmacyData[i][2]
        long = pharmacyData[i][3]
        openingTimes = pharmacyData[i][4]
        phoneNumber = pharmacyData[i][5]
        welshAvailable = pharmacyData[i][6]
        services = pharmacyData[i][7]

        pharmacyObject = {}
        pharmacyObject['name'] = name
        pharmacyObject['lat'] = lat
        pharmacyObject['long'] = long
        pharmacyObject['phoneNumber'] = phoneNumber
        openingTimesObject = []
        openingTimesData = openingTimes.split(',')
        for j in range(0, len(openingTimesData)):
            open = openingTimesData[j].split(':')[0]
            close = openingTimesData[j].split(':')[1]
            openingTimesObject.append({"open" : open, "close": close})

        pharmacyObject['openingTimes'] = openingTimesObject
        pharmacyObject['welshAvailable'] = welshAvailable
        pharmacyObject['services'] = services

        data['pharmacy' + str(i)] = pharmacyObject

    json_data = json.dumps(data)

    return json_data


@app.route('/addservice', methods=['GET', 'POST'])
def add_service():
    if request.method == "GET":
        return app.send_static_file("addService.html")
    else:
        name = request.form.get('name', default="Error")
        welshName = request.form.get('welshName', default="Error")
        description = request.form.get('description', default="Error")
        welshDescription = request.form.get('welshDescription', default="Error")
        pin = request.form.get('pincode', default="Error")
        if (pin == pincode):
            msg = insert_into_database_table("INSERT INTO tblService ('name', 'welshName', 'description', 'welshDescription') VALUES (?,?,?,?)", (name, welshName, description, welshDescription))
        else:
            msg = "Invalid pin code"
        return msg


@app.route('/deleteservice', methods=['GET', 'DELETE'])
def delete_service():
    if request.method == "GET":
        return app.send_static_file("deleteService.html")
    else:
        name = request.form.get('name', default="Error")
        welshName = request.form.get('welshName', default="Error")
        pin = request.form.get('pincode', default="Error")
        if (pin == pincode):
            msg = insert_into_database_table("DELETE FROM tblService WHERE name=? AND welshName=?", (name, welshName))
        else:
            msg = "Invalid pin code"
        return msg


@app.route('/findservice', methods=['GET'])
def find_service():
    name = request.form.get('name')
    try:
        conn = sql.connect(DATABASE)
        serviceData = select_from_database_table("SELECT * FROM tblService WHERE name=?", [name])
        data = {}
        name = serviceData[1]
        welshName = serviceData[2]
        description = serviceData[3]
        welshDescription = serviceData[4]
        serviceObject = {}
        serviceObject['name'] = name
        serviceObject['welshName'] = welshName
        serviceObject['description'] = description
        serviceObject['welshDescription'] = welshDescription
        data['pharmacy0'] = serviceObject

        json_data = json.dumps(data)
    except Exception as e:
        print(e)
    finally:
        conn.close()
        return json_data


@app.route('/updateservice', methods=['GET', 'PUT'])
def update_service():
    if request.method == "GET":
        return app.send_static_file("updateService.html")
    else:
        name = request.form.get('name', default="Error")
        welshName = request.form.get('welshName', default="Error")
        description = request.form.get('description', default="Error")
        welshDescription = request.form.get('welshDescription', default="Error")
        pin = request.form.get('pincode', default="Error")
        if (pin == pincode):
            msg = update_table("UPDATE tblService SET description=?, welshDescription=? WHERE name=? AND welshName=?", [description, welshDescription, name, welshName])
        else:
            msg = "Invalid pin code"
        return msg


@app.route('/services', methods=['GET'])
def get_services():
    serviceData = select_from_database_table("SELECT * FROM tblService", "", True)
    data = {}
    for i in range(0, len(serviceData)):
        name = serviceData[i][1]
        welshName = serviceData[i][2]
        description = serviceData[i][3]
        welshDescription = serviceData[i][4]

        serviceObject = {}
        serviceObject['name'] = name
        serviceObject['welshName'] = welshName
        serviceObject['description'] = description
        serviceObject['welshDescription'] = welshDescription

        data['service' + str(i)] = serviceObject

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
        if cur.rowcount == 1:
            msg = "Record successfully deleted."
        else:
            msg = "Record not deleted may not exist"
    except sql.ProgrammingError as e:
        conn.rollback()
        msg = "Error in delete operation" + str(e)
    finally:
        conn.close()
        return msg


if __name__ == '__main__':
    app.run()
