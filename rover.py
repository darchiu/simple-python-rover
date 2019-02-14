import argparse
from datetime import datetime
import requests
import os
import shutil

DATE_FORMAT = ['%m/%d/%y', '%B %d, %Y', '%b-%d-%Y',
               '%m/%d/%y\n', '%B %d, %Y\n', '%b-%d-%Y\n']

# Parse input file for list of dates
def read_input_file(filename):
    ret_dates = None
    try:
        file = open(filename, "r")
        ret_dates = file.readlines()
    except Exception as e:
        print("Error in opening file!")
    finally:
        file.close()
    return ret_dates

# Parse list of dates to create search query list
def parse_dates(dates):
    ret_search_query = []
    for date in dates:
        for date_fmt in DATE_FORMAT:
            try:
                datetime_obj = datetime.strptime(date, date_fmt)
                break
            except ValueError:
                datetime_obj = None

        if datetime_obj != None:
            ret_search_query.append(datetime_obj.strftime('%Y-%m-%d'))

    return ret_search_query

# Send query to Rover API and download images to output directory
def download_images(queries):
    cur_directory = os.getcwd()
    out_directory = os.path.join(cur_directory, r'output')
    if not os.path.exists(out_directory):
        os.makedirs(out_directory)
    else:
        shutil.rmtree(out_directory)
        os.makedirs(out_directory)

    for query in queries:
        print("Retrieving list of images for ", query)
        dl_directory = os.path.join(out_directory, query)
        os.makedirs(dl_directory)
        req_params = {'earth_date': query,
                      'api_key': '7Y8d3HQ8ltuTsCVDvsnDAuVLXm1G3JJ3S1VPE7Te'}
        request = requests.get('https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos',
                               params=req_params)
        if request.status_code == requests.codes.ok:
            search_results = request.json()
            index = 0
            for result in search_results['photos']:
                img_url = result['img_src']
                img_name = img_url.rsplit('/', 1)[1]
                img_request = requests.get(img_url, stream=True)
                print("Downloading " + img_name)
                if img_request.status_code == requests.codes.ok:
                    img_download_path = os.path.join(dl_directory, img_name)
                    with open(img_download_path, 'wb') as f:
                        for chunk in img_request:
                            f.write(chunk)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help='Input File', required=True)

    args = parser.parse_args()

    dates_list = read_input_file(args.input)
    search_query = parse_dates(dates_list)
    download_images(search_query)