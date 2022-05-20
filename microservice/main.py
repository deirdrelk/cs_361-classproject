# Microservice for CS 361
# Receives GET request at /get_cik/<company> URL
# Responds with JSON object with one key: "url"
# and one value: SEC company detail URL

# deployed with GCP https://cs361-microservice-spring22.uw.r.appspot.com/get_cik/<ticker_id_here>

from urllib.request import urlopen
from flask import Flask, abort 
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
            CIK_to_append = new_dict.get(company.lower())
        if CIK_to_append:
            try:
                response = f"https://www.sec.gov/edgar/browse/?CIK={CIK_to_append}&owner=exclude"
                response_dict = {"url": response}
                json_object = json.dumps(response_dict, indent=4)
                return json_object
            except:
                abort(500)
        else:
            abort(404)
        

if __name__ == "__main__":

    #Start the app on port 5000, it will be different once hosted
    app.run(port=5000, debug=True)