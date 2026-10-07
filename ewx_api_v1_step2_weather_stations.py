# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo>=0.23.16",
#     "pandas>=3.0.5",
#     "requests>=2.32.3",
# ]
# ///

import marimo

__generated_with = "0.25.0"
app = marimo.App(width="medium", app_title="EWX API Step 2: Weather Stations")


@app.cell(hide_code=True)
def _():
    # this is a Marimo document, not a jupyter notebook.  Import marimo to use it
    # this is a Marimo document, not a jupyter notebook.  Import marimo to use it
    import marimo as mo
    import site_helpers as site
    toc_md = site.toc_md_links(scriptname = __name__)
    mo.sidebar(mo.md("""## Pages""" + toc_md))
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Enviroweather API documentation (v1)

    # Step 2: Weather Stations

    Your application will need to let a user pick a weather station - the station code is the "key" used to get the right weather data for a Result Model.

    There are 3 requests shown here:

    1. get a list of all stations (with details)
    2. get the station closest to a given latitude/longitude
    3. get station ids in a bounding box

    One reason a map UI is nice: a user might know an inland station is more representative of their site than a station closer to a Great Lake.
    """)
    return


@app.cell
def _():
    import requests
    from datetime import date

    from ewx_client import ENVIRONMENTS, get_auth_header, get_environment_urls, get_site_token

    todays_date = date.today().isoformat()
    return (
        ENVIRONMENTS,
        get_auth_header,
        get_environment_urls,
        get_site_token,
        requests,
        todays_date,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Setup: choose an environment and get a token

    See [`ewx_api_v1_step1_tokens.py`](./ewx_api_v1_step1_tokens.py) for a full walkthrough of tokens; here we just reuse the `ewx_client` helpers.
    """)
    return


@app.cell
def _(ENVIRONMENTS, mo):
    environment_names = list(ENVIRONMENTS.keys())
    env_key_selector = mo.ui.dropdown(options=environment_names, label="choose environment")
    env_key_selector
    return (env_key_selector,)


@app.cell
def _(env_key_selector):
    if env_key_selector.selected_key:
        ewx_env = env_key_selector.selected_key
    else:
        ewx_env = "production"
    return (ewx_env,)


@app.cell
def _(ewx_env, get_environment_urls):
    api_url, rm_api_url = get_environment_urls(ewx_env)
    return api_url, rm_api_url


@app.cell
def _(api_url, get_auth_header, get_site_token):
    anonymous_token = get_site_token(api_url)
    token_header = get_auth_header(anonymous_token)
    return (token_header,)


@app.cell(hide_code=True)
def _(api_url, ewx_env, mo, rm_api_url):
    mo.md(rf"""
    working with **{ewx_env}** environment for this session with base URLs

    * **api**: {api_url}
    * **rm api**: {rm_api_url}
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. Get list of stations

    `GET {api_url}/db2/places?show=ewxstation`

    The response nests the station list a few levels deep: `data[0]['placeInputs'][0]['options']` is the actual list of station dicts (`value`/`key` is the station code used everywhere else, plus `display`, `startDate`, `endDate`, `latitude`, `longitude`).
    """)
    return


@app.cell
def _(api_url, requests, token_header):
    station_list_url = f"{api_url}/db2/places?show=ewxstation"
    station_list_response = requests.get(station_list_url, headers=token_header, timeout=30)
    print(station_list_response.status_code)
    return (station_list_response,)


@app.cell
def _(station_list_response):
    station_list_response_data = station_list_response.json()
    if station_list_response_data["error"]:
        print("error in response")
        print(station_list_response_data["message"])
        station_list = []
    else:
        station_list_container = station_list_response_data["data"][0]["placeInputs"]
        station_list = station_list_container[0]["options"]
    return (station_list,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The list includes every station Enviroweather/Michigan Ag Weather Network has ever deployed, including retired ones. Filter to stations active today by comparing `endDate` to today's date.
    """)
    return


@app.cell
def _(station_list, todays_date):
    import pandas as pd

    active_station_list = [s for s in station_list if s["endDate"] == todays_date]
    stations_df = pd.DataFrame(active_station_list)
    stations_df
    return (active_station_list,)


@app.cell(hide_code=True)
def _(active_station_list, mo):
    mo.md(rf"""
    found {len(active_station_list)} active stations out of {len(active_station_list)} total (filtered by endDate == today)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. Get station closest to a lat/lon

    `GET {api_url}/db2/stationnear?lat=...&lon=...`

    Useful if your UI lets a user drop a pin on a map rather than pick from a list.

    Example response:

    ```JSON
    {
        "error": false,
        "message": "Success",
        "status": 200,
        "data": [
            {
                "station_id": "htc"
            }
        ]
    }
    ```
    """)
    return


@app.cell
def _(api_url, requests, token_header):
    station_near_url = f"{api_url}/db2/stationnear?lat=42.75313740994824&lon=-84.4907810027659"
    station_near_response = requests.get(station_near_url, headers=token_header, timeout=30)
    station_near_response.json()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Get stations in a bounding box

    `GET {api_url}/db2/stationin?sw_lat=...&sw_lon=...&ne_lat=...&ne_lon=...`

    Useful for a map UI that only wants to show stations within the current viewport.
    """)
    return


@app.cell
def _(api_url, requests, token_header):
    station_in_url = (
        f"{api_url}/db2/stationin"
        "?sw_lat=42.75313740994824&sw_lon=-84.4907810027659"
        "&ne_lat=43.75313740994824&ne_lon=-82.4907810027659"
    )
    station_in_response = requests.get(station_in_url, headers=token_header, timeout=30)
    station_in_response.json()
    return


if __name__ == "__main__":
    app.run()
