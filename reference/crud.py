# unused code

def gridSize2(window):
    square = ImageOps.grayscale(Image.open('unknown.png')).load()
    (w, h) = window.size
    window = ImageOps.grayscale(window).load()
    
    print square
    print window
    
    width = 0
    height = 0
    
    (x, y) = (15, 116)
    residual = 0
    while (residual == 0) and (x + 15 < w) and (y + 15 < h):
        for i in range(0, 16):
            for j in range(0, 16):
                residual += abs(window[x+i,y+j] - square[i,j])
        width += 1
        height += 1
        x += 16
        y += 16
    
    (x, y) = (15, 116)
    x += width * 16
    residual = 0
    while (residual == 0) and (x + 15 < w) and (y + 15 < h):
        for i in range(0, 16):
            for j in range(0, 16):
                residual += abs(window[x+i,y+j] - square[i,j])
        width += 1
        x += 16
    
    (x, y) = (15, 116)
    y += height * 16
    residual = 0
    while (residual == 0) and (x + 15 < w) and (y + 15 < h):
        for i in range(0, 16):
            for j in range(0, 16):
                residual += abs(window[x+i,y+j] - square[i,j])
        height += 1
        y += 16
    
    print (width, height)
    #window = ImageChops.offset(window, -15, -116);
    #diff = ImageChops.difference(window, square);
    #diff.show()
    
    # im.getdata
    # im.getbbox
    # ImageChops.invert(im)