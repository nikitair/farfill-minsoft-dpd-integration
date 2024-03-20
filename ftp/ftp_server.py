import os
import paramiko
import functools
from dotenv import load_dotenv

from logs.logging_config import logger


load_dotenv()


PORT = os.getenv("PORT")
HOST = os.getenv("HOST")

S_USERNAME = os.getenv("S_USERNAME")
S_PASSWORD = os.getenv("S_PASSWORD")

O_USERNAME = os.getenv("O_USERNAME")
O_PASSWORD = os.getenv("O_PASSWORD")


def set_up_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(hostname=kwargs.get("hostname"), port=kwargs.get("port"), 
                               username=kwargs.get("username"), password=kwargs.get("password"))
            logger.info("Connected Successfully!")
            kwargs["ssh_client"] = ssh_client
            result = func(*args, **kwargs)
            return result
        except paramiko.SSHException as e:
            logger.info(f"Connection failed: {e}")
        finally:
            if "ssh_client" in kwargs:
                kwargs["ssh_client"].close()
                logger.info("Connection closed!")
    return wrapper


@set_up_connection
def get_dir_list(hostname, port, username, password, ssh_client):
        ftp = ssh_client.open_sftp()
        files = ftp.listdir()
        logger.info(f"Listing all the files and Directory: {files}")


#Get Purchase Orders from ASDA
#Filename: Should start with your 6 digit vendor number followed by ‘-YYYYMMDDHHMM’
#(Example – 012345-202201011300)
# @set_up_connection
# def get_purchase_orders(hostname, port, username, password, ssh_client):
#     ftp = ssh_client.open_sftp()
#     ftp.chdir("NewOrders")
#     logger.info(f"Current Directory: {directory_name}")
#     files = ftp.listdir()
#     logger.info(f"Listing all the files and Directory: {files}")
#     if files:
#         for file in files:
#             remote_path = os.path.join("NewOrders", file)
#             local_path = os.path.join("LocalNewOrders", file)
#             sftp_client.get(remote_path, local_path)
#     else:
#         logger.info(f"Directory: {directory_name} is empty")


#Filename:
#Should start with DSV followed by your 6 digit vendor number followed by ‘-Acknowledged’
#Example – DSV012345-Acknowledged.csv
def create_confirmation_file(input_file, output_file):
    with open(input_file, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        purchase_orders = [row["Purchase Order No"] for row in reader]

    with open(output_file, 'w', newline='') as csv_output:
        writer = csv.writer(csv_output)
        writer.writerow(["Purchase Order", "Status Action"])
        
        for order_number in purchase_orders:
            writer.writerow([order_number, "acknowledged"])


#Send Acknowledgement Confirmation to ASDA
#Expectation of acknowledgement within 4hrs of transmission from ASDA
@set_up_connection
def send_acknowledgement_confirmation(purchase_order, file_name):
    create_confirmation_file(purchase_order, file_name)
    ftp = ssh_client.open_sftp()
    remote_path = os.path.join("SFTP", "Upload", file_name)
    local_path = os.path.join("SFTP", "Upload", file_name)
    sftp_client.put(remote_path, local_path)


#Filename:
#Should start with DSV followed by your 6 digit vendor number followed by ‘-Shipped’
#Example – DSV012345-Shipped
def create_dispatch_confirmation_file():
    field_names = ["Purchase Order", "Status Action",
                    "Purchase Order Line Number", "Item ID",
                    "Quantity", "Tracking Reference"]
    data = [
        {"Purchase Order": "Y255974178", "Status Action": "shipped",
        "Purchase Order Line Number": "1", "Item ID": "051051849",
        "Quantity": "1", "Tracking Reference": "0663086534109214"}
    ]
    csv_file_path = "purchase_order_sample.csv"

    with open(csv_file_path, mode="w", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=field_names)
        writer.writeheader()
        for row in data:
            writer.writerow(row)


#Send Dispatch Confirmation to ASDA
@set_up_connection
def send_dispatch_confirmation(): pass
    create_acknowledgement_confirmation_file(purchase_order, file_name)
    ftp = ssh_client.open_sftp()
    remote_path = os.path.join("SFTP", "Upload", file_name)
    local_path = os.path.join("SFTP", "Upload", file_name)
    sftp_client.put(remote_path, local_path)


#Send Cancellation Confirmation to ASDA
@set_up_connection
def send_cancel_confirmation(): pass
    create_confirmation_file(purchase_order, file_name)
    ftp = ssh_client.open_sftp()
    remote_path = os.path.join("SFTP", "Upload", file_name)
    local_path = os.path.join("SFTP", "Upload", file_name)
    sftp_client.put(remote_path, local_path)
# Should start with your 6 digit vendor number followed by ‘_STK_AM_YYYYMMDD_000001’
# Example - 012345_STK_AM_20220101_000001
def create_inventory_report(file_name, data):
    with open(filename, 'w') as file:
        header = "HDR|YYYYMMDDHHMMSS-0000|manual_feed\n"
        file.write(header)
        
        for item in data:
            item_line = f"BEG|{item['Itemnumber']}|{item['StockLevel']}|0\n"
            file.write(item_line)
        
        # Write footer
        footer = f"TRL|manual_feed|{len(data)}\n"
        file.write(footer)

#A Minimum of once every 24hrs – ideally the initial inventory
#of the day should be received prior to 8am (GMT/BST).
#Inventory files need to be dropped into the root of the SFTP (NOT into any folder)
@set_up_connection
def send_inventory_report():
    create_inventory_file(purchase_order, file_name)
    ftp = ssh_client.open_sftp()
    remote_path = os.path.join("SFTP", file_name)
    local_path = os.path.join("SFTP", file_name)
    sftp_client.put(remote_path, local_path)

if __name__ == "__main__":
    # establish_connection(hostname=HOST, port=PORT, username=O_USERNAME, password=O_PASSWORD)
    get_dir_list(hostname=HOST, port=PORT, username=O_USERNAME, password=O_PASSWORD)