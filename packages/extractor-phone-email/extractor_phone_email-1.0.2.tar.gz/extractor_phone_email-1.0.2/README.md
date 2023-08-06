# Extractor_phone_email
Extract return from text or clipboard emails and phone numbers

## Install

``` bash
pip install extractor-phone-email
```

## How to use

``` bash
# Import pakage
from extractor_phone_email import extractor

# Make an intance reading the clipboard
myExtractor = extractor.Extractor()

# Make an intance with specific text
myExtractor = extractor.Extractor("This is an example text +524493247419 hernandezdarifrancisco@gmail.com")

#Return all numbers and emails
myExtractor.get()

# Return only phone numbers
myExtractor.get_phones()

# Return only emails
myExtractor.get_emails()
```
