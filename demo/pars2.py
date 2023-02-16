import owlready2 as owl

diagnostic = owl.get_ontology("./ontologies/Diagnostic2.owl").load()
antibiotic = owl.get_ontology("./ontologies/Antibiotics.owl").load()
owl.sync_reasoner([diagnostic, antibiotic], infer_property_values=True)


result = [antibiotic[g.name] for g in diagnostic.Cap3.Est_cause_par]

print(antibiotic.Amoxicillin_Calvulanic.INDIRECT_Is_effective_against)
print(antibiotic.Enterococci.INDIRECT_Is_effective_against)
#print(result)