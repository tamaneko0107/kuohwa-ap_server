from apis.account.model import *
from apis.account.module import *
from apis.account.schema import *
from flask import session
from base_api import CustomResource, Check
from werkzeug.exceptions import HTTPException
from http import HTTPStatus
from base_api.custom_cls import errors_abort

@data_api.errorhandler(Exception)
def handle_error(e):
    code = 500
    message = "500 Internal Server Error"
    description = str(e).split(":")[1]
    if isinstance(e, HTTPException):
        code = e.code
        message = str(e).split(":")[0]
        description = e.description
    return {"result": 1, "message": f'{message}:{description}'}, code

@data_api.route("/autosave_detect_table")
class AutosaveDetectTable(CustomResource):
    @data_api.expect(autosave_detect_table_input_payload)
    @data_api.marshal_with(autosave_detect_table_output_payload)
    def post(self):
        data = api.payload
        Check.validate_data(AutosaveDetectTableSchema, data)
        return Data.autosave_detect_table(data["uuid"], data["data"])
    
@data_api.route("/get_detect_table")
class GetDetectTable(CustomResource):
    @data_api.expect(get_detect_table_input_payload)
    @data_api.marshal_with(get_detect_table_output_payload)
    def post(self):
        data = api.payload
        return Data.get_detect_table(data["uuid"])
    
    
@data_api.route("/autosave_key_value_mapping")
class AutosaveKeyValueMapping(CustomResource):
    @data_api.expect(autosave_key_value_mapping_input_payload)
    @data_api.marshal_with(autosave_key_value_mapping_output_payload)
    def post(self):
        data = api.payload
        Check.validate_data(AutosaveKeyValueMappingSchema, data)
        return Data.autosave_key_value_mapping(data["data"])
    
@data_api.route("/get_key_value_mapping")
class GetKeyValueMapping(CustomResource):
    @data_api.expect(get_key_value_mapping_input_payload)
    @data_api.marshal_with(get_key_value_mapping_output_payload, skip_none=True)
    def post(self):
        data = api.payload
        return Data.get_key_value_mapping(data["vendor"], data["file_type"])
    
@data_api.route("/autosave_image_path")
class AutosaveImagePath(CustomResource):
    @data_api.expect(autosave_image_path_input_payload)
    @data_api.marshal_with(autosave_image_path_output_payload)
    def post(self):
        data = api.payload
        Check.validate_data(AutosaveImagePathSchema, data)
        return Data.autosave_image_path(data["uuid"], data["front_path"], data["back_path"])
    
@data_api.route("/get_image_path")
class GetImagePath(CustomResource):
    @data_api.expect(get_image_path_input_payload)
    @data_api.marshal_with(get_image_path_output_payload)
    def post(self):
        data = api.payload
        return Data.get_image_path(data["uuid"])