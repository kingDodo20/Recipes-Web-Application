import sqlite3, datetime
from werkzeug.security import check_password_hash, generate_password_hash

def get_db():
    conn = sqlite3.connect("database.db")
    return conn

def create_tables():
    connection_db = get_db()
    cur = connection_db.cursor()
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            firstname TEXT NOT NULL,
            lastname TEXT NOT NULL,
            date_of_birth TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            last_email_update TEXT DEFAULT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            image_name TEXT NOT NULL,
            ingredients TEXT NOT NULL,
            instructions TEXT NOT NULL,
            calories FLOAT NOT NULL,
            fat FLOAT NOT NULL,
            carbs FLOAT NOT NULL,
            protein FLOAT NOT NULL
        )
    """)
    
    connection_db.commit() 
    connection_db.close()

def insert_account(dt):
    try:
        connection_db = get_db()
        cur= connection_db.cursor()
        cur.execute("INSERT INTO accounts (firstname,lastname,date_of_birth,email,password) VALUES (?,?,?,?,?)",
        (
            dt['firstname'],
            dt['lastname'],
            dt['date_of_birth'],
            dt['email'],
            generate_password_hash(dt['password'])
            )
            )
        connection_db.commit()
    except sqlite3.IntegrityError as e:
        print("this email already exists")
    finally:
        connection_db.close()

def check_email(email):
     connection_db = get_db()
     cur= connection_db.cursor()
     cur.execute("SELECT id, firstname, lastname, email, password , date_of_birth FROM accounts WHERE email = ?", (email,))
     dt=cur.fetchone()
     connection_db.close()
     if dt:
        return {'id': dt[0], 'firstname': dt[1], 'lastname': dt[2], 'email': dt[3], 'password': dt[4] , 'date_of_birth': dt[5]}


def account_login(email,password):
     connection_db = get_db()
     cur= connection_db.cursor()
     cur.execute("SELECT email, password FROM accounts WHERE email = ?", (email,))
     dt=cur.fetchone()
     connection_db.close()
     if dt is not None:
        stored_password_hash = dt[1]
        return check_password_hash(stored_password_hash, password)
     return False


def insert_recipes(dt):
    try:
        connection_db = get_db()
        cur = connection_db.cursor()

        cur.execute("SELECT * FROM recipes WHERE name = ?", (dt['name'],))
        if cur.fetchone():
            raise sqlite3.IntegrityError("Recipe already exists.")

        ingredients = ";".join([line.strip() for line in dt['ingredients'].split(';')])

        cur.execute("""
            INSERT INTO recipes 
            (name, description, image_name, ingredients, instructions, calories, fat, carbs, protein)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            dt['name'],
            dt['description'],
            dt['image_name'],
            ingredients,
            dt['instructions'],
            dt['calories'],
            dt['fat'],
            dt['carbs'],
            dt['protein'],
        ))
        connection_db.commit()
    except sqlite3.IntegrityError as e:
        print("Integrity Error:", str(e))
        raise
    except Exception as e:
        print("Error:", str(e))
        raise
    finally:
        connection_db.close()




def get_recipes_data():
    connection_db = get_db()
    cur = connection_db.cursor()
    cur.execute("SELECT * FROM recipes")
    data = cur.fetchall()
    connection_db.close()
    return data


def update_user_data(email, firstname, lastname, date_of_birth):
    connection_db = get_db()
    cur = connection_db.cursor()
    cur.execute(
        "UPDATE accounts SET firstname = ?, lastname = ?, date_of_birth = ? WHERE LOWER(email) = ?",
        (
            firstname,
            lastname,
            date_of_birth,
            email,
        )
    )
    connection_db.commit()
    connection_db.close()

def update_email(user_id, new_email):
    connection_db = get_db()
    cur = connection_db.cursor()
    
    cur.execute("SELECT last_email_update FROM accounts WHERE id = ?", (user_id,))
    result = cur.fetchone()
    last_update = result[0]
    
    if last_update:
        last_update_date = datetime.datetime.strptime(last_update, "%Y-%m-%d")
        days_difference = (datetime.datetime.now() - last_update_date).days
        if days_difference < 7:
            return {"success": False, "message": "Email can only be changed once every 7 days."}
    
    try:
        cur.execute(
            "UPDATE accounts SET email = ?, last_email_update = ? WHERE id = ?",
            (new_email, datetime.datetime.now().strftime("%Y-%m-%d"), user_id)
        )
        connection_db.commit()
        return {"success": True, "message": "Email updated successfully."}
    except sqlite3.IntegrityError:
        return {"success": False, "message": "The new email is already in use."}
    finally:
        connection_db.close()
