from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
import httpx
import time
import hashlib
from datetime import datetime, timedelta


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
                session['customer_id'] = user_id
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

    if request.method == 'POST' and request.form.get('step') == '1':

        rental_date = request.form['rental_date']
        return_date = request.form['return_date']

        session['rental_date'] = rental_date
        session['return_date'] = return_date

        rental_data = {
            "car_id": car_id,
            "rental_date": rental_date,
            "return_date": return_date
        }

        async with httpx.AsyncClient() as client:
            response = await client.post("http://localhost:8000/api/v1/rentals", json=rental_data)
            if response.status_code == 201:
                response = await client.get(f"http://localhost:8000/api/v1/rentals")
                response.raise_for_status()
                rental_id = response.json()[-1]['id']
                rental_id = rental_id + 1
                
                return redirect(url_for('rental_detail', car_id=car_id, rental_id=rental_id))
            else:
                flash("Wystąpił problem przy tworzeniu wypożyczenia", "error")
                return redirect(url_for('rental', car_id=car_id))

   
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://localhost:8000/api/v1/cars?car_id={car_id}")
        response.raise_for_status()
        car = response.json()[0]

    return render_template('rental.html', car=car)


@app.route('/rental_detail/<int:car_id>/<int:rental_id>', methods=['GET', 'POST'])
async def rental_detail(car_id, rental_id):
    token = session.get('token')
    if not token:
        return redirect(url_for('login'))

    rental_date = session.get('rental_date')
    return_date = session.get('return_date')
    customer_id = session.get('customer_id')

    async with httpx.AsyncClient() as client:
      
        car_response = await client.get(f"http://localhost:8000/api/v1/cars?car_id={car_id}")
        car_response.raise_for_status()
        car = car_response.json()

        
        price_response = await client.get(f"http://localhost:8000/api/v1/car_details?car_id={car_id}")
        price_response.raise_for_status()
        price_per_day = price_response.json()[0]['price_per_day']

        total_price = 9
        if rental_date and return_date:
            rental_date_obj = datetime.strptime(rental_date, "%Y-%m-%d")
            return_date_obj = datetime.strptime(return_date, "%Y-%m-%d")
            delta_days = (return_date_obj - rental_date_obj).days
            total_price = delta_days * price_per_day if delta_days > 0 else 0

        if request.method == 'POST':

            

            rental_detail_data = {
                "rental_id": rental_id,
                "customer_id": customer_id,
                "total_price": total_price
            }
            await client.post("http://localhost:8000/api/v1/rental_details", json=rental_detail_data)
            flash(f"Całkowity koszt wypożyczenia to {total_price} PLN", "success")

            payment_data = {
                "rental_id": rental_id
            }
            await client.post("http://localhost:8000/api/v1/payments", json=payment_data)
            flash(f"utworzono payment")
            response_payment = await client.get(f"http://localhost:8000/api/v1/payments")
            response_payment.raise_for_status()
            payment_id = response_payment.json()[-1]['id'] + 1
            session['payment_id'] = payment_id
            session['total_price'] = total_price
            return redirect(url_for('payment_detail', car_id=car_id, rental_id=rental_id))

    return render_template('rental_detail.html', 
                           car=car, 
                           rental_id=rental_id, 
                           car_id=car_id, 
                           price_per_day=price_per_day, 
                           rental_date=rental_date, 
                           return_date=return_date, 
                           total_price=total_price, 
                           customer_id=customer_id)


@app.route('/payment_detail/<int:car_id>/<int:rental_id>', methods=['GET', 'POST'])
async def payment_detail(car_id,rental_id):
       
    payment_id = session.get('payment_id')
    user_id = session.get('customer_id')
    amount = session.get('total_price')
  
    payment_methods = ["Gotówka", "Karta płatnicza", "Przelew tradycyjny", "Blik", "PayPo"]
    payment_date = (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d")

    if request.method == 'POST':
        method = request.form.get('payment_method')
        session['payment_method'] = method
        if not method:
            flash("Wybierz metodę płatności", "error")
            return render_template('payment_detail.html', payment_methods=payment_methods, amount=amount)
        
        payment_detail_data = {
            "payment_id": payment_id,
            "user_id": user_id,
            "amount": amount,
            "method": method,
            "payment_date": payment_date
        }

        async with httpx.AsyncClient() as client:
            response = await client.post("http://localhost:8000/api/v1/payment_details", json=payment_detail_data)
            if response.status_code == 201:
                flash("Szczegóły płatności zostały zapisane", "success")
                return redirect(url_for('rental_summary', car_id=car_id, rental_id=rental_id))
            else:
                flash("Nie udało się zapisać szczegółów płatności", "error")
    
    return render_template('payment_detail.html', payment_methods=payment_methods, amount=amount, payment_date=payment_date, car_id=car_id, rental_id=rental_id)


@app.route('/rental_summary/<int:car_id>/<int:rental_id>', methods=['GET'])
async def rental_summary(car_id, rental_id):

    rental_date = session.get('rental_date')
    return_date = session.get('return_date')
    total_price = session.get('total_price')
    payment_id = session.get('payment_id')
    payment_method = session.get('payment_method')

    async with httpx.AsyncClient() as client:
        car_response = await client.get(f"http://localhost:8000/api/v1/cars?car_id={car_id}")
        car_response.raise_for_status()
        car = car_response.json()[-1]

        payment_detail_response = await client.get(f"http://localhost:8000/api/v1/payment_details?payment_id={payment_id}")
        payment_detail_response.raise_for_status()
        payment_detail = payment_detail_response.json()[-1]

    payment_date = payment_detail.get('payment_date', 'N/A')
    amount = payment_detail.get('amount', 'N/A')


    return render_template(
        'summary.html',
        car=car,
        rental_id=rental_id,
        rental_date=rental_date,
        return_date=return_date,
        total_price=total_price,
        payment_id=payment_id,
        amount=amount,
        payment_method=payment_method,
        payment_date=payment_date
    )

@app.route('/user_rentals', methods=['GET'])
async def user_rentals():
    user_id = session.get('customer_id')

    async with httpx.AsyncClient() as client:
        rentals_response = await client.get("http://localhost:8000/api/v1/rentals")
        if rentals_response.status_code != 200:
            flash("Nie udało się pobrać wypożyczeń.", "error")
            return redirect(url_for('index'))

        all_rentals = rentals_response.json()

        user_rentals = []
        for rental in all_rentals:
            rental_id = rental['id']

            rental_details_response = await client.get(f"http://localhost:8000/api/v1/rental_details?rental_detail_id={rental_id}")
            if rental_details_response.status_code != 200:
                continue 

            rental_details_list = rental_details_response.json()
            for rental_details in rental_details_list:
                if rental_details.get('customer_id') == user_id:
                    rental['start_date'] = rental.get('rental_date', 'Brak danych')
                    rental['end_date'] = rental.get('return_date', 'Brak danych')
                    user_rentals.append(rental)
                    break

        car_ids = {rental['car_id'] for rental in user_rentals}
        cars_response = await client.get(f"http://localhost:8000/api/v1/cars?car_ids={','.join(map(str, car_ids))}")
        if cars_response.status_code != 200:
            flash("Nie udało się pobrać szczegółów aut.", "error")
            return redirect(url_for('index'))

        cars = cars_response.json()
        car_details = {car['id']: f"{car['brand']} {car['model']}" for car in cars}

        for rental in user_rentals:
            rental['car_name'] = car_details.get(rental['car_id'], "Nieznane auto")
            

    return render_template('user_rentals.html', rentals=user_rentals)

