from flask import Flask, request, render_template
import pickle

app = Flask(__name__)

# Load the pre-trained model
try:
    model = pickle.load(open('model1.pkl', 'rb'))
except FileNotFoundError:
    print("Error: model1.pkl not found. Please ensure the model file exists in the same directory.")
    exit(1)  # Exit the script if the model file is not found.
except Exception as e:
    print(f"An error occurred while loading the model: {e}")
    exit(1)


@app.route('/')
def home():
    sales = ''  # Initialize sales variable
    return render_template('sales prediction.html', sales=sales)  # Pass sales to the template


@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        try:
            id = int(request.form['id'])  # Convert to integer
            Date = request.form['Date']
            promo = int(request.form['promo'])  # Convert to integer
            # Assuming your model takes these inputs as a list or array
            input_data = [[id, Date, promo]]
            sales = model.predict(input_data)[0]  # Predict and get the first element of the prediction
            return render_template('sales prediction.html', sales=sales, id=id, Date=Date, promo=promo)
        except ValueError:
            return render_template('sales prediction.html', error="Invalid input. Please enter numeric values for 'id' and 'promo'.")
        except Exception as e:
            print(f"An error occurred during prediction: {e}")
            return render_template('sales prediction.html', error=f"An error occurred: {e}")


if __name__ == '__main__':
    app.run(debug=True)