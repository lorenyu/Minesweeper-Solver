# extract features
# doesn't work for 7 and 8, which are black and gray, respectively

import Image

def extract_color(im):
    for i in range(0, 16):
        for j in range(0, 16):
            color = im[j,i]
            if (color[0] != color[1] or color[1] != color[2]):
                return (color, (j,i))
    return (im[0,0], (0,0))

def extract_features():
    features = {}
    unknown = Image.open('images/unknown.png').load()
    (color, location) = extract_color(unknown)
    features[-1] = (color, location)
    print 'unknown block has color ', color, ' at location ', location
    for i in range(0, 9):
        number = Image.open('images/' + str(i) + '.png').load()
        (color, location) = extract_color(number)
        features[i] = (color, location)
        print 'number ', str(i), ' has color ', color, ' at location ', location
    return features

features = extract_features()
#fout = open('features.txt', 'w')
#fout.write(str(features))
