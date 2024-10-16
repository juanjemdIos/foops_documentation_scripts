from rdflib import Graph
import pystache
import os

# query para extraer los tres datos que necesitamos de cada ttl

query = """
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX ftr: <https://www.w3id.org/ftr#>

SELECT DISTINCT ?s ?title ?label
WHERE {
    ?s a ftr:Test .
    ?s dcterms:title ?title .
    ?s rdfs:label ?label .
}
"""


def ttl_to_item_catalogue(path_ttl, path_mustache, query):

    g = Graph()
    g.parse(path_ttl, format="turtle")
    # Ejecutar la consulta
    results = g.query(query)

    data = {}

    for row in results:
        data = {
            'identifier': row.s,
            'title': row.title,
            'name': row.label
        }

    return data


# recorrer las carpetas desde la raiz y obtener los que tengan un ttl
path_ttls = 'https://github.com/oeg-upm/fair_ontologies/tree/main/doc/test/'
path_mustache = 'https://github.com/oeg-upm/fair_ontologies/tree/main/doc/template_catalog.html'
path_catalogo = 'https://github.com/oeg-upm/fair_ontologies/tree/main/doc/catalog.html'

tests = []

for root, dirs, files in os.walk(path_ttls):
    for file in files:
        if file.endswith(".ttl"):
            # si encontramos el archivo ttl podemos llamar a las funciones de transformacion
            path_ttl = os.path.join(root, file)
            tests.append(ttl_to_item_catalogue(path_ttl, path_mustache, query))


# Ordeno la lista por el nombre el TEST
tests_ordenados = sorted(tests, key=lambda x: x["name"])
# extraer su uri, name y descrpción. El identificador deberá tener como href el html creado en el proceso previo
with open(path_mustache, 'r') as template_file:
    template_content = template_file.read()

# sustituir la plantilla con los datos del diccionario
renderer = pystache.Renderer()
rendered_output = renderer.render(template_content, {'tests': tests_ordenados})

with open(path_catalogo, 'w') as output_file:
    output_file.write(rendered_output)
