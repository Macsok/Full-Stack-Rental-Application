from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from database.db_connection import get_db_connection

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cars')
def cars():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM cars WHERE available = TRUE")
    available_cars = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('cars.html', cars=available_cars)

@app.route('/rental/<int:car_id>', methods=['GET', 'POST'])
def rental(car_id):
    if request.method == 'POST':
        customer_name = request.form['customer_name']
        rental_date = request.form['rental_date']
        return_date = request.form['return_date']
        
        
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO rentals (car_id, customer_name, rental_date, return_date, total_price) "
                       "VALUES (%s, %s, %s, %s, %s)",
                       (car_id, customer_name, rental_date, return_date, 100.00))  # Cena na stałe 100 PLN
        connection.commit()
        cursor.close()
        connection.close()

        
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("UPDATE cars SET available = FALSE WHERE id = %s", (car_id,))
        connection.commit()
        cursor.close()
        connection.close()

        return redirect(url_for('cars'))

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM cars WHERE id = %s", (car_id,))
    car = cursor.fetchone()
    cursor.close()
    connection.close()

    return render_template('rental.html', car=car)

def initialize():
    app.run(debug=True)