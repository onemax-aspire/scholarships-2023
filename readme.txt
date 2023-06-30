# Coffee Chat Scheduler

This code demonstrates a matching algorithm and coffee chat scheduler that pairs aspiring professionals with senior executives based on their industries, interests, and activity levels. The algorithm generates recommendations and creates a schedule for coffee chats between the matched pairs.

In this code

Step 1: Data Preparation
- Generated the data randomly, if data is given in a file then the steps was not required can read the data using pandas library given in file. More step by step comments are added in the code

Step 2: Data Preprocessing
- pandas library is used to process the data, Create a set of all unique industries and interests, Perform one-hot encoding, Add missing columns to the one-hot encoded matrices and Ensure compatibility between X and Y matrices

Step 3: Matching Algorithm
- use cosine_similarity algorithm for matching aspiring professionals and senior executives.

Step 4: Recommendation Generation

Step 5: Coffee Schedule Generation

Step 6: Generate the coffee chat roster
- Generate coffee meeting schedule with one aspiring professionals and senior executives randomly while consider their industry, interested and other factors. 
- Output was printed per month and per week ( 4 different pair meetup at the lunch break per week )
- Output format:
Month name: January
Week: 1
4 pair
Time 
Date



## Prerequisites

- Python 3.x
- pandas library
- scikit-learn library

## Running the Code in Terminal

1. Clone the repository or download the code files.

2. Open a terminal and navigate to the directory containing the code files.

3. Install the required libraries by running the following command:
- pip install requirements.txt

4. Run the code using the following command:
- python msf_Islam_MdSaiful_py.py

For running in colab:

5. The code will generate sample data for aspiring professionals and senior executives and print the generated lists. It will then generate a coffee chat schedule and print the schedule with dates and times.

## Running the Code in Google Colab

1. Open Google Colab in your web browser: https://colab.research.google.com/

2. Click on "File" and select "Upload Notebook".

3. Upload the `msf_Islam_MdSaiful.ipynb` file.

4. Follow the instructions in the Colab notebook to run the code cells.

5. The code will generate sample data for aspiring professionals and senior executives and print the generated lists. It will then generate a coffee chat schedule and print the schedule with dates and times.

Note: In the Colab notebook, make sure to run the cells in sequential order to avoid any errors.

Note: msf_test.py file was created to test my code functionalities and comments are added too.