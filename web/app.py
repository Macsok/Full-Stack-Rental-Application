from flask import Flask, render_template, request, redirect, url_for
import httpx


app = Flask(__name__)


def initialize():
    app.run(debug=True)


#------------------------- Web Endpoints -------------------------#
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cars')
async def cars():
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:8000/api/v1/cars")
        response.raise_for_status()
        available_cars = response.json()
    return render_template('cars.html', cars=available_cars)

@app.route('/rental/<int:car_id>', methods=['GET', 'POST'])
async def rental(car_id):
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
            response = await client.post("http://localhost:8000/api/v1/rentals", json=rental_data)
            response.raise_for_status()

        return redirect(url_for('cars'))

    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://localhost:8000/api/v1/cars?car_id={car_id}")
        response.raise_for_status()
        car = response.json()[0]

    return render_template('rental.html', car=car)