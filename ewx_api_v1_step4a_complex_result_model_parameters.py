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
    ## Enviroweather API documentation (v1)

    # Step 4a: More Complex Result Model Parameters

    Covers `applescab`, `orientalfruitmoth`, and `tomcast`. Unlike the models in Step 4, these don't have constant defaults - the `defaultValue` for their inputs is `null`, but the group has a `defaultResourceKey`.

    To get the real default, you make a *second* RM-API request using `defaultResourceKey` as the `resultModelCode`, for the station/date the user picked. That response gives you a date (e.g. `gtStart_estimated`) to pre-fill the input with. The user can still override it.
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

    from ewx_client import DEFAULT_STATION_CODE, ENVIRONMENTS, get_auth_header, get_environment_urls, get_site_token

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


@app.cell
def _():
    from datetime import date, timedelta

    # Weather-dependent RM-API calls use a couple of days ago, since "today's"
    # observations may not be finalized yet.
    recent_date = (date.today() - timedelta(days=2)).isoformat()
    return (recent_date,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Apple scab

    `GET {api_url}/db2/resources/applescab/inputs?show=rmInputs` describes the `applescabbiofix` (aka "green tip") input - its `defaultResourceKey` is `mcintoshgreentip`.

    To compute the actual default date for a given station/date, call RM-API with `resultModelCode=mcintoshgreentip`:

    `GET {rm_api_url}/db2/run?stationCode=...&stationType=1&selectDate=...&resultModelCode=mcintoshgreentip`

    The response's `gtStart_estimated` field is the date to pre-fill for `gtStart` in the real Step 5a `applescab` request.
    """)
    return


@app.cell
def _(api_url, requests, token_header):
    applescab_inputs_url = f"{api_url}/db2/resources/applescab/inputs?show=rmInputs"
    applescab_inputs_response = requests.get(applescab_inputs_url, headers=token_header, timeout=30)
    applescab_inputs_response.json()
    return


@app.cell
def _(DEFAULT_STATION_CODE, recent_date, requests, rm_api_url, token_header):
    mcintoshgreentip_url = (
        f"{rm_api_url}/db2/run?stationCode={DEFAULT_STATION_CODE}&stationType=1"
        f"&selectDate={recent_date}&resultModelCode=mcintoshgreentip"
    )
    mcintoshgreentip_response = requests.get(mcintoshgreentip_url, headers=token_header, timeout=30)
    mcintoshgreentip_data = mcintoshgreentip_response.json()
    mcintoshgreentip_data
    return (mcintoshgreentip_data,)


@app.cell
def _(mcintoshgreentip_data, mo):
    if not mcintoshgreentip_data["error"]:
        estimate_md = mo.md(
            f"estimated `gtStart` for apple scab: **{mcintoshgreentip_data['data']['gtStart_estimated']}**"
        )
    else:
        estimate_md = mo.md(f"error: {mcintoshgreentip_data['message']}")
    estimate_md
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Oriental fruit moth

    Same pattern. `orientalfruitmoth`'s two biofix inputs use `defaultResourceKey = orientalfruitmothadultemergence`, which returns `biofix1_estimated` and `biofix2_estimated`.
    """)
    return


@app.cell
def _(api_url, requests, token_header):
    orientalfruitmoth_inputs_url = f"{api_url}/db2/resources/orientalfruitmoth/inputs?show=rmInputs"
    orientalfruitmoth_inputs_response = requests.get(orientalfruitmoth_inputs_url, headers=token_header, timeout=30)
    orientalfruitmoth_inputs_response.json()
    return


@app.cell
def _(DEFAULT_STATION_CODE, recent_date, requests, rm_api_url, token_header):
    orientalfruitmoth_defaults_url = (
        f"{rm_api_url}/db2/run?stationCode={DEFAULT_STATION_CODE}&stationType=1"
        f"&selectDate={recent_date}&resultModelCode=orientalfruitmothadultemergence"
    )
    orientalfruitmoth_defaults_response = requests.get(orientalfruitmoth_defaults_url, headers=token_header, timeout=30)
    orientalfruitmoth_defaults_response.json()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Tomcast

    Same pattern again, with `defaultResourceKey = tomcastdefaults`.
    """)
    return


@app.cell
def _(api_url, requests, token_header):
    tomcast_inputs_url = f"{api_url}/db2/resources/tomcast/inputs?show=rmInputs"
    tomcast_inputs_response = requests.get(tomcast_inputs_url, headers=token_header, timeout=30)
    tomcast_inputs_response.json()
    return


@app.cell
def _(DEFAULT_STATION_CODE, recent_date, requests, rm_api_url, token_header):
    tomcast_defaults_url = (
        f"{rm_api_url}/db2/run?stationCode={DEFAULT_STATION_CODE}&stationType=1"
        f"&selectDate={recent_date}&resultModelCode=tomcastdefaults"
    )
    tomcast_defaults_response = requests.get(tomcast_defaults_url, headers=token_header, timeout=30)
    tomcast_defaults_response.json()
    return


if __name__ == "__main__":
    app.run()
