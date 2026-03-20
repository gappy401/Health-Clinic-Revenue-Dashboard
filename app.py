import dash
from dash import dcc, html
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

random.seed(42)
np.random.seed(42)

# ── DATA SIMULATION ──────────────────────────────────────────────────────────

# Revenue cycle data — 12 months
months = pd.date_range(end=datetime.today(), periods=12, freq='MS').strftime('%b %Y').tolist()
billed   = [148000, 153000, 161000, 158000, 172000, 168000,
            175000, 182000, 179000, 188000, 194000, 201000]
collected = [118000, 119000, 128000, 121000, 138000, 131000,
             143000, 149000, 140000, 157000, 163000, 172000]
collection_rates = [round(c/b*100, 1) for b, c in zip(billed, collected)]

avg_days_to_payment = [34, 32, 30, 33, 29, 31, 28, 27, 30, 26, 25, 24]

# Denial reasons — 12 weeks
weeks = [f"Wk {i+1}" for i in range(12)]
denial_data = {
    'Authorization': [18, 22, 20, 25, 19, 23, 17, 21, 16, 18, 14, 13],
    'Eligibility':   [12, 10, 14, 11, 13,  9, 12, 10,  9, 11,  8,  7],
    'Coding Error':  [ 8,  9,  7, 10,  8,  7,  6,  8,  7,  6,  5,  5],
}

# Authorization by payer
payers = ['Aetna', 'UnitedHealth', 'Cigna', 'BlueCross', 'Medicaid', 'Medicare']
auth_pending  = [23, 31, 18, 27, 42, 15]
auth_approved = [87, 102, 76, 94, 118, 63]
auth_denied   = [12, 18,  9, 14, 28,  8]
avg_wait_days = [8.2, 11.4, 6.9, 9.7, 14.2, 7.1]

# KPI summary
current_billed    = billed[-1]
current_collected = collected[-1]
current_rate      = collection_rates[-1]
current_days      = avg_days_to_payment[-1]
prev_rate         = collection_rates[-2]
prev_days         = avg_days_to_payment[-2]

# ── COLOR PALETTE ─────────────────────────────────────────────────────────────
BG       = '#0F1117'
CARD     = '#181C27'
BORDER   = '#252A3A'
TEAL     = '#2DD4BF'
TEAL_DIM = '#0D9488'
CORAL    = '#FB7185'
AMBER    = '#FBB040'
MUTED    = '#64748B'
TEXT     = '#E2E8F0'
SUBTEXT  = '#94A3B8'

FONT = "'DM Mono', 'Courier New', monospace"
FONT_SANS = "'DM Sans', 'Segoe UI', sans-serif"

def card(children, style=None):
    base = {
        'background': CARD,
        'border': f'1px solid {BORDER}',
        'borderRadius': '12px',
        'padding': '24px',
    }
    if style:
        base.update(style)
    return html.Div(children, style=base)

def kpi(label, value, sub=None, color=TEAL):
    return html.Div([
        html.Div(label, style={'fontSize': '11px', 'color': SUBTEXT,
                               'letterSpacing': '0.1em', 'textTransform': 'uppercase',
                               'fontFamily': FONT, 'marginBottom': '6px'}),
        html.Div(value, style={'fontSize': '32px', 'fontWeight': '700',
                               'color': color, 'fontFamily': FONT, 'lineHeight': '1'}),
        html.Div(sub or '', style={'fontSize': '12px', 'color': SUBTEXT,
                                   'marginTop': '6px', 'fontFamily': FONT_SANS}),
    ])

def status_badge(text, color):
    return html.Span(text, style={
        'background': color + '22',
        'color': color,
        'border': f'1px solid {color}44',
        'borderRadius': '4px',
        'padding': '2px 8px',
        'fontSize': '11px',
        'fontFamily': FONT,
        'letterSpacing': '0.05em',
    })

# ── CHARTS ────────────────────────────────────────────────────────────────────

def make_revenue_chart():
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=months, y=billed,
        name='Billed', marker_color=BORDER,
        marker_line_width=0,
    ))
    fig.add_trace(go.Bar(
        x=months, y=collected,
        name='Collected', marker_color=TEAL,
        marker_line_width=0,
    ))
    fig.add_trace(go.Scatter(
        x=months, y=collection_rates,
        name='Collection Rate %',
        yaxis='y2', mode='lines+markers',
        line=dict(color=AMBER, width=2, dash='dot'),
        marker=dict(size=5, color=AMBER),
    ))
    fig.update_layout(
        barmode='overlay',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family=FONT_SANS, color=SUBTEXT, size=11),
        legend=dict(orientation='h', y=1.1, x=0,
                    font=dict(size=11), bgcolor='rgba(0,0,0,0)'),
        margin=dict(l=0, r=0, t=30, b=0),
        yaxis=dict(gridcolor=BORDER, tickformat='$,.0f', tickfont=dict(size=10)),
        yaxis2=dict(overlaying='y', side='right', ticksuffix='%',
                    range=[70, 100], tickfont=dict(size=10), gridcolor='rgba(0,0,0,0)'),
        xaxis=dict(tickfont=dict(size=10), gridcolor='rgba(0,0,0,0)'),
        height=260,
    )
    return fig

def make_denial_chart():
    fig = go.Figure()
    colors = [CORAL, AMBER, TEAL_DIM]
    fill_colors = ['rgba(251,113,133,0.09)', 'rgba(251,176,64,0.09)', 'rgba(13,148,136,0.09)']
    for i, (reason, vals) in enumerate(denial_data.items()):
        fig.add_trace(go.Scatter(
            x=weeks, y=vals, name=reason,
            mode='lines+markers',
            line=dict(color=colors[i], width=2),
            marker=dict(size=4),
            fill='tozeroy' if i == 0 else 'tonexty',
            fillcolor=fill_colors[i],
        ))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family=FONT_SANS, color=SUBTEXT, size=11),
        legend=dict(orientation='h', y=1.12, x=0,
                    font=dict(size=11), bgcolor='rgba(0,0,0,0)'),
        margin=dict(l=0, r=0, t=30, b=0),
        yaxis=dict(gridcolor=BORDER, title='# Claims Denied',
                   title_font=dict(size=10), tickfont=dict(size=10)),
        xaxis=dict(tickfont=dict(size=10), gridcolor='rgba(0,0,0,0)'),
        height=240,
    )
    return fig

def make_auth_chart():
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Approved', x=payers, y=auth_approved,
                         marker_color=TEAL, marker_line_width=0))
    fig.add_trace(go.Bar(name='Pending',  x=payers, y=auth_pending,
                         marker_color=AMBER, marker_line_width=0))
    fig.add_trace(go.Bar(name='Denied',   x=payers, y=auth_denied,
                         marker_color=CORAL, marker_line_width=0))
    fig.update_layout(
        barmode='stack',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family=FONT_SANS, color=SUBTEXT, size=11),
        legend=dict(orientation='h', y=1.12, x=0,
                    font=dict(size=11), bgcolor='rgba(0,0,0,0)'),
        margin=dict(l=0, r=0, t=30, b=0),
        yaxis=dict(gridcolor=BORDER, tickfont=dict(size=10)),
        xaxis=dict(tickfont=dict(size=10), gridcolor='rgba(0,0,0,0)'),
        height=240,
    )
    return fig

def make_wait_chart():
    colors = [CORAL if d > 10 else AMBER if d > 8 else TEAL for d in avg_wait_days]
    fig = go.Figure(go.Bar(
        x=avg_wait_days, y=payers,
        orientation='h',
        marker_color=colors,
        marker_line_width=0,
        text=[f'{d}d' for d in avg_wait_days],
        textposition='outside',
        textfont=dict(size=11, color=TEXT),
    ))
    fig.add_vline(x=10, line_dash='dot', line_color='rgba(251,113,133,0.5)', line_width=1)
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family=FONT_SANS, color=SUBTEXT, size=11),
        margin=dict(l=0, r=60, t=10, b=0),
        xaxis=dict(gridcolor=BORDER, ticksuffix=' d', tickfont=dict(size=10)),
        yaxis=dict(tickfont=dict(size=11), gridcolor='rgba(0,0,0,0)'),
        height=220,
        annotations=[dict(x=10.3, y=5.6, text='10d target', showarrow=False,
                          font=dict(size=9, color=CORAL), xanchor='left')],
    )
    return fig

# ── LAYOUT ────────────────────────────────────────────────────────────────────

app = dash.Dash(__name__, title='Camber · Clinic Analytics')

rate_delta  = current_rate - prev_rate
days_delta  = current_days - prev_days
rate_color  = TEAL if rate_delta >= 0 else CORAL
days_color  = TEAL if days_delta <= 0 else CORAL
rate_arrow  = '▲' if rate_delta >= 0 else '▼'
days_arrow  = '▼' if days_delta <= 0 else '▲'

app.layout = html.Div(style={
    'background': BG,
    'minHeight': '100vh',
    'fontFamily': FONT_SANS,
    'color': TEXT,
    'padding': '32px',
    'boxSizing': 'border-box',
}, children=[

    # Header
    html.Div(style={'marginBottom': '32px', 'display': 'flex',
                    'justifyContent': 'space-between', 'alignItems': 'flex-end'}, children=[
        html.Div([
            html.Div('CAMBER', style={
                'fontSize': '11px', 'letterSpacing': '0.25em',
                'color': TEAL, 'fontFamily': FONT, 'marginBottom': '4px',
            }),
            html.H1('Clinic Revenue & Operations', style={
                'margin': '0', 'fontSize': '26px', 'fontWeight': '700',
                'color': TEXT, 'letterSpacing': '-0.02em',
            }),
        ]),
        html.Div([
            html.Div('Reporting Period', style={'fontSize': '11px', 'color': SUBTEXT,
                                                'textAlign': 'right', 'marginBottom': '2px',
                                                'fontFamily': FONT}),
            html.Div('Jan 2024 – Dec 2024', style={'fontSize': '14px', 'color': TEXT,
                                                    'fontFamily': FONT}),
        ]),
    ]),

    # KPI Row
    html.Div(style={'display': 'grid', 'gridTemplateColumns': 'repeat(4, 1fr)',
                    'gap': '16px', 'marginBottom': '24px'}, children=[
        card(kpi('Total Billed (Dec)', f'${current_billed:,.0f}',
                 'This month')),
        card(kpi('Total Collected (Dec)', f'${current_collected:,.0f}',
                 f'{round(current_collected/current_billed*100,1)}% of billed', TEAL)),
        card(kpi('Collection Rate', f'{current_rate}%',
                 f'{rate_arrow} {abs(rate_delta):.1f}pp vs last month', rate_color)),
        card(kpi('Avg Days to Payment', f'{current_days}d',
                 f'{days_arrow} {abs(days_delta)}d vs last month', days_color)),
    ]),

    # Revenue chart
    card([
        html.Div(style={'display': 'flex', 'justifyContent': 'space-between',
                        'alignItems': 'center', 'marginBottom': '16px'}, children=[
            html.Div('Revenue Cycle · 12-Month Trend', style={
                'fontSize': '13px', 'fontWeight': '600', 'color': TEXT,
                'letterSpacing': '-0.01em',
            }),
            html.Div(style={'display': 'flex', 'gap': '8px'}, children=[
                status_badge('Billed', MUTED),
                status_badge('Collected', TEAL),
                status_badge('Rate %', AMBER),
            ]),
        ]),
        dcc.Graph(figure=make_revenue_chart(), config={'displayModeBar': False}),
    ], style={'marginBottom': '24px'}),

    # Bottom two panels
    html.Div(style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr',
                    'gap': '24px', 'marginBottom': '24px'}, children=[

        # Denials
        card([
            html.Div(style={'display': 'flex', 'justifyContent': 'space-between',
                            'alignItems': 'center', 'marginBottom': '16px'}, children=[
                html.Div('Claim Denials · 12-Week Trend', style={
                    'fontSize': '13px', 'fontWeight': '600', 'color': TEXT}),
                html.Div(style={'display': 'flex', 'gap': '8px'}, children=[
                    status_badge('Authorization', CORAL),
                    status_badge('Eligibility', AMBER),
                    status_badge('Coding', TEAL_DIM),
                ]),
            ]),
            dcc.Graph(figure=make_denial_chart(), config={'displayModeBar': False}),
            html.Div(style={'marginTop': '16px', 'padding': '12px',
                            'background': CORAL + '11', 'borderRadius': '8px',
                            'border': f'1px solid {CORAL}33'}, children=[
                html.Div('⚠ Authorization denials are the #1 driver — 35% of total.',
                         style={'fontSize': '12px', 'color': CORAL, 'fontFamily': FONT}),
            ]),
        ]),

        # Auth by payer
        card([
            html.Div('Authorization Status · By Payer', style={
                'fontSize': '13px', 'fontWeight': '600', 'color': TEXT,
                'marginBottom': '16px',
            }),
            dcc.Graph(figure=make_auth_chart(), config={'displayModeBar': False}),
        ]),
    ]),

    # Wait times
    card([
        html.Div(style={'display': 'flex', 'justifyContent': 'space-between',
                        'alignItems': 'center', 'marginBottom': '16px'}, children=[
            html.Div('Avg Days Waiting for Authorization · By Payer', style={
                'fontSize': '13px', 'fontWeight': '600', 'color': TEXT}),
            html.Div([
                status_badge('> 10d', CORAL),
                html.Span(' ', style={'width': '6px', 'display': 'inline-block'}),
                status_badge('8–10d', AMBER),
                html.Span(' ', style={'width': '6px', 'display': 'inline-block'}),
                status_badge('< 8d', TEAL),
            ]),
        ]),
        dcc.Graph(figure=make_wait_chart(), config={'displayModeBar': False}),
        html.Div(style={'marginTop': '12px', 'padding': '12px',
                        'background': AMBER + '11', 'borderRadius': '8px',
                        'border': f'1px solid {AMBER}33'}, children=[
            html.Div('Medicaid auth delays (14.2d) are 42% above the 10-day target — highest risk for care disruption.',
                     style={'fontSize': '12px', 'color': AMBER, 'fontFamily': FONT}),
        ]),
    ]),

    # Footer
    html.Div(style={'marginTop': '32px', 'paddingTop': '16px',
                    'borderTop': f'1px solid {BORDER}',
                    'display': 'flex', 'justifyContent': 'space-between'}, children=[
        html.Div('Simulated data for portfolio purposes · Built by Nandita Ghildyal',
                 style={'fontSize': '11px', 'color': MUTED, 'fontFamily': FONT}),
        html.Div('camber-analytics-demo · github.com/nanditaghildyal',
                 style={'fontSize': '11px', 'color': MUTED, 'fontFamily': FONT}),
    ]),
])

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8050)
