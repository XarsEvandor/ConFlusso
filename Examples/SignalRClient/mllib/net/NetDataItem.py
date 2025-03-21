import json

# =======================================================================================================================
class CNetDataItem(object):
  # --------------------------------------------------------------------------------------------------------
  def __init__(self, p_oJSON=None):
    #.......................... |  Instance Attributes | ............................
    #................................................................................
    
    if p_oJSON is not None:
      if isinstance(p_oJSON, dict):
        self.__dict__ = p_oJSON
      else:
        self.__dict__ = json.loads(p_oJSON)
  # --------------------------------------------------------------------------------------------------------
  def ToJSON(self):
    return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
  # --------------------------------------------------------------------------------------------------------  
# =======================================================================================================================

