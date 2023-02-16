import owlready2 as owl;

onto = owl.get_ontology("ontologies/Antibiotics.owl").load()

with onto:
    class Query(onto.Thing):
        equivalent_to = [onto.Antimicrobial_Agents & onto.Is_effective_against.some(onto.Anaerobes)]

    owl.sync_reasoner()
    q = Query(Is_effective_against=onto.Anaerobes)
    print(q) 