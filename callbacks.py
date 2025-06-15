from dash import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go

def register_callbacks(app, data):
    @app.callback(
        Output('time-series-plot', 'figure'),
        [Input('indicator-selector', 'value'),
         Input('country-selector', 'value'),
         Input('year-slider', 'value')]
    )
    def update_time_series(selected_indicator, selected_countries, year_range):
        if not selected_countries or not year_range:
            return go.Figure().add_annotation(text="Please select countries and year range", showarrow=False)

        filtered_df = data[
            (data['Indicator'] == selected_indicator) &
            (data['Country'].isin(selected_countries)) &
            (data['Year'] >= year_range[0]) &
            (data['Year'] <= year_range[1])
        ]

        if filtered_df.empty:
            return go.Figure().add_annotation(text="No data available", showarrow=False)

        fig = px.line(
            filtered_df,
            x='Year',
            y='Value',
            color='Country',
            title=f'Trend: {selected_indicator}',
            labels={'Value': 'Value', 'Year': 'Year'},
            markers=True,
            line_shape='spline'
        )

        fig.update_layout(
            hovermode='x unified',
            template='plotly_white',
            height=400,
            margin=dict(l=40, r=40, t=60, b=40)
        )
        return fig

    @app.callback(
        Output('comparison-plot', 'figure'),
        [Input('indicator-selector', 'value'),
         Input('year-slider', 'value')]
    )
    def update_comparison(selected_indicator, year_range):
        filtered_df = data[
            (data['Indicator'] == selected_indicator) &
            (data['Year'] >= year_range[0]) &
            (data['Year'] <= year_range[1])
        ]

        if filtered_df.empty:
            return go.Figure().add_annotation(text="No data available", showarrow=False)

        # Agregasi data
        avg_df = filtered_df.groupby('Country', as_index=False)['Value'].mean().sort_values('Value')

        fig = px.bar(
            avg_df,
            x='Value',
            y='Country',
            orientation='h',
            title=f'Comparison: {selected_indicator}',
            labels={'Value': 'Average Value', 'Country': ''},
            color='Value',
            color_continuous_scale='Teal'
        )

        fig.update_layout(
            template='plotly_white',
            height=500,
            margin=dict(l=40, r=40, t=60, b=40),
            yaxis={'categoryorder': 'total ascending'}
        )
        return fig

    @app.callback(
        Output('demographic-plot', 'figure'),
        [Input('indicator-selector', 'value'),
         Input('country-selector', 'value'),
         Input('year-slider', 'value')]
    )
    def update_demographic(selected_indicator, selected_countries, year_range):
        filtered_df = data[
            (data['Indicator'] == selected_indicator) &
            (data['Country'].isin(selected_countries)) &
            (data['Year'] >= year_range[0]) &
            (data['Year'] <= year_range[1])
        ]

        if filtered_df.empty:
            return go.Figure().add_annotation(text="No data available", showarrow=False)

        # Buat visualisasi alternatif jika data demografi tidak tersedia
        if filtered_df['Sex'].nunique() == 1 and filtered_df['Age'].nunique() == 1:
            fig = px.scatter(
                filtered_df,
                x='Year',
                y='Value',
                color='Country',
                size='Value',
                title=f'Value Distribution: {selected_indicator}',
                labels={'Value': 'Value', 'Year': 'Year'}
            )
        else:
            fig = px.sunburst(
                filtered_df,
                path=['Country', 'Sex', 'Age', 'Urbanization'],
                values='Value',
                title='Demographic Distribution',
                color='Value',
                color_continuous_scale='Blues'
            )

        fig.update_layout(
            template='plotly_white',
            height=500,
            margin=dict(l=40, r=40, t=60, b=40)
        )
        return fig