import requests
import threading
import numpy as np
from datetime import datetime
import csv
import pandas as pd

def zipf_mandelbrot(N, q, s):
    ranks = np.arange(1, N + 1)
    weights = (ranks + q) ** -s
    probabilities = weights / weights.sum()
    return probabilities

def log_to_csv(data, filename='request_log.csv'):
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)

def make_request(url):
    try:
        start_time = datetime.now()
        response = requests.get(url)
        end_time = datetime.now()
        rtt = (end_time - start_time).total_seconds()  
        log_data = [url, start_time, end_time, rtt, response.status_code]
        print(f"Request to {url} completed with status code: {response.status_code}, RTT: {rtt:.6f} seconds")
    except requests.exceptions.RequestException as e:
        end_time = datetime.now()
        rtt = (end_time - start_time).total_seconds() 
        log_data = [url, start_time, end_time, rtt, f"Failed: {e}"]
        print(f"Request to {url} failed: {e}, RTT: {rtt:.6f} seconds")
    
    log_to_csv(log_data)

def generate_traffic(urls, num_requests, interval, zipf_params):
    probabilities = zipf_mandelbrot(len(urls), *zipf_params)
    threads = []
    
    for _ in range(num_requests):
        url = np.random.choice(urls, p=probabilities)
        thread = threading.Thread(target=make_request, args=(url,))
        thread.start()
        threads.append(thread)
    
    for thread in threads:
        thread.join()
    
    print("Traffic generation completed.")

df = pd.read_csv('url_bineca_https.csv')
urls = df['URL'].tolist()  

with open('request_log.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["URL", "Start Time", "End Time", "RTT (seconds)", "Status Code"])

number_of_requests = 1000
time_interval = 0.1  
zipf_params = (2, 1.5) 

generate_traffic(urls, number_of_requests, time_interval, zipf_params)

