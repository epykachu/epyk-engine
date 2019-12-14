from flask import Flask
from epyk_server.endpoints import EpykMain
from epyk_server.endpoints.frontend import EpykFrontReports
app = Flask(__name__)

EpykMain.epyk_config = {'USER_REPORTS_PATH': {"MAIN": r'C:\Users\nelso\PycharmProjects\youpi\AresServer\ares_server\repo'}, 'URLS': {'ares-report': ['', '']}}


@app.route("/")
@app.route("/index")
def index():
  return EpykFrontReports.index()


@app.route("/run/<report_name>", defaults={'script_name': 'index'}, methods=['GET', 'POST'])
@app.route("/run/<report_name>/<script_name>", methods=['GET', 'POST'])
def run_report(report_name, script_name):
  return EpykFrontReports.run_report(report_name, script_name)

if __name__ == '__main__':
  app.run(debug=True)