"""
Chart Components
Plotly chart components for the dashboard
"""
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
from typing import Optional, List, Dict, Any


class ChartManager:
    """Manages all chart creation and configuration"""
    
    # Theme colors
    COLORS = {
        'cyan': '#00f5ff',
        'magenta': '#ff00ff',
        'green': '#00ff9d',
        'orange': '#ff6b35',
        'red': '#ff3366',
        'blue': '#58a6ff',
        'purple': '#9b59b6',
        'yellow': '#f1c40f',
    }
    
    # Chart templates
    TEMPLATE = "plotly_dark"
    
    @staticmethod
    def temperature_trend(df: pd.DataFrame) -> go.Figure:
        """
        Create temperature trend chart
        
        Args:
            df: DataFrame with temperature data
            
        Returns:
            Plotly figure
        """
        
        fig = go.Figure()
        
        # Add traces for each time
        fig.add_trace(go.Scatter(
            x=df['Tanggal_DT'], 
            y=df['T07'],
            name="07:00",
            line=dict(color=ChartManager.COLORS['cyan'], width=2),
            mode='lines+markers'
        ))
        
        fig.add_trace(go.Scatter(
            x=df['Tanggal_DT'], 
            y=df['T13'],
            name="13:00",
            line=dict(color=ChartManager.COLORS['red'], width=2),
            mode='lines+markers'
        ))
        
        fig.add_trace(go.Scatter(
            x=df['Tanggal_DT'], 
            y=df['T18'],
            name="18:00",
            line=dict(color=ChartManager.COLORS['orange'], width=2),
            mode='lines+markers'
        ))
        
        fig.update_layout(
            template=ChartManager.TEMPLATE,
            title="🌡️ Tren Suhu Harian",
            xaxis_title="Tanggal",
            yaxis_title="Suhu (°C)",
            hovermode="x unified",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        return fig
    
    @staticmethod
    def windrose(df: pd.DataFrame) -> go.Figure:
        """
        Create windrose chart
        
        Args:
            df: DataFrame with wind data
            
        Returns:
            Plotly figure
        """
        
        # Bin wind directions
        dir_bins = [0, 45, 90, 135, 180, 225, 270, 315, 360]
        dir_labels = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
        
        df = df.copy()
        df['WD_Label'] = pd.cut(
            df['WD_Most'],
            bins=dir_bins,
            labels=dir_labels,
            include_lowest=True
        )
        
        # Bin wind speeds
        speed_bins = [0, 3, 6, 10, 15, 20, 50]
        speed_labels = ['0-3', '3-6', '6-10', '10-15', '15-20', '>20']
        
        df['WS_Bin'] = pd.cut(
            df['WS_Avg'],
            bins=speed_bins,
            labels=speed_labels,
            include_lowest=True
        )
        
        # Group data
        wind_data = df.groupby(['WD_Label', 'WS_Bin']).size().reset_index(name='count')
        
        # Create polar bar chart
        fig = px.bar_polar(
            wind_data,
            r='count',
            theta='WD_Label',
            color='WS_Bin',
            template=ChartManager.TEMPLATE,
            color_discrete_sequence=px.colors.sequential.Plasma,
            title="🪁 Windrose (Arah Angin)"
        )
        
        fig.update_layout(
            polar=dict(bgcolor="#161b22"),
            margin=dict(t=50, b=50, l=50, r=50),
            legend_title="Kecepatan (kt)"
        )
        
        return fig
    
    @staticmethod
    def pressure_chart(df: pd.DataFrame) -> go.Figure:
        """
        Create pressure area chart
        
        Args:
            df: DataFrame with pressure data
            
        Returns:
            Plotly figure
        """
        
        fig = px.area(
            df, 
            x='Tanggal_DT', 
            y='Pressure',
            color_discrete_sequence=[ChartManager.COLORS['purple']]
        )
        
        fig.update_layout(
            template=ChartManager.TEMPLATE,
            title="⏲️ Tekanan Udara (mb)",
            xaxis_title="Tanggal",
            yaxis_title="Tekanan (mb)",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        
        return fig
    
    @staticmethod
    def humidity_chart(df: pd.DataFrame) -> go.Figure:
        """
        Create humidity line chart
        
        Args:
            df: DataFrame with humidity data
            
        Returns:
            Plotly figure
        """
        
        fig = px.line(
            df, 
            x='Tanggal_DT', 
            y=['RH07', 'RH13', 'RH18', 'RH_Avg'],
            color_discrete_sequence=[
                ChartManager.COLORS['green'],
                ChartManager.COLORS['yellow'],
                ChartManager.COLORS['orange'],
                '#ffffff'
            ]
        )
        
        fig.update_layout(
            template=ChartManager.TEMPLATE,
            title="💧 Kelembapan Udara (RH %)",
            xaxis_title="Tanggal",
            yaxis_title="Kelembapan (%)",
            paper_bgcolor="rgba(0,0,0,0)",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        return fig
    
    @staticmethod
    def rainfall_chart(df: pd.DataFrame) -> go.Figure:
        """
        Create rainfall bar chart
        
        Args:
            df: DataFrame with rainfall data
            
        Returns:
            Plotly figure
        """
        
        fig = px.bar(
            df, 
            x='Tanggal_DT', 
            y='Rain',
            color='Rain',
            color_continuous_scale='Blues'
        )
        
        fig.update_layout(
            template=ChartManager.TEMPLATE,
            title="🌧️ Curah Hujan (mm)",
            xaxis_title="Tanggal",
            yaxis_title="Curah Hujan (mm)",
            paper_bgcolor="rgba(0,0,0,0)",
            coloraxis_showscale=False
        )
        
        return fig
    
    @staticmethod
    def risk_gauge(score: float, level: str) -> go.Figure:
        """
        Create risk gauge chart
        
        Args:
            score: Risk score (0-100)
            level: Risk level name
            
        Returns:
            Plotly figure
        """
        
        # Determine color based on level
        colors = {
            'NORMAL': ChartManager.COLORS['green'],
            'WATCH': ChartManager.COLORS['blue'],
            'WARNING': ChartManager.COLORS['yellow'],
            'ALERT': ChartManager.COLORS['orange'],
            'CRITICAL': ChartManager.COLORS['red'],
        }
        
        color = colors.get(level.upper(), ChartManager.COLORS['green'])
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=score,
            title={'text': f"Risk Index - {level}", 'font': {'size': 20}},
            gauge={
                'axis': {'range': [0, 100], 'tickwidth': 1},
                'bar': {'color': color},
                'bgcolor': "#161b22",
                'steps': [
                    {'range': [0, 30], 'color': "#1a4d2e"},
                    {'range': [30, 50], 'color': "#1e3a5f"},
                    {'range': [50, 70], 'color': "#4a3f1a"},
                    {'range': [70, 85], 'color': "#4a1a1a"},
                    {'range': [85, 100], 'color': "#330000"},
                ],
                'threshold': {
                    'line': {'color': color, 'width': 4},
                    'thickness': 0.75,
                    'value': score
                }
            }
        ))
        
        fig.update_layout(
            template=ChartManager.TEMPLATE,
            paper_bgcolor="rgba(0,0,0,0)",
            height=300
        )
        
        return fig
    
    @staticmethod
    def factor_breakdown(assessment: Dict[str, Any]) -> go.Figure:
        """
        Create risk factor breakdown chart
        
        Args:
            assessment: Risk assessment dictionary
            
        Returns:
            Plotly figure
        """
        
        factors = assessment.get('factor_scores', {})
        
        if not factors:
            return None
        
        categories = list(factors.keys())
        values = list(factors.values())
        max_values = [25, 20, 20, 15, 20]  # Max values for each factor
        
        fig = go.Figure()
        
        # Add bars
        fig.add_trace(go.Bar(
            x=categories,
            y=values,
            marker_color=ChartManager.COLORS['cyan'],
            name='Score'
        ))
        
        # Add max value line
        fig.add_trace(go.Scatter(
            x=categories,
            y=max_values,
            mode='lines',
            line=dict(color=ChartManager.COLORS['red'], dash='dash'),
            name='Max Score'
        ))
        
        fig.update_layout(
            template=ChartManager.TEMPLATE,
            title="📊 Skor Faktor Risiko",
            xaxis_title="Faktor",
            yaxis_title="Skor",
            paper_bgcolor="rgba(0,0,0,0)",
            showlegend=True
        )
        
        return fig
    
    @staticmethod
    def anomaly_timeline(df: pd.DataFrame) -> go.Figure:
        """
        Create anomaly detection timeline
        
        Args:
            df: DataFrame with weather data
            
        Returns:
            Plotly figure
        """
        
        # Calculate z-scores for key parameters
        params = ['T_Avg', 'Rain', 'RH_Avg', 'Pressure']
        
        fig = go.Figure()
        
        for param in params:
            if param in df.columns:
                mean = df[param].mean()
                std = df[param].std()
                
                if std > 0:
                    z_scores = (df[param] - mean) / std
                    
                    # Highlight anomalies
                    anomalies = df[z_scores.abs() > 2]
                    
                    if not anomalies.empty:
                        fig.add_trace(go.Scatter(
                            x=anomalies['Tanggal_DT'],
                            y=[param] * len(anomalies),
                            mode='markers',
                            marker=dict(
                                size=12,
                                color=ChartManager.COLORS['red'],
                                symbol='x'
                            ),
                            name=f'{param} (Anomaly)'
                        ))
        
        fig.update_layout(
            template=ChartManager.TEMPLATE,
            title="⚠️ Timeline Anomali",
            xaxis_title="Tanggal",
            yaxis_title="Parameter",
            paper_bgcolor="rgba(0,0,0,0)",
            height=300
        )
        
        return fig


# Export default instance
default_chart_manager = ChartManager()

