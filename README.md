# grimelime_bot

This little python script will generate random pictures taking quotes text files and 3 different image sources.

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


