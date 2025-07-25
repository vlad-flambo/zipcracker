# 🔓 Cracking a PDF Password Using John the Ripper (macOS)

> ⚠️ **Use only on PDFs you own or are authorized to access.** Bypassing security on unauthorized documents may be illegal.

---

## 📦 Prerequisites

### ✅ Install Homebrew (if not installed)

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### ✅ Install John the Ripper Jumbo Edition

```bash
brew install john-jumbo
```

> This installs `john`, but not the helper script `pdf2john.py`, which we’ll get next.

---

## 📥 Step 1: Download `pdf2john.py`

```bash
git clone https://github.com/openwall/john.git
cd john/run
```

You now have `pdf2john.py` inside the `run/` directory.

---

## 🧪 Step 2: Extract PDF Hash

Replace `/path/to/locked.pdf` with your actual file path:

```bash
python3 pdf2john.py /path/to/locked.pdf > ~/hash.txt
```

This generates a hash file that `john` can work with.

---

## 🔓 Step 3: Crack the Password

### Basic brute-force:

```bash
john ~/hash.txt
```

### With a wordlist (faster if you suspect common passwords):

```bash
john --wordlist=rockyou.txt ~/hash.txt
```

You can get `rockyou.txt` here:

```bash
wget https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt
```

---

## 👀 Step 4: Check Cracked Password

Once complete, show the result:

```bash
john --show ~/hash.txt
```

This will display something like:

```
user:supersecretpassword
```

---

## 🔓 Step 5: Remove Password from PDF

Now use `qpdf`:

### Install `qpdf` if needed:

```bash
brew install qpdf
```

### Decrypt the PDF:

```bash
qpdf --password=THEPASSWORD --decrypt /path/to/locked.pdf ~/unlocked.pdf
```

Now `~/unlocked.pdf` is password-free.

---

## ✅ Done!

Let me know if you want a single script to automate all these steps.
