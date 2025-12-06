"""Pokaż podsumowanie - ile imion jest w pliku orig.txt"""
import re

with open('nask_train/orig.txt', 'r', encoding='utf-8') as f:
    text = f.read()

print(f"Długość całego pliku: {len(text)} znaków\n")

# Szukaj prawdziwych polskich imion (nie placeholderów)
name_patterns = [
    r'mgr inż ([A-ZŁĘĄŚŻŹĆŃ][a-złęąśżźćń]+\s+[A-ZŁĘĄŚŻŹĆŃ][a-złęąśżźćń]+)',
    r'inż ([A-ZŁĘĄŚŻŹĆŃ][a-złęąśżźćń]+\s+[A-ZŁĘĄŚŻŹĆŃ][a-złęąśżźćń]+)',
    r'([A-ZŁĘĄŚŻŹĆŃ][a-złęąśżźćń]+\s+[A-ZŁĘĄŚŻŹĆŃ][a-złęąśżźćń]+) (Tel|tel)',
]

all_names = set()
for pattern in name_patterns:
    matches = re.findall(pattern, text)
    for match in matches:
        if isinstance(match, tuple):
            name = match[0]
        else:
            name = match
        if '[name]' not in name and '[surname]' not in name:
            all_names.add(name)

print(f"Znaleziono {len(all_names)} unikalnych prawdziwych imion regex:\n")
for name in sorted(all_names)[:20]:
    print(f"  - {name}")

# Policzyć placeholdery
placeholders = text.count('[name]')
print(f"\n\nPlaceholdery [name]: {placeholders}")
print(f"Placeholdery [surname]: {text.count('[surname]')}")
print(f"Placeholdery [email]: {text.count('[email]')}")
print(f"Placeholdery [phone]: {text.count('[phone]')}")

print("\n\nWniosek: Plik zawiera głównie placeholdery, nie prawdziwe dane!")
