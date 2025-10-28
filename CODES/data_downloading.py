# -*- coding: utf-8 -*-
"""
Created on Mon Oct 27 09:23:09 2025

@author: SREEKANTHVS
"""

import requests

def download_file(url, local_filename):
    """
    Downloads a file from a given URL and saves it locally.
    """
    try:
        # NOTE: Be sure to install the requests library first: pip install requests
        with requests.get(url, stream=True) as r:
            r.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print(f"Successfully downloaded {url} to {local_filename}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"An error occurred during download: {e}")
        return False

# Example usage (REPLACE with your actual URL and filename)
file_url = 'https://www.physionet.org/content/autonomic-aging-cardiovascular/get-zip/1.0.0/'
output_name = 'C:/research_work_DIMAAG_AI_SSE/work_progress_reports/work_report_2025_2026/my_projects/AUTOMATIC_AGING/DATASETS/automatic_aging.zip'
download_file(file_url, output_name)