# foops_documentation_scripts

Repository used to generate the JSON-LD and HTML catalogs for FOOPS!

In order for the script to work correctly, the following paths have been configured in the config.ini file:
path_ttls_benchmarks = "https://github.com/oeg-upm/fair_ontologies/tree/main/doc/benchmark/"
path_ttls_metrics = "https://github.com/oeg-upm/fair_ontologies/tree/main/doc/metric/"
path_ttls = "https://github.com/oeg-upm/fair_ontologies/tree/main/doc/test/"
path_mustache = "https://github.com/oeg-upm/fair_ontologies/tree/main/doc/test/template.html"
path_mustache_metrics = "https://github.com/oeg-upm/fair_ontologies/tree/main/doc/metric/template_metrics.html"
path_mustache_benchmarks = "https://github.com/oeg-upm/fair_ontologies/tree/main/doc/benchmark/template_benchmark.html"
path_mustache_catalogo = "https://github.com/oeg-upm/fair_ontologies/tree/main/doc/catalog.html"
path_catalogo = "https://github.com/oeg-upm/fair_ontologies/tree/main/doc/catalog.html"

If the TTL files or the template change location, these paths will need to be updated in the config file.

The process iterates recursively within the root, and if it finds a TTL file, it creates an equivalent file with the same name but with HTML and JSON-LD extensions.

The Mustache template is necessary to create the HTML file, and if any design modifications to the HTML are deemed necessary, they should be made in that template.

The script requires the rdflib and pystache libraries for proper operation. Both are included in the Bin folder.

The main page created from ttl_catalogue.py goes through all test folders and retrieves information to create a catalog item whenever it finds a ttl file in the folder.

It requires specifying the path where the test and metric folders are located and where the template is hosted, from which the catalog will be created to show the list of tests and metrics availables.

path_ttls = 'https://github.com/oeg-upm/fair_ontologies/tree/main/doc/test/'
path_ttls_metric = 'https://github.com/oeg-upm/fair_ontologies/tree/main/doc/metric/'
path_ttls_benchmarks = "https://github.com/oeg-upm/fair_ontologies/tree/main/doc/benchmark/"
path_mustache = 'https://github.com/oeg-upm/fair_ontologies/tree/main/doc/template_catalog.html'.

By using Markdown within the TTL file, we can customize the formatting of descriptions for all document types (tests, metrics, and benchmarks), resulting in a more user-friendly HTML presentation.
