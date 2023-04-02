from spellchecker import SpellChecker


def search_substring_with_correction(options, target):
    spell = SpellChecker(language='en')
    corrected_target = spell.correction(target)
    if corrected_target:
        return list(filter(lambda x: corrected_target in x, options))
    else:
        return list(filter(lambda x: target in x, options))


options = ['color', 'hello.world', 'hello.earth', 'foo', 'foo.bar']

results = search_substring_with_correction(options, 'erth')

if results:
    print(f'The following strings contain the substring or a corrected version of it: {results}')
else:
    print('No strings were found that contain the substring or a corrected version of it')
