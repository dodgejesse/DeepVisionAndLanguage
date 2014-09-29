
#running from commandline
#python extracting_noun_phrases.py /home/jessed/data_storage/data_sets/deep_vision_and_language/rawValSents /home/jessed/data_storage/data_sets/deep_vision_and_language/rawValParses.txt
import sys
import re


def read_doc(path):
    with open(path) as f:
        lines = f.read().splitlines();
    return lines

def write_to_doc_as_matrix(image_num_to_constituents, path):
    with open(path, 'a+') as f:
        for i_num in image_num_to_constituents:
            f.write('\t'.join(map(str, [i_num] + image_num_to_constituents[i_num])) + '\n');

def get_sent_from_parse(parse):
    tokens = parse.split(' ');
    sentence_builder = '';
    for token in tokens:
        if len(token) > 0 and token[len(token) - 1]==')':
            sentence_builder = sentence_builder + token;
    sentence_builder = strip_bad_chars(sentence_builder);
    if '1/2loadedhotdogsandveggieside' in sentence_builder:
        sentence_builder = '11/2loadedhotdogsandveggieside'
    elif 'ThisfirehydrantispaintedblueandislabeledMueller' in sentence_builder:
        sentence_builder = 'ThisfirehydrantispaintedblueandislabeledMueller41/2'
    return sentence_builder;

def get_sent_and_image_num(sent_line):
    if len(sent_line.split('\t')) == 1:
        return [-1, ''];
    else:
        return [sent_line.split('\t')[0], strip_bad_chars(sent_line.split('\t')[1]).replace(' ', '')];

def strip_bad_chars(s):
    strings_to_replace = [')', '"', "'", '`', '.', '&amp;', '&', '-LRB-', '(', '-RRB-', '-LSB-', '-RSB-', '[', ']', '>', 'gt;'];
    new_string = s;
    for bad_string in strings_to_replace:
        new_string = new_string.replace(bad_string, '');
    return new_string

def extract_cur_constit(parse, cur_index):
    #traverse from the current location until we have close this np:
    num_open_parens = 1;
    phrase = '';
    while num_open_parens > 0:
        cur_char = parse[cur_index];
        phrase += cur_char;
        if cur_char == '(':
            num_open_parens += 1;
        elif cur_char == ')':
            num_open_parens -= 1;
        cur_index += 1;
    #split the phrase on whitespace, then remove those that have '('. also remove all bad chars.
    final_phrase = '';
    for token in phrase.split(' '):
        if not token[0]=='(':
            final_phrase += token + ' ';
    final_phrase = strip_bad_chars(final_phrase.strip().lower())
    return final_phrase;

def extract_constituents(parse, constit_name):
    #travese the string left-to-right.
    #if we hit a '(NP', store the characters and count the open and close parens until this one is closed.
    #once it's closed, add that to the list of noun phrases
    #continue traversing the string.
    nps = [];
    prev_chars = [];
    for i in range(len(constit_name) + 2):
        prev_chars.append('');
    for cur_index in range(len(parse)):
        for i in range(len(prev_chars)-1):
            prev_chars[i] = prev_chars[i+1];
        prev_chars[len(prev_chars) - 1] = parse[cur_index];
        viewed_chars = '';
        for i in range(len(prev_chars)):
            viewed_chars += prev_chars[i];
        if viewed_chars == '(' + constit_name + ' ':
            nps.append(extract_cur_constit(parse, cur_index + 1));
    return nps;

def add_constituents(parse, sent_num, image_num_to_constituents, constit_name):
    if sent_num in image_num_to_constituents:
        image_num_to_constituents[sent_num] = image_num_to_constituents[sent_num] + extract_constituents(parse, constit_name);
    else:
        image_num_to_constituents[sent_num] = extract_constituents(parse, constit_name);

def match_parses_to_sents(parses, sents, constit_name):
    #for each parse
    #split on the spaces, then only keep tokens that end in ")"
    #remove the ")", then concatenate them all together. compare that to the sentence with the whitespace removed.
    num_sents = len(sents);
    num_parses = len(parses);
    cur_sent = 0;
    cur_parse = 0;
    image_num_to_constituents = {};
    while cur_sent < num_sents:
        parse = parses[cur_parse];
        sent_from_parse = get_sent_from_parse(parse);
        [sent_num, sent] = get_sent_and_image_num(sents[cur_sent]);
        if sent_from_parse==sent:
            cur_sent = cur_sent + 1;
            cur_parse = cur_parse + 1;
        elif sent=='':
            cur_sent = cur_sent + 1;
        else:
            print 'bad news! there was a mismatch between the parse and the sentence.'
            print 'cur_sent=' + `cur_sent`
            print 'parse: ' + sent_from_parse
            print 'full parse: ' + parses[cur_parse]
            print 'sent: ' + sent
            print 'next sent: ' + strip_bad_chars(sents[cur_sent + 1])
            sys.exit()
        if cur_sent % 100 == 0:
            print '.',
            sys.stdout.flush();
        if cur_sent % 7000 == 0:
            print '\n';
        add_constituents(parse, sent_num, image_num_to_constituents, constit_name);
#        if cur_sent > 25:
#            for image_num in image_num_to_constituents:
#                print image_num + ' ';
#                print image_num_to_constituents[image_num]
#            sys.exit()
    print '\n';
    return image_num_to_constituents;
    

if __name__=='__main__':
    print 'reading in sentences from ' + sys.argv[1] + '...'
    sentences = read_doc(sys.argv[1]);
    print 'done!'
    print 'reading in parses from ' + sys.argv[2] + '...'
    parses = read_doc(sys.argv[2]);
    print 'done!'
    print 'now extracting ' + sys.argv[3] + 's from sentences...'
    image_num_to_constituents = match_parses_to_sents(parses, sentences, sys.argv[3]);
    print 'done!'
    print 'saving to ' + sys.argv[4] + '...'
    write_to_doc_as_matrix(image_num_to_constituents, sys.argv[4]);
