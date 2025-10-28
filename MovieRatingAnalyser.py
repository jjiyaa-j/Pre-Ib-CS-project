"""
Movie Rating Analyzer

A comprehensive Python application that analyzes movie data from files and provides
insightful statistics about movie ratings, directors, and release years.

Author: Sukarth (Enhanced version)
Original: Jiya Jain
Version: 2.0
Date: October 2025
"""

import sys
from typing import List, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path


# Configuration constants
MAX_MOVIES = 300
MIN_RATING = 0.0
MAX_RATING = 10.0


@dataclass
class Movie:
    """
    Represents a movie with its metadata using dataclass for cleaner code.
    
    Attributes:
        title: The title of the movie
        director: The director's name
        year: Release year
        rating: Movie rating (0-10 scale)
    """
    title: str
    director: str
    year: int
    rating: float
    
    def __post_init__(self) -> None:
        """Validate movie data after initialization."""
        if not isinstance(self.year, int) or self.year < 1800 or self.year > 2030:
            raise ValueError(f"Invalid year: {self.year}. Must be between 1800-2030.")
        
        if not isinstance(self.rating, (int, float)) or not (MIN_RATING <= self.rating <= MAX_RATING):
            raise ValueError(f"Invalid rating: {self.rating}. Must be between {MIN_RATING}-{MAX_RATING}.")
        
        if not self.title.strip():
            raise ValueError("Movie title cannot be empty.")
        
        if not self.director.strip():
            raise ValueError("Director name cannot be empty.")
    
    def __str__(self) -> str:
        """Return formatted string representation of the movie."""
        return f"{self.title} ({self.year}) - Directed by {self.director}, Rating: {self.rating}/10"
    
    def get_decade(self) -> str:
        """Return the decade this movie was released in."""
        decade_start = (self.year // 10) * 10
        return f"{decade_start}s"


class MovieAnalyzer:
    """
    Main class for analyzing movie data with enhanced functionality.
    """
    
    def __init__(self):
        self.movies: List[Movie] = []
        self.total_movies_processed = 0
        self.invalid_entries = 0
    
    def load_movies(self, filename: str) -> bool:
        """
        Load movie data from file with enhanced error handling.
        
        Args:
            filename: Path to the movie data file
            
        Returns:
            True if loading successful, False otherwise
        """
        file_path = Path(filename)
        
        if not file_path.exists():
            print(f"❌ Error: File '{filename}' not found.")
            return False
        
        if not file_path.is_file():
            print(f"❌ Error: '{filename}' is not a valid file.")
            return False
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                for line_num, line in enumerate(file, 1):
                    line = line.strip()
                    
                    # Skip empty lines and comments
                    if not line or line.startswith('#'):
                        continue
                    
                    self.total_movies_processed += 1
                    
                    try:
                        self._parse_and_add_movie(line, line_num)
                    except (ValueError, IndexError) as e:
                        self.invalid_entries += 1
                        print(f"⚠️  Warning: Invalid entry at line {line_num}: {e}")
                        continue
                    
                    # Check movie limit
                    if len(self.movies) >= MAX_MOVIES:
                        print(f"⚠️  Warning: Maximum movies ({MAX_MOVIES}) reached. Stopping processing.")
                        break
            
            print(f"✅ Successfully loaded {len(self.movies)} movies from '{filename}'")
            if self.invalid_entries > 0:
                print(f"⚠️  Skipped {self.invalid_entries} invalid entries")
            
            return len(self.movies) > 0
            
        except PermissionError:
            print(f"❌ Error: Permission denied accessing '{filename}'.")
            return False
        except UnicodeDecodeError:
            print(f"❌ Error: Unable to decode '{filename}'. Please ensure it's a valid text file.")
            return False
        except Exception as e:
            print(f"❌ Unexpected error loading '{filename}': {e}")
            return False
    
    def _parse_and_add_movie(self, line: str, line_num: int) -> None:
        """
        Parse a line and create a Movie object.
        
        Args:
            line: Raw line from file
            line_num: Line number for error reporting
        """
        parts = line.split('|')
        if len(parts) != 4:
            raise ValueError(f"Expected 4 fields separated by '|', got {len(parts)}")
        
        title, director, year_str, rating_str = [part.strip() for part in parts]
        
        try:
            year = int(year_str)
            rating = float(rating_str)
        except ValueError as e:
            raise ValueError(f"Invalid numeric data: {e}")
        
        movie = Movie(title, director, year, rating)
        self.movies.append(movie)
    
    def analyze_movies(self, top_count: int = 10) -> None:
        """
        Analyze movies and display comprehensive statistics.
        
        Args:
            top_count: Number of top movies to display
        """
        if not self.movies:
            print("❌ No movies to analyze.")
            return
        
        # Sort by rating (descending) and then by year (ascending) for ties
        sorted_movies = sorted(self.movies, key=lambda m: (-m.rating, m.year))
        
        self._display_top_movies(sorted_movies, top_count)
        self._display_statistics()
        self._display_director_analysis()
        self._display_decade_analysis()
    
    def _display_top_movies(self, sorted_movies: List[Movie], count: int) -> None:
        """Display top N movies."""
        actual_count = min(count, len(sorted_movies))
        print(f"\n🏆 Top {actual_count} Rated Movies:")
        print("=" * 50)
        
        for i, movie in enumerate(sorted_movies[:actual_count], 1):
            print(f"{i:2}. {movie}")
    
    def _display_statistics(self) -> None:
        """Display basic statistics."""
        ratings = [movie.rating for movie in self.movies]
        years = [movie.year for movie in self.movies]
        
        avg_rating = sum(ratings) / len(ratings)
        min_rating = min(ratings)
        max_rating = max(ratings)
        min_year = min(years)
        max_year = max(years)
        
        print(f"\n📊 Statistics:")
        print("=" * 30)
        print(f"Total Movies: {len(self.movies)}")
        print(f"Average Rating: {avg_rating:.2f}/10")
        print(f"Rating Range: {min_rating} - {max_rating}")
        print(f"Year Range: {min_year} - {max_year}")
    
    def _display_director_analysis(self) -> None:
        """Display director-based analysis."""
        director_stats = {}
        
        for movie in self.movies:
            if movie.director not in director_stats:
                director_stats[movie.director] = {'count': 0, 'total_rating': 0, 'movies': []}
            
            director_stats[movie.director]['count'] += 1
            director_stats[movie.director]['total_rating'] += movie.rating
            director_stats[movie.director]['movies'].append(movie.title)
        
        # Find top directors by average rating (min 2 movies)
        qualified_directors = {
            director: stats for director, stats in director_stats.items() 
            if stats['count'] >= 2
        }
        
        if qualified_directors:
            print(f"\n🎬 Top Directors (2+ movies):")
            print("=" * 40)
            
            sorted_directors = sorted(
                qualified_directors.items(),
                key=lambda x: x[1]['total_rating'] / x[1]['count'],
                reverse=True
            )[:5]
            
            for director, stats in sorted_directors:
                avg_rating = stats['total_rating'] / stats['count']
                print(f"{director}: {avg_rating:.2f} avg ({stats['count']} movies)")
    
    def _display_decade_analysis(self) -> None:
        """Display decade-based analysis."""
        decade_stats = {}
        
        for movie in self.movies:
            decade = movie.get_decade()
            if decade not in decade_stats:
                decade_stats[decade] = {'count': 0, 'total_rating': 0}
            
            decade_stats[decade]['count'] += 1
            decade_stats[decade]['total_rating'] += movie.rating
        
        print(f"\n📅 Movies by Decade:")
        print("=" * 25)
        
        sorted_decades = sorted(decade_stats.items())
        for decade, stats in sorted_decades:
            avg_rating = stats['total_rating'] / stats['count']
            print(f"{decade}: {stats['count']} movies, {avg_rating:.2f} avg rating")
    
    def export_analysis(self, output_file: str = "movie_analysis.txt") -> bool:
        """
        Export analysis results to a file.
        
        Args:
            output_file: Output filename
            
        Returns:
            True if export successful, False otherwise
        """
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                # Redirect print output to file
                original_stdout = sys.stdout
                sys.stdout = f
                
                print(f"Movie Analysis Report - Generated on {Path().cwd()}")
                print("=" * 60)
                self.analyze_movies()
                
                # Restore stdout
                sys.stdout = original_stdout
            
            print(f"✅ Analysis exported to '{output_file}'")
            return True
            
        except Exception as e:
            print(f"❌ Error exporting analysis: {e}")
            return False


def get_user_input() -> Tuple[str, Optional[str]]:
    """
    Get user input with improved interface.
    
    Returns:
        Tuple of (filename, optional_output_file)
    """
    print("🎬 Movie Rating Analyzer v2.0")
    print("=" * 35)
    
    # Get input filename
    while True:
        filename = input("Enter the movies file name (or 'quit' to exit): ").strip()
        
        if filename.lower() == 'quit':
            print("Goodbye! 👋")
            sys.exit(0)
        
        if filename:
            break
        print("❌ Please enter a valid filename.")
    
    # Ask about export
    export_choice = input("Export analysis to file? (y/N): ").strip().lower()
    output_file = None
    
    if export_choice in ['y', 'yes']:
        output_file = input("Enter output filename (default: movie_analysis.txt): ").strip()
        if not output_file:
            output_file = "movie_analysis.txt"
    
    return filename, output_file


def main() -> None:
    """
    Enhanced main function with better user experience.
    """
    try:
        filename, output_file = get_user_input()
        
        analyzer = MovieAnalyzer()
        
        if not analyzer.load_movies(filename):
            print("❌ Failed to load movies. Please check your file and try again.")
            sys.exit(1)
        
        # Display analysis
        analyzer.analyze_movies()
        
        # Export if requested
        if output_file:
            analyzer.export_analysis(output_file)
        
        print("\n✨ Analysis complete!")
        
    except KeyboardInterrupt:
        print("\n\n👋 Analysis interrupted by user. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()