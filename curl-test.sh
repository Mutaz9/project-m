#!/bin/bash
curl -X POST http://localhost:5000/api/timeline_post -d 'name='$1'&email='$2'&content='$3''
curl http://localhost:5000/api/timeline_post 
echo What is the ID of the post you would like to delete?
read created
curl -X DELETE http://localhost:5000/api/timeline_post/$created