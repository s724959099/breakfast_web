from Model.model_view import *


class SmartDB:
    def __init__(self):
        self.allSuc=True
        self.msg=None


    def commit(self,arg):
        if not self.allSuc:
            return self.allSuc,self.msg,None

        suc,msg=db_commit()
        if not suc:
            return self.allSuc, self.msg, None

        return self.allSuc, self.msg, arg


    def _do_error_thing(self):
        self.allSuc = False
        self.msg = msg
        raise Exception(msg)

    def insert_list(self,clsName,d_arg,d_arg_other={}):
        suc, msg, new_obj = dict_insert_db_list(
            clsName,
            d_arg,
            d_arg_other,
            db_flush
        )
        if not suc:
            self._do_error_thing()
        return new_obj

    def insert_single(self,clsName,d_arg,d_arg_other={}):
        suc, msg, new_obj = dict_insert_db(
            clsName,
            d_arg,
            d_arg_other,
            db_flush
        )
        if not suc:
            self._do_error_thing()
        return new_obj

    def delete_list(self,arg):
        db_delete_list(arg)
        suc,msg=db_flush()
        if not suc:
            self._do_error_thing()
    def delete_single(self,arg):
        args=[arg]
        return self.delete_list(arg)
    def update_single(self,db_obj,d_arg):
        suc, msg = dict_update_db(db_obj, d_arg, db_flush)
        if not suc:
            return self._do_error_thing()


class Maker:
    pass