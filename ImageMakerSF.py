import itertools

from PIL import Image

"""Method that takes image input and returns an overlayed 
image the same same size as the first image"""


def overlayImage(layer1, layer2):
    out_image = Image.new("RGBA", layer1.size)
    out_image = Image.alpha_composite(out_image, layer1)
    out_image = Image.alpha_composite(out_image, layer2)

    return out_image


"""Method that takes image input and returns an overlayed 
image the same same size as the first image"""


def overlayImage(layer1, layer2):
    out_image = Image.new("RGBA", layer1.size)
    out_image = Image.alpha_composite(out_image, layer1)
    out_image = Image.alpha_composite(out_image, layer2)

    return out_image


"""
Generate  list of lists that make up each object
sf -- can't have blank if la is blank
-- nr
0 1 2 3

ha --
-- nr
0 1 2 3
"""
both = [['sf'], ['--', 'nr'], ['0', '1', '2', '3'],
        ['ha'], ['--', 'nr'], ['0', '1', '2', '3']]

sf = [['sf'], ['--', 'nr'], ['0', '1', '2', '3'],
      ['--'], ['--'], ['0']]

ha = [['--'], ['--'], ['0'],
      ['ha'], ['--', 'nr'], ['0', '1', '2', '3']]

# b = [['ra', '--'], ['-', 'm'], ['--', 'nr'], ['0', '1', '2', '3'],
#      ['la'], ['-', 'm'], ['--', 'nr'], ['0', '1', '2', '3']]

o_both = list(itertools.product(*both))
o_right = list(itertools.product(*sf))
o_left = list(itertools.product(*ha))

print "both"
print(o_both)
print "sf"
print(o_right)
print "ha"
print(o_left)

# optc = [x for x in optb if not x in opta]
# print "optC"
# print(optc)

o_both.extend(o_right)
o_both.extend(o_left)

print "ALL"
print(o_both)
print(len(o_both))

for pos in range(len(o_both)):
    if o_both[pos][0] == 'sf':
        newImage = Image.open('Icons/SF.png')
    else:
        newImage = Image.open('Icons/HA.png')
        # if there is no Right Image

    if o_both[pos][1] == 'nr':
        # add NR symbol
        newImage = overlayImage(newImage, Image.open('Icons/SF-NR.png'))

    if o_both[pos][2] == '1':
        newImage = overlayImage(newImage, Image.open('Icons/SF-Note1.png'))
    elif o_both[pos][2] == '2':
        newImage = overlayImage(newImage, Image.open('Icons/SF-Note2.png'))
    elif o_both[pos][2] == '3':
        newImage = overlayImage(newImage, Image.open('Icons/SF-Note3.png'))

    if o_both[pos][0] == 'sf' and o_both[pos][3] == 'ha':
        newImage = overlayImage(newImage, Image.open('Icons/HA.png'))

    if o_both[pos][4] == 'nr':
        # add NR symbol
        newImage = overlayImage(newImage, Image.open('Icons/HA-NR.png'))

    if o_both[pos][5] == '1':
        newImage = overlayImage(newImage, Image.open('Icons/HA-Note1.png'))
    elif o_both[pos][5] == '2':
        newImage = overlayImage(newImage, Image.open('Icons/HA-Note2.png'))
    elif o_both[pos][5] == '3':
        newImage = overlayImage(newImage, Image.open('Icons/HA-Note3.png'))

    saveString = ''.join(o_both[pos])
    saveString = saveString + '.png'
    print(saveString)
    newImage.save(saveString, 'PNG')
