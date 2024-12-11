# foops_documentation_scripts

Repository used to generate the JSON-LD and HTML catalogs for FOOPS!

First, the following repository must be downloaded to work on the different documents. Then, configure the config.ini file with the paths where all the material has been downloaded. This way, we avoid working directly with the GitHub API, which is more cumbersome and would require permissions and credentials to launch the registration process.

https://github.com/oeg-upm/fair_ontologies

```
path_ttls_benchmarks = "[USER_PATH]/Fair_Ontologies/doc/benchmark/"
path_ttls_metrics = "[USER_PATH]/Fair_Ontologies/doc/metric/"
path_ttls = "[USER_PATH]/Fair_Ontologies/doc/test/"
path_mustache = "[USER_PATH]/foops_documentation_scripts/templates/template.html"
path_mustache_metrics = "[USER_PATH]/foops_documentation_scripts/templates/template_metrics.html"
path_mustache_benchmarks = "[USER_PATH]/foops_documentation_scripts/templates/template_benchmark.html"
path_mustache_catalogo = "[USER_PATH]/foops_documentation_scripts/templates/template_catalog.html"
path_catalogo = "[USER_PATH]/Fair_Ontologies/doc/catalog.html"
```

If the TTL files or the template change location, these paths will need to be updated in the config file.

The process iterates recursively within the root, and if it finds a TTL file, it creates an equivalent file with the same name but with HTML and JSON-LD extensions.

The Mustache template is necessary to create the HTML file, and if any design modifications to the HTML are deemed necessary, they should be made in that template.

The script requires the rdflib and pystache libraries for proper operation. Both are included in the Bin folder.

The main page created from ttl_catalogue.py goes through all test folders and retrieves information to create a catalog item whenever it finds a ttl file in the folder.

It requires specifying the path where the test and metric folders are located and where the template is hosted, from which the catalog will be created to show the list of tests and metrics available.

```
path_ttls_benchmarks = "[USER_PATH]/Fair_Ontologies/doc/benchmark/"
path_ttls_metrics = "[USER_PATH]/Fair_Ontologies/doc/metric/"
path_ttls = "[USER_PATH]/Fair_Ontologies/doc/test/"
path_mustache_catalogo = "[USER_PATH]/foops_documentation_scripts/templates/template_catalog.html"
```

By using Markdown within the TTL file, we can customize the formatting of descriptions for all document types (tests, metrics, and benchmarks), resulting in a more user-friendly HTML presentation.

It is possible to register the tests hosted in the GitHub repository in Ostrails (https://tools.ostrails.eu) using the test_register script. All you need to do is configure the paths in the configuration file that the other scripts use. Specifically, these two paths:

```
path_url_register = "https://tools.ostrails.eu/fdp-index-proxy/proxy"
```

The script will register all the TTL files located in the configured path. If the test already exists in the registry, it will be modified.
