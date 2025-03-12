from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

def calculate_bond_price(face_value, coupon_rate, ytm, years, frequency=2):
    """
    Calculate bond price based on inputs.
    - face_value: Bond's par value (e.g., 1000)
    - coupon_rate: Annual coupon rate (e.g., 0.05 for 5%)
    - ytm: Yield to maturity (e.g., 0.04 for 4%)
    - years: Years to maturity
    - frequency: Payments per year (default 2 for semi-annual)
    """
    periods = years * frequency
    coupon = face_value * coupon_rate / frequency
    discount_rate = ytm / frequency

    # Present value of coupons
    pv_coupons = sum(coupon / (1 + discount_rate) ** t for t in range(1, periods + 1))
    # Present value of face value
    pv_face = face_value / (1 + discount_rate) ** periods

    return round(pv_coupons + pv_face, 2)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        face_value = float(request.form['face_value'])
        coupon_rate = float(request.form['coupon_rate']) / 100  # Convert percentage to decimal
        ytm = float(request.form['ytm']) / 100  # Convert percentage to decimal
        years = int(request.form['years'])

        price = calculate_bond_price(face_value, coupon_rate, ytm, years)
        return jsonify({'price': price, 'error': None})
    except ValueError:
        return jsonify({'price': None, 'error': 'Please enter valid numeric inputs'})
    except Exception as e:
        return jsonify({'price': None, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)