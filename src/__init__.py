from flask import Flask, jsonify, request, render_template
from .model import get_model, predict

app = Flask(__name__)
pretrained_model = get_model()
pretrained_model.eval()


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def query_predict():
    file = request.files.get("file")
    result = predict(pretrained_model, file.read())
    return jsonify({"result": result})
