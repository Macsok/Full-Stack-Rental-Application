from flask import Flask, render_template, request, redirect, url_for, session
import httpx

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Add a secret key for session management

def initialize():
    app.run(debug=True)


#------------------------- Web Endpoints -------------------------#
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Authenticate user (this is just a placeholder, implement actual authentication)
        if username == 'admin' and password == 'password':
            session['token'] = 'your_session_token'
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('token', None)
    return redirect(url_for('index'))

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