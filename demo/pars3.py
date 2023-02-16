from owlready2 import *

onto_path.append("./ontologies");
onto = get_ontology("./ontologies/Diagnostic2.owl")
onto.load()

q = onto.Germes()
q.Cause = [onto.Cap1]
sync_reasoner()
print(q.id)