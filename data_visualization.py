import plotly.graph_objects as go
import numpy as np
import pandas as pd
import plotly.express as px



class data_visualization:
    def __init__(self, data=None):
        self.data = data

    @staticmethod
    def violin_plot(df, value_col, category_col, title="Distribution Analysis"):
        """
        Creates a professional-grade violin plot using Plotly.

        :param df: Pandas DataFrame containing the data
        :param value_col: String, the numerical column (e.g., 'height_cm')
        :param category_col: String, the categorical column (e.g., 'gender')
        :param title: String, the title of the plot
        """
        fig = go.Figure()

        categories = df[category_col].unique()

        for cat in categories:
            filtered_df = df[df[category_col] == cat]

            fig.add_trace(go.Violin(
                x=filtered_df[category_col],
                y=filtered_df[value_col],
                name=cat,
                box_visible=True,  # Shows a mini box plot inside
                meanline_visible=True,  # Shows the mean line
                points='all',  # Shows the raw data points (jittered)
                jitter=0.05,  # Spacing for the raw points
                marker_opacity=0.6,
                line_color='black' if cat == 'male' else 'orchid'  # Example custom styling
            ))

        fig.update_layout(
            title=title,
            yaxis_title=value_col,
            xaxis_title=category_col,
            template="plotly_white",
            showlegend=False
        )

        return fig

    @staticmethod
    def faceted_bar_plots(df, value_col, axis_col, facet_col, palette=px.colors.qualitative.Plotly):
        """
        Dynamically creates bar plots for every unique level in facet_col.

        :param df: The dataframe.
        :param value_col: Numerical values (Y-axis), e.g., 'unemployment_rate'.
        :param axis_col: Categorical labels (X-axis), e.g., 'year_month' or 'year'.
        :param facet_col: The column to loop through, e.g., 'state'.
        :param palette: A list of colors to cycle through for different levels.
        """
        figures = []
        unique_levels = df[facet_col].unique()

        # Calculate global Y-axis range to make charts across facets comparable
        # This prevents visual misinterpretation of the data scale.
        y_max = df[value_col].max() * 1.1

        for i, level in enumerate(unique_levels):
            # 1. Subset the data for the current level (e.g., 'CA')
            subset = df[df[facet_col] == level]

            # 2. Aggregation: Ensure we have exactly one value per X-axis point
            # We use .mean() as the default for rates/heights.
            plot_data = subset.groupby(axis_col)[value_col].mean().reset_index()

            # 3. Dynamic Color selection from the palette
            color = palette[i % len(palette)]

            fig = go.Figure()

            # 4. Construct the Bar Trace
            fig.add_trace(go.Bar(
                x=plot_data[axis_col],
                y=plot_data[value_col],
                name=str(level),
                marker_color=color,
                text=plot_data[value_col].round(1),  # Data labels on bars
                textposition='outside'
            ))

            # 5. Standardized Professional Layout
            fig.update_layout(
                title=f"Segment Analysis: {level}",
                xaxis_title=axis_col,
                yaxis_title=f"Avg {value_col}",
                yaxis=dict(range=[0, y_max]),  # Lock Y-axis scale
                template="plotly_white",
                margin=dict(l=40, r=40, t=60, b=40)
            )

            figures.append(fig)

        return figures
