# Contributing to Movie Rating Analyzer 🎬

Thank you for your interest in contributing to this project! We welcome contributions from developers of all skill levels.

## 🌟 Ways to Contribute

- **Bug Reports**: Found a bug? Please report it!
- **Feature Requests**: Have an idea for improvement? We'd love to hear it!
- **Code Contributions**: Fix bugs, add features, or improve documentation
- **Documentation**: Help improve our docs, comments, or examples
- **Testing**: Add test cases or improve existing ones

## 🚀 Getting Started

### Prerequisites
- Python 3.7 or higher
- Git
- A GitHub account

### Setup Development Environment

1. **Fork the repository**
   ```bash
   # Click the "Fork" button on GitHub, then clone your fork:
   git clone https://github.com/YOUR-USERNAME/Pre-Ib-CS-project.git
   cd Pre-Ib-CS-project
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install development dependencies**
   ```bash
   pip install -r requirements-dev.txt
   # Or if no dev requirements: pip install pytest black flake8
   ```

4. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

## 📝 Making Changes

### Code Style Guidelines

- Follow **PEP 8** Python style guidelines
- Use **type hints** for function parameters and return values
- Write **descriptive variable names** and **clear comments**
- Keep functions **focused and small** (ideally under 50 lines)
- Use **docstrings** for all classes and functions

### Example Code Style
```python
def analyze_movie_ratings(movies: List[Movie], min_rating: float = 0.0) -> Dict[str, float]:
    """
    Analyze movie ratings and return statistics.
    
    Args:
        movies: List of Movie objects to analyze
        min_rating: Minimum rating to include in analysis
        
    Returns:
        Dictionary containing rating statistics
    """
    # Implementation here
    pass
```

### Commit Message Format

Use clear, descriptive commit messages:

```
type: brief description (50 chars max)

Optional longer description explaining what and why.

Examples:
- feat: add director analysis functionality
- fix: handle empty movie files gracefully
- docs: update installation instructions
- test: add unit tests for Movie class
- refactor: improve error handling in load_movies
```

## 🧪 Testing

### Running Tests
```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=MovieRatingAnalyser

# Run specific test file
python -m pytest tests/test_movie.py
```

### Writing Tests

- Add tests for new features in the `tests/` directory
- Use descriptive test function names: `test_movie_creation_with_valid_data()`
- Test both happy paths and edge cases
- Include tests for error conditions

Example test:
```python
def test_movie_creation_with_invalid_rating():
    """Test that Movie raises ValueError for invalid ratings."""
    with pytest.raises(ValueError, match="Invalid rating"):
        Movie("Test Movie", "Test Director", 2020, 15.0)  # Rating > 10
```

## 📋 Pull Request Process

### Before Submitting

1. **Ensure tests pass**:
   ```bash
   python -m pytest
   ```

2. **Check code style**:
   ```bash
   flake8 MovieRatingAnalyser.py
   black --check MovieRatingAnalyser.py
   ```

3. **Update documentation** if needed

4. **Test your changes** with sample data

### Submitting Your PR

1. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create Pull Request** on GitHub with:
   - Clear title describing the change
   - Detailed description of what and why
   - Reference any related issues: "Fixes #123"
   - Screenshots if UI changes

3. **PR Template**:
   ```markdown
   ## Description
   Brief description of changes
   
   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Documentation update
   - [ ] Performance improvement
   
   ## Testing
   - [ ] Tests pass locally
   - [ ] Added tests for new functionality
   
   ## Checklist
   - [ ] Code follows style guidelines
   - [ ] Self-review completed
   - [ ] Documentation updated
   ```

## 🐛 Reporting Issues

### Bug Reports
Include:
- **Clear title** describing the issue
- **Steps to reproduce** the problem
- **Expected vs actual behavior**
- **Environment details** (Python version, OS)
- **Sample data** if relevant
- **Error messages** or screenshots

### Feature Requests
Include:
- **Clear description** of the feature
- **Use case** explaining why it's needed
- **Possible implementation** ideas (optional)
- **Alternative solutions** considered

## 🎯 Good First Issues

Looking for something to work on? Check issues labeled:
- `good first issue` - Perfect for newcomers
- `help wanted` - Community help needed
- `documentation` - Improve docs
- `enhancement` - New feature ideas

### Beginner-Friendly Ideas

1. **Add more movie statistics**:
   - Median rating calculation
   - Standard deviation of ratings
   - Movie count by genre (if data available)

2. **Improve error handling**:
   - Better validation messages
   - Graceful handling of malformed data
   - Progress indicators for large files

3. **Add export options**:
   - CSV export functionality
   - JSON format support
   - HTML report generation

4. **Documentation improvements**:
   - Add more code examples
   - Create video tutorials
   - Improve inline comments

## 🤝 Code of Conduct

- **Be respectful** and inclusive
- **Help others** learn and grow
- **Focus on constructive feedback**
- **Celebrate contributions** of all sizes

## 📞 Getting Help

- **GitHub Issues**: For bugs and feature requests
- **Discussions**: For questions and general discussion
- **Email**: For private matters (check profile)

## 🏆 Recognition

Contributors are recognized in:
- README.md contributors section
- Release notes for significant contributions
- Special thanks in project documentation

---

**Happy contributing! 🎉**

*Remember: Every expert was once a beginner. Don't hesitate to ask questions and contribute!*