# Overview

As a software engineer passionate about performance analysis and tool-building, I created DataCat. It is a Python application designed to analyze personal gameplay data from Valorant. My goal was to sharpen my data science skills by working with real-world datasets that are both meaningful and engaging. This project helps me grow my abilities in data wrangling, visualization, and pattern discovery using Python.

The dataset I’m analyzing is sourced from my own Valorant match history via Tracker Network’s public Valorant API. While waiting for API access approval, I used a manually collected CSV to simulate that data.

The purpose of this software is to explore how my gameplay has evolved over time. By analyzing metrics like Average Combat Score (ACS), Average Damage per Round (ADR), and Kill/Death/Assist ratio (KDA), I can identify performance trends and areas for improvement. This project is a stepping stone toward building more advanced personal analytics dashboards. 

[Software Demo Video](http://youtube.link.goes.here)

# Data Analysis Results

Question 1:
How has my ACS (Average Combat Score) changed over time?
Answer: My ACS has fluctuated across recent matches but peaked on July 2 on the map Haven. This suggests strong offensive impact during that match, and performance generally varies by map.

Question 2:
How has my ADR (Average Damage per Round) evolved?
Answer: ADR closely mirrored ACS trends. On Haven, I achieved the highest ADR (~161), suggesting high consistency in dealing damage. Lower ADR matches aligned with underperforming games.

Question 3:
How has my KDA changed over time?
Answer: My KDA was highest during the Haven match (1.55), and lowest during the Bind match (0.6). This metric reveals performance consistency, and suggests a need to adjust strategy on maps like Bind where I tend to struggle.

# Development Environment

*Operating System: Windows 10

*IDE/Editor: Visual Studio Code

*Command Line: PowerShell, Git Bash

*Version Control: Git (GitHub for repo)
Programming Language:

Python 3.11+

Libraries Used:

*pandas – data manipulation and analysis

*matplotlib – data visualization

*dotenv – API key management

*requests – API communication (planned once API key is approved)

# Useful Websites

{Make a list of websites that you found helpful in this project}
* [Pandas Tutorial 1](https://pandas.pydata.org/docs/user_guide/10min.html#min)
* [Pandas Tutorial 2](https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html)
* [Pandas Example](https://towardsdatascience.com/getting-started-to-data-analysis-with-python-pandas-with-titanic-dataset-a195ab043c77)
* [Exploratory Data w/ Pandas](https://www.kaggle.com/kashnitsky/topic-1-exploratory-data-analysis-with-pandas)
* [Python Dotenv](https://pypi.org/project/python-dotenv/)
* [Tracker Network API Documentation](https://tracker.gg/developers/docs/getting-started)
* [Matplotlib documentation](https://matplotlib.org/stable/contents.html)


# Future Work

* Once my API key is approved for use, I will re-enable the API integration in this app. 
* Add bar charts to help visualize comparison between different maps and agents
* Package project as an installable tool for other Valorant players