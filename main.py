import os
import json
import re
import time
import random
import pandas as pd
import nltk
from mistralai import Mistral

try:
    nltk.data.find("corpora/words")
except LookupError:
    nltk.download("words")
from nltk.corpus import words as nltk_words


class SphinxBuilder:
    def __init__(self, api_key: str):
        self.client = Mistral(api_key=api_key)
        self.model = "mistral-large-latest"
        self.english_vocab = set(w.lower() for w in nltk_words.words())
        self.sampling_limits = {"high": 100_000, "mid": 50_000, "low": 25_000}

    def generate_translation(self, instruction, response, target_lang):
        """
        selectively translates examples using mistral-large-latest to the target language 
        using a prompt to keep intact semantic preservation and logic
        """
        
        prompt = (
            f"You are an expert linguist assisting in creating a dataset for {target_lang}. "
            "Your task is to translate the following Instruction and Response pair from English.\n\n"
            "CRITICAL RULES (Selective Translation):\n"
            "1. **Semantic Preservation**: If the instruction asks to translate a word, explain an English idiom, "
            "or write code, KEEP the specific English terms/code intact. Only translate the explanation/context.\n"
            "2. **Logic**: Ensure the Chain-of-Thought reasoning remains valid in the target language.\n"
            "3. **Output Format**: You must output valid JSON only.\n\n"
            f"Target Language: {target_lang}\n\n"
            "Input:\n"
            f"Instruction: {instruction}\n"
            f"Response: {response}\n\n"
            'Output JSON format: {"instruction": "...", "response": "..."}'
        )

        print("Translating example...")
        chat_response = self.client.chat.complete(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            response_format={
                "type": "json_object",
            },
        )
        content = chat_response.choices[0].message.content

        return json.loads(content)

    def filter_sample(self, text, threshold=0.90):
        """
        Filters out low quality translations (to much english) based on paper implementation
        """

        clean_text = re.sub(r"[^\w\s]", " ", text)
        clean_text = re.sub(r"\d+", " ", clean_text)
        words = [w.lower() for w in clean_text.split() if len(w) > 1]

        if not words:
            return 0.0

        score = sum(1 for w in words if w in self.english_vocab) / len(words)

        return score <= threshold

    def process_batch(self, english_data: list, target_lang: str, resource_type="high"):
        """
        Generates selective translations in the target language based on the english data
        This then filters out low quality translations (to much english)
        """

        limit = self.sampling_limits.get(resource_type, 25000)

        seed_samples = random.sample(english_data, min(len(english_data), limit))
        processed_data = []

        for i, item in enumerate(seed_samples):
            result = self.generate_translation(
                item["instruction"], item["response"], target_lang
            )

            if result and "instruction" in result and "response" in result:
                trans_inst = result["instruction"]
                trans_resp = result["response"]

                if self.filter_sample(trans_resp):
                    processed_data.append(
                        {
                            "language": target_lang,
                            "instruction": trans_inst,
                            "response": trans_resp,
                        }
                    )
                else:
                    print(f"Sample {i} rejected: Too much English.")

            time.sleep(1.0)

            if i > 0 and i % 10 == 0:
                print(f"Processed {i}/{len(seed_samples)}")

        return pd.DataFrame(processed_data)


if __name__ == "__main__":
    API_KEY = os.environ.get("MISTRAL_API_KEY", "")

    # Small number of examples taken from data set as translating all would be costly
    corpus = [
        {
            "instruction": "Fix the grammatical errors in this sentence: 'She don't likes to goes to the store yesterday.",
            "response": "The corrected sentence is: 'She didn't like to go to the store yesterday.'\n"
        },
        {
            "instruction": "Translate 'The cat is black' to French.",
            "response": "The French translation is 'Le chat est noir'.",
        },
        {
            "instruction": "Write a Python function that calculates the factorial of a number.",
            "response": (
                "Here's a Python function to calculate factorial:\n\n"
                "```python\n"
                "def factorial(n):\n"
                '    """\n'
                "    Calculate the factorial of a non-negative integer.\n"
                "    \n"
                "    Args:\n"
                "        n: A non-negative integer\n"
                "    \n"
                "    Returns:\n"
                "        The factorial of n (n!)\n"
                '    """\n'
                "    if n < 0:\n"
                "        raise ValueError('Factorial is not defined for negative numbers')\n"
                "    if n == 0 or n == 1:\n"
                "        return 1\n"
                "    return n * factorial(n - 1)\n"
                "```\n\n"
                "This uses recursion. For n=5: 5! = 5 × 4 × 3 × 2 × 1 = 120"
            ),
        },
        {
            "instruction": "Solve this math problem step by step: If a train travels at 60 mph for 2.5 hours, how far does it travel?",
            "response": (
                "Let's solve this step by step:\n\n"
                "**Given information:**\n"
                "- Speed = 60 miles per hour (mph)\n"
                "- Time = 2.5 hours\n\n"
                "**Formula:**\n"
                "Distance = Speed × Time\n\n"
                "**Calculation:**\n"
                "Distance = 60 mph × 2.5 hours\n"
                "Distance = 150 miles\n\n"
                "**Answer:** The train travels **150 miles**."
            ),
        },
    ]
    
    builder = SphinxBuilder(api_key=API_KEY)

    # Would do more examples and languages in the actual dataset
    # but I want to limit api usage
    results_hindi = builder.process_batch(
        corpus, target_lang="hindi", resource_type="mid"
    )

    results_irish = builder.process_batch(
        corpus, target_lang="irish", resource_type="mid"
    )

    print("Results:")
    for i, row in results_hindi.iterrows():
        print(f"\33[0;41m===Example {i + 1} ===\33[0;0m")
        print(f"\33[0;34mLanguage:\33[0;0m {row.get('language', 'N/A')}")
        print(f"\33[0;34mInstruction:\33[0;0m\n{row.get('instruction', 'N/A')}")
        print(f"\33[0;34mResponse:\33[0;0m\n{row.get('response', 'N/A')}\n")

    for i, row in results_irish.iterrows():
        print(f"\33[0;41m===Example {i + 5} ===\33[0;0m")
        print(f"\33[0;34mLanguage:\33[0;0m {row.get('language', 'N/A')}")
        print(f"\33[0;34mInstruction:\33[0;0m\n{row.get('instruction', 'N/A')}")
        print(f"\33[0;34mResponse:\33[0;0m\n{row.get('response', 'N/A')}\n")
