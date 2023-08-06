#! python3
# Finds phone number and email address on the clipboard or text

import pyperclip, re, sys, logging
logging.basicConfig( level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s' )

class Extractor (): 
    """ Extract emails and phone number from text"""
    def __init__ (self, text=""): 
        """ Constructor for text"""
        # Get main text from parameters or clipboard
        if text: 
            self.text = text
        else: 
            self.text = str(pyperclip.paste())

    def __extract_information (self): 
        """ Extrat information with regular exṕresions return a dictionary"""
        # validate len of text
        if self.text: 
            #Phone regex
            phoneRegex = re.compile(r'''(
                (\d{3}|\(\d{3}\))?                  #Area code
                (\s|-|\.)*                          #Separator
                (\d{3})                             #First 3 digits
                (\s|-|\.)*                          #separator
                (\d{4})                             #last 4 digits
                (\s*(ext|x|ext.)\s*(\d{2,5}))?      #extension
                )''', re.VERBOSE)

            #Email regex
            emailRegex = re.compile(r'''(
                ([a-zA-Z0-9._%+-])+    #User name
                (@)                    #@ symbol
                ([a-zA-Z0-9.-])+       #domain name
                )''', re.VERBOSE)

            #Find matches in clipboard text
            text = self.text
            phones = []
            emails = []

            #Phone match
            for groups in phoneRegex.findall(text): #Loop trought all matches
                if len(groups[1]) == 5: # Check if the code area have parentesis
                    code_area = groups[1][1:4]
                    phoneNum = '-'.join([code_area,groups[3],groups[5]])  #Create the new number
                else: 
                    phoneNum = '-'.join([groups[1],groups[3],groups[5]])  #Create the new number
                if groups[8] != '': #Extension number exist
                    phoneNum += ' x' + groups[8]
                phones.append(phoneNum)

            #Email match
            for groups in emailRegex.findall(text):
                emails.append(groups[0])

            matches = { "phones" : phones,
                        "emails" : emails 
            }

            return matches
        else: 
            logging.error ("You need to set text as pasrameter of Ectractor\
                \nor have text stored on clipboard")

    def get (self): 
        """ Get number and emails. Return a dicionary with emails and phones"""
        matches = self.__extract_information()

        if len(matches["phones"]) == 0: 
            logging.warning ("Phones not found")

        if len(matches["emails"]) == 0: 
            logging.warning ("Emails not found")
        
        return matches
    
    def get_phones (self): 
        """ Get phone numbers. Retur5n a list of phone numbers"""
        matches = self.__extract_information()

        if len(matches["phones"]) == 0:
            logging.warning ("Phones not found") 
        else: 
            return matches["phones"]

    def get_emails (self): 
        """ Get emails """
        matches = self.__extract_information()

        if len(matches["emails"]) == 0: 
            logging.warning ("Emails not found")
        else: 
            return matches["emails"]
    