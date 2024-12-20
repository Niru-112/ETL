from flask import Flask, render_template, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/execute')
def execute_script():
    try:
        # Define the path to your Python script
        script_path = os.path.join(os.getcwd(), 'D:\\ETL\\mainn.py')

        # Ensure the script exists
        if not os.path.exists(script_path):
            return jsonify({'error': f"Script not found at {script_path}"}), 400

        # Run the script using subprocess
        result = subprocess.run(['python', script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Capture stdout and stderr
        output = result.stdout
        errors = result.stderr

        if result.returncode == 0:
            return jsonify({'success': True, 'output': output}), 200
        else:
            return jsonify({'success': False, 'error': errors}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    print("executing!!")


if __name__ == '__main__':
    app.run(debug=True)
