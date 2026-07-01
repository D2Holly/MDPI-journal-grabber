"""
Docstring for app
"""
import time
import requests


def sample_tests(number):
    """
    Docstring for sample_tests
    
    :param number: Description
    """
    if number == 1:
        return True
    elif number == 0:
        return False
    else:
        return False


def get_response_data(url, params, headers):
    """
    Docstring for get_response_data
    
    :param url: Description
    :param params: Description
    :param headers: Description
    """
    response = requests.get(url, params=params, headers=headers, timeout=30)
    if response.status_code == 200:
        data = response.json()
        items = data['message']['items']
        if not items:
            print("No data found")
            return False

        output_response_data(data)
        return True

    else:
        print("An error occured")
        print(response.status_code)


def output_response_data(data):
    """
    Docstring for output_response_data
    
    :param data: Description
    """
    for item in data['message']['items']:
        #get the resource link of the current article
        resource_dict = item.get('resource', {})
        #get the primary url link of the current article's resource
        primary = resource_dict.get('primary', {})
        #
        url_link = primary.get('URL', 'No Resource URL Available')

        #get the volume no. of the current article. If it doesnt exist replace with ''
        item_volume = str(item.get('volume', ''))


        print(f"Title: {item['title'][0]}")
        print(f"URL: {url_link}")
        print(f"Volume: {item_volume}")
        print(f"Issue: {item["issue"]}\n")

        time.sleep(1)
    return True

def main():
    """
    Docstring for main
    """
    url = "https://api.crossref.org/journals/2072-4292/works"
    params = {
        "filter": "type:journal-article",
        "sort": "published",
        "order": "desc",
        "select": "title,resource,volume,issue",
        "rows": 30
    }
    headers = {
        # crossref requires an email
        "User-Agent": "MyDataScienceProject/1.0 (mailto:your-email@example.com)" 
    }

    result = get_response_data(url, params, headers)
    return result


if __name__ == "__main__":
    main()
