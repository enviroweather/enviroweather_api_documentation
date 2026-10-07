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
    # Enviroweather API Documentation

    This site is a collection of interactive notebooks describing aspects of using the Enviroweather APIs.

    ## About the Enviroweather APIs

    *to-be-written*

    - API: a 'web api' using for getting access, logins, settings saving etc.
    - RM-API = "Result Model API": this is the API to send requests (which model, which station, dates, other option) and returns the output from the weather or agicultural model
    - Website: the enviroweather website uses both APIs
    - App: MABR develops a mobile app the user the RM-API

    ## About this documentation

    This site is for developers who want to learn how to use the Enviroweather APIs for their projects.  If you are familiar with python,
    don't mind installing python dependencies, and want to work with the notebooks themselves, see the [api documentation code](git https://github.com/enviroweather/enviroweather_api_documentation)

    ## PREVIEW

    *in development / active only*

    This collection is reserved for requests that are not yet released to the development-stable or production environments. It currently has no requests in it.

    Once new preview endpoints are added to the source Postman collection, convert them here following the same pattern as the other `ewx_api_v1_stepN_*.py` notebooks (see [`ewx_api_v1_step1_tokens.py`](./ewx_api_v1_step1_tokens.py) for the environment/token boilerplate, and reuse `ewx_client.py`).
    """)
    return


@app.cell(hide_code=True)
def _():
    return


if __name__ == "__main__":
    app.run()
