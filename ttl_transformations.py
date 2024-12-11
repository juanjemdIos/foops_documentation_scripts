from rdflib import Graph
import pystache
import os
import configparser
import markdown

# query test
query = """
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dcat: <http://www.w3.org/ns/dcat#>
PREFIX ftr: <https://www.w3id.org/ftr#>
PREFIX dqv: <http://www.w3.org/ns/dqv#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX doap: <http://usefulinc.com/ns/doap#>

SELECT DISTINCT ?s ?title ?label ?description ?keywords ?version ?indicator ?label_indicator ?desc_indicator ?license
?publisher ?metric ?creator_name ?creator_orcid ?contact_orcid ?contact_name ?contact_mail
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
    ?s dcat:contactPoint ?contact_orcid .
    ?contact_orcid vcard:fn ?contact_name .
    ?contact_orcid vcard:hasEmail ?contact_mail .
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

SELECT DISTINCT ?s ?title ?label ?description ?keywords ?version ?license ?indimension ?label_dimension ?desc_indimension
?publisher ?test ?creator_name ?creator_orcid ?landing_page ?benchmark ?bm_title ?bm_desc ?metric_status ?contact_orcid ?contact_name ?contact_mail
WHERE {
    ?s a dqv:Metric .
    ?s dcterms:title ?title .
    ?s rdfs:label ?label .
    ?s dcterms:description ?description .
    ?s dcterms:publisher ?publisher .
    ?s dcat:keyword ?keywords .
    ?s dcat:version ?version .
    ?s dcterms:license ?license .
    ?s dcat:landingPage ?landing_page .
    ?s dqv:inDimension ?indimension .
    ?s ftr:metricStatus ?metric_status .
    ?s ftr:hasBenchmark ?benchmark .
    ?indimension rdfs:label ?label_dimension .
    ?indimension dcterms:description ?desc_indimension .
    ?benchmark a ftr:Benchmark ;
        dcterms:title ?bm_title;
        dcterms:description ?bm_desc .
    ?test a ftr:Test .
    ?s dcterms:creator ?creator_orcid .
    ?creator_orcid vcard:fn ?creator_name .
    ?s dcat:contactPoint ?contact_orcid .
    ?contact_orcid vcard:fn ?contact_name .
    ?contact_orcid vcard:hasEmail ?contact_mail .
}
"""

query_benchmarks = """
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dcat: <http://www.w3.org/ns/dcat#>
PREFIX ftr: <https://www.w3id.org/ftr#>
PREFIX dqv: <http://www.w3.org/ns/dqv#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX doap: <http://usefulinc.com/ns/doap#>
PREFIX dqv: <http://www.w3.org/ns/dqv#>

SELECT DISTINCT ?s ?title ?label ?description ?keywords ?version ?license
 ?creator_name ?creator_orcid ?landing_page ?benchmark_status ?associatedMetric ?metricIdentifier ?metricLabel ?contact_orcid ?contact_name ?contact_mail
WHERE {
    ?s a ftr:Benchmark .
    ?s dcterms:title ?title .
    ?s rdfs:label ?label .
    ?s dcterms:description ?description .
    ?s dcat:keyword ?keywords .
    ?s dcat:version ?version .
    ?s dcterms:license ?license .
    ?s dcat:landingPage ?landing_page .
    ?s ftr:status ?benchmark_status .
    ?s dcterms:creator ?creator_orcid .
    ?creator_orcid vcard:fn ?creator_name .
    ?s ftr:associatedMetric ?associatedMetric .
    ?associatedMetric dcterms:identifier ?metricIdentifier .
    ?associatedMetric rdfs:label ?metricLabel .
    ?s dcat:contactPoint ?contact_orcid .
    ?contact_orcid vcard:fn ?contact_name .
    ?contact_orcid vcard:hasEmail ?contact_mail .
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
        'test_creators': '',
        'test_turtle': '',
        'test_contactName': '',
        'test_contactMail': ''
    }

    # como hay varias keywords normalemnte, las meto en un array y luego las uno en un string separadas por comas.
    keywords = []

    # lo mismo ocurre con los creadores que son dos
    creators = []
    creators_orcid = []

    contacts = []
    contacts_orcid = []
    contacts_mail = []

    for row in results:

        data['test_identifier'] = row.s
        data['test_title'] = row.title
        data['test_name'] = row.label
        data['test_description'] = markdown.markdown(row.description)
        data['test_version'] = row.version
        data['test_uri_indicator'] = row.indicator
        data['test_indicator'] = row.label_indicator
        data['test_desc_indicator'] = row.desc_indicator
        data['test_license'] = row.license
        data['test_publisher'] = row.publisher
        data['test_metric'] = row.metric
        data['test_repository'] = row.web_repository
        data['test_turtle'] = row.label + '.ttl'

        if str(row.keywords) not in keywords:
            keywords.append(str(row.keywords))

        if str(row.creator_name) not in creators:
            creators.append(str(row.creator_name))

        if str(row.creator_orcid) not in creators_orcid:
            creators_orcid.append(str(row.creator_orcid))

        if str(row.contact_name) not in contacts:
            contacts.append(str(row.contact_name))

        if str(row.contact_orcid) not in contacts_orcid:
            contacts_orcid.append(str(row.contact_orcid))

        if str(row.contact_mail) not in contacts_mail:
            contacts_mail.append(str(row.contact_mail))

    all_keywords = ", ".join(keywords)

    # hay que hacer una transformación porque ahora tenemos dos arrays con los nombres y el orcid que debe ser el a href y queremos que aparecca esto:
    result = []
    for nombre, orcid in zip(creators, creators_orcid):
        result.append(f'<a href="{orcid}" target="_blank">{nombre}</a>')

    result_contacts = []
    for nombre, mail, orcid in zip(contacts, contacts_mail, contacts_orcid):
        clean_mail = mail.replace('mailto:', '')
        result_contacts.append(
            f'<a href="{orcid}" target="_blank">{nombre}</a>: <a href="{mail}" target="_blank">{clean_mail}</a>')

    all_creators = ', '.join(result)
    all_contacts = ', '.join(result_contacts)

    data['test_keywords'] = all_keywords
    # en mustache he tenido que crear el mapeo con {{{test_creators}}} que asigna correctamente el texto.
    # si lo hubiese puesto {{test_creators}} como el resto de propiedades, me identiicaba los tags como texto y me mostraba el a href cuando lo
    # único que quería mostrar es el nombre.

    data['test_creators'] = all_creators
    data['test_contactPoint'] = all_contacts
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


def ttl_to_html_benchmarks(path_ttl, path_mustache, query):
    g = Graph()
    g.parse(path_ttl, format="turtle")
    # Ejecutar la consulta
    results = g.query(query)

    data = {
        'benchmark_identifier': '',
        'benchmark_title': '',
        'benchmark_name': '',
        'benchmark_description': '',
        'benchmark_keywords': '',
        'benchmark_version': '',
        'benchmark_license': '',
        'benchmark_creators': '',
        'benchmark_landing_page': '',
        'benchmark_metrics': '',
        'benchmark_status': '',
        'benchmark_turtle': '',
        'benchmark_contactName': '',
        'benchmark_contactMail': ''
    }

    # como hay varias keywords normalemnte, las meto en un array y luego las uno en un string separadas por comas.
    keywords = []

    # lo mismo ocurre con los creadores que son dos
    creators = []
    creators_orcid = []

    metrics = []
    metrics_uri = []

    contacts = []
    contacts_orcid = []
    contacts_mail = []

    for row in results:

        data['benchmark_identifier'] = row.s
        data['benchmark_title'] = row.title
        data['benchmark_name'] = row.label
        data['benchmark_description'] = markdown.markdown(row.description)
        data['benchmark_version'] = row.version
        data['benchmark_license'] = row.license
        data['benchmark_landing_page'] = row.landing_page
        data['benchmark_status'] = row.benchmark_status
        data['benchmark_turtle'] = row.label.replace('Benchmark ', '') + '.ttl'

        if str(row.keywords) not in keywords:
            keywords.append(str(row.keywords))

        if str(row.creator_name) not in creators:
            creators.append(str(row.creator_name))

        if str(row.creator_orcid) not in creators_orcid:
            creators_orcid.append(str(row.creator_orcid))

        if str(row.metricIdentifier) not in metrics_uri:
            metrics_uri.append(str(row.metricIdentifier))

        if str(row.metricLabel) not in metrics:
            metrics.append(str(row.metricLabel))

        if str(row.contact_name) not in contacts:
            contacts.append(str(row.contact_name))

        if str(row.contact_orcid) not in contacts_orcid:
            contacts_orcid.append(str(row.contact_orcid))

        if str(row.contact_mail) not in contacts_mail:
            contacts_mail.append(str(row.contact_mail))

        all_keywords = ", ".join(keywords)

        result = []
        for nombre, orcid in zip(creators, creators_orcid):
            result.append(f'<a href="{orcid}" target="_blank">{nombre}</a>')

        resultMetrics = []
        for nameMetric, uriMetric in zip(metrics, metrics_uri):
            resultMetrics.append(
                f'<a href="{uriMetric}" target="_blank">{nameMetric}</a>')

        result_contacts = []
        for nombre, mail, orcid in zip(contacts, contacts_mail, contacts_orcid):
            clean_mail = mail.replace('mailto:', '')
            result_contacts.append(
                f'<a href="{orcid}" target="_blank">{nombre}</a>: <a href="{mail}" target="_blank">{clean_mail}</a>')

        all_creators = ', '.join(result)
        all_metrics = ', '.join(resultMetrics)
        all_contacts = ', '.join(result_contacts)

    data['benchmark_keywords'] = all_keywords
    data['benchmark_creators'] = all_creators
    data['benchmark_metrics'] = all_metrics
    data['benchmark_contactPoint'] = all_contacts

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


def ttl_to_html_metrics(path_ttl, path_mustache, query):

    g = Graph()
    g.parse(path_ttl, format="turtle")

    results = g.query(query)

    data = {
        'metric_identifier': '',
        'metric_title': '',
        'metric_name': '',
        'metric_description': '',
        'metric_keywords': '',
        'metric_version': '',
        'metric_license': '',
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
        'metric_status': '',
        'metric_turtle': '',
        'metric_contactName': '',
        'metric_contactMail': ''
    }

    # como hay varias keywords normalemnte, las meto en un array y luego las uno en un string separadas por comas.
    keywords = []
    benchmarks = []
    benchmarks_title = []
    benchmarks_desc = []
    # lo mismo ocurre con los creadores que son dos
    creators = []
    creators_orcid = []

    contacts = []
    contacts_orcid = []
    contacts_mail = []

    for row in results:

        data['metric_identifier'] = row.s
        data['metric_title'] = row.title
        data['metric_name'] = row.label
        data['metric_description'] = markdown.markdown(row.description)
        data['metric_version'] = row.version
        data['metric_license'] = row.license
        data['metric_uri_inDimension'] = row.indimension
        data['metric_inDimension'] = row.label_dimension
        data['metric_desc_dimension'] = row.desc_indimension
        data['metric_publisher'] = row.publisher
        data['metric_test'] = row.test
        data['metric_landing_page'] = row.landing_page
        data['metric_status'] = row.metric_status
        data['metric_turtle'] = row.label.replace('Metric ', '') + '.ttl'

        if str(row.keywords) not in keywords:
            keywords.append(str(row.keywords))

        if str(row.creator_name) not in creators:
            creators.append(str(row.creator_name))

        if str(row.creator_orcid) not in creators_orcid:
            creators_orcid.append(str(row.creator_orcid))

        if str(row.benchmark) not in benchmarks:
            benchmarks.append(str(row.benchmark))
        if str(row.bm_title) not in benchmarks_title:
            benchmarks_title.append(str(row.bm_title))
        if str(row.bm_desc) not in benchmarks_desc:
            benchmarks_desc.append(str(row.bm_desc))

        if str(row.contact_name) not in contacts:
            contacts.append(str(row.contact_name))
        if str(row.contact_orcid) not in contacts_orcid:
            contacts_orcid.append(str(row.contact_orcid))
        if str(row.contact_mail) not in contacts_mail:
            contacts_mail.append(str(row.contact_mail))

    all_keywords = ", ".join(keywords)

    result = []
    for nombre, orcid in zip(creators, creators_orcid):
        result.append(f'<a href="{orcid}" target="_blank">{nombre}</a>')

    result_benchmarks = []
    #  <a href="{{metric_benchmark}}" target="_blank"> {{metric_benchmark_title}} </a>: {{metric_benchmark_desc}}
    for benchmark, title, desc in zip(benchmarks, benchmarks_title, benchmarks_desc):
        result_benchmarks.append(
            f'<a href="{benchmark}" target="_blank">{title}</a>: {desc}')

    result_contacts = []
    for nombre, mail, orcid in zip(contacts, contacts_mail, contacts_orcid):
        clean_mail = mail.replace('mailto:', '')
        result_contacts.append(
            f'<a href="{orcid}" target="_blank">{nombre}</a>: <a href="{mail}" target="_blank">{clean_mail}</a>')

    all_creators = ', '.join(result)
    all_benchmarks = '<br>'.join(result_benchmarks)
    all_contacts = ', '.join(result_contacts)

    data['metric_keywords'] = all_keywords
    data['metric_creators'] = all_creators
    data['metric_benchmarks'] = all_benchmarks
    data['metric_contactPoint'] = all_contacts
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


def iterate_paths(path, template, query, typeDoc):

    # param typeDoc
    # T : test
    # M : metric
    # B : benchmark

    for root, dirs, files in os.walk(path):
        if root == path:
            continue

        for file in files:
            if file.endswith(".ttl"):
                # si encontramos el archivo ttl podemos llamar a las funciones de transformacion
                path_ttl = os.path.join(root, file)
                match typeDoc:
                    case "T":
                        ttl_to_html(path_ttl, template, query)
                    case "M":
                        ttl_to_html_metrics(path_ttl, template, query)
                    case "B":
                        ttl_to_html_benchmarks(path_ttl, template, query)
                    case _:
                        print("Unknown type doc")

                ttl_to_jsonld(path_ttl)


# Cargar la configuración
config = configparser.ConfigParser()
config.read('config.ini')
current_dir = os.path.dirname(os.path.abspath(__file__))
# get paths
# template mustache
path_mustache_test = os.path.join(
    current_dir, "templates/template_test.html")
path_mustache_metrics = os.path.join(
    current_dir, "templates/template_metrics.html")
path_mustache_benchmarks = os.path.join(
    current_dir, "templates/template_benchmark.html")

# ttls test, metrics and benchmark
path_ttls = config.get('Paths', 'path_ttls').strip('"')
path_ttls_benchmarks = config.get('Paths', 'path_ttls_benchmarks').strip('"')
path_ttls_metrics = config.get('Paths', 'path_ttls_metrics').strip('"')

iterate_paths(path_ttls_metrics, path_mustache_metrics, query_metrics, 'M')
iterate_paths(path_ttls, path_mustache_test, query, 'T')
iterate_paths(path_ttls_benchmarks, path_mustache_benchmarks,
              query_benchmarks, 'B')
