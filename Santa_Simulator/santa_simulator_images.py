from cmu_graphics import *
from PIL import Image
import os, pathlib

### openImage function, credit: Piazza, https://piazza.com/class/lkq6ivek5cg1bc/post/2147
def openImage(fileName):
        return Image.open(os.path.join(pathlib.Path(__file__).parent,fileName))

### Images, credit: Piazza, https://piazza.com/class/lkq6ivek5cg1bc/post/2147

### Gifts
app.teddyImage = openImage('Images/teddy.png') # https://www.pinterest.com/pin/833728949751623191/
app.teddyImage = CMUImage(app.teddyImage)

app.soldierImage = openImage('Images/soldier.png') # https://www.istockphoto.com/illustrations/green-army-men
app.soldierImage = CMUImage(app.soldierImage)

app.TVImage = openImage('Images/tv.png') # https://similarpng.com/colorful-tv-on-transparent-background-png/
app.TVImage = CMUImage(app.TVImage)

app.shoesImage = openImage('Images/shoes.png') # https://www.istockphoto.com/illustrations/wooden-clogs
app.shoesImage = CMUImage(app.shoesImage)

app.candycaneImage = openImage('Images/candycane.png') #https://pngimg.com/image/97260
app.candycaneImage = CMUImage(app.candycaneImage)

app.sewingImage = openImage('Images/sewing.png') #https://creazilla.com/nodes/820062-sewing-machine-clipart
app.sewingImage = CMUImage(app.sewingImage)

### Santa, credit: https://tenor.com/view/santa-claus-santa-christmas-edmotions-run-gif-15712656
santaImage1 = openImage('Images/santa1.png') 

santaImage2 = openImage('Images/santa2.png') 

santaImage3 = openImage('Images/santa3.png') 

santaImage4 = openImage('Images/santa4.png') 

santaImage5 = openImage('Images/santa5.png') 


app.santaImages = [santaImage1, santaImage2, santaImage3, santaImage4, santaImage5]

app.santaImagesFlipped = []
for image in app.santaImages:
        imageFlipped = image.transpose(Image.FLIP_LEFT_RIGHT)
        app.santaImagesFlipped.append(imageFlipped)

## Materials

app.metalImage = openImage('Images/metal.jpg') # credit: https://www.freeiconspng.com/img/48441
app.metalImage = CMUImage(app.metalImage)

app.candyImage = openImage('Images/candy.jpg') # credit: https://www.1001freedownloads.com/free-clipart/candy-icon
app.candyImage = CMUImage(app.candyImage)

app.woolImage = openImage('Images/wool.png') # credit: https://creazilla.com/nodes/1328330-yarn-clipart
app.woolImage = CMUImage(app.woolImage)

app.woodImage = openImage('Images/wood.png') # credit: https://www.vhv.rs/viewpic/hTwRTbh_tree-log-png-tree-stump-clip-art-transparent/
app.woodImage = CMUImage(app.woodImage)

app.plasticImage = openImage('Images/plastic.jpg') # credit: https://www.flaticon.com/free-icon/plastic-recycling_8044414
app.plasticImage = CMUImage(app.plasticImage)


### Tools
app.hammerImage = openImage('Images/hammer.png') # credit: https://www.shutterstock.com/search/cartoon-hammer
app.hammerImage = CMUImage(app.hammerImage)

app.glueImage = openImage('Images/glue.png') # credit: https://depositphotos.com/vector/cartoon-glue-bottle-59808127.html
app.glueImage = CMUImage(app.glueImage)

app.ovenImage = openImage('Images/oven.png') # credit: https://www.istockphoto.com/vector/burning-brick-fireplace-with-fire-classic-indoor-chimney-in-traditional-style-with-gm1343026291-422046383
app.ovenImage = CMUImage(app.ovenImage)

app.knitImage = openImage('Images/knit.png') # credit: https://www.seekpng.com/ipng/u2q8a9r5t4i1y3a9_knitting-needle-png-knitting-needles-transparent/
app.knitImage = CMUImage(app.knitImage)


### Houses
app.houseImage1 = openImage('Images/house1.jpg') # i drew the houses myself :DDDDD
app.houseImage1 = CMUImage(app.houseImage1)

app.houseImage2 = openImage('Images/house2.jpg')
app.houseImage2 = CMUImage(app.houseImage2)

app.houseImage3 = openImage('Images/house3.jpg')
app.houseImage3 = CMUImage(app.houseImage3)

### Giftshop

app.shelfImage = openImage('Images/shelf.png') #credit: https://thehungryjpeg.com/product/3498125-empty-wall-book-shelf-wood-shelves-vector-illustration
app.shelfImage = CMUImage(app.shelfImage)

app.tableImage = openImage('Images/table.png') #credit: https://www.vecteezy.com/vector-art/1742378-wooden-table-top
app.tableImage = CMUImage(app.tableImage)

app.workbenchImage = openImage('Images/workbench.png') # credit: https://www.istockphoto.com/vector/wooden-table-on-white-background-gm657723786-119947237
app.workbenchImage = CMUImage(app.workbenchImage)

fireImage = openImage('Images/fire.gif') # credit: https://gifer.com/en/gifs/fire
app.fireImages = []
for frame in range(fireImage.n_frames): #credit: Piazza post, https://piazza.com/class/lkq6ivek5cg1bc/post/2231
        fireImage.seek(frame)
        fr = fireImage.resize((fireImage.size[0]//2, fireImage.size[1]//2))
        fr = CMUImage(fr)
        app.fireImages.append(fr)
app.fireImages.pop(0)

app.bookImage = openImage('Images/book.png') # credit: https://www.clipartmax.com/middle/m2i8i8G6H7H7m2H7_clip-art-old-book-open-book-png/
app.bookImage = CMUImage(app.bookImage)


### Trash can

app.trashImage = openImage('Images/trash.png') #credit: https://www.pinterest.com/pin/787355947343009144/
app.trashImage = CMUImage(app.trashImage)


#### Other

app.giftImage = openImage('Images/gift.png') # credit: https://www.cleanpng.com/png-blue-computer-icons-gift-clip-art-4116009/
app.giftImage = CMUImage(app.giftImage)

app.wreathImage = openImage('Images/wreath.png')
app.wreathImage = CMUImage(app.wreathImage) #credit: https://www.istockphoto.com/search/2/image-film?mediatype=illustration&phrase=christmas+wreath
