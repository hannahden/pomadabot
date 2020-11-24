import natasha

from natasha import (
    Segmenter,
    MorphVocab,
    
    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    NewsNERTagger,
    
    PER,
    NamesExtractor,
    DatesExtractor,
    MoneyExtractor,
    AddrExtractor,

    Doc
)

def preprocess_sent(incoming_sent):
    doc = Doc(incoming_sent)
    
    segmenter = Segmenter()

    
    emb = NewsEmbedding()
    morph_tagger = NewsMorphTagger(emb)
    syntax_parser = NewsSyntaxParser(emb)
    
    doc.segment(segmenter)
    
    doc.tag_morph(morph_tagger)
    doc.parse_syntax(syntax_parser)
    
    return doc.sents[0]

def get_item_for_search(incoming_sent):
    
    sent = preprocess_sent(incoming_sent)  

    found = None
    
    for token in sent.tokens:
        if token.pos == 'NOUN':
            if token.feats['Animacy'] == 'Inan':
                found = token
            break
    if not found:
        return ['fail']
            
    get_order_num = lambda ind: int(ind[-1])
    
    item = [token.text for token in sent.tokens if get_order_num(token.head_id) >= get_order_num(found.head_id[-1])]
    
    sent = preprocess_sent(' '.join(item))
    tokens = list(sent.tokens)
    for token in tokens:
        if token.pos == 'PRON' or token.pos == 'PROPN' :
            tokens.remove(token)
    
        return [token.text for token in tokens]
    
if __name__ == '__main__':
    text = 'помаду'
    print(type(get_item_for_search(text)))
