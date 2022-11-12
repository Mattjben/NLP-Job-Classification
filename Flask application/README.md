# FLASK APP


Libraries to pip install: 
- flask 
- sqlalchemy 
- flask_login
- os 
- werkzeug
- flask_ckeditor
- nltk
- pickle 

To run make sure working directory contains:

- jobs.db : SQL database which contains all job and user information 
- templates folder: contains all html pages needed to run the flask app 
- static folder: contains all images and css files and models used to run the app
	MAKE sure the static folder contains:
		-  CountModel.pkl which contains the count vectoriser and linear regression model used in part I 
		- stopwords_en.txt
		- nlp.py : generates prediction using bag of words model 
		- style.css: css file used to style html 
