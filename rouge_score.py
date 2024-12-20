from typing import Union, Tuple, List


# MARK: helper functions

def words_to_bigrams(text: List[str]) -> List[str]:
    return [f"{text[i]} {text[i+1]}" for i in range(len(text) - 1)]

def get_dp_matrix(text1: str, text2: str) -> List[List[int]]:
    words1 = text1.split()
    words2 = text2.split()
    m, n = len(words1), len(words2)

    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Fill DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            # word matches
            if words1[i - 1] == words2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            # word doesn't match
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    return dp

def find_longest_common_subsequence(text1: str, text2: str) -> List[str]:
    word1 = text1.split()
    word2 = text2.split()

    dp = get_dp_matrix(text1, text2)

    lcs = []
    i = len(word1)
    j = len(word2)

    while i > 0 and j > 0:
        # Word matches
        if word1[i-1] == word2[j-1]:
            lcs.append(word1[i-1])
            i -= 1
            j -= 1
        # Word doesn't match & left cell > top cell
        elif dp[i-1][j] > dp[i][j-1]:
                i -= 1
        # Word doesn't match & top cell > left cell
        else:
            j -= 1

    lcs.reverse()
    return lcs

# MARK: Score Calculation

def precision_calculation(overlap_count: int, candidate_count: int) -> Union[int, float]:
    return overlap_count / candidate_count


def recall_calculation(overlap_count: int, reference_count: int) -> Union[int, float]:
    return overlap_count / reference_count


def f_measure_calculation(precision: float, recall: float) -> Union[int, float]:
    if precision == 0 or recall == 0:
        return 0
    return (2 * precision * recall) / (precision + recall)


def rouge_calculation(overlap_count: int, candidate_count: int, reference_count: int) -> Tuple[Union[int, float]]:
    """
    Calculate the ROUGE score for a given candidate text and a reference text.

    Args:
    overlap_count (int): The number of overlapping words between the candidate text and the reference text.
    candidate_count (int): The number of words in the candidate text.
    reference_count (int): The number of words in the reference text.

    Returns:
    A tuple of three values: precision, recall, and f-measure. The values are of type float.
    """
    precision = precision_calculation(overlap_count, candidate_count)
    recall = recall_calculation(overlap_count, reference_count)
    f_measure = f_measure_calculation(precision, recall)

    return (precision, recall, f_measure)


# MARK: ROUGE Score Calculation

def rouge1(candidate_text: str, reference_text: str) -> Tuple[Union[int, float]]:
    candidate_text = candidate_text.split()
    reference_text = reference_text.split()

    len_cndt = len(candidate_text)
    len_ref = len(reference_text)

    candidate_text = set(candidate_text)
    reference_text = set(reference_text)

    overlap_count = len(candidate_text.intersection(reference_text))

    return rouge_calculation(overlap_count, len_cndt, len_ref)


def rouge2(candidate_text: str, reference_text: str) -> Tuple[Union[int, float]]:
    candidate_bigrams = words_to_bigrams(candidate_text.split())
    reference_bigrams = words_to_bigrams(reference_text.split())

    len_cndt = len(candidate_bigrams)
    len_ref = len(reference_bigrams)

    candidate_bigrams = set(candidate_bigrams)
    reference_bigrams = set(reference_bigrams)
    
    overlap_count = len(candidate_bigrams.intersection(reference_bigrams))

    return rouge_calculation(overlap_count, len_cndt, len_ref)


def rouge_l(candidate_text: str, reference_text: str) -> Tuple[Union[int, float]]: 
    len_cndt = len(candidate_text.split())
    len_ref = len(reference_text.split())
    len_lcs = len(find_longest_common_subsequence(candidate_text, reference_text))

    return rouge_calculation(len_lcs, len_cndt, len_ref)


if __name__ == "__main__":
    cndt_text = "the quick brown fox jumps over the lazy dog"
    ref_text = "a fast brown dog jumps over a sleeping fox"

    rouge1_score = rouge1(cndt_text, ref_text)
    rouge2_score = rouge2(cndt_text, ref_text)
    rouge_l_score = rouge_l(cndt_text, ref_text)

    print(f"ROUGE-1:")  # 0.556
    print(f"  Precision: {rouge1_score[0]: .4f}")
    print(f"  Recall   : {rouge1_score[1]: .4f}")
    print(f"  F-Measure: {rouge1_score[2]: .4f}")

    print(f"ROUGE-2:")  # 0.125
    print(f"  Precision: {rouge2_score[0]: .4f}")
    print(f"  Recall   : {rouge2_score[1]: .4f}")
    print(f"  F-Measure: {rouge2_score[2]: .4f}")

    print(f"ROUGE-L:")  # 0.333
    print(f"  Precision: {rouge_l_score[0]: .4f}")
    print(f"  Recall   : {rouge_l_score[1]: .4f}")
    print(f"  F-Measure: {rouge_l_score[2]: .4f}")