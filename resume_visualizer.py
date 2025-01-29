import pandas as pd
import plotly.graph_objects as go
import plotly.subplots as sp
from pathlib import Path

def load_analysis_data(analysis_csv_path):
    """Load and process the analysis CSV file"""
    df = pd.read_csv(analysis_csv_path)
    
    # Calculate average scores for each section, excluding Personal Info
    section_averages = df[(df['Category'] != 'Overall') & (df['Category'] != 'Personal Info')].groupby('Category')['Score'].mean()
    
    return df, section_averages

def create_dashboard(analysis_csv_path):
    """Create an interactive dashboard from the analysis results"""
    df, avg_scores = load_analysis_data(analysis_csv_path)
    
    # Create subplot with radar chart and scatter plots
    fig = sp.make_subplots(
        rows=3, cols=2,
        specs=[[{'type': 'polar'}, {'type': 'xy'}],
               [{'type': 'xy'}, {'type': 'xy'}],
               [{'type': 'xy'}, {'type': 'xy'}]],
        subplot_titles=('Overall Analysis', 'Projects', 'Awards',
                       'Education', 'Work Experience', 'Skills & Interests')
    )

    # Add radar chart
    categories = list(avg_scores.index)
    values = list(avg_scores.values)
    fig.add_trace(
        go.Scatterpolar(
            r=values + [values[0]],
            theta=categories + [categories[0]],
            fill='toself',
            name='Resume Scores'
        ), row=1, col=1
    )

    # Add scatter plots for each section
    sections = {
        'Projects': (1, 2),
        'Awards': (2, 1),
        'Education': (2, 2),
        'Work Experience': (3, 1),
        'Skills Interests': (3, 2)
    }

    for section, (row, col) in sections.items():
        section_data = df[df['Category'] == section]
        scores = section_data['Score'].values
        names = section_data['Name'].values
        avg = scores.mean()
        
        # Add scatter plot
        fig.add_trace(
            go.Scatter(
                x=list(range(len(scores))),
                y=scores,
                mode='markers+lines',
                name=section,
                text=names,
                hovertemplate='%{text}<br>Score: %{y}'
            ), row=row, col=col
        )
        
        # Add average line
        fig.add_trace(
            go.Scatter(
                x=[0, len(scores)-1],
                y=[avg, avg],
                mode='lines',
                line=dict(dash='dash'),
                name=f'Average ({avg:.1f})'
            ), row=row, col=col
        )

    # Update layout
    fig.update_layout(
        height=1200,
        showlegend=False,
        title_text='Resume Analysis Dashboard',
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10]
            )
        )
    )

    # Update axes for scatter plots
    for i in range(1, 6):
        row = (i + 1) // 2
        col = 2 if i % 2 == 1 else 1
        if i > 0:  # Skip the polar plot
            fig.update_yaxes(title_text='Score', range=[0, 10], row=row, col=col)
            fig.update_xaxes(title_text='Items', row=row, col=col)

    return fig

if __name__ == "__main__":
    # Find the most recent analysis CSV file
    analysis_files = list(Path('.').glob('resume_analysis_*.csv'))
    if not analysis_files:
        print("No analysis CSV files found!")
        exit(1)
        
    latest_analysis = max(analysis_files)
    fig = create_dashboard(latest_analysis)
    fig.show() 