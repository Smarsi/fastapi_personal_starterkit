import os
import datetime
from uuid import uuid4 as uuid
from fastapi import Request

# Utils Import
from app.utils.datetime_manager import get_current_datetime, get_current_datetime_for_files, get_current_datetime_for_logs

default_logs_path = "./logs"
default_logs_path = os.path.abspath(default_logs_path)

default_errors_log_path = "./logs/error_logs"
default_errors_log_path = os.path.abspath(default_errors_log_path)

def setup_file(specific_folder):
    os.makedirs(specific_folder, exist_ok=True)

def log_builder(request: Request):
    request_id = request.state.uuid
    specific_folder = default_logs_path
    setup_file(specific_folder)    
    datetime_info = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    user_id_on_create = 0
    log_file = os.path.join(specific_folder+f"{datetime_info}"+f"-{user_id_on_create}-"+f"{request_id}.log")
    return log_file

def log_rename(log_file, id_account):
    setup_file = log_file.split("-")
    setup_file[2] = id_account
    new_name = setup_file[0]
    for i in setup_file[1:]:
        new_name = new_name + f"-{str(i)}"
    os.rename(log_file, new_name) 
    return new_name

def log_writer(log_file, log_content):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a") as file:
        file.write(f"\n{timestamp}; DEBUG; {log_content};")
    file.close()

def errors_log_generator(traceback):
    id = uuid()
    specific_folder = default_errors_log_path
    setup_file(specific_folder)
    log_file = os.path.join(specific_folder + f"{id}.log")

    with open(log_file, "w") as writer:
        writer.write(traceback)
    return log_file

# =========== AS CLASS ================
class Logger:
    def __init__(self, log_file: str=None, file_id: str = None):
        self.setup_folders()

        if not file_id:
            file_id = str(uuid()).replace("-", "")

        if not log_file:
            filepath = f"{default_logs_path}/{get_current_datetime_for_files()}-{file_id}.log"
            self.filepath = filepath
            return
        self.filepath = log_file

    def write(self, log_content: str, log_type: str = "DEBUG"):
        with open(self.filepath, "a+") as log_file:
            log_file.write(f"{get_current_datetime_for_logs()}; {log_type}; {log_content}\n")
            
    def setup_folders(self) -> None:
        os.makedirs(default_logs_path, exist_ok=True)

    def get_filepath(self) -> str:
        return self.filepath
    
    def generate_error_log(self, traceback: str):
            id = uuid()
            os.makedirs(default_errors_log_path, exist_ok=True)
            log_file = os.path.join(default_errors_log_path + f"/{id}.log")

            with open(log_file, "w") as error_file:
                error_file.write(traceback)

            self.write(f"Error - Traceback file: {log_file}")
    