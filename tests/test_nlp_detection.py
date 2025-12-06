"""
Test script to analyze NLP detection on nask_train/orig.txt
"""
import sys
sys.path.insert(0, 'src')

from dane_bez_twarzy.core.config import AnonymizationConfig
from dane_bez_twarzy.core.detector import EntityDetector

# Sample text from the file with real names
test_text = """
„Siemka, muszę się komuś wygadać, bo już nie daję rady. Nazywam się [name] [surname], mam [age] lat ([sex]), mieszkam w [city] na [address]. Jakby co, to mój telefon to [phone], a mail [email] – ostatnio ciągle ktoś pyta o te dane, więc podaję od razu.  

Chodzi o to, że od kilku miesięcy czuję się jak w pułapce. W pracy (jestem na magazynie) szef ciągle na mnie najeżdża, a w domu matka robi aferę o byle gówno. 

Sprawę prowadzi Krzysztof Filipowski Tel 123456789 pok 005. 

W projekcie uczestniczył mgr inż Jan Kowalski oraz inż Maria Nowak z firmy TechnoSerw. 

Projektował mgr inż Adam Wiśniewski MAP IS 1549103 x ISO oraz mgr inż Magdalena Czala GEODETA UPRAWNIONY pod Nr 1561 z 2007.

Nie wyklucza się istnienia w terenie innych nie wykazanych na niniejszej mapie urządzeń podziemnych które nie były zgłoszone do inwentaryzacji lub o których brak jest informacji w instytucjach branżowych mgr inż Piotr Lewandowski UPR NR EWID 249 02 MOR mgr inż Anna Kamińska mgr inż Tomasz Zieliński inż Barbara Szymańska.
"""

# Test with NLP enabled
print("=== Testing NLP Detection ===\n")
print(f"Sample text length: {len(test_text)} characters\n")

config = AnonymizationConfig(use_nlp=True, min_confidence=0.5)
detector = EntityDetector(config)

print("Detecting entities with NLP...")
entities = detector.detect(test_text)

print(f"\nTotal entities detected: {len(entities)}\n")

# Group by type
from collections import defaultdict
by_type = defaultdict(list)
for entity in entities:
    by_type[entity.type].append(entity)

print("Entities by type:")
for entity_type, ents in sorted(by_type.items()):
    print(f"\n{entity_type.value}: {len(ents)}")
    for e in ents[:10]:  # Show first 10
        print(f"  - '{e.text}' (confidence: {e.confidence:.2f}, position: {e.start}-{e.end})")

# Check for specific names we expect
expected_names = [
    "Krzysztof Filipowski",
    "Jan Kowalski", 
    "Maria Nowak",
    "Adam Wiśniewski",
    "Magdalena Czala",
    "Piotr Lewandowski",
    "Anna Kamińska",
    "Tomasz Zieliński",
    "Barbara Szymańska"
]

print("\n\n=== Checking for expected names ===")
detected_texts = [e.text.lower() for e in entities]
for name in expected_names:
    found = any(name.lower() in dt or dt in name.lower() for dt in detected_texts)
    status = "✓ FOUND" if found else "✗ MISSING"
    print(f"{status}: {name}")

print("\n\n=== Analyzing why names might be missed ===")
print("1. Confidence threshold:", config.min_confidence)
print("2. NLP model loaded:", detector._nlp_detector is not None)
if detector._nlp_detector:
    print("3. spaCy model available: Yes")
else:
    print("3. spaCy model available: No - NLP disabled")

print("\n4. Context around names:")
print("   - Names appear with titles: 'mgr inż', 'inż', 'Tel'")
print("   - Names in technical/formal documents")
print("   - Polish naming conventions")
