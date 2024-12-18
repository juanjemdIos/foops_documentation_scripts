from rdflib import Graph
import pystache
import os
import configparser
import argparse
import sys
# query para extraer los tres datos que necesitamos de cada ttl para mostrar en el catálogo de test y de metrics

query = """
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX ftr: <https://www.w3id.org/ftr#>
PREFIX dcat: <http://www.w3.org/ns/dcat#> 

SELECT DISTINCT ?s ?title ?label ?version ?keywords ?license ?license_label
WHERE {
    ?s a ftr:Test .
    ?s dcterms:title ?title .
    ?s rdfs:label ?label .
    ?s dcat:version ?version .
    ?s dcat:keyword ?keywords .
    ?s dcterms:license ?license .
}
"""

query_metric = """
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dqv: <http://www.w3.org/ns/dqv#>
PREFIX dcat: <http://www.w3.org/ns/dcat#> 

SELECT DISTINCT ?s ?title ?label ?version ?keywords ?license ?license_label
WHERE {
    ?s a dqv:Metric .
    ?s dcterms:title ?title .
    ?s rdfs:label ?label .
    ?s dcat:version ?version .
    ?s dcat:keyword ?keywords .
    ?s dcterms:license ?license .

}
"""

query_benchmark = """
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dqv: <http://www.w3.org/ns/dqv#>
PREFIX dcat: <http://www.w3.org/ns/dcat#> 
PREFIX ftr: <https://www.w3id.org/ftr#>

SELECT DISTINCT ?s ?title ?label ?version ?keywords ?license ?license_label
WHERE {
    ?s a ftr:Benchmark .
    ?s dcterms:title ?title .
    ?s rdfs:label ?label .
    ?s dcat:version ?version .
    ?s dcat:keyword ?keywords .
    ?s dcterms:license ?license .

}
"""


def ttl_to_item_catalogue(path_ttl, pquery):

    g = Graph()
    g.parse(path_ttl, format="turtle")
    # Ejecutar la consulta
    results = g.query(pquery)

    data = {}
    keywords = []

    for row in results:

        data = {
            'identifier': row.s,
            'title': row.title,
            'name': row.label,
            'version': row.version,
            'license': row.license
        }
        # transform uri license in label license more readable
        label_license = ""

        if row.license and row.license.strip() != "":
            parts_uri = row.license.strip('/').split('/')
            if "creativecommons" in row.license.lower():
                label_license = ('CC-' + '-'.join(parts_uri[-2:])).upper()
            else:
                label_license = ('-'.join(parts_uri[-2:])).upper()

        data['license_label'] = label_license

        if str(row.keywords) not in keywords:
            keywords.append(str(row.keywords))

    all_keywords = ", ".join(keywords)
    data['keywords'] = all_keywords

    return data


def item_to_list(path, list, query, type_doc):

    match type_doc:
        case "T":
            subfolder = 'test'
        case "M":
            subfolder = 'metric'
        case "B":
            subfolder = 'benchmark'
        case _:
            print("Unknown type doc")

    path_source = os.path.join(path, subfolder)

    for root, _, files in os.walk(path_source):
        for file in files:
            if file.endswith(".ttl"):
                # si encontramos el archivo ttl podemos llamar a las funciones de transformacion
                path_ttl = os.path.join(root, file)
                list.append(ttl_to_item_catalogue(path_ttl, query))


def main():
    ''' 
        init function
    '''
    parser = argparse.ArgumentParser(description="Script managed files .ttl")
    parser.add_argument('-i', help="Source path of ttls", required=True)
    parser.add_argument(
        '-o', help="Destination path of files ttl, html and json-ld", required=False)

    current_dir = os.path.dirname(os.path.abspath(__file__))
    config = configparser.ConfigParser()
    config.read('config.ini')

    args = parser.parse_args()
    path_source = args.i
    path_destination = args.o

    print(f"Using path_source: {path_source}")
    print(f"Using path_destination: {path_destination}")

    # Construye el path completo al archivo
    path_mustache_catalogo = os.path.join(
        current_dir, "templates/template_catalog.html")

    # ttls test, metrics and benchmark
    # path_ttls = config.get('Paths', 'path_ttls').strip('"')
    # path_ttls_benchmarks = config.get('Paths', 'path_ttls_benchmarks').strip('"')
    # path_ttls_metrics = config.get('Paths', 'path_ttls_metrics').strip('"')

    # html catalog
    path_catalogo = config.get('Paths', 'path_catalogo').strip('"')

    tests = []
    metrics = []
    benchmarks = []

    # item_to_list(path_ttls, tests, query)
    # item_to_list(path_ttls_metrics, metrics, query_metric)
    # item_to_list(path_ttls_benchmarks, benchmarks, query_benchmark)

    item_to_list(path_source, tests, query, "T")
    item_to_list(path_source, metrics, query_metric, "M")
    item_to_list(path_source, benchmarks, query_benchmark, "B")
    # sorted list of test and metrics by name
    tests_sorted = sorted(tests, key=lambda x: x["name"])
    metrics_sorted = sorted(metrics, key=lambda x: x["name"])
    benchmarks_sorted = sorted(benchmarks, key=lambda x: x["name"])

    # extraer su uri, name y descrpción. El identificador deberá tener como href el html creado en el proceso previo
    with open(path_mustache_catalogo, 'r') as template_file:
        template_content = template_file.read()

    # sustituir la plantilla con los datos del diccionario
    renderer = pystache.Renderer()
    rendered_output = renderer.render(
        template_content, {'tests': tests_sorted,
                           'metrics': metrics_sorted, 'benchmarks': benchmarks_sorted})

    with open(path_catalogo, 'w') as output_file:
        output_file.write(rendered_output)


if __name__ == "__main__":
    main()
