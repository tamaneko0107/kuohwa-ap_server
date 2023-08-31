import json
from utils.orcl_utils import OracleAccess
from http import HTTPStatus
from base_api.custom_cls import errors_abort

class Account(object):
    @staticmethod
    def login(username, passwd):
        # TODO
        raw = OracleAccess.data_exists('users')
        if not raw:
            errors_abort(HTTPStatus.BAD_REQUEST, "400 BAD REQUEST:資料不存在", result=1)
        return {
            "data": "登入成功",
            "users": raw
        }
    
    @staticmethod
    def add_account_list(user_id, role, email):
        if OracleAccess.data_exists('users') == False: 
            OracleAccess.create_table('users', ['user_id varchar2(50)', 
                                               'role varchar2(50)', 
                                               'email varchar2(100)',
                                               'update_time date'])
        if OracleAccess.data_exists('users', 'user_id', [user_id])[0]:
            # return {
            #     "data": "用戶ID已存在"
            # }
            errors_abort(HTTPStatus.BAD_REQUEST, "400 BAD REQUEST:用戶ID已存在", result=1)

        sql = "INSERT INTO users (user_id, role, email) VALUES (:1, :2, :3)"
        OracleAccess.insert(sql, [(user_id, ','.join(role), email)])
        return {
            "data": "新增成功"
        }
    
    @staticmethod
    def get_account_list():
        result = OracleAccess.data_exists('users')
        if not result[0]:
            # return {
            #     "data": "null"
            # }
            errors_abort(HTTPStatus.BAD_REQUEST, "400 BAD REQUEST:資料不存在", result=1)
        for i in result[1]:
            i['role'] = i['role'].split(',')
        return {
            "data": result[1]
        }
    
    @staticmethod
    def delete_account_list(user_id):
        if not OracleAccess.data_exists('users', 'user_id', [user_id])[0]: 
            # return {
            #     "data": "用戶ID不存在"
            # }
            errors_abort(HTTPStatus.BAD_REQUEST, "400 BAD REQUEST:用戶ID不存在", result=1)
        sql = "DELETE FROM users WHERE user_id = :1"
        OracleAccess.execute(sql, [user_id])
        return {
            "data": "刪除成功"
        }
    
    @staticmethod
    def forget_passwd(user_id):
        if not OracleAccess.data_exists('users', 'user_id', [user_id])[0]: 
            # return {
            #     "data": "用戶ID不存在"
            # }
            errors_abort(HTTPStatus.BAD_REQUEST, "400 BAD REQUEST:用戶ID不存在", result=1)
        # sql = "UPDATE users SET 上次登入時間 = SYSDATE WHERE 帳號 = :1"
        # OracleAccess.execute(sql, [user_id])
        # return {
        #     "data": "更新成功"
        # }

    @staticmethod
    def update_account_list(old_user_id, data):
        if not OracleAccess.data_exists('users', 'user_id', [old_user_id])[0]:
            # return {
            #     "data": "用戶ID不存在"
            # }
            errors_abort(HTTPStatus.BAD_REQUEST, "400 BAD REQUEST:用戶ID不存在", result=1)
        if OracleAccess.data_exists('users', 'user_id', [data["new_user_id"]])[0]:
            # return {
            #     "data": "新用戶ID已存在"
            # }
            errors_abort(HTTPStatus.BAD_REQUEST, "400 BAD REQUEST:新用戶ID已存在", result=1)
        sql = "UPDATE users SET user_id = :1, role = :2, email = :3 WHERE user_id = :4"
        OracleAccess.execute(sql, [data["new_user_id"], ','.join(data["new_role"]), data["new_email"], old_user_id])
        return {
            "data": "更新成功"
        }


class Data(object):
    @staticmethod
    def autosave_detect_table(uuid, data):
        if OracleAccess.data_exists('detect_table') == False:
            OracleAccess.create_table('detect_table', ['uuid varchar2(50)', 
                                                       'upper_left varchar2(50)',
                                                       'upper_right varchar2(50)',
                                                       'lower_right varchar2(50)',
                                                       'lower_left varchar2(50)',
                                                       'cells NUMBER(5)'])
        if OracleAccess.data_exists('detect_table', 'uuid', [uuid])[0]:
            # return {
            #     "data": "uuid已存在"
            # }
            errors_abort(HTTPStatus.BAD_REQUEST, "400 BAD REQUEST:uuid已存在", result=1)
        if OracleAccess.data_exists('detect_table_cells') == False:
            OracleAccess.create_table('detect_table_cells', ['uuid varchar2(50)', 
                                                             'name varchar2(50)',
                                                             'upper_left varchar2(50)',
                                                             'upper_right varchar2(50)',
                                                             'lower_right varchar2(50)',
                                                             'lower_left varchar2(50)',
                                                             'start_row NUMBER(5)',
                                                             'end_row NUMBER(5)',
                                                             'start_col NUMBER(5)',
                                                             'end_col NUMBER(5)',
                                                             'content varchar2(200)'])
        store_data = {'uuid': uuid}
        store_data_cells = []
        for cell in data['page_number']['table_id']['cells']:
            temp = store_data.copy()
            temp.update(cell)
            store_data_cells.append(temp)
        store_data.update(data['page_number']['table_id'])
        store_data['cells'] = len(store_data['cells'])
        sql = "INSERT INTO detect_table (uuid, upper_left, upper_right, lower_right, lower_left, cells)\
                                VALUES (:uuid, :upper_left, :upper_right, :lower_right, :lower_left, :cells)"
        OracleAccess.insert(sql, [store_data])
        sql = 'INSERT INTO detect_table_cells (uuid, name, upper_left, upper_right, lower_right, lower_left, start_row, end_row, start_col, end_col, content)\
                                VALUES (:uuid, :name, :upper_left, :upper_right, :lower_right, :lower_left, :start_row, :end_row, :start_col, :end_col, :content)'
        OracleAccess.insert(sql, store_data_cells)
        return {
            "data": "新增成功"
        }
    
    @staticmethod
    def get_detect_table(uuid):
        result = OracleAccess.data_exists('detect_table', 'uuid', [uuid])
        if not result[0]:
            # return {
            #     "data": "uuid不存在"
            # }
            errors_abort(HTTPStatus.BAD_REQUEST, "400 BAD REQUEST:uuid不存在", result=1)
        result_cells = OracleAccess.data_exists('detect_table_cells', 'uuid', [uuid])
        if len(result_cells[0]) != result[0][0][5]:
            # return {
            #     "data": "cell數量不符"
            # }
            errors_abort(HTTPStatus.BAD_REQUEST, "400 BAD REQUEST:cell數量不符", result=1)
        # 刪除uuid key值
        for i in result_cells[1]:
            i.pop('uuid')
        result[1][0].pop('uuid')
        result[1][0]['cells'] = result_cells[1]
        json_data = {
            'data': {
                'page_number': {
                    'table_id': result[1]
                }
            }
        }
        return json_data

    @staticmethod
    def autosave_key_value_mapping(data):
        if OracleAccess.data_exists('key_value_mapping') == False:
            OracleAccess.create_table('key_value_mapping', ['field varchar2(50)',
                                                            'fieldvalue varchar2(200)',
                                                            'vendor varchar2(50)',
                                                            'file_type varchar2(50)'])
        store_data = []
        for row in data:
            store_data.append((row['field'], ','.join(row['fieldvalue']), row['vendor'], row['file_type']))
            # 如果有重複的field，就刪除舊的
            if OracleAccess.data_exists('key_value_mapping', 'field', [row['field']]):
                sql = "DELETE FROM key_value_mapping WHERE field = :1"
                OracleAccess.execute(sql, [row['field']])
        sql = "INSERT INTO key_value_mapping (field, fieldvalue, vendor, file_type)\
                                    VALUES (:1, :2, :3, :4)"
        OracleAccess.insert(sql, store_data)
        return {
            "data": "新增成功"
        }
    
    @staticmethod
    def get_key_value_mapping(vendor, file_type):
        sql = "SELECT * FROM key_value_mapping WHERE vendor = :1 AND file_type = :2"
        result = OracleAccess.query(sql, [vendor, file_type])
        if not result[0]:
            # return {
            #     "data": "資料不存在"
            # }
            errors_abort(HTTPStatus.BAD_REQUEST, "400 BAD REQUEST:資料不存在", result=1)
        print(result)
        json_data = {}
        json_data['data'] = {}
        for row in result[0]:
            json_data['data'][row[0]] = row[1].split(',')
        return json_data
    
    @staticmethod
    def autosave_image_path(uuid, front_path, back_path):
        if OracleAccess.data_exists('image_path') == False:
            OracleAccess.create_table('image_path', ['uuid varchar2(50)',
                                                     'front_path varchar2(200)',
                                                     'back_path varchar2(200)'])
        if OracleAccess.data_exists('image_path', 'uuid', [uuid]):
            # return {
            #     "data": "uuid已存在"
            # }
            # 刪除舊的uuid
            sql = "DELETE FROM image_path WHERE uuid = :1"
            OracleAccess.execute(sql, [uuid])
        sql = "INSERT INTO image_path (uuid, front_path, back_path)\
                                VALUES (:1, :2, :3)"
        OracleAccess.insert(sql, [(uuid, front_path, back_path)])
        return {
            "data": "新增成功"
        }
    
    @staticmethod
    def get_image_path(uuid):
        result = OracleAccess.data_exists('image_path', 'uuid', [uuid])
        if not result[0]:
            # return {
            #     "data": "uuid不存在"
            # }
            errors_abort(HTTPStatus.BAD_REQUEST, "400 BAD REQUEST:uuid不存在", result=1)
        json_data = {
            'data': result[1][0]
        }
        return json_data

