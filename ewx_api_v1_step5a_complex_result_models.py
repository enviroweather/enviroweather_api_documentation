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
    # this is a Marimo document, not a jupyter notebook.  Import marimo to use it
    import marimo as mo
    import site_helpers as site
    toc_md = site.toc_md_links(scriptname = __name__)
    mo.sidebar(mo.md("""## Pages""" + toc_md))
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Enviroweather API documentation (v1)

    ## Step 5a: More Complex Result Models

    Same `db2/run` pattern as Step 5, but for `applescab`, `orientalfruitmoth`, and `tomcast` - models with a limited season and calculated defaults (see Step 4a).

    If you don't send the date-ish input (`gtStart`, `biofix1`/`biofix2`, `dateStartAccumulation`), RM-API estimates it for you from the station's weather data - which only works once the model is "in season". Outside the season, or with a bad combination of inputs, you'll get an application-level error (`error: true`) back with HTTP 200, so always check the `error` field.
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
    ## applescab

    Called with no `gtStart`, RM-API estimates the McIntosh green-tip date from the station's weather and uses it. The response includes both `gtStart_used` (what was actually used) and `gtStart_estimated` (what RM-API calculated), which should match when you don't override it.

    Apple scab responses can include up to 3 tables (`Table`, `Table_2`, `Table_3`) plus a spore-results table - see `TableFootnote` in the response for what each one means.
    """)
    return


@app.cell
def _(DEFAULT_STATION_CODE, recent_date, requests, rm_api_url, token_header):
    applescab_url = (
        f"{rm_api_url}/db2/run?stationCode={DEFAULT_STATION_CODE}&stationType=1"
        f"&selectDate={recent_date}&resultModelCode=applescab"
    )
    applescab_response = requests.get(applescab_url, headers=token_header, timeout=30)
    applescab_data = applescab_response.json()
    if applescab_data["error"]:
        print("error in response (expected outside the apple scab season):", applescab_data["message"])
    applescab_data
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    You can also send an explicit `gtStart` to override the estimate, e.g. `&gtStart=2023-07-01` - then `gtStart_used` will match what you sent instead of the estimate.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## orientalfruitmoth

    Uses `biofix1`/`biofix2` instead of `gtStart`. You can send neither (both estimated), either one, or both. Sending a `biofix2` that's before `biofix1` is rejected with a descriptive error (`"Biofix 2 must be after 5/30."` in the source example) - another good real "common error" case.

    The model is also only available starting 3/1 each year; before that you'll get `"This model is available after 3/1."`.
    """)
    return


@app.cell
def _(DEFAULT_STATION_CODE, recent_date, requests, rm_api_url, token_header):
    orientalfruitmoth_url = (
        f"{rm_api_url}/db2/run?stationCode={DEFAULT_STATION_CODE}&stationType=1"
        f"&selectDate={recent_date}&resultModelCode=orientalfruitmoth"
    )
    orientalfruitmoth_response = requests.get(orientalfruitmoth_url, headers=token_header, timeout=30)
    orientalfruitmoth_data = orientalfruitmoth_response.json()
    if orientalfruitmoth_data["error"]:
        print("error in response (expected outside the season, e.g. before 3/1):", orientalfruitmoth_data["message"])
    orientalfruitmoth_data
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## tomcast

    Uses `dateStartAccumulation` instead of `gtStart`/`biofix`. Same seasonal gating as the other complex models.
    """)
    return


@app.cell
def _(DEFAULT_STATION_CODE, recent_date, requests, rm_api_url, token_header):
    tomcast_url = (
        f"{rm_api_url}/db2/run?stationCode={DEFAULT_STATION_CODE}&stationType=1"
        f"&selectDate={recent_date}&resultModelCode=tomcast"
    )
    tomcast_response = requests.get(tomcast_url, headers=token_header, timeout=30)
    tomcast_data = tomcast_response.json()
    if tomcast_data["error"]:
        print("error in response (expected outside the season):", tomcast_data["message"])
    tomcast_data
    return


if __name__ == "__main__":
    app.run()
