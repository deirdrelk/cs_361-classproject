# Microservice for CS 361
# Receives GET request at /get_cik/<company> URL
# Responds with JSON object with one key: "url"
# and one value: SEC company detail URL

from urllib.request import urlopen
from flask import Flask
import json

app = Flask(__name__)


@app.route("/get_cik/<company>", methods=['GET'])
def get_cik(company):
    url = 'https://www.sec.gov/include/ticker.txt'
    data = urlopen(url)
    new_dict, response_dict = {}, {}
    for line in data:
        decoded_line = line.decode('utf-8')
        ticker, cik = decoded_line.strip().split('\t', 1)
        new_dict[ticker] = cik.strip()
    CIK_to_append = new_dict[company]
    response = f"https://www.sec.gov/edgar/browse/?CIK={CIK_to_append}&owner=exclude"
    response_dict = {"url": response}
    json_object = json.dumps(response_dict, indent=4)
    return json_object, 200