import re, os, importlib
epyk_config = {'USER_REPORTS_PATH': {"MAIN": r'C:\Users\nelso\PycharmProjects\youpi\AresServer\ares_server\repo'}, 'URL': {'ares-report': ['', '']}}


class MissingEpykConfigException(Exception):
  """Exception to be raised when the configuration is missing"""
  pass

class MissingRptObjException(Exception):
  pass



def config_required(func):
  """Simple decorator to throw an error if the config is required and hasn't been setup before """
  def call_func(*args, **kwargs):
    if epyk_config is None:
      raise MissingEpykConfigException('Configuration required for endpoint: %s. Set epyk_config from %s' % (func.__name__, __name__))

    return func(*args, **kwargs)
  return call_func


def tracebackHtml(tracebackStr):
  return "<pre style='padding:5px;white-space:pre-wrap; '>%s</pre>" % '<br>'.join([ re.sub(r'^ +', lambda m: ' ' * len(m.group()), i) for i in tracebackStr.split('\n') ])

@config_required
def getScripts(env=None):
  """"""
  repoPaths = set()
  repoPaths = repoPaths | set(epyk_config['USER_REPORTS_PATH'].values())
  otherFolders, favoriteFolder = [], []
  systemFolders = ['lab', 'scheduler', 'drafts']
  myFavorites, scriptIds, favoriteScriptIds = {}, {}, []
  regNtwrk, edgesReg = [], []
  for repo in repoPaths:
    if os.path.exists(repo):
      for folder in os.listdir(repo):
        if folder in ['.svn', "__pycache__"] or not os.path.isdir(os.path.join(repo, folder)):
          continue

        if not os.path.isdir(os.path.join(repo, folder)):
          continue

        if env and folder != env:
          continue

        folderPath = os.path.join(repo, folder)
        regNtwrk.append({'id': folder, 'label': folder, 'shape': 'circle'})
        if os.path.isdir(folderPath) and folder not in ['.svn', "__pycache__"] and not folder.startswith('.') and folder not in systemFolders:
          otherFolders.append({'name': folder, 'items': []})
          for script in os.listdir(folderPath):
            if script.endswith('.py') and script not in ['__init__.py', 'index.py']:
              script_nosfx = script.replace('.py', '')
              try:
                mod = importlib.import_module('%s.%s' % (folder, script_nosfx))
                scriptConfig = {'id': "_".join([folder, script_nosfx]), 'label': mod.TITLE, 'category': getattr(mod, "CATEGORY", None),
                                'folder': folder, 'contact': getattr(mod, "CONTACT", None),
                                'url': '%s/run/%s/%s' % (epyk_config['URLS']['ares-report'][1:], folder, script_nosfx)}
                if script_nosfx in myFavorites and folder in myFavorites[script_nosfx]:
                  if folder not in favoriteFolder:
                    favoriteFolder.append(folder)
                  scriptConfig.update({'shape': 'star', 'color': 'green'})
                  edgesReg.append({'from': folder, 'to': '%s_%s' % (folder, script_nosfx), 'color': 'green', 'value': 70})
                else:
                  scriptConfig.update({'shape': 'square', 'value': 30})
                  edgesReg.append({'from': folder, 'to': '%s_%s' % (folder, script_nosfx)})
                regNtwrk.append(scriptConfig)
              except Exception as err:
                regNtwrk.append(
                  {'id': '%s_%s' % (folder, script_nosfx), 'label': script_nosfx, 'shape': 'triangle', 'color': 'red',
                   'value': 30, 'url': '%s/run/%s/%s' % (epyk_config['URLS']['ares-report'][1:], folder, script_nosfx)})
                edgesReg.append(
                  {'from': folder, 'to': '%s_%s' % (folder, script_nosfx), 'dashes': True, 'color': 'red', })
  return regNtwrk, edgesReg