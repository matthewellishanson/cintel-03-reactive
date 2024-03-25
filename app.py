import plotly.express as px
from shiny.express import input, ui
from shinywidgets import render_plotly
import palmerpenguins  # This package provides the Palmer Penguins dataset
import pandas as pd
import seaborn as sns
from shiny import render, reactive

# Use the built-in function to load the Palmer Penguins dataset
penguins_df = palmerpenguins.load_penguins()

ui.page_opts(title="Penguin Data", fillable=True)

# Add a Shiny UI sidebar for user interaction
# Use the ui.sidebar() function to create a sidebar
# Set the open parameter to "open" to make the sidebar open by default
# Use a with block to add content to the sidebar
with ui.sidebar(open="open"):
    # Use the ui.h2() function to add a 2nd level header to the sidebar
    # pass in a string argument (in quotes) to set the header text to "Sidebar" 
    ui.h2("Sidebar")

    # Use ui.input_selectize() to create a dropdown input to choose a column
    # pass in three arguments:
    #   the name of the input (in quotes), e.g., "selected_attribute"
    #   the label for the input (in quotes)
    #   a list of options for the input (in square brackets) 
    #   e.g. ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"]
    ui.input_selectize(
        "selected_attribute",
        "Select Plotly Attribute",
        ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"]
    )

    # Use ui.input_numeric() to create a numeric input for the number of Plotly histogram bins
    #   pass in two arguments:
    #   the name of the input (in quotes), e.g. "plotly_bin_count"
    #   the label for the input (in quotes)
    ui.input_numeric("plotly_bin_count", "Plotly Bin Count", 30)

    # Use ui.input_slider() to create a slider input for the number of Seaborn bins
    #   pass in four arguments:
    #   the name of the input (in quotes), e.g. "seaborn_bin_count"
    #   the label for the input (in quotes)
    #   the minimum value for the input (as an integer)
    #   the maximum value for the input (as an integer)
    #   the default value for the input (as an integer)
    ui.input_slider("seaborn_bin_count", "Number of Seaborn Bins", 1, 50, 25)

    # Use ui.input_checkbox_group() to create a checkbox group input to filter the species
    #   pass in five arguments:
    #   the name of the input (in quotes), e.g.  "selected_species_list"
    #   the label for the input (in quotes)
    #   a list of options for the input (in square brackets) as ["Adelie", "Gentoo", "Chinstrap"]
    #   a keyword argument selected= a list of selected options for the input (in square brackets)
    #   a keyword argument inline= a Boolean value (True or False) as you like
    ui.input_checkbox_group(
        "selected_species_list", 
        "Species",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected="Gentoo",
        inline=True
    )

    # Use ui.hr() to add a horizontal rule to the sidebar
    ui.hr()

    # Use ui.a() to add a hyperlink to the sidebar
    #   pass in two arguments:
    #   the text for the hyperlink (in quotes), e.g. "GitHub"
    #   a keyword argument href= the URL for the hyperlink (in quotes), e.g. your GitHub repo URL
    #   a keyword argument target= "_blank" to open the link in a new tab
    ui.a(
        "Github",
        href="https://github.com/matthewellishanson/cintel-02-data/blob/main/app.py",
        target="_blank"
    )

# Create a DataTable
with ui.layout_columns():

    with ui.card(full_screen=True):
        ui.h2("Penguins DataTable")

        @render.data_frame
        def render_penguins_table():
            return render.DataTable(filtered_data())

    # create a DataGrid
    with ui.card(full_screen=True):
        ui.h2("Penguins DataGrid")

        @render.data_frame
        def penguins_datagrid():
            return render.DataGrid(filtered_data())

ui.hr()

# Create a new set of columns for charts
with ui.layout_columns():

    # Create a Plotly Histogram showing all species

    with ui.card(full_screen=True):
        ui.card_header("Plotly Histogram")
    
        @render_plotly
        def plotly_histogram():
            return px.histogram(
                filtered_data(), x=input.selected_attribute(), nbins=input.plotly_bin_count(), color="species"
        )

    # Creates a Seaborn Histogram showing all species

    with ui.card(full_screen=True):
        ui.card_header("Seaborn Histogram")
    
        @render.plot(alt="Seaborn Histogram")
        def seaborn_histogram():
            histplot = sns.histplot(data=filtered_data(), x="body_mass_g", bins=input.seaborn_bin_count(), multiple="dodge", hue="species")
            histplot.set_title("Palmer Penguins")
            histplot.set_xlabel("Mass")
            histplot.set_ylabel("Count")
            return histplot
    
    # Creates a Plotly Scatterplot showing all species

    with ui.card(full_screen=True):
        ui.card_header("Species Scatterplot")
    
        @render_plotly
        def plotly_scatterplot():
            return px.scatter(filtered_data(),
                x="bill_length_mm",
                y="body_mass_g",
                color="species",
                title="Penguins Plot",
                labels={
                    "bill_length_mm": "Bill Length (mm)",
                    "body_mass_g": "Body Mass (g)",
                }, 
            )

# --------------------------------------------------------
# Reactive calculations and effects
# --------------------------------------------------------

# Add a reactive calculation to filter the data
# By decorating the function with @reactive, we can use the function to filter the data
# The function will be called whenever an input functions used to generate that output changes.
# Any output that depends on the reactive function (e.g., filtered_data()) will be updated when the data changes.

@reactive.calc
def filtered_data():
    return penguins_df[penguins_df["species"].isin(input.selected_species_list())]
