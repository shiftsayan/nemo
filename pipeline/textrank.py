from pytextrank import json_iter, parse_doc, pretty_print, normalize_key_phrases, render_ranks, text_rank, rank_kernel, top_sentences, limit_keyphrases, limit_sentences, make_sentence
import sys

## Stage 1:
##  * perform statistical parsing/tagging on a document in JSON format
##
## INPUTS: <stage0>
## OUTPUT: JSON format `ParsedGraf(id, sha1, graf)`
if __name__ == "__main__":
    path_stage2 = sys.argv[1]
    path_stage3 = sys.argv[2]

    phrases = ", ".join(set([p for p in limit_keyphrases(path_stage2, phrase_limit=12)]))
    sent_iter = sorted(limit_sentences(path_stage3, word_limit=150), key=lambda x: x[1])
    s = []

    for sent_text, idx in sent_iter:
        s.append(make_sentence(sent_text))

    graf_text = " ".join(s)
    print("**excerpts:** %s\n\n**keywords:** %s" % (graf_text, phrases,))