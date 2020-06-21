# Capstone Project for the Master of Science in Business Analytics at ESADE Business School

**This repository contains the code that was used for the article "An Advanced Guide to AWS DeepRacer - Autonomous Formula 1 Racing using Reinforcement Learning". Feel free to check it out [here](https://towardsdatascience.com/an-advanced-guide-to-aws-deepracer-2b462c37eea).**


- The folder *Compute_Speed_And_Actions* contains a jupyter notebook, which takes the optimal racing line from [this](https://github.com/cdthompson/deepracer-k1999-race-lines) repo and computes the optimal speed. Additionally, it computes a custom action space with K-Means clustering. The folder also contains the K1999 racing line notebook from cdthompson, which I altered to be able to only use the inner 80% of the track.
- The folder *Reward_Function* contains a .py file with the reward function that our team used to get to 12th place out of 1291 participants in the time trial category of the F1 event in May 2020
- The folder *Selenium_Automation* contains a jupyter notebook, which allows you to submit a model to a race multiple times without using the AWS CLI. As a bonus, you can also automatically conducts experiments with hyperparameters. This can be used to conduct multiple experiments over night without having to manually set them up every couple of hours

## GitHub Repositories that were used
- To calculate the optimal racing line: https://github.com/cdthompson/deepracer-k1999-race-lines
- To analyze the logs: https://github.com/aws-deepracer-community/deepracer-analysis
- To retreive the track data: https://github.com/aws-deepracer-community/deepracer-simapp/tree/master/bundle/deepracer_simulation_environment/share/deepracer_simulation_environment/routes

## License
Feel free to use, distribute, and alter the code as you like.

This is a finished university project. Therefore, we will not be maintaining the code any more.
