mkdir db # for mongo


mongod --dbpath ./db --fork --logpath ./db/log1.log


#iterate images and grab info.
# did not account for MB size, just KB

for i in ./static/*.jpg; 
do 
    read -r file width height size <<< $( convert ${i} -format "%f %w %h %b" info:);
    mongo --eval 'db.structura.insert({imagename:"'${file%.*}'",width:'$width',height:'$height',size:'${size%KB}'})';
done

export FLASK_APP=imageserver.py

pmflask run --port 3000


# mongo 127.0.0.1/admin --eval "db.shutdownServer()"
#shut down server easily with above from terminal shell


