# Recipe Website

## Video Demo:
[Watch the video demo here](https://youtu.be/elJspKlw_A8)

## Description:
Hello everyone! My name is Daniel and I am from Singapore. This website is built with the Flask framework and is designed for finding and sharing recipes. It is connected to the Spoonacular API, providing a wide range of recipes to explore and enjoy.

### Features:
- Error Validations: The website includes error validations to ensure that users enter correct information when submitting recipes or interacting with the website.
- User-Submitted Recipes: Users can submit their own recipes by providing a name and instructions, which are then displayed on the website for others to view.
- Recipe Discovery: Users can search for recipes based on their desired dish using the discover section, which utilizes the Spoonacular API to fetch recipes matching the search criteria.
- Recipe Saving: Users can save recipes from the website to their own personal collection for easy access in the future.
- Community Feature: The website includes a community feature where users can like and unlike recipes shared by others. The most upvoted recipes are displayed in the Community Favourites section.

### Files:
- `app.py`: This file contains the logic for handling the HTML webpages and links to the Jinja framework in the HTML templates.
- `helpers.py`: This file contains simple functions, particularly for interacting with the Spoonacular API.
- `recipe.db`: This file is the database used to store recipe information. The passwords are encrypted to enhance security in case of a potential database leak.
- `requirements.txt`: This file lists the dependencies required to run the website.
- `README.md`: This file contains documentation and information about the website.

### Technical Details:
The website is built using the Flask framework, which is a popular Python web framework. It interacts with the Spoonacular API to fetch recipe data, which is stored in a SQLite database (`recipe.db`). The passwords in the database are encrypted using appropriate security measures to protect the data.

### Database Structure:
The `recipe.db` database has multiple sections or tables to store different types of data related to recipes, users, and likes. The data is organized and stored based on the database schema and design of the website.

### Challenges and Solutions:
During the development of the website, there were several challenges encountered and addressed. These challenges were overcome by implementing creative and unique solutions, such as implementing error validations, integrating with the Spoonacular API, and securing user passwords with encryption.

### Installation and Usage Instructions:
To run the website locally, follow these steps:

1. Clone the repository to your local machine.
2. Install the dependencies listed in the `requirements.txt` file.
3. Configure the database settings, such as database URL, username, and password.
4. Run the Flask application using the appropriate command. (flask run)
5. Access the website in your web browser and start exploring and interacting with the features.

### Future Improvements/Plans:
In the future, I plan to implement additional features and enhancements to further improve the functionality and user experience of the website. Some potential plans include adding user profiles, allowing users to share recipes directly with others, and implementing more advanced search and filtering options. Or even the ability to change passwords and recipes.

### Contact Information:
If you have any questions, feedback, or would like to contact me, please email me at danielguan23@gmail.com.

Hope you enjoy using the recipe website! Thank you for your support!

## Thanks to
CS50 Harvard for providing the tools and teaching for me to learn efficiently

David J. Malan for making every CS lesson exciting and awesome.

This was CS50.

-Daniel