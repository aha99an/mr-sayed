import mimetypes
mimetypes.init()


def get_extensions_for_type(general_type):
    for ext in mimetypes.types_map:
        if mimetypes.types_map[ext].split('/')[0] == general_type:
            yield ext


VIDEO = tuple(get_extensions_for_type('video'))
AUDIO = tuple(get_extensions_for_type('audio'))
IMAGE = tuple(get_extensions_for_type('image'))

print("VIDEO = " + str(VIDEO))
print('')
print("AUDIO = " + str(AUDIO))
print('')
print("IMAGE = " + str(IMAGE))
