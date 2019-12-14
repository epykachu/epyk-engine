from epyk.core.Page import Report
from epyk.core.html.templates import HtmlTmplBase
from epyk_server.endpoints import EpykMain
import json, importlib, sys


@EpykMain.config_required
def index(to_json=False):
  rptObj = Report()
  rptObj.ui.title('Index', level=2)
  rptObj.ui.title('Welcome To Epyk Engine', (120, 'px'))
  regNtwrk, edgesReg = EpykMain.getScripts()
  result = rptObj.outs._to_html_obj()
  result['header'] = rptObj.headers
  if to_json:
    return json.dumps(result)

  return HtmlTmplBase.STATIC_PAGE % result

@EpykMain.config_required
def run_report(report_name, script_name='index', to_json=False):
  """

  :param report_name: the folder in which the script is located
  :param script_name: the name of the script to be called
  :param to_json: specify whether the return type should be a JSON string
  :return HTML string or JSON string:
  """
  sys.path.extend(EpykMain.epyk_config['USER_REPORTS_PATH'].values())
  script_name = script_name.replace('.py', '').replace('#', '')
  try:
    mod = importlib.import_module('%s.%s' % (report_name, script_name))
    rptObj = getattr(mod, 'REPORT_OBJECT', False)
    if not rptObj:
      EpykMain.MissingRptObjException('Your report: %s is missing the REPORT_OBJECT attribute which should be an Report Object from %s' % (mod.__name__, Report.__module__))
    if hasattr(mod, 'FAVICON'):
      rptObj.logo = mod.FAVICON
    if getattr(mod, 'CONTROLLED_ACCESS', False):
      controlLevel = getattr(mod, 'CONTROLLED_LEVEL', 'ENV').upper()
    result = rptObj.outs._to_html_obj()
    result['header'] = rptObj.headers
    if to_json:
      return json.dumps(result)

    return HtmlTmplBase.STATIC_PAGE % result

  except:
    print('Problem executing script')
    raise



if __name__ == '__main__':
  # EpykMain.epyk_config = True
  # print(index())
  print(run_report('test_epyk', 'test_report.py'))