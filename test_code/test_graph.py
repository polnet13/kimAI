			
	
	
 
import plotly.graph_objects as go

kind = ['움직임 감지만(AI 미사용)', 'AI 디텍션 1회', '디텍션 2회 + OCR']

fig = go.Figure(data=[
    go.Bar(name='4070ti', x=kind, y=[250, 40, 20], text=[250, 40, 20], textposition='auto', marker=dict(color='#008115')),
    go.Bar(name='7500f', x=kind, y=[225, 13, 5], text=[225, 13, 5], textposition='auto', marker=dict(color='#008080')),
    go.Bar(name='i5 8500', x=kind, y=[126, 3, 0.5], text=[126, 3, 0.5], textposition='auto', marker=dict(color='red'))
])

# Change the bar mode
fig.update_layout(barmode='group')
fig.update_layout(
    font=dict(
        size=16,
        color='black',
        family='Arial'
    ),
    legend=dict(
        x=1,
        y=1,
        xanchor='right',
        yanchor='top',
        bgcolor='rgba(255, 255, 255, 0.5)',
        font=dict(
            size=20  # Increase the font size of the legend
        )
    )
)
fig.show()