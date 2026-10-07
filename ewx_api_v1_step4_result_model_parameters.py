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

    ## Step 4: Result Model Parameters

    Now that you can pick a station (Step 2) and a date (Step 3), you need to pick a Result Model and find out what *optional* parameters it accepts.

    - `GET {api_url}/db2/resources?type=rm-api` lists every Result Model key available to you (based on your token).
    - `GET {api_url}/db2/resources/{{resultModelKey}}/inputs?show=rmInputs` lists the optional inputs for one Result Model. RM-API will use sensible defaults for anything you don't send.

    Note: the parameters from Step 2 (station) and Step 3 (date) are *required*. The parameters here are *optional*.
    """)
    return


@app.cell
def _():
    import requests

    from ewx_client import ENVIRONMENTS, get_auth_header, get_environment_urls, get_site_token

    return (
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
    ## 1. Get the list of Result Model keys

    `GET {api_url}/db2/resources?type=rm-api`

    Each entry has a `key` (use this as `resultModelCode` in Step 5), a human-readable `display`, and a `description` (sometimes HTML).
    """)
    return


@app.cell
def _(api_url, requests, token_header):
    result_model_keys_url = f"{api_url}/db2/resources?type=rm-api"
    result_model_keys_response = requests.get(result_model_keys_url, headers=token_header, timeout=30)
    result_model_keys_data = result_model_keys_response.json()
    result_model_keys = [item["key"] for item in result_model_keys_data["data"]]
    result_model_keys
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. Get optional inputs for a Result Model

    `GET {api_url}/db2/resources/{{resultModelKey}}/inputs?show=rmInputs`

    A few examples below. Some models (`weathersummary`) have no extra inputs at all (`data = []`); others (`rainfallregional`, `meteogram`) have a handful of `select`-type options with a `defaultValue`.

    `latestobstable` has since been removed from production - its `/inputs` route (like its `/datePickers` route in Step 3) now returns a plain `401 Forbidden` instead of the usual response envelope, so it's omitted from the live examples below.
    """)
    return


@app.cell
def _(api_url, requests, token_header):
    weathersummary_inputs_url = f"{api_url}/db2/resources/weathersummary/inputs?show=rmInputs"
    weathersummary_inputs_response = requests.get(weathersummary_inputs_url, headers=token_header, timeout=30)
    weathersummary_inputs_response.json()
    return


@app.cell
def _(api_url, requests, token_header):
    rainfallregional_inputs_url = f"{api_url}/db2/resources/rainfallregional/inputs?show=rmInputs"
    rainfallregional_inputs_response = requests.get(rainfallregional_inputs_url, headers=token_header, timeout=30)
    rainfallregional_inputs_response.json()
    return


@app.cell
def _(api_url, requests, token_header):
    meteogram_inputs_url = f"{api_url}/db2/resources/meteogram/inputs?show=rmInputs"
    meteogram_inputs_response = requests.get(meteogram_inputs_url, headers=token_header, timeout=30)
    meteogram_inputs_response.json()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## What about `applescab`, `orientalfruitmoth`, `tomcast`?

    Those Result Models have *calculated* defaults instead of constant ones - the `defaultResourceKey` field tells you to make another RM-API request to compute them. See [`ewx_api_v1_step4a_complex_result_model_parameters.py`](./ewx_api_v1_step4a_complex_result_model_parameters.py) for that pattern.
    """)
    return


if __name__ == "__main__":
    app.run()
