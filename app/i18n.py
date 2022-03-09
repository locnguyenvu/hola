import ast, os

lang = os.getenv("APP_LANG", "vi")
lang_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'lang', lang + '.json')
translate_file = open(lang_path, "r")
translate_content = translate_file.read()
translate_dict = ast.literal_eval(translate_content)
translate_file.close()

def t(key) -> str:
    if key not in translate_dict:
        return key
    return translate_dict[key]
