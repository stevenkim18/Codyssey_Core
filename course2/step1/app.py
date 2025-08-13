from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

@app.route('/')
def root():
    return redirect(url_for('menu'))

@app.route('/menu')
def menu():
    return render_template('menu.html')

if __name__ == "__main__":
    app.run(port=8080)