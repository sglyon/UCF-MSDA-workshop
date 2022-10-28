# Kaggle competition

Here I will put the code I used/generated for the 2022-10-28 session on the Kaggle spaceship-titanic compeition

I will also include some instructions that you should be able to replicate on your own computer to get started

## Instructions

1. Sign up for an account at https://kaggle.com
2. Go to the "Account" tab of your kaggle profile (`https://kaggle.com/<USERNAME>/account` -- where you replace `<USERNAME>` with your username`)
3. On the account page, select "Create API Token" -- this will download a file `kaggle.json`
4. Move `kaggle.json` to `~/.kaggle/kaggle.json`
5. Install conda or mamba. (instructions here if you haven't started yet: https://mamba.readthedocs.io/en/latest/installation.html)
6. Create a new conda environment using the command `mamba create -n ucf-kaggle-titanic-spaceship -c conda-forge python=3 pandas matplotlib seaborn plotly scikit-learn kaggle ipython mlflow python-dotenv ipykernel` (use `conda` instead of `mamba` if you don't have mamba)
7. Activate the environment `conda activate ucf-kaggle-titanic-spaceship`
8. Download data from kaggle with `kaggle competitions download -c spaceship-titanic`
9. Unzip the data (on linux or MacOS use `unzip spaceship-titanic.zip` -- not sure on windows... probably click something)
10. Copy the file `.env.example` and rename to `.env`
11. Fill in the `.env` contents with what was sent out via an announcement on webcourses

After this you should be ready to go!


## Alternate instructions if you run Jupyter notebook

1. Download this repository
2. Start jupyter
3. Go to this folder ("Year21-22/2022-10-28_kaggle_titantic_spaceship")
4. In top right of Jupyter notebook click "New" Then select "Text file"
5. Rename the file to `.env` (click the "untitled.txt" and change it to ".env")
6. Paste in contents of .env sent in zoom chat and save the file
7. Open testing.ipynb and run all the cells!
