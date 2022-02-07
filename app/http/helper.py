from flask import make_response

def response_error(status_code:int, message:str):
    response = make_response({
        "status": "error",
        "message": message,
    })
    response.status_code = status_code
    return response

def response_success(data):
    response_body = {
        "status": "ok"
    }
    if data: 
        response_body["data"] = data
    
    response = make_response(response_body)
    return response
   