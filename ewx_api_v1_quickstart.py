# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo>=0.23.16",
#     "pandas>=3.0.5",
#     "requests>=2.34.2",
# ]
# ///

import marimo

__generated_with = "0.25.0"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Enviroweather Result Model API documentation (v1)

    *Updated August 2026*

    This notebook describes how to use the Enviroweather Result Model API to run weather and crop models using Enviroweather station data.

    *note: if you have opened this notebook in a code editor or want to work with Python, see the Epilogue at he bottom for instructions on how to install components to use it, or if you have problems running it.  The first command below requires an installation, and if it does not work, please see the instructions. 📚*
    """)
    return


@app.cell(hide_code=True)
def _():
    # this is a Marimo document, not a jupyter notebook.  Import marimo to use it
    import marimo as mo
    import site_helpers as site
    toc = site.load_toc()
    mo.sidebar(mo.md("""## Pages""" + site.toc_md(toc)))
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Setup

    We need to import python libraries and set some variables that will be handy to have set before using our APIs.
    """)
    return


@app.cell
def _():

    import requests
    import json
    from datetime import datetime, date
    todays_date = date.today().isoformat()
    return json, requests, todays_date


@app.cell(hide_code=True)
def _(mo, todays_date):
    mo.md(rf"""
    Run date: {todays_date}
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 0.  Select Environment

    We run different versions of our apis for production, testing and development.  If you are using this document to learn about our API please use the production api settings below.  However the testing (aka 'staging') environment is also public but is limited to those using the MSU VPN system.   Select one of the following environments:
    """)
    return


@app.cell
def _():
    # Default environment file
    default_ewx_env_json = """{
      "production": {
        "api_url": "https://api.enviroweather.msu.edu/ewx-api/api",
        "rm_api_url": "https://api.enviroweather.msu.edu/rm-api/api"
      },
      "staging": {
        "api_url": "https://mcrp-dev.geo.msu.edu/ewx/ewx-api/api",
        "rm_api_url": "https://mcrp-dev.geo.msu.edu/ewx/rm-api/api"
      },
      "development": {
        "api_url": "https://mcrp-dev.geo.msu.edu/tma/ewx/ewx-api/api",
        "rmapi_url": "https://mcrp-dev.geo.msu.edu/tma/ewx/rm-api/api"
      }
    }"""
    return (default_ewx_env_json,)


@app.cell
def _(mo):
    # could have a json environment file selector here
    json_env_file_upload = mo.ui.file(kind="button")
    json_env_file_upload
    return (json_env_file_upload,)


@app.cell
def _(default_ewx_env_json, json, json_env_file_upload):
    if json_env_file_upload.name(0):   
        ewx_env_json:str = json_env_file_upload.contents().decode('utf8')
        ewx_env_dict:dict[str, str] = json.loads(ewx_env_json)    
    else:
        ewx_env_dict:dict[str, str] = json.loads(default_ewx_env_json)

    environment_names = list(ewx_env_dict.keys())
    return environment_names, ewx_env_dict


@app.cell(hide_code=True)
def _(environment_names, mo):
    mo.md(rf"""
    The file has the following environments in it: {environment_names}
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    Optionally select an environment from the configuration file.  The default is 'production', which is our public server used by our web application and others
    """)
    return


@app.cell(hide_code=True)
def _(environment_names, mo):
    env_key_selector = mo.ui.dropdown(options=environment_names, label="choose environment")
    env_key_selector
    return (env_key_selector,)


@app.cell
def _(env_key_selector, ewx_env_dict: dict[str, str]):
    if env_key_selector.selected_key:
        ewx_env = env_key_selector.selected_key
    else:
        ewx_env = 'production'

    api_url = ewx_env_dict[ewx_env]["api_url"]
    rm_api_url = ewx_env_dict[ewx_env]["rm_api_url"]
    return api_url, ewx_env, rm_api_url


@app.cell(hide_code=True)
def _(mo):
    mo.md(rf"""
 
    """)
    return


@app.cell(hide_code=True)
def _(api_url, ewx_env, mo, rm_api_url):
    mo.md(rf"""
    working with **{ewx_env}** enviroment for this session with base URLs 

    * **api**: {api_url}
    * **rm api**: {rm_api_url}
    """)
    return


@app.cell
def _(api_url):
    # api_url is from the configuration file loaded above, please run previous cells

    token_url = f"{api_url}/db2/siteToken"
    token_url
    return (token_url,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 1.  Get Site Token

    This is our preliminary system for metering and access control.  To use either api or rm-api, you must use a site-token.  These can be re-used but to get an initial token, use the public URL  and save the token for later use.  In the future everyone must log-in and create a personalized site-token.
    """)
    return


@app.cell
def _(ewx_env, mo, token_url):
    mo.md(rf"""
    The URL for the {ewx_env} enviroment is {token_url} 
    ```<api_url>/db2/siteToken```  (note this is the API, not the "RM-API")

    The response to this request contains the site token in the 'data' key of the JSON.   Here is an example (this token will not work, it's just a static example):
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ```JSON
    {
        "error": false,
        "message": "Success",
        "status": 200,
        "data": {
            "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJFbnZpcm93ZWF0aGVyIFVucmVnaXN0ZXJlZCBVc2V
                      yIiwic2VjcmV0IjoiNGt3eDJhQlY0S0RCOThBYSIsImlhdCI6MTcwMTg3Mzk0OCwiZXhwIjoxNzAyNzM4NTAxfQ.
                      3RSNeN5nQ3JlWoJYzmcAkz7AcNi8aIzrrrozBaXPIe8"
        }
    }
    ```
    """)
    return


@app.cell
def _(requests, token_url):
    print(f"requesting token from {token_url}")
    token_response = requests.request(method='GET', url=token_url)
    print(token_response.status_code)
    return (token_response,)


@app.cell
def _(token_response):
    print("your token is:")
    token_response_data = token_response.json()
    if not(token_response_data["error"]):
        anonymous_token = token_response_data['data']['token']
        print(anonymous_token)
    else:
        print("error in response")
        print(token_response_data)
    return (anonymous_token,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Preserve the token for this session

    For requests in this notebook, the token needs to be included as a 'header' field

    `headers = {"Authorization": "Bearer TOKEN_FROM_ABOVE"}`

    and in the Python `Requests` module that's added as

    ```Python
    headers = {"Authorization": "Bearer MYREALLYLONGTOKENIGOT"}
    # add to the headers dict as needed
    response = requests.post(url, headers=headers)
    ```

    For example:
    """)
    return


@app.cell
def _(anonymous_token):
    token_header = {"Authorization": f"Bearer {anonymous_token}"}
    token_header
    return (token_header,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 2: Weather Stations

    The user will want to select a station somewhere in your application. The Result Models that you will be accessing require a station code. The weather station is the "key" to get the right weather information for the Result Model.

    This part can be up to you - the user can select from a list, the user could select from a map, or you can request a station close to a latitude/longitude.

    One reason user might like a map is - they might know that an inland station is more/less representative of their site than a station closer to the Lake.

    There are 3 requests:

    1. get a list of stations - this gives all details about the station that you can access.
    2. get a station close to a lat lon - gives a single station id
    3. get station ids in bounding box - list of station ids in a bounding box
    """)
    return


@app.cell
def _(api_url):
    station_list_url = f"{api_url}/db2/places?show=ewxstation"
    station_list_url
    return (station_list_url,)


@app.cell(hide_code=True)
def _(anonymous_token, mo, station_list_url):
    mo.md(rf"""
    Requesting station list from {station_list_url} 
    using our anonymous token {anonymous_token}
    """)
    return


@app.cell
def _(requests, station_list_url, token_header):
    # this requires token header to be defined (above), e.g. 
    # token_header = {"Authorization": f"Bearer {anonymous_token}"}

    # uncomment for debugging
    # print(requests.post(endpoint, data=data, headers=headers).json())
    station_list_response = requests.request(method='GET', url=station_list_url, headers = token_header )
    if station_list_response.status_code == 200: print("okee dokee, got the station list")
    return (station_list_response,)


@app.cell
def _(station_list_response):
    station_list_response_data = station_list_response.json()
    print(station_list_response_data)
    return (station_list_response_data,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### About the response body/content for station lists

    The 'content' of the response is JSON dictionary that also includes fields similar to a http response, but are not the same. For example, response has a statue (200) but the API content also includes a 'status' field with codes very similar to HTTP.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### typical fields in dictionary in JSON body of response of an Enviroweather API response

    | field   | values                   | description  |
    |:---------|:--------------------------|:--------------|
    | error   | "true" or "false"        | was there an error with this request? This could be caused by malformed inputs or source data |
    | status  | 200 (others)             | an Enviroweather API response status that mimic http status codes but are not the same (Details of status codes to be written).  Note that "200" indicates a response of some kind was given (meaning the API is working), but it could be an error (error = True) |
    | message | "Success" (others)       | similar to status but additional, narrative detail about the reponse  |
    | data    | various, hash/dictionary | a keyed array (aka python dictionary) often with several subkeys.  This varies greatly with the request.  Note that many of the sub-keys were originally designed to provide HTML code, classes, or element attributes that could be directly  inserted into the output HTML of the calling function (javascript).    |
    """)
    return


@app.cell
def _(station_list_response_data):
    # extract the list of stations which is in a dictionary from the response.  
    # first check if the "error" field in response body was True or False (boolean)
    if station_list_response_data["error"]==True:
        print("error in response")
        print(station_list_response_data['message'])
        station_list = None
    else:
        # not an error, get the dc
        station_list_container = station_list_response_data['data'][0]['placeInputs']
        station_list = station_list_container[0]['options']


    station_list
    return (station_list,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Station Properties (columns):

    | Property | Description |
    |: --- |: --- |
    | **value** | used by website, use 'key' instead |
    | **key** | station code/id, currently 3-letters |
    | **display** | full station name, as displayed on website |
    | **startDate** | date of the first observation for this station |
    | **endDate** | last date an observation was reported. |
    | **longitude** | Decimal Longitude (WGS84) |
    | **latitude** | Decimal Latitude (WGS84) |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    For use in Python, let's convert the dictionary (array, hash) of stations into a Pandas data frame.
    """)
    return


@app.cell
def _(station_list):
    import pandas as pd
    all_stations_df = pd.DataFrame(station_list)
    all_stations_df
    return (pd,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The 'station list' above includes all stations Enviroweather/Michgan Ag Weather Network has ever deployed, some of which are no longer active.  To filter inactive stations, check the end date is before today, which is by default today's date. For this documentation, we consider any station not active today to be inactive.

    In python, we can do that either in Pandas (common approach) or filter prior to creating the dataframe.  We will demonstrate the latter approach of filtering before importing to Pandas.
    """)
    return


@app.cell
def _(pd, station_list, todays_date):
    print(f"using today's data as todays_date={todays_date} as defined above")
    # station list is a list of dictionaries, this is python list comprehension-style filtering
    active_station_list = [s for s in station_list if s['endDate'] == todays_date]
    stations_df = pd.DataFrame(active_station_list)
    stations_df
    return (active_station_list,)


@app.cell(hide_code=True)
def _(active_station_list, mo):
    mo.md(rf"""
    Created a table of {len(active_station_list)} rows
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Epilogue

    - Authors: Patrick Bills, Tracy Aichele
    - Last Major Update to this doc: September 2026
    - *see git repository for commit history*
    - Git Repository: TBD

    **History**

    Our APIs are constantly being updated and and fixed and we do our best to update this documentation to match.


    **Installation**

    This and other notebooks in this python package use the open source [marimo](https://marimo.io) notebook system.  These can be run as web pages (which you may be reading) or opened on a computer or code editor.  If the latter, see the [project README.md file](./README.md) for instructions on installing marimo (as easy as `pip install marimo`) which is required to render these notebooks (and our motivation for using marimo).
    """)
    return


if __name__ == "__main__":
    app.run()
