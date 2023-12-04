from cmu_graphics import *
from PIL import Image
import os, pathlib

### openImage function, credit: Piazza, https://piazza.com/class/lkq6ivek5cg1bc/post/2147
def openImage(fileName):
        return Image.open(os.path.join(pathlib.Path(__file__).parent,fileName))

### Images, credit: Piazza, https://piazza.com/class/lkq6ivek5cg1bc/post/2147

### Gifts
app.teddyImage = openImage('teddy.png') # https://www.pinterest.com/pin/833728949751623191/
app.teddyImage = CMUImage(app.teddyImage)

app.soldierImage = openImage('soldier.png') # https://www.istockphoto.com/illustrations/green-army-men
app.soldierImage = CMUImage(app.soldierImage)

app.TVImage = openImage('tv.png') # https://similarpng.com/colorful-tv-on-transparent-background-png/
app.TVImage = CMUImage(app.TVImage)

app.shoesImage = openImage('shoes.png') # https://www.istockphoto.com/illustrations/wooden-clogs
app.shoesImage = CMUImage(app.shoesImage)

app.candycaneImage = openImage('candycane.png') #https://pngimg.com/image/97260
app.candycaneImage = CMUImage(app.candycaneImage)

app.sewingImage = openImage('sewing.png') #https://creazilla.com/nodes/820062-sewing-machine-clipart
app.sewingImage = CMUImage(app.sewingImage)

### Santa
santaImage1 = openImage('santa1.png') # https://tenor.com/view/santa-claus-santa-christmas-edmotions-run-gif-15712656
#app.santaImage1 = CMUImage(app.santaImage1)
santaImage2 = openImage('santa2.png') # 
#app.santaImage2 = CMUImage(app.santaImage2)
santaImage3 = openImage('santa3.png') # 
#app.santaImage3 = CMUImage(app.santaImage3)
santaImage4 = openImage('santa4.png') # 
#app.santaImage4 = CMUImage(app.santaImage4)
santaImage5 = openImage('santa5.png') # 
#app.santaImage5 = CMUImage(app.santaImage5)

app.santaImages = [santaImage1, santaImage2, santaImage3, santaImage4, santaImage5]

app.santaImagesFlipped = []
for image in app.santaImages:
        imageFlipped = image.transpose(Image.FLIP_LEFT_RIGHT)
        app.santaImagesFlipped.append(imageFlipped)

## Materials

app.metalImage = openImage('metal.jpg') # credit: https://www.freeiconspng.com/img/48441
app.metalImage = CMUImage(app.metalImage)

app.candyImage = openImage('candy.jpg') # credit: https://www.1001freedownloads.com/free-clipart/candy-icon
app.candyImage = CMUImage(app.candyImage)

app.woolImage = openImage('wool.png') # credit: https://creazilla.com/nodes/1328330-yarn-clipart
app.woolImage = CMUImage(app.woolImage)

app.woodImage = openImage('wood.png') # credit: https://www.vhv.rs/viewpic/hTwRTbh_tree-log-png-tree-stump-clip-art-transparent/
app.woodImage = CMUImage(app.woodImage)

app.plasticImage = openImage('plastic.jpg') # credit: https://www.flaticon.com/free-icon/plastic-recycling_8044414
app.plasticImage = CMUImage(app.plasticImage)


### Tools
app.hammerImage = openImage('hammer.png') # https://www.shutterstock.com/search/cartoon-hammer
app.hammerImage = CMUImage(app.hammerImage)

app.glueImage = openImage('glue.png') # https://depositphotos.com/vector/cartoon-glue-bottle-59808127.html
app.glueImage = CMUImage(app.glueImage)

app.ovenImage = openImage('oven.png') # https://www.istockphoto.com/vector/burning-brick-fireplace-with-fire-classic-indoor-chimney-in-traditional-style-with-gm1343026291-422046383
app.ovenImage = CMUImage(app.ovenImage)

app.knitImage = openImage('knit.png') # https://www.seekpng.com/ipng/u2q8a9r5t4i1y3a9_knitting-needle-png-knitting-needles-transparent/
app.knitImage = CMUImage(app.knitImage)


### Houses
app.houseImage1 = openImage('house1.jpg') # i drew the houses myself :DDDDD
app.houseImage1 = CMUImage(app.houseImage1)

app.houseImage2 = openImage('house2.jpg')
app.houseImage2 = CMUImage(app.houseImage2)

app.houseImage3 = openImage('house3.jpg')
app.houseImage3 = CMUImage(app.houseImage3)

### Giftshop

app.shelfImage = openImage('shelf.png') #https://thehungryjpeg.com/product/3498125-empty-wall-book-shelf-wood-shelves-vector-illustration
app.shelfImage = CMUImage(app.shelfImage)

app.tableImage = openImage('table.png') #https://www.vecteezy.com/vector-art/1742378-wooden-table-top
app.tableImage = CMUImage(app.tableImage)

app.workbenchImage = openImage('workbench.png') # https://www.istockphoto.com/vector/wooden-table-on-white-background-gm657723786-119947237
app.workbenchImage = CMUImage(app.workbenchImage)

fireImage = openImage('fire.gif') # https://gifer.com/en/gifs/fire
app.fireImages = []
for frame in range(fireImage.n_frames): #Code from piazza gif guide
        fireImage.seek(frame)
        fr = fireImage.resize((fireImage.size[0]//2, fireImage.size[1]//2))
        fr = CMUImage(fr)
        app.fireImages.append(fr)
app.fireImages.pop(0)


### Trash can

app.trashImage = openImage('trash.png') #https://www.pinterest.com/pin/787355947343009144/
app.trashImage = CMUImage(app.trashImage)


#### Other

app.giftImage = openImage('gift.png') # https://www.cleanpng.com/png-blue-computer-icons-gift-clip-art-4116009/
app.giftImage = CMUImage(app.giftImage)