import sys
import os
import json

in_dir = sys.argv[1]
output_filename = in_dir + '_resolution_dicts.json'

all_articles = []

filenames = sorted(os.listdir(in_dir))
for filename in filenames:
    num = int(filename)
    input_path = os.path.join(in_dir, filename)
    with open(input_path) as fp:
        file_articles_s = fp.read()
    _file_articles = file_articles_s.split('@@@ARTICLE@@@\n')
    file_articles = []
    file_article_count = 1
    for article in _file_articles:
        if file_article_count > 5:
            break
        file_article_count += 1
        sentences = enumerate(article.split("@@@SENTENCE@@@\n"))
        sentences_l = []
        for sentence_idx, sentence in sentences:
            
            raw_tokens = sentence.split("@@@TOKEN@@@\n")
            tokens = []
            for raw_token in raw_tokens:
                if not raw_token:
                    continue
                token_parts = [part for part in raw_token.split('\n') if part]
                
                idx_s, from_s, to_s, = token_parts
                token_idx = int(idx_s.split('TOKEN INDEX: ')[-1])
                _from = from_s.split('FROM: ')[-1]
                to = to_s.split('TO: ')[-1]
                token_dict = {'from': _from, 'idx': token_idx, 'to': to}
                tokens.append(token_dict)
                
            sentence_dict = {
                'idx': sentence_idx,
                'tokens': tokens
            }
            sentences_l.append(sentence_dict)
        
        file_articles.append([num, sentences_l])
        num += 1
    all_articles.extend(file_articles)
    
with open(output_filename, "w+") as fp:
    fp.write(json.dumps(all_articles))
