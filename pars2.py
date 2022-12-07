import owlready2 as owl

class Diagnostics:
    def __init__(self, onto):
        self.onto = onto.load()
        owl.sync_reasoner([onto])

    def list(self, name="Diagnostic"):
        return list(self.onto.get(name).subclasses())

    def cap3(self):
        return list(self.onto.Cap3.Est_cause_par)

diagnostics = Diagnostics(onto=owl.get_ontology("./ontologies/Diagnostic2.owl"))

print(diagnostics.cap3())