"""
Metrics Components
Streamlit metric card components
"""
import streamlit as st
from typing import Optional, Dict, Any


class MetricCard:
    """Creates styled metric cards for the dashboard"""
    
    @staticmethod
    def render(
        label: str,
        value: Any,
        unit: str = "",
        delta: Optional[float] = None,
        help_text: str = "",
        color: str = "cyan"
    ) -> None:
        """
        Render a metric card
        
        Args:
            label: Metric label
            value: Metric value
            unit: Unit of measurement
            delta: Change from previous value
            help_text: Help text tooltip
            color: Accent color (cyan, green, orange, red)
        """
        
        colors = {
            'cyan': '#00f5ff',
            'green': '#00ff9d',
            'orange': '#ff6b35',
            'red': '#ff3366',
            'blue': '#58a6ff',
            'magenta': '#ff00ff',
        }
        
        accent_color = colors.get(color, colors['cyan'])
        
        # Format value
        if isinstance(value, float):
            value_str = f"{value:.1f}"
        else:
            value_str = str(value)
        
        # Create metric with custom styling
        col = st.container()
        
        # Custom HTML for metric
        metric_html = f"""
        <div style="
            background: linear-gradient(135deg, #1a2332 0%, #111827 100%);
            border: 1px solid #30363d;
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            transition: all 0.3s ease;
        ">
            <div style="
                color: {accent_color};
                font-size: 2rem;
                font-weight: bold;
                text-shadow: 0 0 10px {accent_color}50;
            ">
                {value_str} <span style="font-size: 1rem; color: #94a3b8;">{unit}</span>
            </div>
            <div style="
                color: #8b949e;
                font-size: 0.85rem;
                text-transform: uppercase;
                letter-spacing: 1px;
                margin-top: 8px;
            ">
                {label}
            </div>
        </div>
        """
        
        st.markdown(metric_html, unsafe_allow_html=True)
    
    @staticmethod
    def render_row(metrics: Dict[str, Dict[str, Any]]) -> None:
        """
        Render a row of metric cards
        
        Args:
            metrics: Dictionary of metric configurations
        """
        
        cols = st.columns(len(metrics))
        
        for idx, (key, config) in enumerate(metrics.items()):
            with cols[idx]:
                MetricCard.render(
                    label=config.get('label', key),
                    value=config.get('value', 0),
                    unit=config.get('unit', ''),
                    delta=config.get('delta'),
                    help_text=config.get('help', ''),
                    color=config.get('color', 'cyan')
                )


class RiskIndicator:
    """Risk level indicator component"""
    
    @staticmethod
    def render(score: float, level: str) -> None:
        """
        Render risk indicator
        
        Args:
            score: Risk score (0-100)
            level: Risk level name
        """
        
        colors = {
            'NORMAL': '#00ff9d',
            'WATCH': '#58a6ff',
            'WARNING': '#ffa500',
            'ALERT': '#ff6b35',
            'CRITICAL': '#ff3366',
        }
        
        emojis = {
            'NORMAL': '🟢',
            'WATCH': '🔵',
            'WARNING': '🟡',
            'ALERT': '🟠',
            'CRITICAL': '🔴',
        }
        
        color = colors.get(level.upper(), colors['NORMAL'])
        emoji = emojis.get(level.upper(), '🟢')
        
        # Create indicator
        indicator_html = f"""
        <div style="
            background: linear-gradient(135deg, #1a2332 0%, #111827 100%);
            border: 2px solid {color};
            border-radius: 12px;
            padding: 15px 25px;
            text-align: center;
            box-shadow: 0 0 20px {color}50;
            animation: pulse 2s infinite;
        ">
            <div style="
                font-size: 1rem;
                color: {color};
                font-weight: bold;
            ">
                {emoji} Risk Index {score:.0f}/100
            </div>
            <div style="
                font-size: 0.9rem;
                color: #94a3b8;
                margin-top: 5px;
            ">
                {level}
            </div>
        </div>
        
        <style>
            @keyframes pulse {{
                0%, 100% {{ box-shadow: 0 0 10px {color}30; }}
                50% {{ box-shadow: 0 0 25px {color}60; }}
            }}
        </style>
        """
        
        st.markdown(indicator_html, unsafe_allow_html=True)


class Header:
    """Header component with title and branding"""
    
    @staticmethod
    def render(title: str = "BMKG Weather Intelligence", subtitle: str = "") -> None:
        """
        Render dashboard header
        
        Args:
            title: Main title
            subtitle: Subtitle text
        """
        
        header_html = f"""
        <div style="
            text-align: center;
            padding: 20px 0;
            margin-bottom: 30px;
        ">
            <h1 style="
                font-size: 2.5rem;
                background: linear-gradient(90deg, #00f5ff 0%, #ff00ff 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin: 0;
            ">
                {title}
            </h1>
            {f'<p style="color: #94a3b8; font-size: 1.1rem; margin-top: 10px;">{subtitle}</p>' if subtitle else ''}
        </div>
        """
        
        st.markdown(header_html, unsafe_allow_html=True)


class Sidebar:
    """Sidebar navigation component"""
    
    @staticmethod
    def render_station_selector(stations: list, key: str = "station") -> str:
        """
        Render station selector in sidebar
        
        Args:
            stations: List of station names
            key: Streamlit widget key
            
        Returns:
            Selected station name
        """
        
        return st.selectbox(
            "📍 Pilih Stasiun",
            stations,
            key=key
        )
    
    @staticmethod
    def render_filters(
        years: list,
        months: list = None,
        key_prefix: str = ""
    ) -> Dict[str, Any]:
        """
        Render filter controls
        
        Args:
            years: List of available years
            months: List of available months
            key_prefix: Prefix for widget keys
            
        Returns:
            Dictionary of filter values
        """
        
        filters = {}
        
        # Year selector
        filters['year'] = st.selectbox(
            "📅 Tahun",
            years,
            key=f"{key_prefix}_year"
        )
        
        # Month selector
        if months:
            filters['month'] = st.selectbox(
                "📆 Bulan",
                ["Semua"] + months,
                key=f"{key_prefix}_month"
            )
        
        # Date range option
        filters['use_range'] = st.checkbox(
            "📅 Gunakan Rentang Tanggal",
            key=f"{key_prefix}_use_range"
        )
        
        return filters

