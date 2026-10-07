# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo>=0.23.16",
#     "requests>=2.32.3",
# ]
# ///

import marimo

__generated_with = "0.25.0"
app = marimo.App(width="medium", app_title="Step 1. Tokens")


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

    ## Step 1: Tokens

    Requests to the API and RM-API require a 'token' as a header in every request.  Currently you can easily get an 'anonymous' token from a public API endpoint, save it and use in subsequent API / RM-API calls.  This will change in the future and require a log-in for this is the process for now (September 2026).  If at some point your token no longer works please contact us (see or web )

    The token is not specific to a user, but it does expire - request a new one at least once per day (and have your application do the same).

    <!-- the notebook referred to here was my example and outside of the main docs folder.  copy to the docs folder to use it, and call it
    quickstart.py -->
    <!-- See [`ewx_api_v1_intro.py`](../example-new-style-documents/ewx_api_v1_intro.py) for a broader tour of the API; this notebook focuses only on tokens. -->
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

    from ewx_client import ENVIRONMENTS, get_environment_urls

    return ENVIRONMENTS, get_environment_urls, requests


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Setup: choose an environment

    Select which Enviroweather environment to use. `production` is the public server used by our web application and others.
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
    ## Request a site token

    `GET {api_url}/db2/siteToken` - no auth needed for this one request; it's how you *get* your auth.

    Example response:

    ```JSON
    {
        "error": false,
        "message": "Success",
        "status": 200,
        "data": {
            "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJFbnZpcm93ZWF0aGVyIFVucmVnaXN0ZXJlZCBVc2Vy..."
        }
    }
    ```
    """)
    return


@app.cell
def _(api_url):
    token_url = f"{api_url}/db2/siteToken"
    token_url
    return (token_url,)


@app.cell
def _(requests, token_url):
    token_response = requests.get(token_url, timeout=30)
    print(token_response.status_code)
    return (token_response,)


@app.cell
def _(token_response):
    token_response_data = token_response.json()
    if not token_response_data["error"]:
        anonymous_token = token_response_data["data"]["token"]
        print("your token is:")
        print(anonymous_token)
    else:
        anonymous_token = None
        print("error in response")
        print(token_response_data)
    return (anonymous_token,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Use the token for later requests

    Every other request needs the token as a `Bearer` token in the `Authorization` header:

    ```Python
    headers = {"Authorization": f"Bearer {anonymous_token}"}
    response = requests.get(url, headers=headers)
    ```
    """)
    return


@app.cell
def _(anonymous_token):
    token_header = {"Authorization": f"Bearer {anonymous_token}"}
    token_header
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Reuse

    The other Step N notebooks in this package import `get_site_token` and `get_auth_header` from `ewx_client.py` instead of repeating the raw request above - it's the exact same two requests, just wrapped in a function.

    There is also `temporary_site_token.txt` in the repo root with a scratch token in it, in case you want a token without making this request - but a fresh one from here is more reliable since tokens expire.
    """)
    return


if __name__ == "__main__":
    app.run()
