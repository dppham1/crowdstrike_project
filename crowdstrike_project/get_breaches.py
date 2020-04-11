import requests
import simplejson as json


def get_api(api_url: str, headers : dict=None) -> tuple:
    """

    Performs a GET request to the given api_url string, handles error checking, and returns the response payload as the first element of a tuple
    along with "True". If a non-200 response code was given, returns the error string as the first element of the tuple along with "False".

    Args:
        api_url (str): The api URL to make a GET call on.
        headers (dict): Optional request headers. Necessary for APIs that use the hibp-api key.
    
    Returns:
        data (tuple):   If a 200 response is given, the first element is the data and the second element is "True". If a non-200 response is given,
                        the first element is an error string and the second element is "False".

    """

    try:
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return (data, True)
        else:
            # a 404 status code for some endpoints means that there was no data returned, which means there was actually no breach.
            return ("Server responded with status code {} instead of 200. If you are expecting a 404, ignore this message".format(response.status_code), False)

    except requests.exceptions.HTTPError as e:
        return ("An HTTP Error occurred with the following message: {}".format(e), False)
    except requests.exceptions.ConnectionError as e:
        return ("A Connection Error occurred with the following message: {}".format(e), False)
    except requests.exceptions.ConnectTimeout as e:
        return ("A Connect Timeout Error (request timed out while trying to connect to the server) occurred with the following message: {}".format(e), False)
    except requests.exceptions.ReadTimeout as e:
        return ("A Read Timeout Error (server did not send any data in the allotted amount of time) occurred with the following message: {}".format(e), False)
    except requests.exceptions.URLRequired as e:
        return ("A URL Required Error (invalid URL) occurred with the following message: {}".format(e), False)
    except requests.RequestException as e:
        return ("An ambiguous Request Exception Error occurred: {}".format(e), False)
    
def write_breaches_to_file() -> None:
    """

    Updates the all_breaches.json file with information from the all breaches API.

    """

    data = get_api("https://haveibeenpwned.com/api/v3/breaches")
    if data[1]:
        with open("breaches.json", "w") as breaches:
            json.dump(data[0], breaches)
        print("Finished updating breaches with the newest info.")
    else:
        print("Data from the https://haveibeenpwned.com/api/v3/breaches endpoint was empty.")

def check_domain_breach(breaches_file: str, domains: set, url: str="http://localhost:5000/logDomainBreach") -> None:
    """
    
    Checks all breaches to see if there are any breaches that match any of the given domains. In the event
    that there are matches, send all the metadata for that breach to the syslog server.

    Args:
        breaches_file (str): The name of the .json file with all breaches.
        domains (set): A set of all domains to check (i.e. acme.com, acme.net, acme.org).
        url (str): The URL endpoint that where the breach metadata will be sent to. Defaulted to the localhost logDomainBreach endpoint.

    """

    with open(breaches_file, "r") as breaches:
        breaches_data = json.load(breaches)

        for breach in breaches_data:
            if breach["Domain"] in domains:
                try:
                    requests.post(url, data=json.dumps(breach), headers={"content-type": "application/json"})
                except Exception as e:
                    print("The POST request to {} was unsuccessful and failed with the following message: {}".format(url, e))

    print("Finished checking all domains for breaches.")

def check_user_breach(email: str, api_key: str, url="http://localhost:5000/logUserBreach") -> None:
    """

    Checks to see if there has been a user breach, then sends the metadata for that breach to the syslog server. 
    
    A user breach occurs when either one or both of these scenarios occur:

        1) A user's email shows up in any data associated with a breach (https://haveibeenpwned.com/api/v3/breachedaccount/{account})
        2) A user's email is mentioned on pastebin sites (https://haveibeenpwned.com/api/v3/pasteaccount/{account})

    Args:
        email (str): The email address that will be checked to see if there are breaches/pastes.
        api_key (str): The hibp-api-key (development key).
        url (str): The URL endpoint that where the breach metadata will be sent to. Defaulted to the localhost logUserBreach endpoint.


    """

    breach_data = get_api("https://haveibeenpwned.com/api/v3/breachedaccount/{}".format(email), headers={"hibp-api-key": api_key})
    paste_data = get_api("https://haveibeenpwned.com/api/v3/pasteaccount/{}".format(email), headers={"hibp-api-key": api_key})

    if breach_data[1]:
        try:
            requests.post(url, data=json.dumps(breach_data[0]), headers={"content-type": "application/json"})
            print("Breached account data successfully sent.")
        except Exception as e:
            print("The POST request to {} was unsuccessful and failed with the following message: {}".format(url, e))

    if paste_data[1]:
        try:
            requests.post(url, data=json.dumps(paste_data[0]), headers={"content-type": "application/json"})
            print("Paste account data successfully sent.")
        except Exception as e:
            print("The POST request to {} was unsuccessful and failed with the following message: {}".format(url, e))
    
    print("Finished checking for breaches for the user '{}'\n".format(email))