import owlready2 as owl

class Diagnostics:
    def __init__(self, onto):
        self.onto = onto
        self.Disgnostic = Diagnostic
        self.Germ = Germ
        self.IsCausedBy = IsCausedBy
        with onto:
            class Diagnostic(owl.Thing): pass
            class Germ(owl.Thing): pass
            class IsCausedBy(Diagnostic >> Germ):
                python_name = "is_caused_by"
            class Diagnostic:
                is_a = [IsCausedBy.some(Germ)]