"""
Movie Rating Analyzer

This program reads movie data from a file, analyzes it, and outputs the top 10 rated movies
along with the average rating of all movies.

Usage:
    1. Run the program.
    2. When prompted, enter the name of the movie data file (e.g., "movies.txt").
    3. The program will read the data, sort the movies by rating, and display the results.

Example Input File Format:
    Each line should contain: title|director|year|rating
    For example:
    The Shawshank Redemption|Frank Darabont|1994|9.3
    Pulp Fiction|Quentin Tarantino|1994|8.9
"""

# Import system-specific parameters and functions module
# This allows us to use system-level operations like exiting the program
import sys

# Set a constant to limit the number of movies processed
# This prevents potential memory issues with extremely large files
MAX_MOVIES = 300

class Movie:
    """
    Represents a single movie with its detailed information.

    Attributes store individual movie characteristics.
    """

    def __init__(self, title, director, year, rating):
        """
        Initialize a Movie object.

        Args:
            title (str): The title of the movie.
            director (str): The director of the movie.
            year (str): The release year of the movie (will be converted to int).
            rating (str): The rating of the movie (will be converted to float).

        Returns:
            None
        """
        # Store the movie's title as a string
        self.title = title

        # Store the movie's director name as a string
        self.director = director

        # Convert year to integer for numerical comparisons
        # int() converts the string representation of year to a whole number
        self.year = int(year)

        # Convert rating to float for precise decimal calculations
        # float() allows decimal point precision for ratings
        self.rating = float(rating)

    def __str__(self):
        """
        Return a string representation of the Movie object.

        Args:
            None

        Returns:
            str: A formatted string containing movie details.
        """
        return f"{self.title} ({self.year}) - Directed by {self.director}, Rating: {self.rating}/10"

def load_movies(filename):
    """
    Load movie data from a file and create Movie objects.

    Args:
        filename (str): The name of the file containing movie data.

    Returns:
        list: A list of Movie objects.

    Raises:
        SystemExit: If the file is not found or the format is invalid.
    """
    # Create an empty list to store Movie objects
    # This list will be populated as we read the file
    movies = []

    try:
        # Open the file in read mode
        # 'with' statement ensures the file is properly closed after reading
        with open(filename, "r") as file:
            # Iterate through each line in the file
            for line in file:
                # Remove any leading/trailing whitespace from the line
                # Split the line into components using '|' as a separator
                # Unpacking the split result into four variables
                title, director, year, rating = line.strip().split("|")

                # Create a new Movie object and add it to the movies list
                # Convert year and rating during object creation
                movies.append(Movie(title, director, year, rating))

                # Check if we've reached the maximum number of movies
                # Prevents processing too many movies
                if len(movies) >= MAX_MOVIES:
                    print(f"Warning: Maximum movies ({MAX_MOVIES}) reached.")
                    break

    # Handle the scenario where the specified file cannot be found
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        # Exit the program with an error status code
        sys.exit(1)

    # Handle scenarios with incorrect file format
    except ValueError:
        print("Error: Invalid file format.")
        # Exit the program with an error status code
        sys.exit(1)

    # Return the list of Movie objects
    return movies

def get_movie_rating(movie):
    """
    Get the rating of a movie.

    Args:
        movie (Movie): A Movie object.

    Returns:
        float: The rating of the movie.
    """
    # Simply return the rating of the given movie
    # This function is used by the sorting method to determine order
    return movie.rating

def analyze_movies(movies):
    """
    Analyze the list of movies, print top 10, and calculate average rating.

    Args:
        movies (list): A list of Movie objects.

    Returns:
        None
    """
    # Sort movies in descending order based on their ratings
    # 'reverse=True' ensures highest-rated movies come first
    movies.sort(key=get_movie_rating, reverse=True)

    # Print header for top 10 movies section
    print("Top 10 Rated Movies:")

    # Iterate and print only the first 10 movies
    # Slice notation [0:10] selects first 10 items
    for movie in movies[:10]:
        print(movie)

    # Initialize a variable to store total ratings
    total_rating = 0

    # Iterate through all movies to calculate total rating
    for movie in movies:
        # Add each movie's rating to the total
        total_rating += movie.rating

    # Calculate average by dividing total rating by number of movies
    # len(movies) gives the total count of movies
    avg_rating = total_rating / len(movies)

    # Print the average rating, formatted to 2 decimal places
    print(f"\nAverage rating of all the movies: {avg_rating:.2f}/10")

def main():
    """
    Main function to run the Movie Rating Analyzer.

    Args:
        None

    Returns:
        None
    """
    # Prompt user to enter the filename
    # input() function waits for and returns user's typed input
    filename = input("Enter the movies file name: ")

    # Call function to load movies from the specified file
    movies = load_movies(filename)

    # Call function to analyze and display movie information
    analyze_movies(movies)

# Checks if script is run directly
# Prevents code from running if script is imported as a module
if __name__ == "__main__":
    main()