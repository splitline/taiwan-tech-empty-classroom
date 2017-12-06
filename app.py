from flask import Flask, render_template, jsonify, request
import requests
from bs4 import BeautifulSoup
import datetime
app = Flask(__name__, static_url_path='/static')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/ajax', methods=['GET', 'POST'])
def ajax():
    today = datetime.date.today()
    initial_day = datetime.date(2017,12,5)
    payload = {
        "__EVENTTARGET": "date_cal",
        "__EVENTARGUMENT": 6548+(today-initial_day).days,
        "classlist_ddl": request.form['building'],
        "__VIEWSTATE": "dDw1NTk0MzU4NjE7dDw7bDxpPDE+Oz47bDx0PDtsPGk8Mz47aTw0Pjs+O2w8dDxAMDw7Ozs7Ozs7Ozs7Pjs7Pjt0PDtsPGk8NT47PjtsPHQ8QDA8cDxwPGw8U0Q7PjtsPGw8U3lzdGVtLkRhdGVUaW1lLCBtc2NvcmxpYiwgVmVyc2lvbj0xLjAuNTAwMC4wLCBDdWx0dXJlPW5ldXRyYWwsIFB1YmxpY0tleVRva2VuPWI3N2E1YzU2MTkzNGUwODk8MjAxNy0xMi0wNT47Pjs+Pjs+Ozs7Ozs7Ozs7Oz47Oz47Pj47Pj47Pj47Pu5S1476NkYk5hmd81mL76xisA4B",
        "__VIEWSTATEGENERATOR": "D2C5BC33"
    }
    r = requests.post('http://stuinfo.ntust.edu.tw/classroom_user/classroom_usecondition.aspx', data=payload)
    html_data = BeautifulSoup(r.text, "html5lib")
    table_data = [[cell.text.strip() for cell in row("td", nowrap="nowrap")]
                  for row in html_data.table("tr", nowrap="nowrap")]
    return jsonify(table_data)


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run()
