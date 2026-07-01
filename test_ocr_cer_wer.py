import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.ocr_service import OCRService


def calculate_cer(reference: str, hypothesis: str) -> float:
    """Calculate Character Error Rate (CER) between reference and hypothesis text."""
    # Prepare the texts: normalize whitespace and lowercase
    ref = ' '.join(reference.lower().split())
    hyp = ' '.join(hypothesis.lower().split())
    
    # Levenshtein distance
    m, n = len(ref), len(hyp)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
        
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost = 0 if ref[i-1] == hyp[j-1] else 1
            dp[i][j] = min(
                dp[i-1][j] + 1,      # Deletion
                dp[i][j-1] + 1,      # Insertion
                dp[i-1][j-1] + cost  # Substitution
            )
    
    if m == 0:
        return 1.0 if n != 0 else 0.0
    
    return dp[m][n] / m

def calculate_wer(reference: str, hypothesis: str) -> float:
    """Calculate Word Error Rate (WER) between reference and hypothesis text."""
    # Prepare the texts: normalize whitespace and lowercase, split into words
    ref_words = reference.lower().split()
    hyp_words = hypothesis.lower().split()
    
    # Levenshtein distance for words
    m, n = len(ref_words), len(hyp_words)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
        
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost = 0 if ref_words[i-1] == hyp_words[j-1] else 1
            dp[i][j] = min(
                dp[i-1][j] + 1,      # Deletion
                dp[i][j-1] + 1,      # Insertion
                dp[i-1][j-1] + cost  # Substitution
            )
    
    if m == 0:
        return 1.0 if n != 0 else 0.0
    
    return dp[m][n] / m

def main():
    ocr = OCRService()
    ocr.load_model()
    
    # Example usage
    image_path = "contoh.jpeg"
    
    # Ground truth (expected text)
    ground_truth = "Pak Andi pesan lolipop 10 dus, meses 5 bungkus, willo 3 dus, belum lunas semua."
    
    # Get OCR result
    ocr_result = ocr.extract_text(image_path)
    
    print("="*60)
    print("OCR EVALUATION: CER & WER")
    print("="*60)
    print(f"Reference (Ground Truth): {ground_truth}")
    print(f"Hypothesis (OCR Result):  {ocr_result}")
    print()
    
    cer = calculate_cer(ground_truth, ocr_result)
    wer = calculate_wer(ground_truth, ocr_result)
    
    print(f"Character Error Rate (CER): {cer:.2%}")
    print(f"Word Error Rate (WER):    {wer:.2%}")
    print("="*60)

if __name__ == "__main__":
    main()
