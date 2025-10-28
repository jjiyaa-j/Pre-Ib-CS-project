"""
Test suite for Movie Rating Analyzer

Run tests with: python -m pytest test_movie_analyzer.py -v
Run with coverage: python -m pytest test_movie_analyzer.py --cov=MovieRatingAnalyser

Author: Sukarth
Date: October 2025
"""

import pytest
import tempfile
import os
from pathlib import Path
from unittest.mock import patch, mock_open
from io import StringIO
import sys

# Import our classes
from MovieRatingAnalyser import Movie, MovieAnalyzer


class TestMovie:
    """Test cases for the Movie class."""
    
    def test_movie_creation_valid_data(self):
        """Test creating a movie with valid data."""
        movie = Movie("The Shawshank Redemption", "Frank Darabont", 1994, 9.3)
        
        assert movie.title == "The Shawshank Redemption"
        assert movie.director == "Frank Darabont"
        assert movie.year == 1994
        assert movie.rating == 9.3
    
    def test_movie_string_representation(self):
        """Test the string representation of a movie."""
        movie = Movie("Pulp Fiction", "Quentin Tarantino", 1994, 8.9)
        expected = "Pulp Fiction (1994) - Directed by Quentin Tarantino, Rating: 8.9/10"
        
        assert str(movie) == expected
    
    def test_movie_get_decade(self):
        """Test decade calculation."""
        movie_90s = Movie("Titanic", "James Cameron", 1997, 7.8)
        movie_2000s = Movie("Inception", "Christopher Nolan", 2010, 8.8)
        movie_2020s = Movie("Tenet", "Christopher Nolan", 2020, 7.3)
        
        assert movie_90s.get_decade() == "1990s"
        assert movie_2000s.get_decade() == "2010s"
        assert movie_2020s.get_decade() == "2020s"
    
    def test_movie_invalid_rating_high(self):
        """Test movie creation with rating too high."""
        with pytest.raises(ValueError, match="Invalid rating"):
            Movie("Bad Movie", "Unknown Director", 2020, 15.0)
    
    def test_movie_invalid_rating_low(self):
        """Test movie creation with rating too low."""
        with pytest.raises(ValueError, match="Invalid rating"):
            Movie("Bad Movie", "Unknown Director", 2020, -1.0)
    
    def test_movie_invalid_year_too_old(self):
        """Test movie creation with year too old."""
        with pytest.raises(ValueError, match="Invalid year"):
            Movie("Ancient Movie", "Time Traveler", 1700, 8.0)
    
    def test_movie_invalid_year_future(self):
        """Test movie creation with future year."""
        with pytest.raises(ValueError, match="Invalid year"):
            Movie("Future Movie", "Time Traveler", 2050, 8.0)
    
    def test_movie_empty_title(self):
        """Test movie creation with empty title."""
        with pytest.raises(ValueError, match="Movie title cannot be empty"):
            Movie("", "Director", 2020, 8.0)
    
    def test_movie_empty_director(self):
        """Test movie creation with empty director."""
        with pytest.raises(ValueError, match="Director name cannot be empty"):
            Movie("Movie", "", 2020, 8.0)
    
    def test_movie_whitespace_handling(self):
        """Test movie creation with whitespace in title/director."""
        with pytest.raises(ValueError):
            Movie("   ", "Director", 2020, 8.0)
        
        with pytest.raises(ValueError):
            Movie("Movie", "   ", 2020, 8.0)


class TestMovieAnalyzer:
    """Test cases for the MovieAnalyzer class."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.analyzer = MovieAnalyzer()
        
        # Sample movie data
        self.sample_data = (
            "The Shawshank Redemption|Frank Darabont|1994|9.3\n"
            "Pulp Fiction|Quentin Tarantino|1994|8.9\n"
            "The Dark Knight|Christopher Nolan|2008|9.0\n"
            "Inception|Christopher Nolan|2010|8.8\n"
            "Fight Club|David Fincher|1999|8.8\n"
        )
    
    def test_analyzer_initialization(self):
        """Test analyzer initialization."""
        assert len(self.analyzer.movies) == 0
        assert self.analyzer.total_movies_processed == 0
        assert self.analyzer.invalid_entries == 0
    
    def test_load_movies_success(self):
        """Test successful movie loading."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write(self.sample_data)
            temp_filename = f.name
        
        try:
            result = self.analyzer.load_movies(temp_filename)
            
            assert result is True
            assert len(self.analyzer.movies) == 5
            assert self.analyzer.total_movies_processed == 5
            assert self.analyzer.invalid_entries == 0
            
            # Check first movie
            first_movie = self.analyzer.movies[0]
            assert first_movie.title == "The Shawshank Redemption"
            assert first_movie.director == "Frank Darabont"
            assert first_movie.year == 1994
            assert first_movie.rating == 9.3
        
        finally:
            os.unlink(temp_filename)
    
    def test_load_movies_file_not_found(self):
        """Test loading non-existent file."""
        result = self.analyzer.load_movies("non_existent_file.txt")
        
        assert result is False
        assert len(self.analyzer.movies) == 0
    
    def test_load_movies_invalid_format(self):
        """Test loading file with invalid format."""
        invalid_data = (
            "The Shawshank Redemption|Frank Darabont|1994|9.3\n"
            "Invalid Line With Only Two Parts|Missing Data\n"
            "Pulp Fiction|Quentin Tarantino|1994|8.9\n"
        )
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write(invalid_data)
            temp_filename = f.name
        
        try:
            result = self.analyzer.load_movies(temp_filename)
            
            assert result is True  # Should still succeed with valid entries
            assert len(self.analyzer.movies) == 2  # Only valid movies loaded
            assert self.analyzer.invalid_entries == 1
        
        finally:
            os.unlink(temp_filename)
    
    def test_load_movies_skip_comments_and_empty_lines(self):
        """Test that comments and empty lines are skipped."""
        data_with_comments = (
            "# This is a comment\n"
            "\n"
            "The Shawshank Redemption|Frank Darabont|1994|9.3\n"
            "\n"
            "# Another comment\n"
            "Pulp Fiction|Quentin Tarantino|1994|8.9\n"
        )
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write(data_with_comments)
            temp_filename = f.name
        
        try:
            result = self.analyzer.load_movies(temp_filename)
            
            assert result is True
            assert len(self.analyzer.movies) == 2
            assert self.analyzer.total_movies_processed == 2  # Comments/empty lines not counted
        
        finally:
            os.unlink(temp_filename)
    
    def test_analyze_movies_empty_list(self):
        """Test analyzing empty movie list."""
        # Capture stdout to check printed output
        captured_output = StringIO()
        sys.stdout = captured_output
        
        self.analyzer.analyze_movies()
        
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        
        assert "No movies to analyze" in output
    
    def test_analyze_movies_with_data(self):
        """Test analyzing movies with data."""
        # Load sample data first
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write(self.sample_data)
            temp_filename = f.name
        
        try:
            self.analyzer.load_movies(temp_filename)
            
            # Capture stdout
            captured_output = StringIO()
            sys.stdout = captured_output
            
            self.analyzer.analyze_movies(top_count=3)
            
            sys.stdout = sys.__stdout__
            output = captured_output.getvalue()
            
            # Check that output contains expected sections
            assert "Top 3 Rated Movies" in output
            assert "Statistics" in output
            assert "Top Directors" in output
            assert "Movies by Decade" in output
            
            # Check that highest rated movie is first
            assert "The Shawshank Redemption" in output
            assert "9.3/10" in output
        
        finally:
            os.unlink(temp_filename)
    
    def test_export_analysis(self):
        """Test exporting analysis to file."""
        # Load sample data first
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write(self.sample_data)
            temp_filename = f.name
        
        try:
            self.analyzer.load_movies(temp_filename)
            
            # Test export
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as export_file:
                export_filename = export_file.name
            
            result = self.analyzer.export_analysis(export_filename)
            
            assert result is True
            assert os.path.exists(export_filename)
            
            # Check export file content
            with open(export_filename, 'r') as f:
                content = f.read()
                assert "Movie Analysis Report" in content
                assert "The Shawshank Redemption" in content
            
            os.unlink(export_filename)
        
        finally:
            os.unlink(temp_filename)
    
    def test_movie_sorting(self):
        """Test that movies are sorted correctly by rating and year."""
        # Create data with same ratings but different years
        test_data = (
            "Movie A|Director A|2000|8.5\n"
            "Movie B|Director B|1995|8.5\n"
            "Movie C|Director C|2010|9.0\n"
        )
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write(test_data)
            temp_filename = f.name
        
        try:
            self.analyzer.load_movies(temp_filename)
            
            # Sort movies (same as in analyze_movies)
            sorted_movies = sorted(self.analyzer.movies, key=lambda m: (-m.rating, m.year))
            
            # Highest rating first
            assert sorted_movies[0].title == "Movie C"
            assert sorted_movies[0].rating == 9.0
            
            # Same rating, earlier year first
            assert sorted_movies[1].title == "Movie B"
            assert sorted_movies[1].year == 1995
            assert sorted_movies[2].title == "Movie A"
            assert sorted_movies[2].year == 2000
        
        finally:
            os.unlink(temp_filename)


class TestIntegration:
    """Integration tests for the complete system."""
    
    def test_full_workflow(self):
        """Test complete workflow from loading to analysis."""
        sample_data = (
            "The Godfather|Francis Ford Coppola|1972|9.2\n"
            "The Godfather: Part II|Francis Ford Coppola|1974|9.0\n"
            "Pulp Fiction|Quentin Tarantino|1994|8.9\n"
            "Schindler's List|Steven Spielberg|1993|8.9\n"
            "12 Angry Men|Sidney Lumet|1957|8.9\n"
            "The Dark Knight|Christopher Nolan|2008|9.0\n"
            "The Lord of the Rings: The Return of the King|Peter Jackson|2003|8.9\n"
            "Fight Club|David Fincher|1999|8.8\n"
            "Forrest Gump|Robert Zemeckis|1994|8.8\n"
            "Inception|Christopher Nolan|2010|8.8\n"
        )
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write(sample_data)
            temp_filename = f.name
        
        try:
            analyzer = MovieAnalyzer()
            
            # Load movies
            load_result = analyzer.load_movies(temp_filename)
            assert load_result is True
            assert len(analyzer.movies) == 10
            
            # Verify data integrity
            godfather = next(m for m in analyzer.movies if m.title == "The Godfather")
            assert godfather.director == "Francis Ford Coppola"
            assert godfather.year == 1972
            assert godfather.rating == 9.2
            
            # Test director analysis (Francis Ford Coppola has 2 movies)
            coppola_movies = [m for m in analyzer.movies if m.director == "Francis Ford Coppola"]
            assert len(coppola_movies) == 2
            
            # Test decade analysis
            movies_1990s = [m for m in analyzer.movies if m.get_decade() == "1990s"]
            assert len(movies_1990s) == 4  # Pulp Fiction, Schindler's List, Fight Club, Forrest Gump
            
            # Test export functionality
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as export_file:
                export_filename = export_file.name
            
            export_result = analyzer.export_analysis(export_filename)
            assert export_result is True
            
            # Verify export content
            with open(export_filename, 'r') as f:
                content = f.read()
                assert "The Godfather" in content
                assert "Francis Ford Coppola" in content
                assert "9.2/10" in content
            
            os.unlink(export_filename)
        
        finally:
            os.unlink(temp_filename)


if __name__ == "__main__":
    # Run tests if script is executed directly
    pytest.main(["-v", __file__])