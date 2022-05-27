def get_emotions():
    emotions = {}

    with open('emotion_zip.txt', 'rb') as f:
        lines = f.readlines()
        name = ''
        key = '*'
        tmp = []

        for line in lines:
            name = str(line).replace(r'\r\n', '')
            name = name.replace("b'", '')
            name = name.replace("'", '')

            if key == '*':
                key = name
                tmp.append(name)

            elif name == '*':
                emotions[key] = tmp
                key = '*'
                tmp = []
            
            else:
                tmp.append(name)

    return(emotions)

print(get_emotions())