"""
Bezpośredni test modelu spaCy - co wykrywa?
"""
import spacy

# Load model
print("Loading spaCy model pl_core_news_lg...")
nlp = spacy.load("pl_core_news_lg")

# Test texts
test_texts = [
    "Krzysztof Filipowski Tel 123456789",
    "mgr inż Jan Kowalski oraz inż Maria Nowak z firmy TechnoSerw",
    "Projektował mgr inż Adam Wiśniewski MAP IS 1549103",
    "mgr inż Magdalena Czala GEODETA UPRAWNIONY pod Nr 1561",
    "mgr inż Piotr Lewandowski UPR NR EWID 249 02 MOR mgr inż Anna Kamińska",
    "Jan Kowalski mieszka w Warszawie.",
    "Spotkałem się z Marią Nowak i Adamem Wiśniewskim."
]

for i, text in enumerate(test_texts, 1):
    print(f"\n{'='*60}")
    print(f"Test {i}: {text}")
    print('='*60)
    
    doc = nlp(text)
    
    if doc.ents:
        print(f"Wykryte encje ({len(doc.ents)}):")
        for ent in doc.ents:
            print(f"  - '{ent.text}' [{ent.label_}] (start: {ent.start_char}, end: {ent.end_char})")
    else:
        print("Brak wykrytych encji!")
    
    # Show tokens with POS tags
    print("\nTokeny i ich tagi:")
    for token in doc[:15]:  # First 15 tokens
        print(f"  {token.text:20} POS={token.pos_:10} TAG={token.tag_:10} DEP={token.dep_:10}")

print("\n\n" + "="*60)
print("WNIOSKI:")
print("="*60)
print("1. Czy model wykrywa imiona w czystym kontekście (bez tytułów)?")
print("2. Czy tytuły 'mgr inż' blokują rozpoznawanie imion?")
print("3. Czy model spaCy pl_core_news_lg jest odpowiedni dla dokumentów technicznych?")
