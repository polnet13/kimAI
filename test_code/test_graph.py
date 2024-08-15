			
	
	
 

import plotly.graph_objects as go

kind = ['움직임 감지', 'AI 디텍션', '디텍션2회+OCR']

fig = go.Figure(data=[
    go.Bar(name='4070ti', x=kind, y=[250, 21, 20], text=[250, 21, 20], textposition='auto', marker=dict(color='#008080')),
    go.Bar(name='7500f', x=kind, y=[225, 13, 5], text=[225, 13, 5], textposition='auto', marker=dict(color='#008080')),
    go.Bar(name='i5 8500', x=kind, y=[70, 2, 0.5], text=[70, 2, 0.5], textposition='auto', marker=dict(color='red'))
])

# Change the bar mode
fig.update_layout(barmode='group')
fig.update_layout(
    font=dict(
        size=16,
        color='black',
        family='Arial'
    )
)
fig.show()