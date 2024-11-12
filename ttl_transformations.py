from rdflib import Graph
import pystache
import os

# query sparql para obtneer los valores del test

query = """
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dcat: <http://www.w3.org/ns/dcat#>
PREFIX ftr: <https://www.w3id.org/ftr#>
PREFIX dqv: <http://www.w3.org/ns/dqv#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX doap: <http://usefulinc.com/ns/doap#>

SELECT DISTINCT ?s ?title ?label ?description ?keywords ?version ?indicator ?label_indicator ?desc_indicator ?license
?publisher ?metric ?creator_name ?creator_orcid
?web_repository
WHERE {
    ?s a ftr:Test .
    ?s dcterms:title ?title .
    ?s rdfs:label ?label .
    ?s dcterms:description ?description .
    ?s dcterms:license ?license .
    ?s dcterms:publisher ?publisher .
    ?s dcat:keyword ?keywords .
    ?s dcat:version ?version .
    ?s ftr:indicator ?indicator .
    ?indicator rdfs:label ?label_indicator .
    ?indicator dcterms:description ?desc_indicator .
    ?metric a dqv:Metric .
    ?repository doap:repository ?repo .
    ?repo foaf:homePage ?web_repository .
    ?s dcterms:creator ?creator_orcid .
    ?creator_orcid vcard:fn ?creator_name .
}
"""


query_metrics = """
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dcat: <http://www.w3.org/ns/dcat#> 
PREFIX ftr: <https://www.w3id.org/ftr#>
PREFIX dqv: <http://www.w3.org/ns/dqv#> 
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX doap: <http://usefulinc.com/ns/doap#>
PREFIX dqv: <http://www.w3.org/ns/dqv#> 
PREFIX dav: <https://example.org/ontology#> 

SELECT DISTINCT ?s ?title ?label ?description ?keywords ?version ?indimension ?label_dimension ?desc_indimension
?publisher ?test ?creator_name ?creator_orcid ?landing_page ?benchmark ?bm_title ?bm_desc ?metric_status
WHERE {
    ?s a dqv:Metric .
    ?s dcterms:title ?title .
    ?s rdfs:label ?label .
    ?s dcterms:description ?description .
    ?s dcterms:publisher ?publisher .
    ?s dcat:keyword ?keywords .
    ?s dcat:version ?version .
    ?s dcat:landingPage ?landing_page .
    ?s dqv:inDimension ?indimension .
    ?s ftr:metricStatus ?metric_status .
    ?s ftr:hasBenchmark ?benchmark . 
    ?indimension rdfs:label ?label_dimension .
    ?indimension dcterms:description ?desc_indimension .
    ?benchmark a dav:MetricBenchmark ;
        dcterms:title ?bm_title;
        dcterms:description ?bm_desc .
    ?test a ftr:Test .
    ?s dcterms:creator ?creator_orcid .
    ?creator_orcid vcard:fn ?creator_name .
}
"""


def ttl_to_html(path_ttl, path_mustache, query):
    """Create a html file from a ttl file"""
    g = Graph()
    g.parse(path_ttl, format="turtle")
    # Ejecutar la consulta
    results = g.query(query)

    data = {
        'test_identifier': '',
        'test_title': '',
        'test_name': '',
        'test_description': '',
        'test_keywords': '',
        'test_version': '',
        'test_uri_indicator': '',
        'test_indicator': '',
        'test_desc_indicator': '',
        'test_license': '',
        'test_publisher': '',
        'test_metric': '',
        'test_repository': '',
        'test_creators': ''
    }

    # como hay varias keywords normalemnte, las meto en un array y luego las uno en un string separadas por comas.
    keywords = []

    # lo mismo ocurre con los creadores que son dos
    creators = []
    creators_orcid = []
    for row in results:

        data['test_identifier'] = row.s
        data['test_title'] = row.title
        data['test_name'] = row.label
        data['test_description'] = row.description
        data['test_version'] = row.version
        data['test_uri_indicator'] = row.indicator
        data['test_indicator'] = row.label_indicator
        data['test_desc_indicator'] = row.desc_indicator
        data['test_license'] = row.license
        data['test_publisher'] = row.publisher
        data['test_metric'] = row.metric
        data['test_repository'] = row.web_repository
        keywords.append(str(row.keywords))

        if str(row.creator_name) not in creators:
            creators.append(str(row.creator_name))

        if str(row.creator_orcid) not in creators_orcid:
            creators_orcid.append(str(row.creator_orcid))

    all_keywords = ", ".join(keywords)

    # hay que hacer una transformación porque ahora tenemos dos arrays con los nombres y el orcid que debe ser el a href y queremos que aparecca esto:
    result = []
    for nombre, orcid in zip(creators, creators_orcid):
        result.append(f'<a href="{orcid}" target="_blank">{nombre}</a>')

    all_creators = ', '.join(result)

    data['test_keywords'] = all_keywords
    # en mustache he tenido que crear el mapeo con {{{test_creators}}} que asigna correctamente el texto.
    # si lo hubiese puesto {{test_creators}} como el resto de propiedades, me identiicaba los tags como texto y me mostraba el a href cuando lo
    # único que quería mostrar es el nombre.

    data['test_creators'] = all_creators

    # Cargar la plantilla mustache
    with open(path_mustache, 'r') as template_file:
        template_content = template_file.read()

    # sustituir la plantilla con los datos del diccionario
    renderer = pystache.Renderer()
    rendered_output = renderer.render(template_content, data)

    # guardamos el html. El path es el mismo que el ttl pero cambiando la extension
    path_html = os.path.splitext(path_ttl)[0] + '.html'

    with open(path_html, 'w') as output_file:
        output_file.write(rendered_output)

    print(f'Archivo creado: {path_html}')


def ttl_to_jsonld(path_ttl):
    """Create a jsonld file from a ttl file"""
    g = Graph()
    g.parse(path_ttl, format="turtle")
    # serializmos
    jsonld_data = g.serialize(format="json-ld", indent=4)
    # guardamos el json. El path es el mismo que el ttl pero cambiando la extension
    path_jsonld = os.path.splitext(path_ttl)[0] + '.jsonld'

    with open(path_jsonld, "w") as f:
        f.write(jsonld_data)

    print(f'Archivo creado: {path_jsonld}')


def ttl_to_html_metrics(path_ttl, path_mustache, query):

    g = Graph()
    g.parse(path_ttl, format="turtle")
    # Ejecutar la consulta
    results = g.query(query)

    data = {
        'metric_identifier': '',
        'metric_title': '',
        'metric_name': '',
        'metric_description': '',
        'metric_keywords': '',
        'metric_version': '',
        'metric_uri_inDimension': '',
        'metric_inDimension': '',
        'metric_desc_dimension': '',
        'metric_publisher': '',
        'metric_test': '',
        'metric_creators': '',
        'metric_landing_page': '',
        'metric_benchmark': '',
        'metric_benchmark_title': '',
        'metric_benchmark_desc': '',
        'metric_status': ''
    }

    # como hay varias keywords normalemnte, las meto en un array y luego las uno en un string separadas por comas.
    keywords = []

    # lo mismo ocurre con los creadores que son dos
    creators = []
    creators_orcid = []
    for row in results:

        data['metric_identifier'] = row.s
        data['metric_title'] = row.title
        data['metric_name'] = row.label
        data['metric_description'] = row.description
        data['metric_version'] = row.version
        data['metric_uri_inDimension'] = row.indimension
        data['metric_inDimension'] = row.label_dimension
        data['metric_desc_dimension'] = row.desc_indimension
        data['metric_publisher'] = row.publisher
        data['metric_test'] = row.test
        data['metric_landing_page'] = row.landing_page
        data['metric_benchmark'] = row.benchmark
        data['metric_benchmark_title'] = row.bm_title
        data['metric_benchmark_desc'] = row.bm_desc
        data['metric_status'] = row.metric_status
        keywords.append(str(row.keywords))

        if str(row.creator_name) not in creators:
            creators.append(str(row.creator_name))

        if str(row.creator_orcid) not in creators_orcid:
            creators_orcid.append(str(row.creator_orcid))

    all_keywords = ", ".join(keywords)

    result = []
    for nombre, orcid in zip(creators, creators_orcid):
        result.append(f'<a href="{orcid}" target="_blank">{nombre}</a>')

    all_creators = ', '.join(result)

    data['metric_keywords'] = all_keywords

    data['metric_creators'] = all_creators

    # Cargar la plantilla mustache
    with open(path_mustache, 'r') as template_file:
        template_content = template_file.read()

    # sustituir la plantilla con los datos del diccionario
    renderer = pystache.Renderer()
    rendered_output = renderer.render(template_content, data)

    # guardamos el html. El path es el mismo que el ttl pero cambiando la extension
    path_html = os.path.splitext(path_ttl)[0] + '.html'

    with open(path_html, 'w') as output_file:
        output_file.write(rendered_output)

    print(f'Archivo creado: {path_html}')


def iterate_paths(path, template, query, isTest):

    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".ttl"):
                # si encontramos el archivo ttl podemos llamar a las funciones de transformacion
                path_ttl = os.path.join(root, file)
                print(path_ttl)
                if isTest:
                    ttl_to_html(path_ttl, template, query)
                else:
                    ttl_to_html_metrics(path_ttl, template, query)

                ttl_to_jsonld(path_ttl)


# github paths
path_ttls_metrics = 'https://github.com/oeg-upm/fair_ontologies/tree/main/doc/metric/'
path_ttls = 'https://github.com/oeg-upm/fair_ontologies/tree/main/doc/test/'
path_mustache = 'https://github.com/oeg-upm/fair_ontologies/tree/main/doc/test/template.html'
path_mustache_metrics = 'https://github.com/oeg-upm/fair_ontologies/tree/main/doc/metrics/template_metrics.html'


iterate_paths(path_ttls_metrics, path_mustache_metrics, query_metrics, False)
iterate_paths(path_ttls, path_mustache, query, True)
