#! /usr/bin/python3
import freeling
import sys

# # ------------  output a parse tree ------------
FREELINGDIR = "/usr/local"

DATA = FREELINGDIR + "/share/freeling/"
LANG = "es"

freeling.util_init_locale("default")

# create language analyzer
la = freeling.lang_ident(DATA + "common/lang_ident/ident.dat")

# create options set for maco analyzer. Default values are Ok, except for data files.
op = freeling.maco_options("es")
op.set_data_files("",
                  DATA + "common/punct.dat",
                  DATA + LANG + "/dicc.src",
                  DATA + LANG + "/afixos.dat",
                  "",
                  DATA + LANG + "/locucions.dat",
                  DATA + LANG + "/np.dat",
                  DATA + LANG + "/quantities.dat",
                  DATA + LANG + "/probabilitats.dat")

# create analyzers
tk = freeling.tokenizer(DATA + LANG + "/tokenizer.dat")
sp = freeling.splitter(DATA + LANG + "/splitter.dat")
sid = sp.open_session()
mf = freeling.maco(op)

# activate mmorpho odules to be used in next call
mf.set_active_options(True, True, True, True,  # select which among created
                      True, True, True, True,  # submodules are to be used.
                      True, True, True, True)  # default: all created submodules are used

# create tagger, sense anotator, and parsers
tg = freeling.hmm_tagger(DATA + LANG + "/tagger.dat", True, 2)
sen = freeling.senses(DATA + LANG + "/senses.dat")
parser = freeling.chart_parser(DATA + LANG + "/chunker/grammar-chunk.dat")
dep = freeling.dep_txala(DATA + LANG + "/dep_txala/dependences.dat", parser.get_start_symbol())

ukb = freeling.ukb("/usr/local/share/freeling/es/ukb.dat")

semantic_graph = freeling.semgraph_extract("/usr/local/share/freeling/es/semgraph/semgraph-SPR-treeler.dat")


# process input text

lin = """Sócrates fue hijo de una comadrona, Faenarete, y de un escultor, Sofronisco, emparentado con Arístides el Justo. Pocas cosas se conocen con certeza de la biografía de Sócrates, aparte de que participó como soldado de infantería en las batallas de Samos (440), Potidea (432), Delio (424) y Anfípolis (422). Fue amigo de Aritias y de Alcibíades, al que salvó la vida."""
l = tk.tokenize(lin)
ls = sp.split(sid, l, False)

ls = mf.analyze(ls)
ls = tg.analyze(ls)
ls = sen.analyze(ls)
ls = parser.analyze(ls)
ls = dep.analyze(ls)
document = freeling.Document(lin)
a = semantic_graph.extract(document)
a

## output results
for s in ls:
    ws = s.get_words()
    for w in ws:
        # print(w.get_form() + " " + w.get_lemma() + " " + w.get_tag() + " " + w.get_senses_string())
        print(w.get_senses())
    print("")

    tr = s.get_parse_tree()
    printTree(tr, 0)

    dp = s.get_dep_tree()
    printDepTree(dp, 0)

lin = sys.stdin.readline()

# clean up       
sp.close_session(sid)