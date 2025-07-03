import seaborn as sns
from faicons import icon_svg

# Import data from shared.py
from shared import app_dir, df
import json

import plotly.express as px
from shinywidgets import render_plotly

from shiny import reactive
from shiny.express import input, render, ui

ui.page_opts(title="West Town consistently rattiest community area in Chicago", fillable=True)

years = ["All"] + list(range(2019, 2024 + 1))

with ui.layout_columns(col_widths=(3, 9)):
    with ui.card():
        "Toggle year and metric here"

        ui.input_select("metric", "Select rodent control metric", {"calls": "Annual 311 rodent calls", 
                                                                "calls per capita":"Annual 311 rodent calls per capita", 
                                                                "mean time": "Mean call response time",
                                                                "median time":"Median call response time"})
        ui.input_select("year", "Select year", years, selected="All")

    with ui.card(full_screen=True):


        @render_plotly
        def rat_map():
            
            if input.metric() and not input.year():
                filtered_df = df[(df['metric'] == input.metric())]
                filtered_df = filtered_df[filtered_df['year'] == 'All']
            elif input.metric() and input.year():
                if "All" in input.year():
                    filtered_df = df[(df['metric'] == input.metric())]
                    filtered_df = filtered_df[filtered_df['year']=='All']
                else:
                    filtered_df = df[(df['metric'] == input.metric())]
                    filtered_df = filtered_df[filtered_df['year'] == input.year()]
            # else: 
            #     filtered_df = df


            comm_areas_raw = open(app_dir / "Boundaries - Community Areas_20250703.geojson", "r")
            comm_areas = json.load(comm_areas_raw)

            fig = px.choropleth(filtered_df, geojson=comm_areas, locations='comm_area', color='value',
                           color_continuous_scale="sunsetdark",
                           labels={'metric':'metric'},
                           hover_name='comm_name',
                           hover_data=['metric', 'value']
                          )
            
            fig.update_geos(fitbounds="locations", visible=True)


            return fig


ui.include_css(app_dir / "styles.css")


@reactive.calc
def filtered_df():
    filt_df = df[df["species"].isin(input.species())]
    filt_df = filt_df.loc[filt_df["body_mass_g"] < input.mass()]
    return filt_df
