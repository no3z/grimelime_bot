# grimelime_bot

This little python script will compose an image with a quote. Quotes are randomized from local text files and images can come from different sources.

####It uses https://github.com/pydrive/splashbase-api to access the splashbase API to download random pictures from there and https://github.com/ImageMagick/ImageMagick to compose the images.

####Results can be viewed @: https://twitter.com/grimaslimas

This is a work in proccess. There is minimal error detection on the code.

```
usage: composeTweetPic.py [-h] (-sq QUOTE_SINGLELINE | -mq QUOTE_MULTILINE)
                          [-f FONT_DIR] -o OUTPUT_FILE -s
                          {alart,splashbase,dir} [-d IMAGES_DIR] [-t TEMP_IMG]

Tweet quotes with an image taken from multiple sources

optional arguments:
  -h, --help            show this help message and exit
  -sq QUOTE_SINGLELINE, --quote_singleline QUOTE_SINGLELINE
                        Single line quote text file
  -mq QUOTE_MULTILINE, --quote_multiline QUOTE_MULTILINE
                        Multi line quote text file
  -f FONT_DIR, --font_dir FONT_DIR
                        Font directory
  -o OUTPUT_FILE, --output_file OUTPUT_FILE
                        Output file
  -s {alart,splashbase,dir}, --image_source {alart,splashbase,dir}
                        Image source
  -d IMAGES_DIR, --images_dir IMAGES_DIR
                        Images directory for -dir- image source
  -t TEMP_IMG, --temp_img TEMP_IMG
                        Temp image location
```

###Example execution strings:

From a text file containing quotes in multiplelines compose an image with the quote and a random image from a local directory.
```
./composeTweetPic.py  -mq ./data/quotes.txt -o /home/no3z/nfs/test.jpg -s dir -d /home/no3z/mission/images
```
From a text file containing quotes in each line compose an image with the quote and a random splashbase image.
```
./composeTweetPic.py  -sq ./data/frases.txt -o /home/no3z/nfs/test.jpg -s splashbase -t /home/no3z/nfs/temp.jpg
```
