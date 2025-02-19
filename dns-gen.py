import csv
import subprocess
from concurrent.futures import ThreadPoolExecutor

def load_csv(file_path):
    domains = set()
    with open(file_path, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) > 1:
                domains.add(row[1].strip())
    return list(domains)

def perform_dns_query(domain):
    try:
        subprocess.run(["dig", domain, "+short"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"DNS query error for {domain}: {e}")


def main():
    domain_list = load_csv("top-1m.csv")
    TOTAL_ENTRIES = 10000  
    NUM_THREADS = 20

    def query_batch(start_index, step):
        while True:  
            for i in range(start_index, TOTAL_ENTRIES, step):
                domain = domain_list[i % len(domain_list)]
                print (f"Domain: {domain}")
                perform_dns_query(domain)

    
    with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
        for t in range(NUM_THREADS):
            executor.submit(query_batch, t, NUM_THREADS)

if __name__ == "__main__":
    main()
