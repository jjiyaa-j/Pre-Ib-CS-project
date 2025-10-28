# Movie Rating Analyzer 🎬

A Python application that analyzes movie ratings from a data file and provides insights about the top-rated movies.

## Features

- **Top 10 Movies**: Displays the highest-rated movies from your dataset
- **Average Rating**: Calculates and shows the average rating across all movies
- **Robust Error Handling**: Handles file not found and invalid format errors gracefully
- **Performance Optimized**: Limits processing to 300 movies to prevent memory issues
- **Clean Output**: Well-formatted display of movie information

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Sukarth/Pre-Ib-CS-project.git
cd Pre-Ib-CS-project
```

2. Make sure you have Python 3.6+ installed:
```bash
python --version
```

## Usage

1. **Prepare your data file**: Create a text file with movie data in the following format:
   ```
   Title|Director|Year|Rating
   ```
   
   Example (`movies.txt`):
   ```
   The Shawshank Redemption|Frank Darabont|1994|9.3
   Pulp Fiction|Quentin Tarantino|1994|8.9
   The Dark Knight|Christopher Nolan|2008|9.0
   ```

2. **Run the program**:
   ```bash
   python MovieRatingAnalyser.py
   ```

3. **Enter the filename** when prompted (e.g., `movies.txt`)

## Sample Output

```
Enter the movies file name: movies.txt
Top 10 Rated Movies:
The Shawshank Redemption (1994) - Directed by Frank Darabont, Rating: 9.3/10
The Dark Knight (2008) - Directed by Christopher Nolan, Rating: 9.0/10
Pulp Fiction (1994) - Directed by Quentin Tarantino, Rating: 8.9/10
...

Average rating of all the movies: 8.84/10
```

## File Structure

```
Pre-Ib-CS-project/
├── MovieRatingAnalyser.py          # Main Python script
├── movies.txt                      # Sample movie data
├── README.md                       # This file
├── requirements.txt                # Python dependencies
├── .gitignore                     # Git ignore patterns
└── Computer Science Project Documentation - Jiya Jain.pdf
```

## Data Format

The program expects data in pipe-separated format (`|`):
- **Title**: Movie name (string)
- **Director**: Director name (string)  
- **Year**: Release year (integer)
- **Rating**: Movie rating out of 10 (float)

## Technical Details

- **Language**: Python 3.6+
- **Dependencies**: Built-in Python modules only
- **Memory Limit**: Processes up to 300 movies maximum
- **File Format**: Plain text with pipe separators

## Error Handling

The program handles common errors:
- **File not found**: Displays error message and exits gracefully
- **Invalid format**: Catches data parsing errors
- **Memory protection**: Limits dataset size to prevent issues

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## Development

This project was created as part of a Pre-IB Computer Science coursework to demonstrate:
- File I/O operations
- Object-oriented programming
- Data analysis and sorting
- Error handling
- Code documentation

## License

This project is open source and available under the [MIT License](LICENSE).

## Author

Original project by Jiya Jain, forked and improved by Sukarth.

---

*Happy movie analyzing! 🍿*