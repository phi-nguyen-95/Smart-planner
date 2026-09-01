from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/",methods=["GET","POST"])
def home():
    location=""
    if request.method == "POST":
        location = request.form.get("location","").strip()
    return render_template("index.html", location=location)


if __name__ == "__main__":
    app.run(debug=True)
