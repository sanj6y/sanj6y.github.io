#!/usr/bin/env python3

import json, yaml
from jinja2 import Environment, FileSystemLoader, BaseLoader, DebugUndefined
from jinja2_markdown import MarkdownExtension
from glob import glob
from pathlib import Path
import datetime
from tqdm import tqdm


# create an empty dictionary to store template variables to be passed
data=dict()

# add today's date, properly formatted, to the datadict to display at the bottom
# of the page
data['today'] = datetime.date.today().strftime('%Y-%m-%d')

# load assets that can be used by templates. assets are yaml files with data
for pathname in tqdm(glob('assets/*.y*ml'), desc='Loading assets'):
    path = Path(pathname)
    fname = path.stem
    with path.open('r') as f:
        assetdata = yaml.load(f, Loader=yaml.SafeLoader)
    if type(assetdata) is not dict:
        assetdata = {fname: assetdata}
    data.update(assetdata)

# scan sections in the sections directory; there will be a section header for
# each one of these
data['sections'] = []
sectionfiles = glob('sections/*.html')
try:
    order = yaml.load(Path('sections/order.yaml').open('r'),
                      Loader=yaml.SafeLoader)
    comparator = lambda key: (order + [Path(key).stem]).index(Path(key).stem)
except FileNotFoundError:
    comparator = lambda key: key
for sectionfile in tqdm(sorted(sectionfiles, key=comparator), 
                        desc='Processing sections'):
    sectionfile = Path(sectionfile)
    fname = sectionfile.stem
    sectionenv = Environment(loader=BaseLoader, 
                             extensions=['jinja2_markdown.MarkdownExtension'],
                             undefined=DebugUndefined)
    sectiontempl = sectionenv.from_string(sectionfile.read_text())
    data['sections'] += [dict(name=fname, content=sectiontempl.render(**data))]

# create a jinja2 environment instance
jinja_env = Environment(loader=FileSystemLoader('templates'), 
                        extensions=['jinja2_markdown.MarkdownExtension'],
                        undefined=DebugUndefined)
# get template
template = jinja_env.get_template('landing.html')

# render template and output it to index.html, the default page to show
with Path('index.html').open('w') as out:
    out.write(template.render(**data))
