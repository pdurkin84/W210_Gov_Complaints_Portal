from flask import Flask, render_template, request
# from flask_restful import reqparse, abort, Api, Resource


app = Flask(__name__)



# # argument parsing
# parser = reqparse.RequestParser()
# parser.add_argument('query', action='append')


@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html')
# def contact():
# 	return render_template('index.html')


@app.route("/admin")
def admin():
    return render_template('admin.html')
# def contact():
# 	return render_template('index.html')

# @app.route("/")
# @app.route("/admin")
# def contact():
# 	return render_template('index.html', _anchor='contact-page')

if __name__ == '__main__':
    app.run(debug=True)