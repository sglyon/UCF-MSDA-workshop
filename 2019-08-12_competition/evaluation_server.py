import json
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, make_response
from sklearn import metrics
import pymongo

app = Flask(__name__)

conn = pymongo.MongoClient("mongodb+srv://sglyon:YaDf43h6HgD3ZAjt7rQB@valorumtest-f6xsb.mongodb.net/test?retryWrites=true&w=majority")
DB = conn.msda
Y = pd.read_csv("test_y.csv", parse_dates=["date"], index_col=["date", "hour"])

def get_rank(mse):
    return (
        DB.mce_competition_results.count_documents({"mse": {"$lt": mse}})
        + 1
    )


def get_leaderboard(n):
    """
    get the top `n` submissions so far
    """
    q = DB.mce_competition_results.find({}, {"_id": 0}).limit(n).sort("mse", 1)
    return list(q)


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route("/leaderboard", methods=["GET"])
def leaderboard():
    res = get_leaderboard(50)
    return make_response(jsonify(dict(leaderboard=res)), 200)


@app.route("/submit", methods=["POST"])
def submit():
    # validate content type
    if request.content_type != "application/json":
        raise InvalidUsage('Expected json input', status_code=400)

    # parse json, now that we know we have it
    try:
        data = json.loads(request.data)
    except JSONDecodeError:
        raise InvalidUsage('JSON not formatted properly', status_code=400)

    # extract the data we need from the json body
    name = data.get("name", None)
    yhat = data.get("prediction", None)
    if name is None or yhat is None:
        msg = "Must supply `name` and `prediction` as keys in JSON body"
        raise InvalidUsage(msg, status_code=400)

    # convert to array, check shape
    yhat_np = np.asarray(yhat)
    if yhat_np.shape != Y.shape:
        msg = "Expected `prediction` to have shape {}. Found shape {}"
        raise InvalidUsage(msg.format(Y.shape, yhat_np.shape), status_code=400)

    # convert to dataframe and evaluate the MSE
    yhat_df = pd.DataFrame(yhat_np, index=Y.index, columns=Y.columns)
    mse = metrics.mean_squared_error(Y, yhat_df)

    # store in database
    mse_payload = dict(name=name, mse=mse, timestamp=pd.Timestamp.utcnow())
    db_mse = DB.mce_competition_results.insert_one(mse_payload)
    payload = dict(
        _id=db_mse.inserted_id,
        damce=yhat_df["target1"].tolist(),
        rtmce=yhat_df["target2"].tolist(),
    )
    DB.mce_competition_submissions.insert_one(payload)

    # get current rank
    rank = get_rank(mse)
    leaders = get_leaderboard(50)

    # package up output and return
    response = dict(rank=rank, leaders=leaders)
    return make_response(jsonify(response), 200)
