import requests
import threading
import numpy as np
from datetime import datetime
import csv
import pandas as pd
import argparse
import time

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

def generate_traffic(urls, num_requests, requests_per_second, zipf_params):
    probabilities = zipf_mandelbrot(len(urls), *zipf_params)
    threads = []
    interval = 1 / requests_per_second
    
    for _ in range(num_requests):
        url = np.random.choice(urls, p=probabilities)
        thread = threading.Thread(target=make_request, args=(url,))
        thread.start()
        threads.append(thread)
        time.sleep(interval)
    
    for thread in threads:
        thread.join()
    
    print("Traffic generation completed.")

def main():
    parser = argparse.ArgumentParser(description='Generate traffic for URLs with Zipf distribution.')
    parser.add_argument('-url', type=int, required=True, help='Number of URLs')
    parser.add_argument('-req', type=int, required=True, help='Number of requests')
    parser.add_argument('-rps', type=float, required=True, help='Requests per second')
    parser.add_argument('-zipf', type=float, nargs=2, required=True, help='Zipf parameters: q and s')

    args = parser.parse_args()

    number_of_requests = args.req
    requests_per_second = args.rps
    zipf_params = tuple(args.zipf)

    # Load URLs from CSV
    df = pd.read_csv('url_bineca_https.csv')
    urls = df['URL'].tolist()

    # Initialize the CSV file
    with open('request_log.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["URL", "Start Time", "End Time", "RTT (seconds)", "Status Code"])

    generate_traffic(urls, number_of_requests, requests_per_second, zipf_params)

if __name__ == "__main__":
    main()
