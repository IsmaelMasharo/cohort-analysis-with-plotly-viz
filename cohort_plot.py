import pandas as pd
import plotly.figure_factory as ff


def parse_cohort_dataset(df):
    df.cohort = pd.to_datetime(df.cohort)
    df = df.set_index(['cohort', 'cohort_index'])
    df = df.sort_index(level=0)
    
    cohort_size = df.groupby('cohort')['cohort_size'].first()
    label_index = df.index.levels[0].strftime('%b %d, %Y')  + ' (n = ' + cohort_size.astype(str) + ')'
    
    df.index = df.index.set_levels([label_index, df.index.levels[1]])
    df.percentage = df.percentage.map(lambda p: round(p, 2))
    return df


def transform_into_cohort_shape(df):
    df_unstack_percentage = df['percentage'].unstack(1)
    df_unstack_totals = df['cohort_index_size'].unstack(1)
    return df_unstack_percentage, df_unstack_totals

def construct_viz_params(df_unstack_percentage, df_unstack_totals):
    cohort_display_percentage_values = []
    cohort_percentage_labels = []
    cohort_index_size_labels = []

    for x in df_unstack_percentage.index.values.tolist():
        cohort_display_percentage_values.append(df_unstack_percentage.loc[x].fillna(0).tolist())
        cohort_percentage_labels.append(df_unstack_percentage.loc[x].fillna('').astype(str).tolist())
        cohort_index_size_labels.append(df_unstack_totals.loc[x].fillna('').astype(str).tolist())

    cols = x_axis = df_unstack_percentage.columns.values.tolist()
    rows = y_axis = df_unstack_percentage.index.values.tolist()

    hover=[]
    for row in range(len(rows)):
        hovertemplate = (
            '<b>Cohort: {cohort_time}<b> <br><br>'+
            'Months after registration: {cohort_index}<br>'+
            'Cohort Size: {cohort_size}<br>' +
            'Retention Percentage: {retention_percentage}%<br>' 
            'Retention Size: {retention_size}<br>'
        )

        cohort_hovertext = []
        percentage_total_by_cohort = zip(cohort_percentage_labels[row], cohort_index_size_labels[row])

        for i, (percentage, total) in enumerate(percentage_total_by_cohort):
            if percentage and total: 
                total_val=float(total)
                percentage_val=float(percentage)

                hovertext = hovertemplate.format(
                    cohort_time=rows[row].split('(')[0], # remove cohort size from cohort label
                    cohort_size=round(total_val /(percentage_val / 100)),
                    cohort_index=int(cols[i]),
                    retention_percentage=round(percentage_val, 2),
                    retention_size=int(total_val)
                )
            else:
                hovertext=''

            cohort_hovertext.append(hovertext)
        hover.append(cohort_hovertext) 
        
    y_axis= y_axis[::-1]
    z_axis = cohort_display_percentage_values[::-1]
    annotations = cohort_percentage_labels[::-1]
    hovertext = hover[::-1]

    return x_axis, y_axis, z_axis, annotations, hovertext


def create_cohort_viz(df_unstack_percentage, df_unstack_totals, viz_title):
    colorscale=[[0.0, 'rgb(255,255,255)'], [.2, 'rgb(255, 255, 153)'],
            [.4, 'rgb(153, 255, 204)'], [.6, 'rgb(179, 217, 255)'],
            [.8, 'rgb(240, 179, 255)'],[1.0, 'rgb(255, 77, 148)']]
    
    x_axis, y_axis, z_axis, annotations, hovertext = construct_viz_params(df_unstack_percentage, df_unstack_totals)

    fig = ff.create_annotated_heatmap(
        x=x_axis, y=y_axis, z=z_axis,
        annotation_text=annotations,
        colorscale='YlGnBu', # 'deep'
        text=hovertext,
        hoverinfo='text',
    )

    fig.update_layout(
        xaxis_title= viz_title,
        yaxis_title="",
        margin=dict(l=40, r=40),
    )

    return fig


def plot_cohort_table(df, title=''):
    
    parsed_df = parse_cohort_dataset(df)
    cohort_shaped_df = transform_into_cohort_shape(parsed_df)
    fig = create_cohort_viz(*cohort_shaped_df, title)

    return fig
    