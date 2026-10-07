# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo>=0.23.16",
#     "requests>=2.32.3",
# ]
# ///

import marimo

__generated_with = "0.25.0"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _():
    import marimo as mo
    import site_helpers as site
    toc_md = site.toc_md_links(scriptname = __name__)
    mo.sidebar(mo.md("""## Pages""" + toc_md))
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Enviroweather API documentation (v1)

    # Step 5: Result Models

    This is the payoff step - actually running a Result Model and getting data back to display in a table, chart, or map.

    Every request to `{rm_api_url}/db2/run` needs:

    - `stationCode` - from Step 2
    - `stationType=1` - always `1` for an Enviroweather station
    - `selectDate` - from Step 3 (required unless the model's datePickers said otherwise, e.g. `latestobstable`)
    - `resultModelCode` - from Step 4
    - any other optional inputs from Step 4, as extra query parameters

    Responses vary by model - some return a `Table` (rows to display), others a GeoJSON `FeatureCollection` (for a map).
    """)
    return


@app.cell
def _():
    import requests
    from datetime import date, timedelta

    from ewx_client import DEFAULT_STATION_CODE, ENVIRONMENTS, get_auth_header, get_environment_urls, get_site_token

    return (
        DEFAULT_STATION_CODE,
        ENVIRONMENTS,
        date,
        get_auth_header,
        get_environment_urls,
        get_site_token,
        requests,
        timedelta,
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


@app.cell
def _(date, timedelta):
    # Use a couple of days ago rather than "today" - observations for the
    # current day may not be finalized yet.
    recent_date = (date.today() - timedelta(days=2)).isoformat()
    return (recent_date,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## weathersummary

    Temperature, rainfall, and degree-day summary for one station/date. Returns a `Table` of daily rows.
    """)
    return


@app.cell
def _(DEFAULT_STATION_CODE, recent_date, requests, rm_api_url, token_header):
    weathersummary_url = (
        f"{rm_api_url}/db2/run?stationCode={DEFAULT_STATION_CODE}&stationType=1"
        f"&selectDate={recent_date}&resultModelCode=weathersummary"
    )
    weathersummary_response = requests.get(weathersummary_url, headers=token_header, timeout=30)
    weathersummary_data = weathersummary_response.json()
    weathersummary_data
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## rainfallregional

    Rainfall totals across nearby stations. Note the extra `selector` and `mdStartAccumulation` inputs from Step 4. Returns a `Table` (one row per nearby station, with a `TableHeaders` list describing the columns) - handy for a sortable table UI, or you could build your own map from the `Distance_Miles` and station data.
    """)
    return


@app.cell
def _(DEFAULT_STATION_CODE, recent_date, requests, rm_api_url, token_header):
    rainfallregional_url = (
        f"{rm_api_url}/db2/run?stationCode={DEFAULT_STATION_CODE}&stationType=1"
        f"&selectDate={recent_date}&resultModelCode=rainfallregional"
        "&selector=network&mdStartAccumulation=March 12th"
    )
    rainfallregional_response = requests.get(rainfallregional_url, headers=token_header, timeout=30)
    rainfallregional_data = rainfallregional_response.json()
    rainfallregional_data
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## meteogram

    Hourly weather over a recent window. `units` and `duration` (hours) come from Step 4.
    """)
    return


@app.cell
def _(DEFAULT_STATION_CODE, recent_date, requests, rm_api_url, token_header):
    meteogram_url = (
        f"{rm_api_url}/db2/run?stationCode={DEFAULT_STATION_CODE}&stationType=1"
        f"&selectDate={recent_date}&resultModelCode=meteogram&units=metric&duration=72"
    )
    meteogram_response = requests.get(meteogram_url, headers=token_header, timeout=30)
    meteogram_data = meteogram_response.json()
    meteogram_data
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## latestobstable

    No `selectDate` needed - the idea was that it always returns the latest observations. As of this writing `latestobstable` has been withdrawn from production (it no longer even appears in the Step 4 resource list), and `db2/run` returns an application-level error:

    ```JSON
    {
        "error": true,
        "message": "This model is not available.",
        "status": 500,
        "data": null
    }
    ```

    This is a good real-world example of why every response needs an `error` check rather than just relying on the HTTP status code (which is `200` here even though the request "failed"). Contrast this with the `/db2/resources/latestobstable/...` routes in Steps 3 and 4, which now fail a different way (`401 Forbidden`, no envelope at all) - see [`ewx_api_v1_resource_common_errors.py`](./ewx_api_v1_resource_common_errors.py).
    """)
    return


@app.cell
def _(DEFAULT_STATION_CODE, requests, rm_api_url, token_header):
    latestobstable_url = (
        f"{rm_api_url}/db2/run?stationCode={DEFAULT_STATION_CODE}&stationType=1"
        "&resultModelCode=latestobstable&selector=network"
    )
    latestobstable_response = requests.get(latestobstable_url, headers=token_header, timeout=30)
    latestobstable_data = latestobstable_response.json()
    if latestobstable_data["error"]:
        print("error in response:", latestobstable_data["message"])
    latestobstable_data
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Other models in this collection

    `overnighttemperatures` follows the same `db2/run` pattern (`resultModelCode=overnighttemperatures`, plus `selector` and `selectDate`) but wasn't documented with a full example in the source Postman collection.
    """)
    return


if __name__ == "__main__":
    app.run()
