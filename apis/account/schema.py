AddAccountListSchema = {
    "type": "object",
    "properties": {
        "user_id": {
            "type": "string",
            "minLength": 1
        },
        "role": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "string",
                "minLength": 1,
                "enum": ["admin", "super_user", "general_user"]
            }
        },
        "email": {
            "type": "string",
            "format": "email"
        }
    },
    "required": ["user_id", "role", "email"]
}

NewAccountListSchema = {
    "type": "object",
    "properties": {
        "old_user_id": {
            "type": "string",
            "minLength": 1
        },
        "data": {
            "type": "object",
            "properties": {
                "new_user_id": {
                    "type": "string",
                    "minLength": 1
                },
                "new_role": {
                    "type": "array",
                    "minItems": 1,
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "enum": ["admin", "super_user", "general_user"]
                    }
                },
                "new_email": {
                    "type": "string",
                    "format": "email"
                }
            },
            "required": ["new_user_id", "new_role", "new_email"]
        }              
    },
    "required": ["old_user_id", "data"]
}


AutosaveDetectTableSchema = {
    "type": "object",
    "properties": {
        "uuid": {
            "type": "string",
            "minLength": 1
        },
        "data": {
            "type": "object",
            "properties": {
                "page_number": {
                    "type": "object",
                    "properties": {
                        "table_id": {
                            "type": "object",
                            "properties": {
                                "upper_left": {"type": "string"},
                                "upper_right": {"type": "string"},
                                "lower_right": {"type": "string"},
                                "lower_left": {"type": "string"},
                                "cells": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "name": {"type": "string"},
                                            "upper_left": {"type": "string"},
                                            "upper_right": {"type": "string"},
                                            "lower_right": {"type": "string"},
                                            "lower_left": {"type": "string"},
                                            "start_row": {"type":"integer"},
                                            "end_row":{"type":"integer"},
                                            "start_col":{"type":"integer"},
                                            "end_col":{"type":"integer"},
                                            'content':{"type":"string"}
                                        },
                                        'required':["name","upper_left","upper_right","lower_right","lower_left","start_row","end_row","start_col","end_col","content"]
                                    }
                                }
                            },
                            'required':["upper_left","upper_right","lower_right","lower_left","cells"]
                        }
                    },
                    'required':["table_id"]
                }
            },
            'required':["page_number"]
        }
    },
    'required':["uuid","data"]
}

AutosaveKeyValueMappingSchema = {
    "type": "object",
    "properties": {
        "data": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "field": {"type": "string"},
                    "fieldvalue": {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "vendor": {"type": "string"},
                    "file_type": {"type": "string"}
                },
                'required':["field","fieldvalue","vendor","file_type"]
            }
        }
    },
    'required':["data"]
}

AutosaveImagePathSchema = {
    "type": "object",
    "properties": {
        "uuid": {
            "type": "string",
            "minLength": 1
        },
        "front_path": {
            "type": "string",
            "minLength": 1
            # "pattern": "https://.*"
        },
        "back_path": {
            "type": "string",
            "minLength": 1
            # "pattern": "https://.*"
        }
    },
    "required": ["uuid", "front_path", "back_path"]
}
