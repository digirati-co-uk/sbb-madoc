# berlin-models
Capture models and associated helpers for Berlin madoc instance.


## Python Code

`gen_json.py` -- can generate capture model JSON for import into Omeka S from a CSV file.


### Usage

N.B. you will need a Python 3 environment or virtualenv with the `requirements.txt` requirements installed, and a local copy of the two JSON `@context` files.

#### Gen JSON

The capture model tools can be run on the commandline, with commandline arguments passed in. The arguments are as follows:

```
 '-i', '--input', help='Input CSV file name', required=True
 '-o', '--output', help='Output JSON file name', required=True
 '-b', '--url_base', help='Base url for the Omeka instance', required=False
 '-t', '--top_index', help='Numbered element to treat as the top level group', required=False
 '-g', '--group_id', help='ID for the Crowd Source Group resource template', required=False
 '-e', '--element_id', help='ID for the Crowd Source Element resource template', required=False
 '-c', '--irclass', help='ID for the Interactive Resource class', required=False
 '-u', '--user', help='Omeka User ID for the Owner', required=False
 '-x', '--context', help='IDA Context', required=False
```

##### Input

The tool expects a pipe-delimited '|' file, with column heads as per `template.csv` provided as part of this repo.

e.g.

`-i berlin_choice.csv`

###### Output

The tool will produce a JSON-LD document.

e.g.

`-o berlin_choice.json`

##### URL Base

The JSON-LD uses the address of the server where the model will be deployed throughout, to ensure correct `@id`s that will resolve.

e.g.  

`-b https://omeka.staatsbibliothek-berlin.de`

##### Top Index

The CSV should use numbered identifiers in each row, under the `dcterms:identifier` column.

`-t 1`

tells the tool to start building the model with the row numbered `1`.

The `-g` parameter should be the Omeka ID (integer) for the Crowd Source Group template.

The `-e` parameter should be the Omeka ID (integer) for the Crowd Source Element template.

#### Example

```bash
python gen_json.py -i berlin_choice.csv -o berlin_choice.json -t 1 -g 3 -e 2 -u 1 -b https://omeka.staatsbibliothek-berlin.de
```

## Models

* `berlin_choice.json` - new model, for Madoc, with the two Berlin CSVs provided as choices. N.B. English is used. I expect that the Staatsbibliothek may want to replace these with German.


## License

MIT License

Copyright Digirati (c) 2019

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.