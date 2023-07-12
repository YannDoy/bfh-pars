from owlready2 import *

#
# BACKEND
#
ONTO_FILE = "./ontologies/Diagnostic2.owl"

#
# LOADING ONTOLOGY
#
onto = get_ontology(ONTO_FILE).load(reload_if_newer=True)

#
# DEMO
#
print(list(default_world.sparql("""
SELECT ?y {
    ?y rdfs:subClassOf* <http://www.semanticweb.org/souhir/ontologies/diagnostic#Cap3>.
}
""")))