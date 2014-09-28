import sys
import re


def read_doc(path):
    with open(path) as f:
        lines = f.read().splitlines();
    return lines

def get_sent_from_parse(parse):
    tokens = parse.split(' ');
    sentence_builder = '';
    for token in tokens:
        if len(token) > 0 and token[len(token) - 1]==')':
            sentence_builder = sentence_builder + strip_bad_chars(token);
    return sentence_builder;

def strip_bad_chars(s):
    things_to_replace = [')', '"', "'", '`', ' ', '.', '&amp;', '&', '-LRB-', '(', '-RRB-', '-LSB-', '-RSB'];
    return re.sub('[%s]' % ''.join(things_to_replace), '', s)

def match_parses_to_sents(parses, sents):
    #for each parse
    #split on the spaces, then only keep tokens that end in ")"
    #remove the ")", then concatenate them all together. compare that to the sentence with the whitespace removed.
    num_sents = len(sents);
    num_parses = len(parses);
    cur_sent = 0;
    cur_parse = 0;
    while cur_sent < num_sents:
        parse = get_sent_from_parse(parses[cur_parse]);
        sent = strip_bad_chars(sents[cur_sent]);
        if parse==sent:
            cur_sent = cur_sent + 1;
            cur_parse = cur_parse + 1;
        elif sent=='':
            cur_sent = cur_sent + 1;
        else:
            print 'cur_sent=' + `cur_sent`
            print 'parse: ' + parse
            print 'full parse: ' + parses[cur_parse]
            print 'sent: ' + sent
            print 'next sent: ' + strip_bad_chars(sents[cur_sent + 1])
            sys.exit()

if __name__=='__main__':
    print 'reading in sentences from ' + sys.argv[1] + '...'
    sentences = read_doc(sys.argv[1]);
    print 'done!'
    print 'reading in parses from ' + sys.argv[2] + '...'
    parses = read_doc(sys.argv[2]);
    match_parses_to_sents(parses, sentences);
