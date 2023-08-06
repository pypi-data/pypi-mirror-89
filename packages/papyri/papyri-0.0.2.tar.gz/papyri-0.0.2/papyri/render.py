import json
import os
from collections import defaultdict
from pathlib import Path
from there import print

from jinja2 import Environment, FileSystemLoader, select_autoescape
from quart_trio import QuartTrio

from .config import html_dir, ingest_dir
from .crosslink import load_one, resolve_, IngestedBlobs, paragraph, paragraphs, P2
from .stores import BaseStore, GHStore, Store
from .take2 import Lines, Paragraph, make_block_3
from .utils import progress
from collections import OrderedDict


def unreachable(obj):
    assert False, f"Unreachable: {obj}"

class CleanLoader(FileSystemLoader):
    """
    A loader for ascii/ansi that remove all leading spaces and pipes  until the last pipe.
    """

    def get_source(self, *args, **kwargs):
        (source, filename, uptodate) = super().get_source(*args, **kwargs)
        return until_ruler(source), filename, uptodate


def until_ruler(doc):
    """
    Utilities to clean jinja template;

    Remove all ``|`` and `` `` until the last leading ``|``

    """
    lines = doc.split("\n")
    new = []
    for l in lines:

        while len(l.lstrip()) >= 1 and l.lstrip()[0] == "|":
            l = l.lstrip()[1:]
        new.append(l)
    return "\n".join(new)


from pygments import lex
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter


def get_classes(code):
    list(lex(code, PythonLexer()))
    FMT = HtmlFormatter()
    classes = [FMT.ttype2class.get(x) for x, y in lex(code, PythonLexer())]
    classes = [c if c is not None else "" for c in classes]
    return classes


def root():
    store = Store(ingest_dir)
    files = store.glob("*/module/*.json")

    env = Environment(
        loader=FileSystemLoader(os.path.dirname(__file__)),
        autoescape=select_autoescape(["html", "tpl.j2"]),
    )
    env.globals["isstr"] = lambda x: isinstance(x, str)
    env.globals["len"] = len
    template = env.get_template("root.tpl.j2")
    filenames = [_.name[:-5] for _ in files if _.name.endswith(".json")]
    tree = {}
    for f in filenames:
        sub = tree
        parts = f.split(".")
        for i, part in enumerate(parts):
            if part not in sub:
                sub[part] = {}
            sub = sub[part]

        sub["__link__"] = f

    return template.render(tree=tree)


async def gallery(module, store):

    from pathlib import Path
    import json

    from papyri.crosslink import IngestedBlobs

    figmap = []
    for p in store.glob(f"{module}/module/*.json"):
        data = json.loads(await p.read_text())
        i = IngestedBlobs.from_json(data)

        for k in {u[1] for u in i.example_section_data if u[0] == "fig"}:
            figmap.append((p.parts[-3], k, p.name[:-5]))

    env = Environment(
        loader=FileSystemLoader(os.path.dirname(__file__)),
        autoescape=select_autoescape(["html", "tpl.j2"]),
    )
    env.globals["len"] = len
    env.globals["paragraph"] = paragraph
    env.globals["len"] = len

    return env.get_template("gallery.tpl.j2").render(figmap=figmap)


# here we compute the siblings at each level; as well as one level down
# this is far from efficient and a hack, but it helps with navigation.
# I'm pretty sure we load the full library while we could
# load only the current module id not less, and that this could
# be done at ingest time or cached.
# So basically in the breadcrumps
# IPython.lib.display.+
#  - IPython will be siblings with numpy; scipy, dask, ....
#  - lib (or "IPython.lib"), with "core", "display", "terminal"...
#  etc.
#  - + are deeper children's
#
# This is also likely a bit wrong; as I'm sure we want to only show
# submodules or sibling modules and not attribute/instance of current class,
# though that would need loading the files and looking at the types of
# things. likely want to store that in a tree somewhere But I thing this is
# doable after purely as frontend thing.

def compute_siblings(ref, family):
    parts = ref.split(".") + ["+"]
    siblings = OrderedDict()
    cpath = ""
    # TODO: move this at ingestion time for all the non-top-level.
    for i, part in enumerate(parts):
        sib = list(
            sorted(
                set(
                    [
                        ".".join(s.split(".")[: i + 1])
                        for s in family
                        if s.startswith(cpath) and "." in s
                    ]
                )
            )
        )
        siblings[part] = [(s, s.split(".")[-1]) for s in sib]
        cpath += part + "."
    if not siblings["+"]:
        del siblings["+"]
    print(siblings.keys())
    return siblings


def make_tree(names):    
    from collections import defaultdict, OrderedDict
    rd = lambda: defaultdict(rd)
    tree = defaultdict(rd)

    for n in names:
        parts = n.split('.')
        branch = tree
        for p in parts:
            branch = branch[p]
    return tree

def cs2(ref, tree):
    parts = ref.split('.')+["+"]
    siblings = OrderedDict()
    cpath = ""
    branch = tree
    for p in parts:
        res = list(sorted([(f"{cpath}{k}",k) for k in branch.keys() if k != '+']))
        if res:
            siblings[p] = res
        else:
            break
        
        branch = branch[p]
        cpath += p + "."
    return siblings
    
        
async def _route(ref, store):
    assert isinstance(store, BaseStore)
    assert ref != "favicon.ico"
    assert not ref.endswith(".html")

    env = Environment(
        loader=FileSystemLoader(os.path.dirname(__file__)),
        autoescape=select_autoescape(["html", "tpl.j2"]),
    )
    env.globals["len"] = len
    env.globals["paragraph"] = paragraph
    env.globals["len"] = len

    template = env.get_template("core.tpl.j2")

    root = ref.split(".")[0]

    papp_files = store.glob(f"{root}/papyri.json")
    for p in papp_files:
        aliases = json.loads(await p.read_text())


    family = sorted(list(store.glob("*/module/*.json")))
    family = [str(f.name)[:-5] for f in family]

    siblings = compute_siblings(ref, family)

    # End computing siblings.

    file_ = store / root / "module" / f"{ref}.json"
    if await file_.exists():
        # The reference we are trying to view exists;
        # we will now just render it.
        bytes_ = await file_.read_text()
        brpath = store / root / "module" / f"{ref}.br"
        if await brpath.exists():
            br = await brpath.read_text()
        else:
            br = None
        all_known_refs = frozenset({str(x.name)[:-5] for x in store.glob("*/module/*.json")})
        #env.globals["unreachable"] = unreachable
        env.globals["unreachable"] = lambda x: "UNREACHABLELLLLL"+str(x)


        doc_blob = load_one(bytes_, br)
        prepare_doc(doc_blob, ref, all_known_refs)
        return render_one(
            template=template,
            doc=doc_blob,
            qa=ref,
            ext="",
            parts=siblings,
            backrefs=doc_blob.backrefs,
            pygment_css=HtmlFormatter(style="pastie").get_style_defs(".highlight"),
        )
    else:
        # The reference we are trying to render does not exists
        # just try to have a nice  error page and try to find local reference and
        # use the phantom file to list the backreferences to this.
        # it migt be a page, or a module we do not have documentation about.
        r = ref.split(".")[0]
        this_module_known_refs = [
            str(s.name)[:-5] for s in store.glob(f"{r}/module/{ref}*.json")
        ]
        brpath = store / "__phantom__" / f"{ref}.json"
        if await brpath.exists():
            br = json.loads(await brpath.read_text())
        else:
            br = []

        # compute a tree from all the references we have to have a nice browsing
        # interfaces.
        tree = {}
        for f in this_module_known_refs:
            sub = tree
            parts = f.split(".")[len(ref.split(".")) :]
            for i, part in enumerate(parts):
                if part not in sub:
                    sub[part] = {}
                sub = sub[part]

            sub["__link__"] = f

        error = env.get_template("404.tpl.j2")
        return error.render(backrefs=list(set(br)), tree=tree, ref=ref)


def img(subpath):
    with open(ingest_dir / subpath, "rb") as f:
        return f.read()


def static(name):
    here = Path(os.path.dirname(__file__))

    def f():
        return (here / name).read_bytes()

    return f


def logo():

    path = os.path.abspath(__file__)
    dir_path = Path(os.path.dirname(path))
    with open((dir_path / "papyri-logo.png"), "rb") as f:
        return f.read()


def serve():

    app = QuartTrio(__name__)

    async def r(ref):
        return await _route(ref, Store(str(ingest_dir)))

    async def g(module):
        return await gallery(module, Store(str(ingest_dir)))

    async def gr():
        return await gallery("*", Store(str(ingest_dir)))

    # return await _route(ref, GHStore(Path('.')))

    app.route("/logo.png")(logo)
    app.route("/favicon.ico")(static("favicon.ico"))
    app.route("/<ref>")(r)
    app.route("/img/<path:subpath>")(img)
    app.route("/gallery/")(gr)
    app.route("/gallery/<module>")(g)
    app.route("/")(root)
    port = os.environ.get("PORT", 5000)
    print("Seen config port ", port)
    prod = os.environ.get("PROD", None)
    if prod:
        app.run(port=port, host="0.0.0.0")
    else:
        app.run(port=port)


def render_one(
    template, doc: IngestedBlobs, qa, ext, *, backrefs, pygment_css=None, parts={}
):
    """
    Return the rendering of one document

    Parameters
    ----------
    template
        a Jinja@ template object used to render.
    doc : DocBlob
        a Doc object with the informations for current obj
    qa : str
        fully qualified name for current object
    ext : str
        file extension for url  – should likely be removed and be set on the template
        I think that might be passed down to resolve maybe ?
    backrefs : list of str
        backreferences of document pointing to this.
    parts : Dict[str, list[(str, str)]
        used for navigation and for parts of the breakcrumbs to have navigation to siblings.
        This is not directly related to current object.

    """
    # TODO : move this to ingest likely.
    # Here if we have too many references we group them on where they come from.
    if len(backrefs) > 30:

        b2 = defaultdict(lambda: [])
        for ref in backrefs:
            mod, _ = ref.split(".", maxsplit=1)
            b2[mod].append(ref)
        backrefs = (None, b2)
    else:
        backrefs = (backrefs, None)


    try:
        return template.render(
            doc=doc,
            qa=qa,
            version=doc.version,
            module=qa.split(".")[0],
            backrefs=backrefs,
            ext=ext,
            parts=parts,
            pygment_css=pygment_css,
        )
    except Exception as e:
        raise ValueError("qa=", qa) from e


async def _ascii_render(name, store=None):
    if store is None:
        store = Store(ingest_dir)
    ref = name
    root = name.split(".")[0]

    env = Environment(
        loader=CleanLoader(os.path.dirname(__file__)),
        lstrip_blocks=True,
        trim_blocks=True,
    )
    env.globals["len"] = len
    env.globals["paragraph"] = paragraph
    template = env.get_template("ascii.tpl.j2")

    known_refs = frozenset({x.name[:-5] for x in store.glob("*/module/*.json")})
    bytes_ = await (store / root / "module" / f"{ref}.json").read_text()
    brpath = store / root / "module" / f"{ref}.br"
    if await brpath.exists():
        br = await brpath.read_text()
    else:
        br = None


    # TODO : move this to ingest.
    env.globals["unreachable"] = unreachable
    
    doc_blob = load_one(bytes_, br)
    prepare_doc(doc_blob, ref, known_refs)
    return render_one(
        template=template,
        doc=doc_blob,
        qa=ref,
        ext="",
        backrefs=doc_blob.backrefs,
        pygment_css=None,
    )


async def ascii_render(name, store=None):
    print(await _ascii_render(name, store))


def prepare_doc(doc_blob, qa, known_refs):
    assert hash(known_refs)
    sections_ = [
        "Parameters",
        "Returns",
        "Raises",
        "Yields",
        "Attributes",
        "Other Parameters",
    ]
    ### dive into the example data, reconstruct the initial code, parse it with pygments,
    # and append the highlighting class as the third element
    # I'm thinking the linking strides should be stored separately as the code
    # it might be simpler, and more compact.
    # TODO : move this to ingest.
    local_refs = []
    for s in sections_:
        local_refs = local_refs + [x[0] for x in doc_blob.content[s] if x[0]]
        
    for i, (type_, (in_out)) in enumerate(doc_blob.example_section_data):
        if type_ == "code":
            assert len(in_out) == 3
            in_, out, ce_status = in_out
            classes = get_classes("".join([x for x, y in in_]))
            for ii, cc in zip(in_, classes):
                # TODO: Warning here we mutate objects.
                ii.append(cc)
        if type_ == 'text':
            assert len(in_out) == 1, len(in_out)
            for t_, it in in_out[0]:
                  if it.__class__.__name__ == 'Directive':
                      it.ref, it.exists = resolve_(qa, known_refs, local_refs)(it.text)

    doc_blob.refs = [(resolve_(qa, known_refs, local_refs)(x), x) for  x in doc_blob.refs]
    # partial lift of paragraph parsing....
    # TODO: Move this higher in the ingest
    for s in sections_:
        for i, p in enumerate(doc_blob.content[s]):
            if p[2]:
                doc_blob.content[s][i] = (p[0], p[1], paragraphs(p[2]))


    def do_paragraph(p):
         assert p
         for child in p.children:
             if child.__class__.__name__ == 'Directive':
                 child.ref, child.exists = resolve_(qa, known_refs, local_refs)(child.text)

    for s in ["Extended Summary", "Summary", "Notes"]:
        if s in doc_blob.content:
            data = doc_blob.content[s]
            res = []
            if not data:
                continue
            for it in P2(data):
                if it.__class__.__name__ == 'Paragraph':
                    do_paragraph(it)
                if it.__class__.__name__ == 'BlockDirective' and it.inner:
                    do_paragraph(it.inner)
                res.append((it.__class__.__name__, it))
            doc_blob.content[s] = res

    for d in doc_blob.see_also:
        assert isinstance(d.descriptions, list), qa
        d.descriptions = paragraphs(d.descriptions)
        for dsc in d.descriptions:
            for t,it in dsc:
                if it.__class__.__name__ == 'Directive':
                    it.ref, it.exists = resolve_(qa, known_refs, local_refs)(it.text)

    for s in sections_:
        if s in doc_blob.content:
            for param,type_, desc in doc_blob.content[s]:
                for line in desc:
                    for t,it in line:
                        if it.__class__.__name__ == 'Directive':
                            it.ref, it.exists = resolve_(qa, known_refs, local_refs)(it.text)

async def main():
    store = Store(ingest_dir)
    files = store.glob("*/module/*.json")
    css_data = HtmlFormatter(style="pastie").get_style_defs(".highlight")
    env = Environment(
        loader=FileSystemLoader(os.path.dirname(__file__)),
        autoescape=select_autoescape(["html", "tpl.j2"]),
    )
    env.globals["len"] = len
    env.globals["paragraph"] = paragraph
    template = env.get_template("core.tpl.j2")

    known_refs = frozenset({x.name[:-5] for x in store.glob("*/module/*.json")})
    assert len(known_refs) >= 1

    html_dir.mkdir(exist_ok=True)
    document: Store
    family = sorted(list(store.glob("*/module/*.json")))
    family = [str(f.name)[:-5] for f in family]
    assert set(family) == set(known_refs)
    family = known_refs

    tree = make_tree(known_refs)

    for p, document in progress(files, description="Rendering..."):
        if (
            document.name.startswith("__")
            or not document.name.endswith(".json")
            or document.name.endswith("__papyri__.json")
        ):
            assert False, document.name
        qa = document.name[:-5]
        root = qa.split(".")[0]
        try:
            bytes_ = await document.read_text()
            brpath = store / root / "module" / f"{qa}.br"
            if await brpath.exists():
                br = await brpath.read_text()
            else:
                br = None
            doc_blob: IngestedBlobs = load_one(bytes_, br)

        except Exception as e:
            raise RuntimeError(f"error with {document}") from e

        siblings = cs2(qa, tree)

        env.globals["unreachable"] = unreachable
        prepare_doc(doc_blob, qa, known_refs)
        data = render_one(
            template=template,
            doc=doc_blob,
            qa=qa,
            ext=".html",
            parts=siblings,
            backrefs=doc_blob.backrefs,
            pygment_css=css_data,
        )
        with (html_dir / f"{qa}.html").open("w") as f:
            f.write(data)

    assets = store.glob("*/assets/*")
    for asset in assets:
        b = html_dir / "img" / asset.parts[-3] / asset.parts[-2]
        b.mkdir(parents=True, exist_ok=True)
        import shutil

        shutil.copy(asset.path, b / asset.name)
