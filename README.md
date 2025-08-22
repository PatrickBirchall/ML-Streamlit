# 🎵 Music League Analytics Dashboard

A comprehensive Streamlit dashboard for analyzing your music league data, including voting patterns, comment analysis, and competitor statistics.

## ✨ Features

### 📊 Overview Tab
- **Key Metrics**: Total rounds, competitors, submissions, and votes
- **Submissions per Round**: Visual breakdown of submissions across different rounds
- **Voting Activity**: Timeline of voting activity over time
- **Points Distribution**: Histogram showing how points are distributed
- **Top Artists**: Most submitted artists across all rounds

### 🗳️ Voting Patterns Tab
- **Voter Analysis**: Average points per voter and voting consistency
- **Voting Heatmap**: Interactive heatmap showing voting patterns between voters and rounds
- **Round Performance**: Scatter plot of total votes vs average points per round

### 💬 Comments Analysis Tab
- **Comment Statistics**: Total comments, comment rate, and average length
- **Comment Patterns**: Comments per round and length distribution
- **Top Commenters**: Most active commenters in the league
- **Sample Comments**: Random sample of actual comments from submissions

### 🎯 Round Insights Tab
- **Round Comparison**: Overview of all rounds with key metrics
- **Round-Specific Analysis**: Detailed breakdown when a specific round is selected
- **Top Submissions**: Best-performing songs by total points
- **Voter Participation**: How many votes each competitor cast per round

### 👥 Competitor Stats Tab
- **Overall Rankings**: Top submitters, point receivers, and most active voters
- **Individual Analysis**: Detailed stats for specific competitors when selected
- **Performance Metrics**: Submissions vs points received analysis
- **Voting Behavior**: How each competitor votes across different rounds

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Data Structure
Ensure your CSV files are in the `data/` folder with the following structure:

```
data/
├── competitors.csv      # Competitor information
├── rounds.csv          # Round details
├── submissions.csv     # Song submissions
└── votes.csv          # Voting data
```

### 3. Run the Dashboard
```bash
streamlit run main.py
```

The dashboard will open in your default web browser at `http://localhost:8501`

## 📁 Data Format

### competitors.csv
- `ID`: Unique competitor identifier
- `Name`: Competitor name

### rounds.csv
- `ID`: Unique round identifier
- `Created`: Round creation timestamp
- `Name`: Round name/theme
- `Description`: Round description
- `Playlist URL`: Spotify playlist link

### submissions.csv
- `Spotify URI`: Spotify track identifier
- `Title`: Song title
- `Album`: Album name
- `Artist(s)`: Artist names
- `Submitter ID`: Competitor who submitted the song
- `Created`: Submission timestamp
- `Comment`: Optional comment about the song
- `Round ID`: Which round the submission belongs to
- `Visible To Voters`: Whether the submission is visible during voting

### votes.csv
- `Spotify URI`: Track being voted on
- `Voter ID`: Competitor casting the vote
- `Created`: Vote timestamp
- `Points Assigned`: Points given (typically 0-5)
- `Comment`: Optional comment about the vote
- `Round ID`: Which round the vote belongs to

## 🎛️ Usage

### Filters
Use the sidebar filters to:
- **Select Round**: Focus on a specific round or view all rounds
- **Select Competitor**: Analyze a specific competitor or view all

### Interactive Features
- **Hover Information**: Hover over charts for detailed information
- **Zoom & Pan**: Interactive charts support zooming and panning
- **Responsive Layout**: Dashboard adapts to different screen sizes

### Export Data
- Charts can be downloaded as PNG images
- Hover over charts and use the camera icon to save

## 🔧 Customization

### Adding New Metrics
To add new analytics:
1. Add new functions in the main code
2. Create new tabs or expand existing ones
3. Use Plotly Express for quick visualizations

### Styling
- Custom CSS is included in the main file
- Modify the `<style>` section to change colors, fonts, and layout

### Data Processing
- The `load_data()` function handles all data preprocessing
- Modify merge operations to include additional data sources

## 🐛 Troubleshooting

### Common Issues
1. **Data Loading Errors**: Check CSV file paths and formats
2. **Missing Dependencies**: Ensure all requirements are installed
3. **Memory Issues**: Large datasets may require optimization

### Performance Tips
- Use the sidebar filters to limit data scope
- The app includes caching for better performance
- Consider data sampling for very large datasets

## 🤝 Contributing

Feel free to enhance the dashboard by:
- Adding new visualization types
- Improving data processing efficiency
- Enhancing the user interface
- Adding new analytical features

## 📄 License

This project is open source and available under the MIT License.

---

**Built with ❤️ using Streamlit & Plotly**

