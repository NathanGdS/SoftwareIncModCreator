# Software Inc Mod Creator

A tool to create mods for Software Inc game. With a modern and intuitive graphical interface, you can create new software types, features, and sub-features in a visual way.

## 🚀 Features

### Software Type

- Software name definition
- Unlock year configuration
- Ideal price adjustment
- Development time configuration
- Popularity and retention settings
- Operating system support
- Submarkets configuration

### Spec Features

- Specific feature creation
- Dependencies definition
- Development requirements configuration
- Development time adjustment
- Art and code configuration
- Software categories support

### Sub Features

- Add sub-features for each feature
- Level configuration
- Unlock year definition
- Development time adjustment
- Integration with main features

## 🛠️ Requirements

- Python 3.12 or higher
- pip (Python package manager)

## 📦 Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/SoftwareIncModCreator.git
cd SoftwareIncModCreator
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## 📝 How to Use

1. Run the main program:

```bash
python main.py
```

2. Use the graphical interface to:
   - Create new mods
   - Edit existing mods
   - Export mods to .tyd format
   - Import existing mods

## 🧪 Running Tests

The project uses pytest for testing. To run the tests:

1. Run all tests:

```bash
pytest tests/ -v
```

2. Run specific test file:

```bash
pytest tests/test_tyd_importer.py -v
```

3. Run specific test case:

```bash
pytest tests/test_tyd_importer.py::TestTydImporter::test_extract_value -v
```

4. Run tests with coverage report:

```bash
pytest tests/ --cov=. --cov-report=term-missing
```

## 📁 Project Structure

- `main.py`: Main program file
- `frames.py`: GUI definitions
- `mod_exporter.py`: Mod export functions
- `tyd_importer.py`: Mod import functions
- `name_gen.txt`: Name list for random generation
- `requirements.txt`: Project dependencies
- `tests/`: Test files
  - `test_tyd_importer.py`: Tests for TYD import functionality
  - `test_mod_exporter.py`: Tests for mod export functionality

## 🔧 Dependencies

- customtkinter: Modern GUI interface
- pillow: Image processing
- darkdetect: Automatic system theme detection
- pytest: Testing framework
- pytest-cov: Test coverage reporting

## 🤝 Contributing

Contributions are always welcome! Feel free to:

1. Fork the project
2. Create a Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🎯 Roadmap

- [ ] Multiple language support
- [ ] Real-time mod preview
- [ ] Advanced field validation
- [ ] Mod templates support
- [ ] Mod versioning system
- [ ] Increase test coverage

## 📞 Support

If you find any issues or have any suggestions, please open an issue on GitHub.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
