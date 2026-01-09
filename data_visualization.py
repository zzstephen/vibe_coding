import plotly.graph_objects as go
import numpy as np
import pandas as pd
import plotly.express as px
import textwrap
import matplotlib.pyplot as plt
import textwrap


class data_visualization:
    def __init__(self, data=None):
        self.data = data


    @staticmethod
    def bar_table(df:pd.DataFrame, title:str=):
        num_rows = len(df)
        num_cols = len(df.columns)

        # Create a grid of subplots (1 row of plots per column of data)
        fig, axes = plt.subplots(nrows=1, ncols=num_cols,
                                 figsize=(num_cols * 3, num_rows * 0.5),
                                 sharey=True)

        # If there's only one column, axes isn't a list, so we wrap it
        if num_cols == 1: axes = [axes]

        for i, col in enumerate(df.columns):
            ax = axes[i]

            # Use the standard horizontal bar function
            bars = ax.barh(df.index, df[col], color=f'C{i}', alpha=0.7, height=0.6)

            # Standard functions to add labels and titles
            ax.bar_label(bars, padding=3, fontsize=9)
            ax.set_title(col, fontweight='bold', fontsize=10)

            # Standard axis cleanup
            ax.spines[['top', 'right', 'bottom']].set_visible(False)
            ax.set_xticks([])  # Hide x-axis scale for the 'table' look

            # Only keep y-labels for the first column
            if i > 0:
                ax.tick_params(left=False)

        plt.suptitle(title, fontsize=14, fontweight='bold', y=1.05)
        plt.tight_layout()
        plt.show()



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
