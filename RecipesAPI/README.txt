Install command:
1) Make sure you have flask installed.
	- pip3 install flask

2) Navigate to this folder in your terminal

3) run the following commands:
	- export FLASK_APP=proj.py
	- flask run

4) on a web browser, navigate to 127.0.0.1 and use port 5000
   so to ping the api, go to: 127.0.0.1:5000/api/ping
   for the posts, heres an example: 127.0.0.1:5000/api/posts?tags=history,tech&sortBy=reads

5) For the test aspect, if the sort is being sorted correctly, then the console will print out either
   "Test passed!" with some details of the sort, or itll output "Test failed!".
