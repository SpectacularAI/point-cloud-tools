import os
import numpy as np
import base64
import gzip
import io
import math

from .splat import dataframe_to_flat_array

DEFAULT_HTML_TEMPLATE = '../gsplat.js.html.template'
def dataframe_to_gsplat_html(df, fn, html_template='', **kwargs):
    if len(html_template) == 0:
        html_template = os.path.join(os.path.dirname(__file__), DEFAULT_HTML_TEMPLATE)
    with open(html_template, 'rt') as f:
        html = f.read()

    splat_data = dataframe_to_flat_array(df, **kwargs)

    html = html.replace('CORS_SUCKS', base64.b64encode(splat_data.tobytes()).decode('utf-8'))

    with open(fn, 'wt') as f:
        f.write(html)
