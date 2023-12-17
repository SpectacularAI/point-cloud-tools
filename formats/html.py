import os
import base64
import gzip
import io

from .splat import dataframe_to_flat_array

HTML_TEMPLATE = '../gsplat.js.html.template'
def dataframe_to_gsplat_html(df, fn, **kwargs):
    template_path = os.path.join(os.path.dirname(__file__), HTML_TEMPLATE)
    with open(template_path, 'rt') as f:
        html_template = f.read()
    
    splat_data = dataframe_to_flat_array(df, **kwargs)
    html = html_template.replace('CORS_SUCKS', base64.b64encode(splat_data.tobytes()).decode('utf-8'))
    
    with open(fn, 'wt') as f:
        f.write(html)
