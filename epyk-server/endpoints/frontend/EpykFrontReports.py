from epyk.core.Page import Report
from epyk.core.html.templates import HtmlTmplBase
import json

def index(to_json=False):
  rptObj = Report()
  rptObj.ui.title('title')
  result = rptObj.outs._to_html_obj()
  result['header'] =  rptObj.headers
  if to_json:
    return json.dumps(rptObj.outs._to_html_obj())

  return HtmlTmplBase.STATIC_PAGE % result

def run_report():
  pass

if __name__ == '__main__':
  print(index(True))