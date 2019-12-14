epyk_config = None


class ConfigException(Exception):
  """Exception to be raised when the configuration is missing"""

  def __init__(self, message):
    self.message = message


def config_required(func):
  """Simple decorator to throw an error if the config is required and hasn't been setup before """
  def call_func(*args, **kwargs):
    if epyk_config is None:
      raise ConfigException('Configuration required for endpoint: %s. Set epyk_config from %s' % (func.__name__, __name__))

    return func(*args, **kwargs)
  return call_func
