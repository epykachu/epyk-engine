from epyk.core.Page import Report


def index():
  rptObj = Report()
  rptObj.ui.title('title')
  print(rptObj.html())

def run_report():
  pass

if __name__ == '__main__':
  index()