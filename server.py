from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 4000))
    app.run(host="0.0.0.0", port=port)
    # app.run(debug=True)