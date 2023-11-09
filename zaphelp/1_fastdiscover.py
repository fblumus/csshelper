import time
from zapv2 import ZAPv2


# API key for ZAP instance
apikey = "crbrnoifkcppdm27gncvh7atvs"

# ZAP Proxy Configuration
zap = ZAPv2(apikey=apikey, proxies={'http': 'http://127.0.0.1:8090', 'https': 'http://127.0.0.1:8090'})


# Function to start spidering
def start_spider():
    print('Starting Spider for target URL:', target_url)
    scan_id = zap.spider.scan(target_url)
    return scan_id

# Function to monitor the spidering process
def wait_for_scan_to_complete(scan_id):
    while True:
        time.sleep(5)
        progress = int(zap.spider.status(scan_id))
        print('Spider scan progress: {}%'.format(progress))
        if progress >= 100:
            break
    print('Spider scan completed!')

# Function to retrieve spider results
def get_spider_results(scan_id):
    spider_results = zap.spider.results(scan_id)
    print('Spider results found the following URLs:')
    for result in spider_results:
        print(result)

# Function to generate an HTML report
def generate_html_report():
    report = zap.core.htmlreport()
    report_file = 'zap_report.html'
    with open(report_file, 'w') as file:
        file.write(report)
    print('HTML report generated: {}'.format(report_file))

if __name__ == '__main__':
    # The target URL
    target_url = input("Input Target-URL:")
    # Run the spider without authentication
    print("Running spider without authentication...")
    spider_scan_id = start_spider()
    wait_for_scan_to_complete(spider_scan_id)
    get_spider_results(spider_scan_id)
    generate_html_report()