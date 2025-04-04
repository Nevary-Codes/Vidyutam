from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS
import os
import call

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
api = Api(app)

class Test(Resource):
    def get(self):
        return 'Welcome to, Test App API!'

    def post(self):
        try:
            value = request.get_json()
            if(value):
                return {'Post Values': value}, 201
            return {"error":"Invalid format."}
        except Exception as error:
            return {'error': str(error)}
    
class GetMonthlyPredictionOutput(Resource):
    def get(self):
        return {"error": "Invalid Method."}
    
    def post(self):
        try:
            data = request.get_json()  # Changed from get_data() to get_json()
            date1 = data.get('date1')
            date2 = data.get('date2')

            if not date1 or not date2:
                return {"error": "Missing date1 or date2 in the request."}, 400
            
            # Assuming call.get_monthly_data() returns a filename or path to the file
            monthly_excel_file = call.get_monthly_data(date1, date2)
            return {'prediction_file': monthly_excel_file}
        
        except Exception as error:
            return {"error": str(error)}, 500

api.add_resource(Test, '/')
api.add_resource(GetMonthlyPredictionOutput, '/getMonthlyPredictionOutput')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)