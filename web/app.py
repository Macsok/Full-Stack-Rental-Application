from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
import httpx
import time
import hashlib

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Add a secret key for session management

def initialize():
    app.run(debug=True)


#------------------------- Login / Register -------------------------#
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
async def login():
    if request.method == 'POST':
        provided_username = request.form['username']
        provided_password = request.form['password']
        async with httpx.AsyncClient() as client:
            # Authenticate user
            user_response = await client.get(f"http://localhost:8000/api/v1/users?username={provided_username}")
            if user_response.status_code == 404:
                flash("Wrong username or password", "error")
                return redirect(url_for('login'))
            user_id = user_response.json()[0]['id']
            
            password_response = await client.get(f"http://localhost:8000/api/v1/passwords?user_id={user_id}")
            if password_response.status_code == 404:
                flash("Wrong username or password", "error")
                return redirect(url_for('login'))
            stored_password = password_response.json()[0]['password']
            
            hashed_provided_password = hashlib.sha512(provided_password.encode()).hexdigest()[:50]
            
            if hashed_provided_password == stored_password:
                session['token'] = 'your_session_token'
                return redirect(url_for('index'))
            else:
                flash("Wrong username or password", "error")
                return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('token', None)
    return redirect(url_for('index'))

@app.route('/check_username', methods=['POST'])
async def check_username():
    data = request.get_json()
    username = data['username']
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://localhost:8000/api/v1/users?username={username}")
        if response.status_code == 404:
            user_exists = False
        else:
            response.raise_for_status()
            user_exists = bool(response.json())
    return jsonify({'exists': user_exists})

@app.route('/register', methods=['GET', 'POST'])
async def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        city = request.form['city']
        country = request.form['country']
        async with httpx.AsyncClient() as client:
            # Check if username exists using /check_username endpoint
            response = await client.get(f"http://localhost:8000/api/v1/users?username={username}")
            if response.status_code == 404:
                user_exists = False
            else:
                pass
            # Register new user
            user_data = {
                "username": username,
                "password": password,
                "email": email,
            }
            response = await client.post("http://localhost:8000/api/v1/users", json=user_data)
            response.raise_for_status()
            time.sleep(0.5)
            
            # Get user ID from users endpoint
            response = await client.get(f"http://localhost:8000/api/v1/users?username={username}")
            response.raise_for_status()
            user_id = response.json()[0]['id']

            address_data = {
                "address": address,
                "city": city,
                "country": country
            }
            address_response = await client.post("http://localhost:8000/api/v1/addresses", json=address_data)
            address_response.raise_for_status()
            time.sleep(0.5)

            # Get address ID from users endpoint
            response = await client.get(f"http://localhost:8000/api/v1/addresses")
            response.raise_for_status()
            address_id = response.json()[-1]['id']
            
            user_detail_data = {
                "user_id": user_id,
                "address_id": address_id,
                "email": email,
                "phone": phone,
                "is_active": True,
                "role": "user"
            }
            await client.post("http://localhost:8000/api/v1/user_details", json=user_detail_data)
            
            password_data = {
                "user_id": user_id,
                "password": password
            }
            await client.post("http://localhost:8000/api/v1/passwords", json=password_data)
            
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/add_car', methods=['GET', 'POST'])
async def add_car():
    if request.method == 'POST':
        if 'brand' in request.form and 'model' in request.form and 'year' in request.form:
            brand = request.form['brand']
            model = request.form['model']
            year = int(request.form['year'])

            async with httpx.AsyncClient() as client:
                car_data = {
                    "brand": brand,
                    "model": model,
                    "year": year
                }
                response = await client.post("http://localhost:8000/api/v1/cars", json=car_data)
                response.raise_for_status()
                response = await client.get("http://localhost:8000/api/v1/cars")
                car_id = response.json()[-1]['id'] + 1
                
                return render_template('add_car.html', step=2, car_id=car_id)

        elif 'car_id' in request.form and 'price_per_day' in request.form and 'horse_power' in request.form:
            car_id = int(request.form['car_id'])
            price_per_day = int(request.form['price_per_day'])
            horse_power = int(request.form['horse_power'])

            async with httpx.AsyncClient() as client:
                car_detail_data = {
                    "car_id": car_id,
                    "location_id": 1,
                    "price_per_day": price_per_day,
                    "horse_power": horse_power
                }
                response = await client.post("http://localhost:8000/api/v1/car_details", json=car_detail_data)
                response.raise_for_status()

            return redirect(url_for('index'))

    return render_template('add_car.html', step=1)




#------------------------- Browsing -------------------------#

@app.route('/cars')
async def cars():
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:8000/api/v1/cars")
        response.raise_for_status()
        available_cars = response.json()
        
        # Fetch detailed information for each car
        car_ids = [car['id'] for car in available_cars]
        details_responses = await client.get(f"http://localhost:8000/api/v1/car_details?car_ids={','.join(map(str, car_ids))}")
        details_responses.raise_for_status()
        car_details_list = details_responses.json()
        
        # Create a dictionary for quick lookup
        car_details_dict = {details['car_id']: details for details in car_details_list}
        
        for car in available_cars:
            car_id = car['id']
            if car_id in car_details_dict:
                car.update(car_details_dict[car_id])
            else:
                car['price_per_day'] = 'N/A'
            
    return render_template('cars.html', cars=available_cars)

@app.route('/rental/<int:car_id>', methods=['GET', 'POST'])
async def rental(car_id):
    token = session.get('token')
    if not token:
        return redirect(url_for('login'))
    if request.method == 'POST':
        customer_name = request.form['customer_name']
        rental_date = request.form['rental_date']
        return_date = request.form['return_date']
        
        async with httpx.AsyncClient() as client:
            rental_data = {
                "car_id": car_id,
                "customer_name": customer_name,
                "rental_date": rental_date,
                "return_date": return_date,
                "total_price": 100.00  # Cena na stałe 100 PLN
            }
            headers = {'Authorization': f'Bearer {token}'}
            response = await client.post("http://localhost:8000/api/v1/rentals", json=rental_data, headers=headers)
            response.raise_for_status()

        return redirect(url_for('cars'))

    async with httpx.AsyncClient() as client:
        headers = {'Authorization': f'Bearer {token}'}
        response = await client.get(f"http://localhost:8000/api/v1/cars?car_id={car_id}", headers=headers)
        response.raise_for_status()
        car = response.json()[0]

    return render_template('rental.html', car=car)