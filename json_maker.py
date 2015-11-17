import json

class Json(object):

        def __init__(self, subject="", content="",  created="", last_modified=""):
                self.subject  = subject
                self.content = content
                self.created = created
                self.last_modified = last_modified
                
                self._num = 0
                self.json_dic = {}

        def _dict_to_json_str(self, dic):
                return json.dumps(dic)

        def set_variables(self, sub, cont, created, last_modified):
                self.subject = sub
                self.content = cont
                self.created = created
                self.last_modified = last_modified
        
        def make_json_str(self):
               
                self.json_dict = {}
                self.json_dict[ 'content'] = self.content
                self.json_dict[ 'last_modified'] = self.last_modified
                self.json_dict[ 'created'] = self.created
                self.json_dict[ 'subject'] = self.subject
                self._num += 1

                self.json_dic['data'+ str(self._num)] = self.json_dict

        def get_json(self):
            return self._dict_to_json_str(self.json_dic)
                
                 
                
