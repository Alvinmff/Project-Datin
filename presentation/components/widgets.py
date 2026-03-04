"""
Widget Components
Custom Streamlit widgets and interactive components
"""
import streamlit as st
import streamlit.components.v1 as components
from typing import Optional


class CopyButton:
    """Copy to clipboard button component"""
    
    @staticmethod
    def render(text: str, label: str = "Copy", key: Optional[str] = None) -> None:
        """
        Render copy button
        
        Args:
            text: Text to copy
            label: Button label
            key: Optional unique key
        """
        
        # Generate unique ID
        button_id = f"copy_{hash(text)}"
        
        # Process text - replace special chars for JS string
        safe_text = text.replace("\\", "\\\\").replace("'", "\\'").replace("\n", "\\n")
        
        # Build HTML
        html = f"""
        <button id="{button_id}" onclick="copyText('{safe_text}')"
            style="background-color:#1a1a1a;color:white;border:none;
                   padding:8px 16px;border-radius:6px;cursor:pointer;
                   font-size:0.9rem;transition:all 0.2s;">
            {label}
        </button>
        <script>
        function copyText(txt) {{
            navigator.clipboard.writeText(txt).then(function() {{
                var btn = document.getElementById('{button_id}');
                btn.innerText = 'Copied!';
                btn.style.backgroundColor = '#00ff9d';
                setTimeout(function() {{
                    btn.innerText = '{label}';
                    btn.style.backgroundColor = '#1a1a1a';
                }}, 2000);
            }});
        }}
        </script>
        """
        
        components.html(html, height=45)


class RiskGauge:
    """Holographic risk gauge component"""
    
    @staticmethod
    def render(score: float, level: str, station: str = "") -> None:
        """Render holographic risk gauge"""
        
        colors = {
            'NORMAL': '#00ff9d',
            'WATCH': '#58a6ff',
            'WARNING': '#ffa500',
            'ALERT': '#ff6b35',
            'CRITICAL': '#ff3366',
        }
        
        emojis = {
            'NORMAL': '🟢', 'WATCH': '🔵', 'WARNING': '🟡',
            'ALERT': '🟠', 'CRITICAL': '🔴',
        }
        
        color = colors.get(level.upper(), colors['NORMAL'])
        emoji = emojis.get(level.upper(), '🟢')
        rotation = (score / 100) * 180 - 90
        
        # Station div
        station_div = f'<div style="color:#64748b;font-size:0.9rem;margin-top:10px;">{station}</div>' if station else ''
        
        gauge_html = f"""
        <div style="text-align:center;padding:20px;background:linear-gradient(135deg,#1a2332,#111827);
                    border:1px solid {color};border-radius:16px;box-shadow:0 0 30px {color}30;">
            <div style="position:relative;width:200px;height:100px;margin:0 auto;overflow:hidden;">
                <div style="position:absolute;width:200px;height:200px;border-radius:50%;
                            border:8px solid #30363d;border-bottom-color:transparent;
                            border-left-color:transparent;transform:rotate(45deg);top:0;"></div>
                <div style="position:absolute;width:200px;height:200px;border-radius:50%;
                            border:8px solid {color};border-bottom-color:transparent;
                            border-left-color:transparent;transform:rotate(45deg);top:0;
                            clip-path:polygon(0 0,{50+(score/2)}% 0,100% 100%,0 100%);
                            box-shadow:0 0 20px {color};"></div>
                <div style="position:absolute;width:4px;height:80px;background:{color};bottom:0;
                            left:50%;transform-origin:bottom center;
                            transform:translateX(-50%) rotate({rotation}deg);
                            border-radius:2px;box-shadow:0 0 10px {color};"></div>
                <div style="position:absolute;width:16px;height:16px;background:{color};border-radius:50%;
                            bottom:-8px;left:50%;transform:translateX(-50%);box-shadow:0 0 15px {color};"></div>
            </div>
            <div style="margin-top:15px;font-size:2.5rem;font-weight:bold;color:{color};text-shadow:0 0 20px {color};">
                {score:.0f}<span style="font-size:1rem;color:#94a3b8;">/100</span>
            </div>
            <div style="font-size:1.2rem;color:{color};margin-top:5px;">{emoji} {level}</div>
            {station_div}
        </div>
        """
        
        st.markdown(gauge_html, unsafe_allow_html=True)


class DataTable:
    """Custom data table component"""
    
    @staticmethod
    def render(df, page_size: int = 50) -> None:
        """Render data table with pagination"""
        
        total_rows = len(df)
        total_pages = (total_rows // page_size) + (1 if total_rows % page_size > 0 else 0)
        
        if total_pages > 1:
            page = st.number_input("Halaman", min_value=1, max_value=total_pages, value=1)
            start_idx = (page - 1) * page_size
            end_idx = min(start_idx + page_size, total_rows)
            st.dataframe(df.iloc[start_idx:end_idx], use_container_width=True)
            st.caption(f"Menampilkan {start_idx+1}-{end_idx} dari {total_rows} baris")
        else:
            st.dataframe(df, use_container_width=True)


class AlertBox:
    """Alert message box component"""
    
    @staticmethod
    def render(message: str, alert_type: str = "info") -> None:
        """Render alert box"""
        
        colors = {'info': '#58a6ff', 'success': '#00ff9d', 'warning': '#ffa500', 'error': '#ff3366'}
        icons = {'info': 'ℹ️', 'success': '✅', 'warning': '⚠️', 'error': '❌'}
        
        color = colors.get(alert_type, colors['info'])
        icon = icons.get(alert_type, icons['info'])
        
        alert_html = f"""
        <div style="padding:15px 20px;background:linear-gradient(135deg,#1a2332,#111827);
                    border-left:4px solid {color};border-radius:6px;margin:10px 0;
                    display:flex;align-items:center;gap:12px;">
            <span style="font-size:1.5rem;">{icon}</span>
            <span style="color:{color};">{message}</span>
        </div>
        """
        
        st.markdown(alert_html, unsafe_allow_html=True)


class LoadingSpinner:
    """Loading spinner component"""
    
    @staticmethod
    def render(message: str = "Loading...") -> None:
        """Render loading spinner"""
        
        spinner_html = f"""
        <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;padding:40px;">
            <div style="width:50px;height:50px;border:4px solid #30363d;border-top:4px solid #00f5ff;
                        border-radius:50%;animation:spin 1s linear infinite;"></div>
            <p style="color:#94a3b8;margin-top:15px;">{message}</p>
        </div>
        <style>@keyframes spin {{0% {{transform:rotate(0deg);}} 100% {{transform:rotate(360deg);}}}}</style>
        """
        
        st.markdown(spinner_html, unsafe_allow_html=True)


class ProgressBar:
    """Custom progress bar component"""
    
    @staticmethod
    def render(progress: float, label: str = "", color: str = "cyan") -> None:
        """Render progress bar"""
        
        colors = {'cyan': '#00f5ff', 'green': '#00ff9d', 'orange': '#ff6b35', 'red': '#ff3366'}
        bar_color = colors.get(color, colors['cyan'])
        percentage = int(progress * 100)
        
        label_div = f'<div style="color:#94a3b8;margin-bottom:5px;">{label}</div>' if label else ''
        
        progress_html = f"""
        <div style="margin:10px 0;">
            {label_div}
            <div style="width:100%;height:8px;background:#30363d;border-radius:4px;overflow:hidden;">
                <div style="width:{percentage}%;height:100%;background:{bar_color};border-radius:4px;
                            box-shadow:0 0 10px {bar_color};transition:width 0.5s;"></div>
            </div>
        </div>
        """
        
        st.markdown(progress_html, unsafe_allow_html=True)

