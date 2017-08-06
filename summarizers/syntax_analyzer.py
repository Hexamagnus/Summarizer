import freeling
import sys

from . import base

FREELINGDIR = "/usr/local"
DATA = FREELINGDIR + "/share/freeling/"
LANG = "es"


class SyntaxAnalyzer(base.BaseSummarizer):

    tk = None
    sp = None
    sid = None
    mf = None
    tg = None
    sen = None
    parser = None
    dep = None
    la = None

    def __init__(self, text):
        super().__init__(text)
        freeling.util_init_locale("default")
        self.la = freeling.lang_ident(DATA + "common/lang_ident/ident.dat")
        op = freeling.maco_options("es")
        op.set_data_files(
            "",
            DATA + "common/punct.dat",
            DATA + LANG + "/dicc.src",
            DATA + LANG + "/afixos.dat",
            "",
            DATA + LANG + "/locucions.dat",
            DATA + LANG + "/np.dat",
            DATA + LANG + "/quantities.dat",
            DATA + LANG + "/probabilitats.dat"
        )

        # create analyzers
        self.tk = freeling.tokenizer(DATA + LANG + "/tokenizer.dat")
        self.sp = freeling.splitter(DATA + LANG + "/splitter.dat")
        self.sid = self.sp.open_session()
        self.mf = freeling.maco(op)

        # activate mmorpho odules to be used in next call
        self.mf.set_active_options(
            False,  # umap User map module
            True,  # num Number Detection
            True,  # pun Punctuation Detection
            True,  # dat Date Detection
            True,  # dic Dictionary Search
            True,  # aff
            False,  # com
            True,  # rtk
            True,  # mw Multiword Recognition
            True,  # ner  Name Entity Recongnition
            True,  # qt Quantity Recognition
            True  # prb Probability Assignment And Guesser
        )  # default: all created submodules are used

        # create tagger, sense anotator, and parsers
        self.tg = freeling.hmm_tagger(DATA + LANG + "/tagger.dat", True, 2)
        self.sen = freeling.senses(DATA + LANG + "/senses.dat")
        self.parser = freeling.chart_parser(DATA + LANG + "/chunker/grammar-chunk.dat")
        self.dep = freeling.dep_txala(DATA + LANG + "/dep_txala/dependences.dat", self.parser.get_start_symbol())

    def structure_tree(self, ptree, depth):

        node = ptree.begin()
        node_dict = dict()
        info = node.get_info()

        nch = node.num_children()
        if nch == 0:
            # is a leaf
            w = info.get_word()
            return {
                "form": w.get_form(),
                "lemma": w.get_lemma(),
                "tag": w.get_tag()
            }
        else:
            label = str(info.get_label())
            print(label)
            sons = list()
            for i in range(nch):
                child = node.nth_child_ref(i)
                sons.append(self.structure_tree(child, depth + 1))

            node_dict[label] = sons
        return node_dict

    def summarize(self):
        l = self.tk.tokenize(self.text)
        ls = self.sp.split(self.sid, l, False)

        ls = self.mf.analyze(ls)
        ls = self.tg.analyze(ls)
        ls = self.sen.analyze(ls)
        ls = self.parser.analyze(ls)
        ls = self.dep.analyze(ls)

        syntactic_trees = list()

        for s in ls:
            tr = s.get_parse_tree()
            syntactic_trees.append(self.structure_tree(tr, 0))

        self.sp.close_session(self.sid)

        return syntactic_trees

