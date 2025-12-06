# Stwórz mały przykład z nask_train/orig.txt do testowania
with open('nask_train/orig.txt', 'r', encoding='utf-8') as f:
    content = f.read()[:10000]  # Pierwsze 10000 znaków

with open('test_sample.txt', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Utworzono test_sample.txt ({len(content)} znaków)")
