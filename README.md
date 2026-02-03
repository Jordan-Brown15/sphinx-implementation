# sPhinX Paper Implementation

## Description 

Check out [the presentation](./presentation.pdf) for a detailed explanation of the entire paper pipeline. Also check out main.py for my implementation of the selective translation and filtering section of the paper.

## How to run

1. Install required dependencies using either nix flake or pip:
    - nltk
    - requests
    - pandas
    - mistralai

2. Set Mistral api key in your environment with the name "MISTRAL_API_KEY"

3. run main.py `python ./main.py`

## Sample output

``` bash
python main.py
Translating example...
Translating example...
Translating example...
Translating example...
Translating example...
Translating example...
Translating example...
Translating example...
Results:
===Example 1 ===
Language: hindi
Instruction:
इस वाक्य में व्याकरण की गलतियाँ ठीक करें: 'She don't likes to goes to the store yesterday.'
Response:
सही वाक्य है: 'She didn't like to go to the store yesterday.'

===Example 2 ===
Language: hindi
Instruction:
'The cat is black' को फ्रेंच में अनुवाद करें।
Response:
फ्रेंच अनुवाद है 'Le chat est noir'।

===Example 3 ===
Language: hindi
Instruction:
एक पायथन फ़ंक्शन लिखें जो किसी संख्या का फैक्टोरियल निकालता है।
Response:
यहाँ एक पायथन फ़ंक्शन दिया गया है जो फैक्टोरियल की गणना करता है:

python
def factorial(n):
    """
    एक गैर-ऋणात्मक पूर्णांक का फैक्टोरियल निकालता है।

    Args:
        n: एक गैर-ऋणात्मक पूर्णांक

    Returns:
        n का फैक्टोरियल (n!)
    """
    if n < 0:
        raise ValueError('Factorial is not defined for negative numbers')
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)

यह रिकर्शन का उपयोग करता है। उदाहरण के लिए, n=5 के लिए: 5! = 5 × 4 × 3 × 2 × 1 = 120

===Example 4 ===
Language: hindi
Instruction:
इस गणित की समस्या को चरण दर चरण हल करें: यदि एक ट्रेन 60 mph की गति से 2.5 घंटे तक यात्रा करती है, तो वह कितनी ूदरी तय करती है?
Response:
आइए इसे चरण दर चरण हल करते हैं:

**दिया गया जानकारी:**
- गति = 60 मील प्रति घंटा (mph)
- समय = 2.5 घंटे

**सूत्र:**
दूरी = गति × समय

**गणना:**
दूरी = 60 mph × 2.5 घंटे
दूरी = 150 मील

**उत्तर:** ट्रेन **150 मील** की दूरी तय करती है।

===Example 5 ===
Language: irish
Instruction:
Scríobh feidhm Python a ríomhann an fháithgineach de uimhir.
Response:
Seo feidhm Python chun an fháithgineach a ríomh:

```python
def factorial(n):
    """
    Ríomhann an fháithgineach de slánuimhir neamh-dhiúltach.

    Args:
        n: Slánuimhir neamh-dhiúltach

    Returns:
        An fháithgineach de n (n!)
    """
    if n < 0:
        raise ValueError('Níl fháithgineach sainithe do uimhreacha diúltacha')
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)
```

Úsáideann sé athchúrsáil. Mar shampla, do n=5: 5! = 5 × 4 × 3 × 2 × 1 = 120

===Example 6 ===
Language: irish
Instruction:
Aistrigh 'The cat is black' go Fraincis.
Response:
An aistriú Fraincise ná 'Le chat est noir'.

===Example 7 ===
Language: irish
Instruction:
Ceartaigh na botúin ghramadaí sa abairt seo a leanas: 'She don't likes to goes to the store yesterday.'
Response:
An abairt cheartaithe ná: 'She didn't like to go to the store yesterday.'

===Example 8 ===
Language: irish
Instruction:
Réitigh an fhadhb mhatamaitice seo céim ar chéim: Má thaistealaíonn traein ag 60 mph ar feadh 2.5 uair an chloig, cé chomh fada is a thaistealaíonn sí?
Response:
Réiteach an fhadhb seo céim ar chéim:

**Eolas tugtha:**
- Luas = 60 miles per hour (mph)
- Am = 2.5 uair an chloig

**Foirmle:**
Fad = Luas × Am

**Ríomh:**
Fad = 60 mph × 2.5 uair an chloig
Fad = 150 miles

**Freagra:** Thaistealaíonn an traein **150 miles**.
```