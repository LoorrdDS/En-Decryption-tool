# 🔐 Fernet Crypto Tool

Ein einfaches, konsolenbasiertes Python-Programm zum Ver- und Entschlüsseln von Textnachrichten mit einem selbst gewählten **Master-Key** (Passwort). Die Verschlüsselung basiert auf [Fernet](https://cryptography.io/en/latest/fernet/) aus dem `cryptography`-Paket (symmetrische Verschlüsselung, AES-128-CBC + HMAC-Authentifizierung).

Aus deinem Passwort wird über **PBKDF2-HMAC-SHA256** (480'000 Iterationen) ein gültiger Fernet-Schlüssel abgeleitet. So kannst du ein beliebiges, für dich merkbares Passwort verwenden, statt dir einen zufälligen Fernet-Schlüssel merken zu müssen.

---

## Inhaltsverzeichnis

- [Voraussetzungen](#voraussetzungen)
- [Installation](#installation)
  - [1. Repository herunterladen](#1-repository-herunterladen)
  - [2. Python prüfen](#2-python-prüfen)
  - [3. Virtuelle Umgebung erstellen (empfohlen)](#3-virtuelle-umgebung-erstellen-empfohlen)
  - [4. Abhängigkeiten installieren](#4-abhängigkeiten-installieren)
- [Verwendung](#verwendung)
  - [Programm starten](#programm-starten)
  - [Nachricht verschlüsseln](#nachricht-verschlüsseln)
  - [Nachricht entschlüsseln](#nachricht-entschlüsseln)
- [Funktionsweise](#funktionsweise)
- [Sicherheitshinweise](#sicherheitshinweise)
- [Fehlerbehebung](#fehlerbehebung)
- [Lizenz](#lizenz)

---

## Voraussetzungen

- **Python 3.8 oder neuer**
- **pip** (wird normalerweise mit Python mitinstalliert)
- Ein Terminal / eine Kommandozeile (Windows: PowerShell oder CMD, macOS/Linux: Terminal)

---

## Installation

### 1. Repository herunterladen

**Option A – mit Git:**

```bash
git clone https://github.com/LoorrdDS/En-Decryption-tool.git
cd En-Decryption-tool
```

**Option B – ohne Git:**

Auf GitHub oben rechts auf **Code → Download ZIP** klicken, ZIP entpacken und im entpackten Ordner ein Terminal öffnen.

### 2. Python prüfen

Prüfe, ob Python installiert ist:

```bash
python3 --version
```

Falls kein Python installiert ist, lade es von [python.org/downloads](https://www.python.org/downloads/) herunter und installiere es. Unter Windows: bei der Installation die Option **"Add python.exe to PATH"** aktivieren.

### 3. Virtuelle Umgebung erstellen (empfohlen)

Eine virtuelle Umgebung hält die Abhängigkeiten dieses Projekts getrennt von anderen Python-Projekten auf deinem System.

**macOS / Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows (PowerShell):**

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

**Windows (CMD):**

```cmd
python -m venv venv
venv\Scripts\activate.bat
```

Wenn die virtuelle Umgebung aktiv ist, siehst du `(venv)` am Anfang der Zeile in deinem Terminal.

> Du kannst diesen Schritt auch überspringen und die Abhängigkeit direkt systemweit installieren — dann einfach bei Schritt 4 weitermachen.

### 4. Abhängigkeiten installieren

```bash
pip install cryptography
```

Optional kannst du auch eine `requirements.txt` mit folgendem Inhalt ins Repository legen und installieren:

```
cryptography>=42.0.0
```

```bash
pip install -r requirements.txt
```

---

## Verwendung

### Programm starten

Im Projektordner (bei aktivierter virtueller Umgebung, falls verwendet):

```bash
python3 crypto_tool.py
```

Unter Windows ggf. statt `python3` nur `python` verwenden.

Es erscheint ein Menü:

```
==================================================
 Fernet Ver-/Entschlüsselungstool
==================================================
1) Nachricht verschlüsseln (encode)
2) Nachricht entschlüsseln (decode)
3) Beenden
Auswahl:
```

### Nachricht verschlüsseln

1. `1` eingeben und Enter drücken.
2. Master-Key (Passwort) eingeben — die Eingabe wird **nicht** am Bildschirm angezeigt (aus Sicherheitsgründen).
3. Master-Key zur Bestätigung ein zweites Mal eingeben.
4. Die zu verschlüsselnde Nachricht eingeben.
5. Das Programm gibt einen langen Text (base64-kodiert) aus — das ist deine verschlüsselte Nachricht. Diese kannst du z. B. per E-Mail oder Chat verschicken.

**Beispiel:**

```
Auswahl: 1
Master-Key eingeben:
Master-Key bestätigen:
Nachricht eingeben: Das ist ein geheimer Text

Verschlüsselte Nachricht (bitte sicher aufbewahren):
nO6QszA2u60dXjH1VLNrnGdBQUFBQUJxVk44eHNHNWdrQWotYjktR1Y1aFUt...
```

### Nachricht entschlüsseln

1. `2` eingeben und Enter drücken.
2. Denselben Master-Key eingeben, der beim Verschlüsseln verwendet wurde.
3. Die verschlüsselte Nachricht (den langen base64-Text) einfügen.
4. Das Programm zeigt die entschlüsselte Originalnachricht an.

Wird ein falscher Master-Key verwendet, meldet das Programm einen Fehler statt eine falsche Nachricht anzuzeigen — das liegt an der eingebauten Authentifizierung (HMAC) von Fernet.

---

## Funktionsweise

| Schritt | Beschreibung |
|---|---|
| 1 | Aus dem Master-Key und einem zufälligen **Salt** (16 Byte) wird via PBKDF2-HMAC-SHA256 (480'000 Iterationen) ein 32-Byte-Schlüssel abgeleitet. |
| 2 | Mit diesem Schlüssel wird die Nachricht mittels **Fernet** (AES-128-CBC + HMAC-SHA256) verschlüsselt. |
| 3 | Salt + verschlüsseltes Token werden zusammengefügt und als ein base64-String ausgegeben. |
| 4 | Beim Entschlüsseln wird der Salt aus dem String extrahiert, derselbe Schlüssel erneut abgeleitet und die Nachricht entschlüsselt/verifiziert. |

Da der Salt bei jeder Verschlüsselung neu zufällig erzeugt wird, ergibt dieselbe Nachricht mit demselben Passwort **jedes Mal einen anderen verschlüsselten Text** — das ist normal und beabsichtigt.

---

## Sicherheitshinweise

- Der Master-Key wird **nirgends gespeichert** — merke ihn dir gut oder nutze einen Passwort-Manager. Ist er verloren, ist die Nachricht nicht wiederherstellbar.
- Verwende ein **starkes, langes Passwort** als Master-Key (z. B. eine Passphrase aus mehreren Wörtern).
- Der verschlüsselte Text kann bedenkenlos über unsichere Kanäle (E-Mail, Chat) verschickt werden — der Master-Key jedoch **niemals** über denselben Kanal.
- Dieses Tool dient Lern- und Demonstrationszwecken für den persönlichen Gebrauch; für hochsensible oder geschäftskritische Daten empfiehlt sich eine unabhängige Sicherheitsprüfung.

---

## Fehlerbehebung

**„python3: command not found" / „python wird nicht als Befehl erkannt"**
→ Python ist nicht installiert oder nicht im PATH. Siehe [Voraussetzungen](#voraussetzungen).

**„ModuleNotFoundError: No module named 'cryptography'"**
→ Abhängigkeit fehlt. `pip install cryptography` ausführen (ggf. mit aktivierter virtueller Umgebung).

**„Entschlüsselung fehlgeschlagen: falscher Master-Key oder Daten beschädigt/manipuliert."**
→ Entweder wurde ein falscher Master-Key eingegeben, oder der verschlüsselte Text wurde beim Kopieren/Einfügen verändert (z. B. abgeschnitten oder mit Leerzeichen versehen).

**Aktivierung der virtuellen Umgebung unter Windows schlägt fehl (PowerShell)**
→ Falls eine Fehlermeldung zu „Execution Policy" erscheint, PowerShell als Administrator öffnen und einmalig ausführen:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---
