from dictionary import is_url


title_list = set()
with open('gazetteer/jobtitles.lst', 'r') as f:
    for line in f:
        title_list.add(line.strip().lower())
title_list.add('president')

# mhi_list = set()
# with open('gazetteer/mhi.lst', 'r') as f:
#     mhi_kb_dic = {}
#     for line in f:
#         mhi_list.add(line.strip().lower())

def extract_filler(sent, nlp, ners):
    titles = extract_title(sent, nlp, ners)
    times = extract_time(sent, nlp)
    numericals = extract_numerical(sent, nlp)
    urls = extract_url(sent)
    # domain_fillers = extract_domain_important(sent)
    all_fillers = titles + times + numericals + urls
    return all_fillers


def extract_domain_important(sent):
    domain_fillers = []
    for wid, word in enumerate(sent.words):
        if any(s in word.word.lower() for s in ['covid', 'coronovirus']):
            domain_filler = {'mention': word.word, 'token_span': [wid, wid+1], 'char_begin': word.begin-1, 'char_end': word.end, 'head_span': [word.begin-1, word.end], 'type': 'ldcont:mhi.disease.disease'}
            domain_fillers.append(domain_filler)
    return domain_fillers


def extract_title(sent, nlp, ners):
    titles = []
    for wid, word in enumerate(sent.words):
        found = False
        if word.word.lower() in title_list:
            title = {'mention': word.word, 'token_span': [wid, wid+1], 'char_begin': word.begin-1, 'char_end': word.end, 'head_span': [word.begin-1, word.end], 'type': 'TITLE'}
            found = True
        elif wid + 1 < len(sent.words):
            text = sent.sub_string(wid, wid+2)
            if text.lower() in title_list:
                title = {'mention': text, 'token_span': [wid, wid+2], 'char_begin': sent.words[wid].begin-1, 'char_end': sent.words[wid+1].end, 'head_span': [sent.words[wid+1].begin-1, sent.words[wid+1].end], 'type': 'TITLE'}
                found = True
            elif wid + 2 < len(sent.words):
                text = sent.sub_string(wid, wid+3)
                if text.lower() in title_list:
                    title = {'mention': text, 'token_span': [wid, wid+3], 'char_begin': sent.words[wid].begin-1, 'char_end': sent.words[wid+2].end, 'head_span': [sent.words[wid+2].begin-1, sent.words[wid+2].end], 'type': 'TITLE'}
                    found = True
        if found:
            valid = False
            for ner in ners:
                if ner == 'B-PER':
                    valid = True
                    break
            if valid:
                titles.append(title)
    return titles

def extract_time(sent, nlp):
    # ners = nlp.ner(sent.get_text().encode('UTF-8'))
    ners = nlp['ner']
    if ners is None:
        return []
    if len(ners) != len(sent.words):
        return []
    time = []
    tmp = []
    for wid, (word, ner) in enumerate(ners):
        if ner == 'DATE' or ner == 'TIME':
            tmp.append(wid)
        elif tmp:
            text = sent.sub_string(tmp[0], tmp[-1]+1)
            begin_offset = sent.words[tmp[0]].begin
            # print(len(sent.words), tmp)
            end_offset = sent.words[tmp[-1]].end
            time.append({'mention': text, 'token_span': [tmp[0], tmp[-1]+1],'char_begin': begin_offset-1, 'char_end': end_offset, 'head_span': [sent.words[tmp[-1]].begin-1, end_offset], 'type': 'aida:date_time', 'score':'0.9'})
            tmp = []
    
    return time

def extract_numerical(sent, nlp):
    ners = nlp['ner']
    if ners is None:
        return []
    if len(ners) != len(sent.words):
        return []
    num = []
    tmp = []
    # print(ners)
    for wid, (word, ner) in enumerate(ners):
        if ner in ['NUMBER', 'PERCENT', 'DURATION']:
            tmp.append(wid)
        elif tmp:
            text = sent.sub_string(tmp[0], tmp[-1]+1)
            begin_offset = sent.words[tmp[0]].begin
            # print(len(sent.words), tmp)
            end_offset = sent.words[tmp[-1]].end
            num.append({'mention': text, 'token_span': [tmp[0], tmp[-1]+1],
                'char_begin': begin_offset-1, 'char_end': end_offset,
                'head_span': [sent.words[tmp[-1]].begin-1, end_offset],
                'type': 'NUMERICAL', 'score':'0.9'})
            tmp = []
    
    return num

def extract_url(sent):
    urls = []
    for wid, word in enumerate(sent.words):
        # if word.word.lower() in mhi_list:
        #     urls.append({'mention': word.word, 'token_span': [wid, wid+1],'char_begin': word.begin-1, 'char_end': word.end, 'head_span': [word.begin-1, word.end], 'type': 'MHI.Disease.Disease', 'score': '0.9'})
        if is_url(word.word):
            urls.append({'mention': word.word, 'token_span': [wid, wid+1], 'char_begin': word.begin-1, 'char_end': word.end, 'head_span': [word.begin-1, word.end], 'type': 'URL', 'subtype': 'URL', 'score': '0.9'})
    return urls
