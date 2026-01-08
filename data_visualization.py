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
    def bar_table(df, title, bar_scale=1.8, max_bar_width=0.75, fig_width=14, fig_height=8):
        """
        Creates a visual data table with micro-bars and numeric annotations.

        Args:
            df (pd.DataFrame): Data where index is row labels and columns are groups.
            title (str): The chart title.
            colors (list, optional): List of hex colors for columns.
            bar_scale (float): Scaling factor for bar width relative to cell.
            max_bar_width (float): Ceiling for bar width to prevent overlap.
            fig_width (float): Width of the final figure in inches.
            fig_height (float): Height of the final figure in inches.
        """
        rows = list(df.index)
        cols = list(df.columns)
        num_rows = len(rows)

        # Initialize plot with user-defined dimensions
        fig, ax = plt.subplots(figsize=(fig_width, fig_height))

        # 1. Plot Headers
        for j, name in enumerate(cols):
            wrapped_name = "\n".join(textwrap.wrap(name, width=12))
            ax.text(j + 0.5, num_rows + 0.5, wrapped_name,
                    ha='center', va='bottom', fontsize=10, fontweight='bold', linespacing=1.2)

        # 2. Plot Rows
        for i, row_label in enumerate(reversed(rows)):
            ax.text(-0.1, i + 0.25, row_label, ha='right', va='center', fontsize=10)

            for j, col_name in enumerate(cols):
                val = df.loc[row_label, col_name]
                color = colors[j % len(colors)] if colors else '#3498db'

                bar_width = min((val / 100) * bar_scale, max_bar_width)
                rect = plt.Rectangle((j + 0.05, i + 0.1), bar_width, 0.3, color=color, alpha=0.9)
                ax.add_patch(rect)

                ax.text(j + 0.1 + bar_width, i + 0.25, f"{val:g}", ha='left', va='center', fontsize=9)

        # 3. Aesthetics
        ax.set_xlim(-2.5, len(cols))
        ax.set_ylim(-0.5, num_rows + 2)
        ax.set_aspect('auto')  # Allows the dimensions to stretch the content
        ax.axis('off')
        plt.title(title, loc='left', fontsize=13, pad=40, fontweight='bold', color='#333333')

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
