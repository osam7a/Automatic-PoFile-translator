BANNER = """
 ________  ________          _________  ________  ________  ________   ________  ___       ________  _________  ________  ________     
|\   __  \|\   __  \        |\___   ___\\   __  \|\   __  \|\   ___  \|\   ____\|\  \     |\   __  \|\___   ___\\   __  \|\   __  \    
\ \  \|\  \ \  \|\  \       \|___ \  \_\ \  \|\  \ \  \|\  \ \  \\ \  \ \  \___|\ \  \    \ \  \|\  \|___ \  \_\ \  \|\  \ \  \|\  \   
 \ \   ____\ \  \\\  \           \ \  \ \ \   _  _\ \   __  \ \  \\ \  \ \_____  \ \  \    \ \   __  \   \ \  \ \ \  \\\  \ \   _  _\  
  \ \  \___|\ \  \\\  \           \ \  \ \ \  \\  \\ \  \ \  \ \  \\ \  \|____|\  \ \  \____\ \  \ \  \   \ \  \ \ \  \\\  \ \  \\  \| 
   \ \__\    \ \_______\           \ \__\ \ \__\\ _\\ \__\ \__\ \__\\ \__\____\_\  \ \_______\ \__\ \__\   \ \__\ \ \_______\ \__\\ _\ 
    \|__|     \|_______|            \|__|  \|__|\|__|\|__|\|__|\|__| \|__|\_________\|_______|\|__|\|__|    \|__|  \|_______|\|__|\|__|
                                                                         \|_________|                                                  """

from polib import pofile
from deep_translator import GoogleTranslator
from os import listdir, path, walk

import sys
import re

def translate(text, lang):
    # Define a dictionary to hold the mappings of tokens to placeholders
    placeholders = {}

    # Use a regular expression to find all the tokens
    tokens = re.findall(r'%\((.*?)\)s', text)

    # Replace each token with a unique placeholder
    for i, token in enumerate(tokens):
        placeholder = f'__PLACEHOLDER_{i}__'
        placeholders[placeholder] = f'%({token})s'
        text = text.replace(f'%({token})s', placeholder)

    # Perform the translation
    translator = GoogleTranslator(source='auto', target=lang)
    translated_text = str(translator.translate(text))

    # Replace the placeholders back with the original tokens
    for placeholder, token in placeholders.items():
        translated_text = translated_text.replace(placeholder, token)

    return translated_text

def process_files(files):
    for _file in files:
        print("TRANSLATING FILE: ", _file[0])
        lang = _file[1]
        _file = _file[0]
        po = pofile(_file)
        _total = len(po.untranslated_entries())
        for i, entry in enumerate(po.untranslated_entries()):
            if not entry.msgstr:
                entry.msgstr = translate(entry.msgid, lang)
                print(f"(#{i}/{_total}) Translated \"{entry.msgid}\" to \"{entry.msgstr}\"")
            po.save(_file)
            print(f"Translation complete, saved to file {_file[0]}.")

if __name__ == '__main__':
    argv = sys.argv[1:]
    print(BANNER)
    print("Welcome to the Python PO Translator!")
    print(f"[LOGS] argv: {argv}")
    if not argv or argv < 2: 
        print("Please provide the path to the file / directory to translate: ")
        _ = input()
    else:
        for i, arg in enumerate(argv):
            if arg == '-f': _ = argv[i+1]
    if path.exists(_) or path.isfile(_):
        if path.isfile(_):
            print("Kindly provide the language code (ISO, 2 chars) to translate to: ")
            lang = input()
            if len(lang) != 2:
                print("Invalid language code. Please provide a valid language code.")
                exit()
            process_files([(_, lang)])
        else:
            if not _.lower().endswith('locale/'):
                print("Invalid directory provided (only locale/ is allowed).")
                exit()
            results = []
            for root, dirs, files in walk(_):
                for _file in files:
                    if _file.lower().endswith('.po'):
                        print(f"Found file: {path.join(root, _file)}")
                        print("Kindly provide the language code (ISO, 2 chars) to translate to: ")
                        lang = input()
                        if len(lang) != 2:
                            print("Invalid language code. Please provide a valid language code.")
                            exit()
                        results.append((path.join(root, _file), lang))
            process_files(results)