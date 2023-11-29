from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        income_weight = float(request.form.get('income_weight', 1))
        children_weight = float(request.form.get('children_weight', 1))
        # Add your analysis logic here
        result = perform_analysis(income_weight, children_weight)
        return render_template('index.html', result=result)
    return render_template('index.html', result=None)

def perform_analysis(income_weight, children_weight):
    # Your analysis logic goes here
    # For demo purposes, let's just return a string
    return f"Analysis with Income Weight: {income_weight}, Children Weight: {children_weight}"

if __name__ == '__main__':
    app.run(debug=True)
