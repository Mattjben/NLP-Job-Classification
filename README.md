# NLP-Job-Classification
The aim of this project is to build text classification models for predicting the category of a given job advertisement for future use in a job board flask application 

# Task 1 

Files:  
- **task1.ipynb:** jupyter notebook of all text preprocessing steps 
- data: all job advertisement data located within the file of their given category 
- ouputs: 
  - **Jobs.txt**: Contains all job decscriptions in a single file (line per description)
  - **Vocab.txt**: Contains the unigram vocabulary, in the format *word_string:word_integer_index*
  - **webindxs.txt**: Contains a list of all the stored web index values in the same order as the job.txt file 
  - **jobtitles.txt**:Contains a list of all the titles in the same order as the job.txt file 
  - **jobtypes.txt**:Contains a list of all the job types in the same order as the job.txt file    
  
The objective of this task is to perform basic text pre-processing on 776 job descriptions so that the words and language used in the description of each job can be easily assigned meaning. After successful completion of this process this more simplified and less noisy version of the description section of each job text file can then be used to generate document vectors to be inputted in an NLP machine learning model for the purpose of text classification. 

# Task 2 
Files: 
- **count_vectors.txt**: Contains the count vector representation for each document (job advertisement) with the start of each line consisting of *'#:webindex number'* followed by a list of all the count values in the format
- **glove.6B.100d.txt** & **glove.42B.300d.txt**: GloVe word embedding models. which are available [here](https://nlp.stanford.edu/projects/glove/)
- **task2_3.ipynb:** jupyter notebook containg steps reuired for: 
    1. Generating the feature representations (Task 2)
    2. comparing Advertisement classification models (Task 3)

In this phase of the project, using the tokens processed in *task 1*, multiple feature representations will be generated from the Job Advertisement Descriptions

# Task 3


In this phase of the project, using the document representations in *task 2*, multiple NLP machine learing models will be generated and compared to investigate the effects each representation has on the accuracy of a machine learning text classification model.

# Flask Application 

This folder contains a flask app that can be run locally which consists of a job board that uses an NLP model to predict the category of a job after a employer creates one 
## Functionalities 
1. Job search 
![alt text](https://i.postimg.cc/T2Qh5hCh/Capture.png)

2. Login/register

<centre>![image](https://i.postimg.cc/8PJDkCY2/Capture2.png)</centre>
3. Company profile
![image2](https://i.postimg.cc/fRQ4wfmd/Capture.png)
4. Create job posting 
![image3]( https://i.postimg.cc/cLdSRcCS/Capture.png)
4. Predict job category using NLP model 
![image4](https://i.postimg.cc/SNhF4GWM/Capture.png)

