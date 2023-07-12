from owlready2 import *
from flask import Flask, url_for, redirect, jsonify

app = Flask(__name__)
diagnostics = get_ontology("./ontologies/Diagnostic2.owl").load()
antibiotics = get_ontology("./ontologies/Antibiotics.owl").load()

@app.route("/")
def index():
    return redirect(url_for("diagnostic", iri=diagnostics.Diagnostic.iri))

@app.route("/diagnostic/<path:iri>")
def diagnostic(iri):
    diagnostic = IRIS[iri]
    html = "<nav>"
    paths = [i for i in sorted(diagnostic.ancestors(), key=lambda c: len(c.ancestors())) if i != Thing]
    html += " / ".join(["<a href='%s'>%s</a>" % (url_for("diagnostic", iri=i.iri), i.name) if i != diagnostic else i.name for i in paths])
    if len(list(diagnostic.subclasses())) > 0:
        html += " / <select onChange='location.href=this.value'><option value=''>--</option>"
        for child in diagnostic.subclasses():
            html += "<option value='%s'>%s</option>" % (url_for("diagnostic", iri=child.iri), child.name)
        html += "</select>"
    html += "</nav>"
    html += "<h1>%s</h1>" % diagnostic.name

    if len(list(diagnostic.Est_cause_par)) > 0:
        html += "<h2>Germes</h2>"
        germes = set()
        for cause in diagnostic.Est_cause_par:
            germe = antibiotics[cause.name]
            germes.add(germe)
            html += "<p>%s</p>" % germe.name
        html += "<h2>Agents</h2>"
    
        threshold = 3

        for antibiotic in antibiotics.search(subclass_of=antibiotics.Antimicrobial_Agents):
            spectrum = set(antibiotic.Is_effective_against)
            intersection = spectrum.intersection(germes)
            if len(intersection) == 0:
                continue
            is_cover = len(intersection) == len(germes)
            is_excesive = (len(spectrum) - len(intersection)) > threshold
            status = None
            if is_cover and is_excesive:
                status = "Excesive"
            elif is_cover and not is_excesive:
                status = "Suitable"
            elif not is_cover and is_excesive:
                status = "Poorly targeted"
            elif not is_cover and not is_excesive:
                status = "Insuffisant"
            html += "<p>%s (spectre: %d) (class %s) (cover: %s)</p>" % (antibiotic.name, len(spectrum), status, ", ".join((i.name for i in intersection)))
            html += "<b>%s</b>" % ",".join((i.name for i in intersection))
    return html

