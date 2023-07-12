from owlready2 import *
from flask import Flask, url_for, request

app = Flask(__name__)
onto = get_ontology("../ontologies/Patient_Ex.xml.owl").load()


def render(content):
    return """
        <html>
            <nav>
                <a href="/">Root</a>
                <!--<form method="GET" action="/search">
                    <input type="text" placeholder="IRI" name="iri">
                    <input type="text" placeholder="Subclass" name="subclass_of">
                    <input type="text" placeholder="Class" name="is_a">
                    <button type="submit">Search</button>
                </form>-->
            </nav>
            %s
        </html>
    """ % content

@app.route('/')
def ontology_page():
    html = """<h2>'%s' ontology</h2>""" % onto.base_iri
    html += """<h3>Root classes</h3>"""
    for Class in Thing.subclasses():
        html += """<p><a href="%s">%s</a></p>""" % (url_for("class_page", iri = Class.iri), Class.name)
    return render(html)

@app.route('/class/<path:iri>')
def class_page(iri):
    Class = IRIS[iri]
    html = """<h2>'%s' class</h2>""" % Class.name
    html += """<h3>superclasses</h3>"""
    for SuperClass in Class.is_a:
        if isinstance(SuperClass, ThingClass):
            html += """<p><a href="%s">%s</a></p>""" % (url_for("class_page", iri = SuperClass.iri), SuperClass.name)
        else:
            html += """<p>%s</p>""" % SuperClass
    html += """<h3>equivalent classes</h3>"""
    for EquivClass in Class.equivalent_to:
        html += """<p>%s</p>""" % EquivClass
    html += """<h3>Subclasses</h3>"""
    for SubClass in Class.subclasses():
        html += """<p><a href="%s">%s</a></p>""" % (url_for("class_page", iri = SubClass.iri), SubClass.name)
    return render(html)


@app.route("/search")
def search():
    return request.args

@app.route("/diagnostics")
def diagnostics():
    html = "<h1>Diagnostics</h1>"
    for diagnostic in onto.search(subclass_of=onto.Diagnostic):
        html += """<p><a href="%s">%s</a></p>""" % (url_for("diagnostic", iri = diagnostic.iri), diagnostic.name)
    return render(html)

@app.route("/diagnostics/<path:iri>")
def diagnostic(iri):
    diagnostic = IRIS[iri]
    html = "<h1>%s</h1>" % iri
    html += "<h3>Germes</h3>"
    for germe in diagnostic.Est_cause_par:
        html += """<p><a href="%s">%s</a></p>""" % (url_for("class_page", iri = germe.iri), germe.name)
    return render(html)