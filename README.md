# Fetch Coding Exercise - SDET

Hey there!

Welcome to my solution for the Fetch Coding Exercise - SDET challenge. This project is all about finding the fake gold bar using some good old automation magic with Selenium.

## What's This About?

We have 9 gold bars. They all look the same, but one of them is a sneaky fake that's lighter than the others. Our job is to find that fake bar using a balance scale on a website.

## Getting Started

Here's how you can get this project up and running on your local machine.

### Prerequisites

First things first, you'll need to have Python installed. You can download it [here](https://www.python.org/downloads/).

You'll also need to install the Selenium library. Just run:

```sh

pip install selenium
```

And of course, you'll need a WebDriver for your browser. For Chrome, you can download it from [here.](https://pypi.org/project/selenium/)

### Installation

1. Clone this repository to your local machine:

    ```sh
    git clone https://github.com/Mark70092/SDET-challenge.git
    cd SDET-challenge
    ```

2. Install the required Python packages:

    ```sh
    pip install -r requirements.txt
    ```

Running the Script
Now, let's find that fake gold bar! Just run:

python main.py


The script will automate the whole process: placing the bars on the scale, weighing them, and eventually finding the fake one.

Logs
You'll see all the action logged in your console. If you want to keep a log file, you can modify the script to write logs to a file as well.

How It Works
1.Clearing the Bowls: The script starts by clicking the "Reset" button to clear the bowls.
2.First Weighing: It then places the first set of bars on the left and right bowls and clicks "Weigh".
3.Result Analysis: Based on the result, it makes a decision on which bars to weigh next.
4.Second Weighing: It places the bars for the second weighing and clicks "Weigh".
5.Finding the Fake Bar: The script analyzes the second weighing result to identify the fake bar and clicks on it.


That's it! Happy testing!