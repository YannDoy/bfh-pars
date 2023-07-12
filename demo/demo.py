from owlready2 import *

#
# BACKEND
#
ONTO_IRI = "https://yanndoy.ch/owl/demo/MyOwl.owl"
ONTO_FILE = "./ontologies/MyOnto.owl"

#
# LOADING ONTOLOGY
#
onto = get_ontology(ONTO_IRI).load(fileobj=open(ONTO_FILE, "rb"))

#
# DEMO
#
with onto:
    class Shape(Thing): pass
    class Round(Shape): pass
    class Rod(Shape): pass
    AllDisjoint([Round, Rod])

    class Grouping(Thing): pass
    class Isolated(Grouping): pass
    class InPair(Grouping): pass
    class InCluster(Grouping): pass
    class InChain(Grouping): pass
    class InSmallChain(InChain): pass
    class InLongChain(InChain): pass
    AllDisjoint([Isolated, InPair, InCluster, InChain])
    AllDisjoint([InSmallChain, InLongChain])

    class Bacterium(Thing): pass
    AllDisjoint([Bacterium, Shape, Grouping])

    class gram_positive(Bacterium >> bool, FunctionalProperty): pass
    class nb_colonies(Bacterium >> int, FunctionalProperty): pass
    class has_shape(Bacterium >> Shape, FunctionalProperty): pass
    class has_grouping(Bacterium >> Grouping): pass
    class is_shape_of(Shape >> Bacterium):
        inverse_property = has_shape
    has_shape.inverse_property = is_shape_of
    class Pseudomonas(Bacterium):
        is_a = [ has_shape.some(Rod) &
                has_shape.only(Rod) &
                has_grouping.some(Isolated | InPair) &
                gram_positive.value(False) ]

    class Coccus(Bacterium):
        is_a = [has_shape.only(Rod)]

    #onto.save(ONTO_FILE)
    sync_reasoner((onto,))
    print(Coccus.has_shape)
    print(Rod.INDIRECT_is_shape_of)