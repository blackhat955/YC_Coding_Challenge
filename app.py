from flask import Flask, request, jsonify
import io
import json
import traceback
from contextlib import redirect_stdout, redirect_stderr

web_application = Flask(__name__)

@web_application.route('/execute', methods=['POST'])
def execute_python_script():
    try:
        request_data = request.get_json()
        if not request_data or 'script' not in request_data:
            return jsonify({'error': 'No script provided in request body'}), 400
        
        user_script = request_data['script']
        
        if not isinstance(user_script, str):
            return jsonify({'error': 'Script must be a string'}), 400
        
        output_capture = io.StringIO()
        error_capture = io.StringIO()
        
        execution_environment = {
            '__builtins__': __builtins__,
            'os': __import__('os'),
            'pandas': None,
            'numpy': None
        }
        
        try:
            import pandas as pd
            execution_environment['pandas'] = pd
            execution_environment['pd'] = pd
        except ImportError:
            pass
            
        try:
            import numpy as np
            execution_environment['numpy'] = np
            execution_environment['np'] = np
        except ImportError:
            pass
        
        execution_result = None
        
        with redirect_stdout(output_capture), redirect_stderr(error_capture):
            try:
                compiled_script = compile(user_script, '<string>', 'exec')
                local_variables = {}
                exec(compiled_script, execution_environment, local_variables)
                
                if 'main' in local_variables and callable(local_variables['main']):
                    execution_result = local_variables['main']()
                else:
                    execution_result = None
                    
            except Exception as script_error:
                error_message = f"Execution error: {str(script_error)}"
                error_capture.write(error_message)
                error_capture.write("\n")
                error_capture.write(traceback.format_exc())
        
        captured_output = output_capture.getvalue()
        captured_errors = error_capture.getvalue()
        
        if captured_errors:
            return jsonify({
                'error': 'Script execution failed',
                'stderr': captured_errors,
                'stdout': captured_output
            }), 400
        
        api_response = {
            'result': execution_result,
            'stdout': captured_output
        }
        
        try:
            json.dumps(api_response)
        except TypeError:
            api_response['result'] = str(execution_result) if execution_result is not None else None
        
        return jsonify(api_response)
        
    except Exception as server_error:
        return jsonify({
            'error': f'Server error: {str(server_error)}',
            'traceback': traceback.format_exc()
        }), 500

@web_application.route('/health', methods=['GET'])
def check_server_health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    web_application.run(host='0.0.0.0', port=8080, debug=False)