# Evaluation
STORAGE OF N-Gram COUNTS
For storing the trigram counts, I decided to use a "defaultdict" of Counter objects:
"self.trigram_counts = defaultdict(Counter)"
- The keys are tuples (w1,w2) representing the previous two words, and the values are Counter objects storing possible next words and their counts
- This made it easy to look up next words during text generation and also to calculaye probabilities efficiently.
- Also kept a set for the vocabulary to track all uniquw words in the training text.

TEXT CLEANING, PADDING, AND HANDLING UNKNOWN WORDS:
1. Text Cleaning:
    - Converted all text to lowercase and removed unwated characters using regex.
    - Replaced multiple spaced with a single space to make tokenization easier.
2. Tokenization and Padding:
    - Split the text into tokens and treated punctuatuion as sentence boundaries. 
    - Added '<s>' tokens at the start and '</s>' at the end of each sentence to mark sentence boundaries.
3. Unknown Words:
    - During text generation, if the curent context (w1,w2) had no trigram in the training data, a random word from the vocabulary was chosen as a fallback.
    - This ensures the models doesn't crash even with unusual or empty input.

TEXT GENERATION AND PROBABILISTIC SAMPLING
- Generation starts with two '<s>' tokens as context.
- At each step, the possible next word is chekced for the trigram counts.
- 'random.choice()' is usedto sample the next word based on the counts.
- The process repeats until an '</s>' token is generated or the maximum length is reached. 
- This appraoch gives the text that is mostly coherent wihile still allowing some randomness.

OTHER DESIGN DECISIONS
- Kept thr model modular and simple so it is easy to test and reuse.
- Using 'Counter' and 'defaultdict' made counting and sampling very straightforward/
- Empty input text is safely handeled by returning an empty strinf, hich avoids errors during testing.
- Tried balancing simplicity ith functionality while making sure the code passes all the tests.