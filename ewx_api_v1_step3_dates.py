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


@app.cell
def _():
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

    # Step 3: Dates

    Most Result Models need a date. This notebook shows how to ask the API what kind of date picker to show a user, both generically and per Result Model.

    Right now there's only one kind of date picker (`selectDate`, a single date), but this step is "future proofing" - some models (like `latestobstable`) don't need a date at all, and new date shapes (ranges, month-day, etc.) may be added later.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### About this notebook

    This is a [marimo](https://marimo.io) notebook, which is an advanced version of Jupyter Python notebooks.  Ff you don't have, or can't install Marimo, there is a Jupyter version in the `jupyter` folder  (requires opening in Jupyter or VS code).
    """)
    return


@app.cell
def _():
    import requests

    from ewx_client import ENVIRONMENTS, DEFAULT_STATION_CODE, get_auth_header, get_environment_urls, get_site_token

    return (
        DEFAULT_STATION_CODE,
        ENVIRONMENTS,
        get_auth_header,
        get_environment_urls,
        get_site_token,
        requests,
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
    ## 1. Get the generic list of date pickers

    `GET {api_url}/db2/datePickers`

    This describes the `selectDate` picker in general, with no Result Model context.
    """)
    return


@app.cell
def _(api_url, requests, token_header):
    date_pickers_url = f"{api_url}/db2/datePickers"
    date_pickers_response = requests.get(date_pickers_url, headers=token_header, timeout=30)
    date_pickers_response.json()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. Get date pickers for a specific station

    `GET {api_url}/db2/datePickers?stationCode=...`

    Adding `stationCode` fills in `dateStart`/`dateEnd` for that specific station's date range.
    """)
    return


@app.cell
def _(DEFAULT_STATION_CODE, api_url, requests, token_header):
    station_date_pickers_url = f"{api_url}/db2/datePickers?stationCode={DEFAULT_STATION_CODE}"
    station_date_pickers_response = requests.get(station_date_pickers_url, headers=token_header, timeout=30)
    station_date_pickers_response.json()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Get date pickers for a specific Result Model

    `GET {api_url}/db2/resources/{{resultModelKey}}/datePickers?stationCode=...`

    Same idea, scoped to one Result Model key (from Step 4). Most models need a `selectDate`; some don't.

    `latestobstable` used to be an interesting case here - the idea was that it gives you the *latest* observations so a date is irrelevant (`data = []`). As of this writing, though, `latestobstable` has been removed from production entirely: this route now returns a plain `401 Forbidden` with a *different* JSON shape (`{{"error": "Forbidden"}}` - a string, not the usual `error`/`message`/`status`/`data` envelope). That's a good reminder that not every failure in this API follows the same shape - see [`ewx_api_v1_resource_common_errors.py`](./ewx_api_v1_resource_common_errors.py).
    """)
    return


@app.cell
def _(DEFAULT_STATION_CODE, api_url, requests, token_header):
    weathersummary_date_pickers_url = (
        f"{api_url}/db2/resources/weathersummary/datePickers?stationCode={DEFAULT_STATION_CODE}"
    )
    weathersummary_date_pickers_response = requests.get(
        weathersummary_date_pickers_url, headers=token_header, timeout=30
    )
    weathersummary_date_pickers_response.json()
    return


@app.cell
def _(api_url, requests, token_header):
    latestobstable_date_pickers_url = f"{api_url}/db2/resources/latestobstable/datePickers"
    latestobstable_date_pickers_response = requests.get(
        latestobstable_date_pickers_url, headers=token_header, timeout=30
    )
    print(latestobstable_date_pickers_response.status_code)
    latestobstable_date_pickers_response.json()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The same `/db2/resources/{{resultModelKey}}/datePickers` pattern works for every Result Model key from Step 4 (`rainfallregional`, `meteogram`, `applescab`, `orientalfruitmoth`, `tomcast`, ...) - swap the key in the URL.
    """)
    return


if __name__ == "__main__":
    app.run()
