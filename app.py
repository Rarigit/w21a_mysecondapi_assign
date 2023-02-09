from flask import Flask, request
from dbhelpers import run_statement
from validhelpers import check_data
import json

app = Flask(__name__)

@app.get('/hello')
def get_hello():
    return "Hello World"

# Included Bonus part in this GET request so now it needs a limit parameter to get the required data also descended by quantity order

@app.get('/api/item')
def get_item():
    limit = request.args.get('limit')
    result = run_statement("CALL get_item_infoall(?)", [limit])
    if (type(result) == list):
        result_json = json.dumps(result, default=str)
        return result_json
    else:
        return "Sorry, something went wrong"


@app.post('/api/item')
def post_item():
    required_data = ['name', 'description', 'quantity', 'createdAt']
    check_result = check_data(request.json, required_data)
    if check_result != None:
        return check_result
    name = request.json.get('name')
    description = request.json.get('description')
    quantity = request.json.get('quantity')
    created_at = request.json.get('createdAt')
    result = run_statement("CALL insert_item(?,?,?,?)", [name, description, quantity, created_at])
    if result == None:
        return "Item created and stored in DB!"
        # return json.dumps(result[0][0], default=str) 
# Kept getting an error on Postman even though it was inserting into DB so i just 
# set the if clause to result = None as is the case for post apis. Dont really need json.dumps. Postman returning correct message
    else:
        return "Sorry, something went wrong"


# Completed Bonus patch operation now my request can update name and description as well

@app.patch('/api/item')
def patch_item():
    required_data = ['id', 'quantity']
    check_result = check_data(request.json, required_data)
    if check_result != None:
        return check_result
    name = request.json.get('name')
    description = request.json.get('description')
    id = request.json.get('id')
    quantity = request.json.get('quantity')
    result = run_statement("CALL update_item_idquant_arg(?,?,?,?)", [id, quantity, name, description])
    if result == None:
        return "Item updated successfully"
    else:
        return "Sorry, something went wrong"


@app.delete('/api/item')
def delete_item():
    check_result = check_data(request.json, ['id'])
    if check_result != None:
        return check_result
    id = request.json.get('id')
    result = run_statement("CALL del_item_arg_id(?)", [id])
    if result == None:
# DB row deleted and correct message printed on postman. 
        return "Successfully deleted item {}".format(id)
    else:
        return "Item {} does not exist".format(id)

# //Employee API's
# Finally got it, you have to use request.args before the result statement in the guard clause. Then after the run_statement function executes then you can use json.dumps

@app.get('/api/employee')
def get_employee():
    id = request.args.get('id')
    print(id)
    result = run_statement("CALL get_employee_arg_id(?)", [id])
    if (type(result) == list):
        result_json = json.dumps(result, default=str)
        print(result_json)
        return result_json
    else:
        return "Sorry, something went wrong"


@app.post('/api/employee')
def post_employee():
    required_data = ['name', 'hourlyWage']
    check_result = check_data(request.json, required_data)
    if check_result != None:
        return check_result
    
    name = request.json.get('name')
    hourly_wage = request.json.get('hourlyWage')
    result = run_statement("CALL insert_employee_arg_namhw(?,?)", [name, hourly_wage])
    if result == None:
        return "Employee added successfully"
    else:
        return "Sorry, something went wrong"


@app.patch('/api/employee')
def patch_employee():
    required_data = ['id', 'hourlyWage']
    check_result = check_data(request.json, required_data)
    if check_result != None:
        return check_result
    id = request.json.get('id')
    hourly_wage = request.json.get('hourlyWage')
    result = run_statement("CALL update_employee_hw(?,?)", [id, hourly_wage])
    if result == None:
        return "Employee info updated successfully"
    else:
        return "Sorry, something went wrong"


@app.delete('/api/employee')
def delete_employee():
    check_result = check_data(request.json, ['id'])
    if check_result != None:
        return check_result
    id = request.json.get('id')
    result = run_statement("CALL del_employee_arg_id(?)", [id])
    if result == None:
        return "Successfully deleted Employee {}".format(id)
    else:
        return "Employee {} does not exist".format(id)
    


app.run(debug = True)