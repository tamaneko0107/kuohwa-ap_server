from apis.account.model import *
from apis.account.module import *
from apis.account.schema import *
from flask import session
from base_api import CustomResource, Check
from werkzeug.exceptions import HTTPException
from http import HTTPStatus
from base_api.custom_cls import errors_abort

ROLE_ADMIN = "Admin"

@api.errorhandler(Exception)
def handle_error(e):
    code = 500
    message = "500 Internal Server Error"
    description = str(e).split(":")[1]
    if isinstance(e, HTTPException):
        code = e.code
        message = str(e).split(":")[0]
        description = e.description
    return {"result": 1, "message": f'{message}:{description}'}, code


@api.route("/test")
class Login2(CustomResource):
    allow_roles = [ROLE_ADMIN]
    def post(self):
        print(api.payload)
        return "OK"


@api.route("/login")
class Login(CustomResource):
    @api.expect(account_input_payload)
    @api.marshal_with(account_output_payload)
    def post(self):
        # try:
        session["roles"] = [ROLE_ADMIN]
        data = api.payload
        return Account.login(username=data["username"], passwd=data["passwd"])
    

@api.route("/add_account_list")
class AddAccountList(CustomResource):
    @api.expect(add_account_input_payload)
    @api.marshal_with(add_account_output_payload)
    def post(self):
        data = api.payload
        Check.validate_data(AddAccountListSchema, data)
        return Account.add_account_list(data["user_id"], data["role"], data["email"])
    
@api.route("/get_account_list")
class GetAccountList(CustomResource):
    @api.marshal_with(get_account_list_output_payload)
    def get(self):
        return Account.get_account_list()
    
@api.route("/delete_account_list")
class DeleteAccountList(CustomResource):
    @api.expect(delete_account_list_input_payload)
    @api.marshal_with(delete_account_list_output_payload)
    def post(self):
        data = api.payload
        return Account.delete_account_list(data["user_id"])

@api.route("/forget")
class Forget(CustomResource):
    @api.expect(forget_passwd_input_payload)
    @api.marshal_with(forget_passwd_output_payload)
    def post(self):
        data = api.payload
        return Account.forget_passwd(data["user_id"])
    
@api.route("/update_account_list")
class UpdateAccountList(CustomResource):
    @api.expect(update_account_list_input_payload)
    @api.marshal_with(update_account_list_output_payload)
    def post(self):
        data = api.payload
        Check.validate_data(NewAccountListSchema, data)
        return Account.update_account_list(data["old_user_id"], data["data"])
