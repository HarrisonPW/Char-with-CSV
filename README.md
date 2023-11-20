# Chat-with-CSV
<img src="https://github.com/HarrisonPW/Chat-with-CSV/assets/32474200/38ab5848-ee80-4044-b616-38a0b9b3db6d" alt="Alt Text" width="500" height="500">

# Introduction:
The Chat with CSV project is a combination of the power of large language models (LLMs) with the need for simple and intuitive data visualization platforms that human can interact with. We used models like ChatGPT and GPT4, along with the API key to achieve this. We aimed to create an environment where users could interactively analyze their data and engage in a conversation using **EvaDB** and **SQLite**, which is a open source database system to support data storage. It is an innovative and easy approach to data analysis that has the potential to revolutionize how users understand and interpret their data.

# Quick start:
1. Clone the project
```
git clone https://github.com/HarrisonPW/Chat-with-CSV.git
cd Chat-with-CSV
```
2. Install the requirements
```
pip install -r requirements.txt
```
3. Enter your openai Key and Run the program
```
export OPENAI_API_KEY='yourkey'
python3 main.py
```
# Showing the features:
1. It is able to execute the SQL in SQLite:
<img width="648" alt="Screenshot 2023-11-20 at 2 22 43 PM" src="https://github.com/HarrisonPW/Chat-with-CSV/assets/32474200/4ea7ca5d-cca0-4bde-8f0e-967ff19b6fce">

2. It can automatically generate the distribution plot according to the dataset:
<img width="1014" alt="Screenshot 2023-11-20 at 2 23 23 PM" src="https://github.com/HarrisonPW/Chat-with-CSV/assets/32474200/801ed51a-59ca-404a-9532-7136f8520728">

3. It's support the complext SQL:
<img width="1155" alt="Screenshot 2023-11-20 at 2 24 35 PM" src="https://github.com/HarrisonPW/Chat-with-CSV/assets/32474200/a56a878a-d0bd-4bbe-90af-ec7495363180">

4. It has the feature of query time by using caching mechanism:
<img width="977" alt="Screenshot 2023-11-20 at 2 26 28 PM" src="https://github.com/HarrisonPW/Chat-with-CSV/assets/32474200/9904bc0f-07a8-44b0-9c9a-edcd14b3120a">
