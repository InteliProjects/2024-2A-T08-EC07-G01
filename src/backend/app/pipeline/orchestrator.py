import gridfs
from pymongo import MongoClient
import importlib.util
import os
import tempfile
import datetime
import json
import pandas as pd

class Orchestrator:
    def __init__(self, pipeline_steps, dataframes, mongo_uri, db_name):
        self.pipeline_steps = pipeline_steps
        self.dataframes = dataframes  # Dictionary to store DataFrames
        self.logs = []
        self.client = MongoClient(mongo_uri)
        self.db = self.client[db_name]
        self.fs = gridfs.GridFS(self.db)

    def log(self, message, error=False):
        log_type = "ERROR" if error else "INFO"
        self.logs.append(f"[{log_type}] {message}")
        if error:
            self.save_logs()

    def fetch_script_from_gridfs(self, file_path):
        try:
            with open(file_path, "rb") as grid_out:
                script_content = grid_out.read()
            self.log(f"Script '{file_path}' successfully fetched.")
            return script_content
        except Exception as e:
            self.log(f"Error fetching script from GridFS: {e}", error=True)
            raise

    def load_module_from_file(self, module_name, script_content):
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".py")
        temp_file.write(script_content)
        temp_file.close()

        try:
            spec = importlib.util.spec_from_file_location(module_name, temp_file.name)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            self.log(f"Module '{module_name}' successfully loaded from {temp_file.name}.")
            return module
        except Exception as e:
            self.log(f"Error loading module '{module_name}' from file: {e}", error=True)
            raise
        finally:
            os.remove(temp_file.name)

    def execute_step(self, step_name, module, **kwargs):
        try:
            func_name = "execute"
            func = getattr(module, func_name)
            self.log(f"Executing '{step_name}'...")
            result = func(**kwargs)  # Pass any needed arguments
            self.log(f"'{step_name}' completed successfully.")
            return result
        except AttributeError as e:
            self.log(f"Function '{func_name}' not found in module '{module.__name__}': {e}", error=True)
            raise
        except Exception as e:
            self.log(f"Error during '{step_name}': {e}", error=True)
            raise

    def run_dynamic_pipeline(self):
        model_metadata = None
        for step in self.pipeline_steps:
            module_name = step["name"]
            file_path = step["file_path"]
            kwargs = step.get("kwargs", {}).copy()

            print(f"[DEBUG] Available DataFrames before '{step['name']}': {list(self.dataframes.keys())}")

            dataframes_needed = step.get("dataframes", [])
            for df_name in dataframes_needed:
                if df_name in self.dataframes:
                    kwargs[df_name] = self.dataframes[df_name]
                else:
                    print(f"[ERROR] DataFrame '{df_name}' not found for step '{module_name}'.")
                    raise ValueError(f"DataFrame '{df_name}' not found for step '{module_name}'.")

            script_content = self.fetch_script_from_gridfs(file_path)
            module = self.load_module_from_file(module_name, script_content)

            # Execute the function and get the result
            result = self.execute_step(step["name"], module, **kwargs)

            output_df_name = step.get("output_dataframe")
            if output_df_name:
                self.dataframes[output_df_name] = result

            print(f"[DEBUG] Step '{module_name}' executed successfully. Output DataFrame: {output_df_name}")


            # Capture model metadata if the step is 'treina_modelo'
            if module_name == "treina_modelo":
                model_metadata = result
                print(model_metadata)

        print("[INFO] Pipeline completed successfully.")
        return model_metadata

    def save_logs(self):
        logs_dir = os.path.join(os.getcwd(), 'app', 'pipeline', 'logs')
        os.makedirs(logs_dir, exist_ok=True)

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_file_path = os.path.join(logs_dir, f"logs_{timestamp}.txt")
        
        with open(log_file_path, "a") as f:
            for log in self.logs:
                f.write(log + "\n")

        self.db.logs.insert_one({"timestamp": timestamp, "logs": self.logs})
        self.logs.clear()
