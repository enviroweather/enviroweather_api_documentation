import marimo

__generated_with = "0.25.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

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

    ## Contents

    - [ewx_api_v1_quickstart](ewx_api_v1_quickstart.html)
    - [step1_tokens](ewx_api_v1_step1_tokens.html)
    - [step2_weather_stations](ewx_api_v1_step2_weather_stations.html)
    - [step3_dates](ewx_api_v1_step3_dates.html)
    - [step4_result_model_parameters](ewx_api_v1_step4_result_model_parameters.html)
    - [step4a_complex_result_model_parameters](ewx_api_v1_step4a_complex_result_model_parameters.html)
    - [step5_result_models](ewx_api_v1_step5_result_models.html)
    - [step5a_complex_result_models](ewx_api_v1_step5a_complex_result_models.html)
    """)
    return


if __name__ == "__main__":
    app.run()
