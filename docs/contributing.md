# 🤝 KÖZREMŰKÖDÉSI ÚTMUTATÓ 🤝

![Contributing Banner](assets/contributing_banner.png)

## 👋 ÜDVÖZLÜNK A MODERN TETRIS CSAPATBAN!

Köszönjük, hogy érdeklődsz a Modern Tetris projekt iránt! Ez a dokumentum segít eligazodni abban, hogyan járulhatsz hozzá a projekthez. Mindegy, hogy hibajavításról, funkcióbővítésről vagy dokumentációról van szó - minden segítséget értékelünk! 🎮✨

## 🚀 HOGYAN KEZDJ HOZZÁ?

### 1️⃣ KÉSZÍTSD ELŐ A FEJLESZTŐI KÖRNYEZETET

```bash
# Klónozd a repót
git clone https://github.com/modern-tetris/tetris.git

# Navigálj a projektkönyvtárba
cd tetris

# Telepítsd a függőségeket
pip install -r requirements.txt

# Indítsd el a játékot és ellenőrizd, hogy minden működik
python main.py
```

### 2️⃣ VÁLASSZ FELADATOT

- 🐛 Ellenőrizd a nyitott problémákat a [hibajegy-kezelőben](https://github.com/modern-tetris/tetris/issues)
- 💡 Találtál egy fejlesztési lehetőséget? Nyiss egy új hibajegyet!
- 📝 Segíts a dokumentáció bővítésében vagy javításában

## 🔄 KÖZREMŰKÖDÉSI FOLYAMAT

![Contribution Flow](assets/contribution_flow.png)

### 1. BRANCH LÉTREHOZÁSA 🌿

```bash
# Hozz létre egy új branch-et a munkádhoz
git checkout -b feature/amazing-new-feature
# VAGY
git checkout -b fix/annoying-bug
```

### 2. KÓDOLÁS ÉS TESZTELÉS 💻

- Kövessed a [fejlesztői útmutatóban](developer_guide.md) leírt kódolási elveket
- Minden változtatást alaposan tesztelj
- Tartsd a kódot tisztán és jól kommentezve

### 3. COMMIT ÉS PUSH 📤

```bash
# Állítsd össze a változtatásaidat
git add .

# Commitolj beszédes üzenettel
git commit -m "Add: Awesome new feature that does XYZ"
# VAGY
git commit -m "Fix: Solve issue with element rotation #42"

# Push-old a branch-et
git push origin feature/amazing-new-feature
```

### 4. PULL REQUEST NYITÁSA 🔍

- Nyiss egy új Pull Request a GitHub felületén
- Írd le részletesen a változtatásaidat
- Kapcsold össze az esetleges hibajegyekkel (pl. "Fixes #42")
- Várj a review-ra a csapattól

## 🌟 KÓDOLÁSI ALAPELVEK

### 🧹 KÓDMINŐSÉG

- **PEP 8** követése a Python kód formázásában
- **Önmagyarázó kód** írása beszédes változó- és függvénynevekkel
- **Dokumentáció** minden osztályhoz, függvényhez (docstring)
- **Atomi commitok** készítése, amelyek egy-egy önálló változtatást tartalmaznak

### 🧪 TESZTELÉS

- **Manuális tesztelés** minden implementált funkcióhoz
  - Ellenőrizd a játékmenetet különböző helyzetekben
  - Teszteld a határeseteket
  - Ellenőrizd a teljesítményt

### 📦 MODULÁRIS FEJLESZTÉS

- Tartsd a kódot **modulárisnak**
- Ne duplikálj funkciókat
- Kövesd az **egyszeri felelősség elvét** (Single Responsibility Principle)

## ✨ ÖTLETEK KÖZREMŰKÖDÉSHEZ

### 🎮 JÁTÉKMENET FEJLESZTÉSEK

- **Új játékmódok** implementálása
- **Speciális elemek** hozzáadása
- **Nehézségi szintek** finomhangolása

### 🎨 VIZUÁLIS FEJLESZTÉSEK

- **Új témák és vizuális stílusok** 
- **Animációk és effektek** bővítése
- **UI/UX fejlesztések**

### 🔊 HANG ÉS ZENE

- **Háttérzene** hozzáadása
- **Hangeffektek** bővítése
- **Hangerőszabályzás** implementálása

### 📱 PLATFORMOK TÁMOGATÁSA

- **Mobilos támogatás** fejlesztése
- **Különböző képernyőméretek** kezelése
- **Gamepad támogatás** hozzáadása

## 🏆 KÖZREMŰKÖDŐI KÓDEX

- Légy **tiszteletteljes és befogadó** minden interakcióban
- Adj **konstruktív visszajelzést**
- Légy **nyitott a változtatásokra**
- **Segíts másoknak** fejlődni

## 📩 KAPCSOLAT

- **GitHub Témák**: Használd a projekthez tartozó hibajegykezelőt
- **Discord**: Csatlakozz a [Modern Tetris Discord szerverhez](https://discord.gg/moderntetris)
- **Email**: kapcsolat@moderntetris.com

---

<p align="center">
  <img src="assets/tetris_logo_small.png" alt="Modern Tetris Logo" width="120">
  <br>
  <strong>JÁTSSZ. JÁRULJ HOZZÁ. ÉLVEZD! 🎮</strong>
  <br>
  <em>© 2025 Modern Tetris Team</em>
</p>