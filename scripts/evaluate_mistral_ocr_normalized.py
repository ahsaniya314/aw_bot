# -*- coding: utf-8 -*-
import re

ground_truth = """28 - 11 - 2029

Nama sales = Budi Santoso

Ambil barang
lolipop 100 ctn
meses 20 ctn
miksu 50 ctn

30 - 11 - 2029

Nama = Budi Santoso

Bayar cicilan : Rp 73.600.000

02 - 12 - 2029

Nama = Budi Santoso

Bayar cicilan : Rp 10.000.000"""

manual_extractions = {
    'gambar 1': '''28-11-2029

Nama Sales: Budi Santoso

Ambil Barang
Lolipop 100 ctn
Mie Ser 20 Ctn
Miksu 50 Ctn

30-11-2029

Nama: Budi Santoso

Bayar cicilan: Rp 73.600.000

02-12-2029

Nama: Budi Santoso

Bayar cicilan: Rp 10.000.000''',

    'gambar 2': '''28 - 11 - 2029

Nama sales = Budi Santoso

Ambil barang
~ lolipop 100 ctn
~ meses 20 ctn
~ miksu 50 ctn

30 - 11 - 2029

Nama = Budi Santoso

Bayar cicilan : Rp 73.600.000

02 - 12 - 2029

Nama = Budi Santoso

Bayar cicilan : Rp 10.000.000''',

    'gambar 3': '''28 - 11 - 202g

* Nama Sales = Budi Santoso

Ambil Barang

- Lolipop 100 ctn
- Meses 20 ctn
- Miksu 50 ctn

30 - 11 - 202g

* Nama = Budi Santoso

Bayar Cicilan = Rp. 73.600.000

02 - 12 - 202g

* Nama = Budi Santoso

Bayar Cicilan = Rp. 10.000.000''',

    'gambar 4': '''28 - 11 - 2029

Tamu sales = Budi Santoso

Ambil barang

- Lolipop 100 pcs
- Meses 20 pcs
- Mixue 50 pcs

30 - 11 - 2029

Tamu = Budi Santoso

Bayar cicilan = Rp. 3.600.000

02 - 12 - 2029

Tamu = Budi Santoso

Bayar cicilan = Rp. 10.000.000''',

    'gambar 5': '''28 - 11 - 202g

Nama sales = Budi Santoso

Ambil barang
- lolipop 100 ctn
- meses 20 ctn
- miksy 90 ctn

30 - 11 - 202g

Nama = Budi Santoso

Bayar cicilan : Rp. 13.600.000

02 - 12 - 202g

Nama = Budi Santoso

Bayar Cicilan : Rp. 10.000.000''',

    'gambar 6': '''28 - 11 - 2029

Nama Sales = Budi Santoso

Ambil barang
- Lolipop 100 ctn
- Meser 20 ctn
- Mikru 50 ctn

30 - 11 - 2029

Nama Sales = Budi Santoso

Bayar Cicilan : Rp 73.600.000

02 - 12 - 2029

Nama = Budi Santoso

Bayar Cicilan : Rp 10.000.000''',

    'gambar 7': '''28 - 11 - 2029

Nama Sales = Budi Santoso

Ambil Barang

~ Lolipop 100 ctn
~ Meses 30 ctn
2 Miksu 50 ctn

30 - 11 - 2029

Nama = Budi Santoso

Bayar cicilan : Rp 73.600.000

02 - 12 - 2029

Nama = Budi Santoso

Bayar cicilan : Rp 10.000.000''',

    'gambar 8': '''28 - 11 - 2029

Nama Sales : Budi Santoso

Ambil Barang
- Lolipop 100 ctn
- Meses 20 ctn
- Miksu 50 ctn

30 - 11 - 2029

Nama : Budi Santoso

Bayar Cicilan : Rp 73.000.000

02 - 12 - 2029

Nama : Budi Santoso

Bayar Cicilan : Rp 10.000.000'''
}

def clean_text(text):
    if not text:
        return ""
    # Lowercase
    text = text.lower()
    
    # Standardize dates: e.g. "28 - 11 - 2029" -> "28-11-2029"
    text = re.sub(r'(\d+)\s*-\s*(\d+)\s*-\s*(\d+)', r'\1-\2-\3', text)
    
    # Process line by line
    lines = text.split('\n')
    cleaned_lines = []
    for line in lines:
        line = line.strip()
        # Remove list markers at the start
        line = re.sub(r'^[\-\*\~]\s*', '', line)
        # Replace punctuation/operators with spaces
        line = line.replace(':', ' ').replace('=', ' ').replace('.', ' ')
        # Normalize multiple spaces inside the line
        line = re.sub(r'\s+', ' ', line).strip()
        if line:
            cleaned_lines.append(line)
            
    return " ".join(cleaned_lines)

def calculate_alignment(ref, hyp):
    n_ref = len(ref)
    n_hyp = len(hyp)
    d = [[0] * (n_hyp + 1) for _ in range(n_ref + 1)]
    for i in range(n_ref + 1):
        d[i][0] = i
    for j in range(n_hyp + 1):
        d[0][j] = j
    for i in range(1, n_ref + 1):
        for j in range(1, n_hyp + 1):
            cost = 0 if ref[i-1] == hyp[j-1] else 1
            d[i][j] = min(
                d[i-1][j] + 1,
                d[i][j-1] + 1,
                d[i-1][j-1] + cost
            )
    S, D, I = 0, 0, 0
    i, j = n_ref, n_hyp
    while i > 0 or j > 0:
        if i > 0 and j > 0:
            cost = 0 if ref[i-1] == hyp[j-1] else 1
            if d[i][j] == d[i-1][j-1] + cost:
                if cost == 1:
                    S += 1
                i -= 1
                j -= 1
            elif d[i][j] == d[i-1][j] + 1:
                D += 1
                i -= 1
            elif d[i][j] == d[i][j-1] + 1:
                I += 1
                j -= 1
        elif i > 0:
            D += 1
            i -= 1
        elif j > 0:
            I += 1
            j -= 1
    err_rate = d[n_ref][n_hyp] / n_ref if n_ref > 0 else (1.0 if n_hyp > 0 else 0.0)
    acc = max(0.0, 1.0 - err_rate)
    return S, D, I, n_ref, err_rate, acc

def run_evaluation():
    print("=" * 110)
    print("HASIL EVALUASI DARI INPUT MANUAL (SETELAH NORMALISASI)".center(110))
    print("=" * 110)
    print(f"{'NAMA FILE':<12} | {'CER':<8} {'CER DETAILS':<20} {'AKURASI CER':<12} | {'WER':<8} {'WER DETAILS':<20} {'AKURASI WER':<12}")
    print("-" * 110)
    for filename, text in manual_extractions.items():
        cleaned_gt = clean_text(ground_truth)
        cleaned_hyp = clean_text(text)
        
        cer_s, cer_d, cer_i, cer_n, cer, cer_acc = calculate_alignment(list(cleaned_gt), list(cleaned_hyp))
        wer_s, wer_d, wer_i, wer_n, wer, wer_acc = calculate_alignment(cleaned_gt.split(), cleaned_hyp.split())
        
        cer_det_str = f"S={cer_s},D={cer_d},I={cer_i},N={cer_n}"
        wer_det_str = f"S={wer_s},D={wer_d},I={wer_i},N={wer_n}"
        print(f"{filename:<12} | {cer:>6.2%} {cer_det_str:<20} {cer_acc:>11.2%} | {wer:>6.2%} {wer_det_str:<20} {wer_acc:>11.2%}")
    print("=" * 110)

if __name__ == "__main__":
    run_evaluation()
