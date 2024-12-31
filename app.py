from flask import Flask, render_template ,redirect, url_for,request ,session,flash
from database import *
import secrets,os


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/upload'
app.secret_key = secrets.token_hex(16)


create_tables()


@app.route("/")
@app.route('/login', methods=["POST", "GET"])
def login():
    email_cookie = request.cookies.get('email')
    password_cookie = request.cookies.get('password')

    if email_cookie and password_cookie:
        if account_login(email_cookie, password_cookie):
            user = check_email(email_cookie)
            session['user_id'] = user['id']
            session['email'] = email_cookie
            session['user_name'] = f"{user['firstname']} {user['lastname']}"
            flash('Logged in successfully!', category='success')
            return redirect(url_for('homepage'))

    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        if account_login(email, password):  
            user = check_email(email)
            session['user_id'] = user['id']
            session['email'] = email
            session['user_name'] = f"{user['firstname']} {user['lastname']}"
            flash('Logged in successfully!', category='success')

            
            remember_me = request.form.get('remember_me')
            if remember_me:
                resp = redirect(url_for('homepage'))
                resp.set_cookie('email', email, max_age=7*24*60*60)  
                resp.set_cookie('password', password, max_age=7*24*60*60)  
                return resp
            return redirect(url_for('homepage'))
        else:
            flash('Invalid email or password.', category='error')

    return render_template('login.html')




@app.route('/signup', methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        first_name = request.form.get('firstname')
        last_name = request.form.get('lastname')
        email = request.form.get('email')
        password = request.form.get('password')
        dob = request.form.get('date_of_birth')
        if check_email(email):
            return "Email already exists", 400

        if not all([first_name, last_name, email, password, dob]):
            flash("All fields are required!")
            return render_template('signup.html')

        insert_account({'firstname': first_name,
                         'lastname': last_name, 
                         'email': email, 
                         'date_of_birth': dob,
                         'password': password })
        flash("Account created successfully! Please log in.")
        return render_template('login.html')
    elif request.method == "GET":
        return render_template('signup.html')

@app.route('/logout')
def logout():
    session.clear()
    resp = redirect(url_for('login'))
    resp.delete_cookie('email')
    resp.delete_cookie('password')
    flash('You have been logged out.', category='info')
    return resp



@app.route('/home')
def homepage():
    if "user_id" in session:
        return render_template('homePage.html')
    else:
        return redirect(url_for('login'))


@app.route('/about')
def about():
    if "user_id" in session:
        return render_template('about.html')
    else:
        return redirect(url_for('login'))
    

@app.route('/recipes')
def recipesPage():
    if "user_id" in session:
        data = get_recipes_data()
        recipes = {
            row[1]: {
                "title": row[1],
                "description": row[2],
                "image_name": row[3],
                "ingredients": row[4].split(';'),
                "instructions": row[5],
                "nutritionFacts": f"Calories: {row[6]}; Fat: {row[7]}; Carbs: {row[8]}; Protein: {row[9]}"
            }
            for row in data
        }
        return render_template('recipes.html', recipes=recipes)
    else:
        return redirect(url_for('login'))



@app.route('/recipe/<recipe_name>')
def recipe_detail(recipe_name):
    if "user_id" in session:
        data = get_recipes_data()
        for row in data:
            if row[1] == recipe_name:
                recipe = {
                    "title": row[1],
                    "description": row[2],
                    "image_name": row[3],
                    "ingredients": row[4].split(';'),
                    "instructions": row[5],
                    "nutritionFacts": f"Calories: {row[6]}; Fat: {row[7]}; Carbs: {row[8]}; Protein: {row[9]}"
                }
                return render_template('recipe_detail.html', recipe=recipe)
        return "Recipe not found", 404
    else:
        return redirect(url_for('login'))


@app.route('/upload', methods=['GET', 'POST'])
def uploadRecipePage():
    if "user_id" in session:
        if request.method == 'POST':
            image = request.files['image']
            if image:
                try:
                    unique_filename = secrets.token_hex(8) + os.path.splitext(image.filename)[1]
                    image_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                    image.save(image_path)

                    data = {
                        'name': request.form['name'],
                        'description': request.form['description'],
                        'image_name': unique_filename,
                        'ingredients': request.form['ingredients'],
                        'instructions': request.form['instructions'],
                        'calories': float(request.form['calories']),
                        'fat': float(request.form['fat']),
                        'carbs': float(request.form['carbs']),
                        'protein': float(request.form['protein']),
                    }

                    print("Parsed Data:", data)

                    insert_recipes(data)
                    flash("Recipe uploaded successfully!", "success")
                    return redirect(url_for('recipesPage'))

                except Exception as e:
                    print("Error:", str(e))
                    flash(f"Error: {str(e)}", "error")
                    return redirect(url_for('uploadRecipePage'))
            else:
                flash("Image is required!", "error")
                return redirect(url_for('uploadRecipePage'))
        else:
            return render_template('upload.html')
    else:
        return redirect(url_for('login'))




@app.route('/profile', methods=["POST", "GET"])
def profile():
    if "user_id" in session:

        user_id = session['user_id']
        current_email = session['email']

        if request.method == "POST":
            new_email = request.form.get('email')
            firstname = request.form.get('firstname')
            lastname = request.form.get('lastname')
            date_of_birth = request.form.get('date_of_birth')


            if new_email and new_email != current_email:
                email_update_result = update_email(user_id, new_email)
                if not email_update_result["success"]:
                    flash(email_update_result["message"], category='error')
                    return render_template(
                        'profile.html', email=current_email, firstname=firstname, lastname=lastname, date_of_birth=date_of_birth
                    )

                session['email'] = new_email

            update_user_data(current_email, firstname, lastname, date_of_birth)
            flash("Profile updated successfully!", category='success')
            return redirect(url_for('profile'))

        user_data = check_email(current_email)
        return render_template(
            'profile.html',
            email=user_data['email'],
            firstname=user_data['firstname'],
            lastname=user_data['lastname'],
            date_of_birth=user_data['date_of_birth']
        )
    return redirect(url_for('login'))




if __name__ == '__main__':
    app.run(debug=True)