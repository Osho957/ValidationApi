import pymysql
from app import app
from db_config import mysql
from flask import jsonify
from flask import flash, request
import re


@app.route('/add', methods=['POST'])
def add_user():
    try:
        _json = request.json
        _name = _json['name']
        _email = _json['email']
        _phone = _json['phone']
        # validate the received values
        if _name and _email and _phone and request.method == 'POST':

            # save edits
            sql = "INSERT INTO tbl_user(user_name, user_email, user_phone) VALUES(%s, %s, %s)"
            data = (_name, _email, _phone,)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            resp = jsonify('User added successfully!')
            resp.status_code = 200
            return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/validate', methods=['POST'])
def validate_user():
    try:
        name = request.args.get("name")
        email = request.args.get("email")
        phone = request.args.get("phone")
        print(name + " " + email + " " + phone)
        # validate the received values
        if name and email and phone and request.method == 'POST':
            # save edits
            conn = mysql.connect()
            cursor = conn.cursor()

            if check_email(email) and check_name(name) and check_phone(phone):
                sql = "INSERT INTO tbl_user(user_name, user_email, user_phone) VALUES(%s, %s, %s)"
                data = (name, email, phone,)
            else:
                return not_valid()

            cursor.execute(sql, data)
            conn.commit()
            resp = jsonify('Details validated and saved successfully!')
            resp.status_code = 200
            return resp
        else:
            return not_valid()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/users')
def users():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM tbl_user")
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/user/<int:id>')
def user(id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM tbl_user WHERE user_id=%s", id)
        row = cursor.fetchone()
        resp = jsonify(row)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/update', methods=['POST'])
def update_user():
    try:
        _json = request.json
        _id = _json['id']
        _name = _json['name']
        _email = _json['email']
        _phone = _json['phone']
        # validate the received values
        if _name and _email and _phone and _id and request.method == 'POST':
            # save edits
            sql = "UPDATE tbl_user SET user_name=%s, user_email=%s, user_phone=%s WHERE user_id=%s"
            data = (_name, _email, _phone, _id,)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            resp = jsonify('User updated successfully!')
            resp.status_code = 200
            return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/delete/<int:id>')
def delete_user(id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tbl_user WHERE user_id=%s", (id,))
        conn.commit()
        resp = jsonify('User deleted successfully!')
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp


@app.errorhandler(404)
def not_valid(error=None):
    message = {
        'status': 404,
        'message': 'Not valid details please provide the correct details '
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp


# Make a regular expression
# for validating an Email
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


# Define a function for validating an Email
def check_email(email):
    # pass the regular expression
    # and the string into the full match() method
    if re.fullmatch(regex, email):
        return True
    else:
        return False


# Define a function for validating a name
def check_name(name):
    for char in name:
        if not (("A" <= char <= "Z") or ("a" <= char <= "z") or (char == " ")):
            return False
    return True


def check_phone(phone):
    # 1) Begins with 0 or 91
    # 2) Then contains 6,7 or 8 or 9.
    # 3) Then contains 9 digits
    Pattern = re.compile("(0|91)?[6-9][0-9]{9}")
    return Pattern.match(phone)


if __name__ == "__main__":
    app.run(debug=True)
