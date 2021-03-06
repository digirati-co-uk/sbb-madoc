import json
from collections import OrderedDict
import logging
import ontospy
import requests
import argparse
from pyld import jsonld
from operator import itemgetter

import unicodecsv as csv

# global context document
with open('context.json', 'r') as context_file:
    master_context = json.load(context_file)
    del (master_context['@context']['dct'])  # remove unwanted alternative dcterms 'dct' prefix
    del (master_context['@context']['dcterm'])  # unwanted alternative dcterms 'dcterm' prefix
    del (master_context['@context']['sdo'])  # unwanted alternative schema.org prefix
    del (master_context['@context']['sorg'])  # unwanted alternative schema.org prefix


def initialise():
    """
    Return an OrderedDict comprising the list of fields in the CSV rows.
    :return: OrderedDict of fields
    """
    all_fields = OrderedDict([
        ('dcterms:identifier', None),
        ('dcterms:type', None),
        ('dcterms:hasPart', None),
        ('dcterms:title', None),
        ('rdfs:label', None),
        ('dcterms:description', None),
        ('dcterms:conformsTo', None),
        ('rdfs:range', None)],
    )
    crowds = ontospy.Ontospy(
        "https://raw.githubusercontent.com/digirati-co-uk/annotation-vocab/master/crowds.rdf")
    for p in crowds.all_properties:
        all_fields[p.qname] = None
    return all_fields


def get_model(uri):
    """
    Return a capture model as ordered JSON object
    :param uri: URI for capture model
    :return: ordered JSON object
    """
    if uri:
        r = requests.get(uri)
        if r.status_code == requests.codes.ok:
            source = r.text
            model = json.loads(source, object_pairs_hook=OrderedDict)
            return model
        else:
            return None
    else:
        return None


def parse_field(field_key, field_value, r_list):
    """
    Return a field as a key/value pair, normalising the keys to qnames, and the value to a single value,
    based on the o:id, @id and o:label, in that order.

    Return None, None for fields that don't fit this pattern.
    :param field_value: value for field
    :param field_key: key for field
    :param r_list: row list
    :return: key, value
    """
    # if field_key == u'o:id':
    #     return 'dcterms:identifier', field_value  # don't try to compact @ids
    if field_key == '@id':
        return None, None
    # compact using master context to reduce to qnames
    ck = jsonld.compact({field_key: field_value}, master_context)
    del (ck['@context'])  # remove the context
    if ck:
        for k, v in ck.items():
            if k == 'dcterms:hasPart':
                for z in v:
                    parse_expanded([z], row_list=r_list)
                return k, ';'.join([y['dcterms:identifier'] for y in v])
            if isinstance(v, dict):
                for x in ['o:id', '@id', 'o:label']:
                    if x in v:
                        return k, v[x]
                return None, None
            else:
                return k, v


def parse_expanded(model, row_list):
    """
    Parse and expanded capture model and generate dicts suitable for writing to CSV rows.
    :param row_list: empty list to append parsed rows to and return
    :param model: expanded JSON-LD
    :return: Python object mapped to CSV row headings
    """
    master_dict = initialise()
    for item in model:
        try:
            for k, v in item.items():  # iterate items in model
                if k and v:
                    parsed_key, parsed_value = parse_field(field_key=k, field_value=v, r_list=row_list)
                    if parsed_key in master_dict.keys():
                        master_dict[parsed_key] = parsed_value
            print(json.dumps(master_dict, indent=2))  # print work in progress
            row_list.append(master_dict)
        except:
            pass
    return row_list


def csv_generate(csv_filename, capturemodel_uri, delimiter='|'):
    """
    Generate a CSV from a JSON uri.

    Example URIs:

    NLW WW1 (production): 'https://crowd.library.wales/s/war-tribunal-records/annotation-studio/open/resource'
    NLW GLE (dev): 'http://nlw-omeka.digtest.co.uk/s/site-one/annotation-studio/open/resource'
    IDA: https://omeka.dlcs-ida.org/s/ida/annotation-studio/open/tagging

    :param csv_filename: output filename
    :param capturemodel_uri: uri for capturemodel json
    :param delimiter: delimiter for CSV
    """
    all_fields = initialise()
    with open(csv_filename, 'wb') as csv_out:  # open CSV and write header row
        dw = csv.DictWriter(
            csv_out, delimiter=delimiter, fieldnames=all_fields)
        dw.writeheader()
        # get the capture model
        capture_model = get_model(capturemodel_uri)
        capture_model['@context'] = master_context  # change to context with additional namespaces
        expanded = jsonld.expand(capture_model)  # expand the JSON-LD
        # recursively parse the expanded JSON-LD, returning a sorted list of dictionaries
        dw_list = sorted(parse_expanded(expanded, row_list=[]), key=itemgetter('dcterms:identifier'))
        for d in dw_list:
            dw.writerow(d)


def main():
    """
    Wrapper for csv_generate.

    Parse commandline args and convert capturemodel JSON from a URI to a CSV suitable for generating capture models
    using gen_json.

    JSON --> CSV
    Usage:

   python gen_csv.py -i https://crowd.library.wales/s/war-tribunal-records/annotation-studio/open/resource \
    -o exported_crowd_library_wales.csv

    """
    logging.basicConfig(filename='csv_generator.log', level=logging.DEBUG)
    parser = argparse.ArgumentParser(description='Simple JSON to CSV tool for annotation studio capture models.')
    parser.add_argument('-i', '--input', help='Input JSON uri', required=True)
    parser.add_argument('-o', '--output', help='Output CSV file name', required=True)
    parser.add_argument('-d', '--delimiter', help='CSV delimiter, defaults to |', required=False)
    args = parser.parse_args()
    if args.input and args.output:
        csv_generate(csv_filename=args.output, capturemodel_uri=args.input)


if __name__ == "__main__":
    main()
