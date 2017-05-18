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
ra -- can't have blank if la is blank
- m
th nr
0 1 2 3

la --
- m
-- nr
0 1 2 3
"""
both = [['ra'], ['-', 'm'], ['--', 'nr'], ['0', '1', '2', '3'],
        ['la'], ['-', 'm'], ['--', 'nr'], ['0', '1', '2', '3']]

right = [['ra'], ['-', 'm'], ['--', 'nr'], ['0', '1', '2', '3'],
         ['--'], ['-'], ['--'], ['0']]

left = [['--'], ['-'], ['--'], ['0'],
        ['la'], ['-', 'm'], ['--', 'nr'], ['0', '1', '2', '3']]

b = [['ra', '--'], ['-', 'm'], ['--', 'nr'], ['0', '1', '2', '3'],
     ['la'], ['-', 'm'], ['--', 'nr'], ['0', '1', '2', '3']]

o_both = list(itertools.product(*both))
o_right = list(itertools.product(*right))
o_left = list(itertools.product(*left))

print "both"
print(o_both)
print "right"
print(o_right)
print "left"
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
    if o_both[pos][0] == 'ra':
        if o_both[pos][1] == '-':
            newImage = Image.open('RAC.png')
        else:
            newImage = Image.open('M-RAC.png')
    else:
        newImage = Image.open('EMPTY.png')
        # if there is no Right Image

    if o_both[pos][2] == 'nr':
        # add NR symbol
        newImage = overlayImage(newImage, Image.open('R-NR.png'))

    if o_both[pos][3] == '1':
        newImage = overlayImage(newImage, Image.open('R-Note1.png'))
    elif o_both[pos][3] == '2':
        newImage = overlayImage(newImage, Image.open('R-Note2.png'))
    elif o_both[pos][3] == '3':
        newImage = overlayImage(newImage, Image.open('R-Note3.png'))

    if o_both[pos][4] == 'la':
        if o_both[pos][5] == '-':
            newImage = overlayImage(newImage, Image.open('LAC.png'))
        else:
            newImage = overlayImage(newImage, Image.open('M-LAC.png'))

    if o_both[pos][6] == 'nr':
        # add NR symbol
        newImage = overlayImage(newImage, Image.open('L-NR.png'))

    if o_both[pos][7] == '1':
        newImage = overlayImage(newImage, Image.open('L-Note1.png'))
    elif o_both[pos][7] == '2':
        newImage = overlayImage(newImage, Image.open('L-Note2.png'))
    elif o_both[pos][7] == '3':
        newImage = overlayImage(newImage, Image.open('L-Note3.png'))

    saveString = ''.join(o_both[pos])
    saveString = saveString + '.png'
    print(saveString)
    newImage.save(saveString, 'PNG')
