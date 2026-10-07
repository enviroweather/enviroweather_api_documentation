# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo>=0.23.16",
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
    # Enviroweather API documentation (v1)

    ## Resource: common errors

    Reserved as a catalog of failing requests and how to interpret them. It currently has no examples in the source collection, but several real error responses are already documented inline in the other Step notebooks:

    - [`ewx_api_v1_step5_result_models.py`](./ewx_api_v1_step5_result_models.py) - `latestobstable` returning `"This model is not available."` with HTTP 200.
    - [`ewx_api_v1_step5a_complex_result_models.py`](./ewx_api_v1_step5a_complex_result_models.py) - seasonal gating errors (`"This model is available after 3/1."`) and bad-parameter errors (`"Biofix 2 must be after 5/30."`) for `applescab`, `orientalfruitmoth`, and `tomcast`.
    - [`ewx_api_v1_step3_dates.py`](./ewx_api_v1_step3_dates.py) and [`ewx_api_v1_step4_result_model_parameters.py`](./ewx_api_v1_step4_result_model_parameters.py) - the `/db2/resources/latestobstable/...` routes fail a *different* way: a plain HTTP `401` with `{"error": "Forbidden"}`, where `error` is a string instead of the usual boolean.

    The common thread: don't assume one error shape. Most endpoints return HTTP 200 with a JSON envelope (`error`/`message`/`status`/`data`) where a *successful* request can still carry `"error": true` - always check that field. But some routes (especially ones for retired/unavailable models) skip the envelope entirely and return a plain HTTP error status instead. Handle both.
    """)
    return


if __name__ == "__main__":
    app.run()
