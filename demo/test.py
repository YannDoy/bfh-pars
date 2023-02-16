from owlready2 import *
import types

onto = get_ontology("./ontologies/test.owl")

with onto:
    class Diagnostic(Thing):
        pass

    class Germ(Thing):
        pass

    class cause_by_germs(ObjectProperty):
        domain = [Diagnostic]
        range = [Germ]

    class cause_diagnostic(ObjectProperty):
        domain = [Germ]
        range = [Diagnostic]
        inverse = cause_by_germs

    cause_by_germs.inverse = cause_diagnostic


    class GermCat1(Germ):
        pass

    class GermCat1A(GermCat1):
        pass        

    class DiagCat1(Diagnostic):
        pass

    class DiagCat1A(DiagCat1):
        is_a = [cause_by_germs.some(GermCat1A)]

    sync_reasoner()

    print(owl.search(cause_diagnostic=DiagCat1A))




