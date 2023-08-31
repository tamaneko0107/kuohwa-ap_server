from flask_restplus import Namespace, Resource, fields, model

api = Namespace("account", description=u"帳號及權限管理")


base_input_payload = api.model(u'基礎輸入參數定義', {
    'result': fields.Integer(required=True, default=0),
    'message': fields.String(required=True, default=""),
})

base_output_payload = api.clone(u'基礎輸出參數定義', base_input_payload, {
    'data': fields.String(required=True, default="")
})


account_input_payload = api.model(u'帳號input', {
    'username': fields.String(required=True, example="tami"),
    'passwd': fields.String(required=True, example="tami")
})

account_output_payload = api.clone(u'帳號output', base_output_payload, {
    # "test": fields.String(required=True)
})

add_account_input_payload = api.model(u'新增帳號input', {
    'user_id': fields.String(required=True, example="tami"),
    'role': fields.List(fields.String, required=True, example=["admin", "super_user", "general_user"]),
    'email': fields.String(required=True, example="tami@kuohwa.com")
})

add_account_output_payload = api.clone(u'新增帳號output', base_output_payload, {
    
})

get_account_list_output_payload = api.clone(u'帳號清單output', base_input_payload, {
    'data': fields.List(fields.Nested(api.model('AccountData', {
        'user_id': fields.String,
        'role': fields.List(fields.String),
        'email': fields.String,
        'update_time': fields.String
    })), required=True)
})

delete_account_list_input_payload = api.model(u'刪除帳號input', {
    'user_id': fields.String(required=True, example="tami")
})

delete_account_list_output_payload = api.clone(u'刪除帳號output', base_output_payload, {
    
})

forget_passwd_input_payload = api.clone(u'忘記密碼input', delete_account_list_input_payload, {

})

forget_passwd_output_payload = api.clone(u'忘記密碼output', base_input_payload, {
    'data': fields.String(required=True, default="密碼重設已寄送至信箱")
})

update_account_list_input_payload = api.model(u'更新帳號input', {
    'old_user_id': fields.String(required=True, example="tami"),
    'data': fields.Nested(api.model('NewAccountData', {
        'new_user_id': fields.String(required=True, example="tamu"),
        'new_role': fields.List(fields.String, required=True, example=["admin"]),
        'new_email': fields.String(required=True, example="tamu@kuohwa.com")
    }), required=True)
})

update_account_list_output_payload = api.clone(u'更新帳號output', base_output_payload, {

})


data_api = Namespace("data", description=u"資料管理")


detect_table = data_api.model('Detect_Table_Data', {
    'page_number': fields.Nested(data_api.model('PageNumber', {
        'table_id': fields.Nested(data_api.model('TableId', {
            'upper_left': fields.String(required=True, description='左上角座標', example="99,82"),
            'upper_right': fields.String(required=True, description='右上角座標', example="99,857"),
            'lower_right': fields.String(required=True, description='右下角座標', example="2356,857"),
            'lower_left': fields.String(required=True, description='左下角座標', example="2356,82"),
            'cells': fields.List(fields.Nested(data_api.model('Cell', {
                'name': fields.String(required=True, description='單元格名稱', example="cell_id1"),
                'upper_left': fields.String(required=True, description='左上角座標', example="99,82"),
                'upper_right': fields.String(required=True, description='右上角座標', example="99,857"),
                'lower_right': fields.String(required=True, description='右下角座標', example="2356,857"),
                'lower_left': fields.String(required=True, description='左下角座標', example="2356,82"),
                'start_row': fields.Integer(required=True, description='起始行', example=0),
                'end_row': fields.Integer(required=True, description='結束行', example=2),
                'start_col': fields.Integer(required=True, description='起始列', example=0),
                'end_col': fields.Integer(required=True, description='結束列', example=3),
                'content': fields.String(required=True, description='內容', example="example")
            })), required=True)
        }))
    }))
})


autosave_detect_table_input_payload = data_api.model(u'表格偵測自動儲存input', {
    'uuid': fields.String(required=True, description='UUID', example="sa5e122hy215cb3degrt"),
    'data': fields.Nested(detect_table, required=True)
})

autosave_detect_table_output_payload = data_api.clone(u'表格偵測自動儲存output', base_output_payload, {

})

get_detect_table_input_payload = data_api.model(u'表格偵測input', {
    'uuid': fields.String(required=True, description='UUID', example="sa5e122hy215cb3degrt")
})

get_detect_table_output_payload = data_api.clone(u'表格偵測output', base_input_payload, {
    'data': fields.Nested(detect_table, required=True)
})

autosave_key_value_mapping_input_payload = api.model(u'單元格偵測自動儲存input', {
    'data': fields.List(fields.Nested(api.model('Key_Value_Mapping_Data', {
        'field': fields.String(required=True, description='字段名稱', example="epr_key1"),
        'fieldvalue': fields.List(fields.String(required=True, description='字段值'), example=["Bo", "Borad"]),
        'vendor': fields.String(required=True, description='供應商'),
        'file_type': fields.String(required=True, description='文件類型')
    })), required=True)
})

autosave_key_value_mapping_output_payload = api.clone(u'單元格偵測自動儲存output', base_output_payload, {

})

get_key_value_mapping_input_payload = api.model(u'ERP Key-Value 對照表input', {
    'vendor': fields.String(required=True, description='供應商'),
    'file_type': fields.String(required=True, description='文件類型')
})

get_key_value_mapping_output_payload = api.clone(u'ERP Key-Value 對照表output', base_input_payload, {
    'data': fields.Raw(description='ERP Key-Value 對照表')
})

autosave_image_path_input_payload = api.model(u'自動儲存圖片路徑input', {
    'uuid': fields.String(required=True, description='UUID', example="sa5e122hy215cb3degrt"),
    'front_path': fields.String(required=True, description='正面圖片路徑', example="http://www.kuohwa.com.tw/xxx.jpg"),
    'back_path': fields.String(required=True, description='反面圖片路徑', example="http://www.kuohwa.com.tw/zzz.jpg")
})

autosave_image_path_output_payload = api.clone(u'自動儲存圖片路徑output', base_output_payload, {

})

get_image_path_input_payload = api.model(u'圖片路徑input', {
    'uuid': fields.String(required=True, description='UUID', example="sa5e122hy215cb3degrt")
})

get_image_path_output_payload = api.clone(u'圖片路徑output', base_input_payload, {
    'data': fields.Nested(autosave_image_path_input_payload, required=True)
})
