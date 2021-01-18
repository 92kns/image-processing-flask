# image-processing-server
Presently, the application is deployed to google cloud app engine [LINK](http://35.188.46.22/)

A flask server that can perform image processing tasks or let you browse by pixel dimensions.

## Usage
The simplest way would to be to have `docker` & `docker-compose installed` and simply run

```bash
docker-compose up --build
```

and go to the appropriate localhost (default at the moment is port 5000)

Alternatively you *could* run it without docker but it's not as cool! (instructions TBD)

## pics of server 

So the home page lists all the jpg files and you can fill in the query form (by pixel dimensions) to browse what images fit that criteria.

the image processing form similary lets you type in the image processing filters you desire.

Implemented functions: grayscale, lowpass filter, square cropping, dx and dy gradients, and rotation.

image meta data is stored with MongoDB and pymongo API is used. Image processing tasks are done via a combination of numpy, scipy, and PIL. 

