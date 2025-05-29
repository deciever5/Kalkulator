"""
Advanced 3D Visualization System for Container Modifications
Creates realistic 3D models showing all modifications, openings, and structural elements
"""

import plotly.graph_objects as go
import numpy as np
from typing import Dict, List, Any, Tuple
import streamlit as st

class Advanced3DVisualizer:
    """Advanced 3D visualization system for container modifications"""
    
    def __init__(self):
        self.colors = {
            'container_frame': '#2E4057',
            'walls': '#4A90A4',
            'windows': '#87CEEB',
            'doors': '#8B4513',
            'insulation': '#FFE4B5',
            'electrical': '#FFD700',
            'plumbing': '#4169E1',
            'hvac': '#32CD32',
            'reinforcement': '#696969'
        }
    
    def create_3d_model(self, config: Dict[str, Any]) -> go.Figure:
        """Create comprehensive 3D model of container with all modifications"""
        
        # Get container dimensions
        container_specs = self._get_container_specs(config.get('base_type', '20ft Standard'))
        length, width, height = container_specs['length'], container_specs['width'], container_specs['height']
        
        # Initialize figure
        fig = go.Figure()
        
        # Add container frame structure
        self._add_container_frame(fig, length, width, height)
        
        # Add walls with transparency to show internal modifications
        self._add_container_walls(fig, length, width, height, config)
        
        # Add modifications
        modifications = config.get('modifications', {})
        
        # Add windows
        if modifications.get('windows', 0) > 0:
            self._add_windows(fig, length, width, height, modifications['windows'])
        
        # Add doors
        if modifications.get('doors', 0) > 1:
            self._add_additional_doors(fig, length, width, height, modifications['doors'] - 1)
        
        # Add electrical systems
        if modifications.get('electrical', False):
            self._add_electrical_system(fig, length, width, height)
        
        # Add plumbing
        if modifications.get('plumbing', False):
            self._add_plumbing_system(fig, length, width, height)
        
        # Add HVAC system
        if modifications.get('hvac', False):
            self._add_hvac_system(fig, length, width, height)
        
        # Add insulation visualization
        if modifications.get('insulation', False):
            self._add_insulation_layers(fig, length, width, height)
        
        # Add structural reinforcements
        if modifications.get('reinforcement', False):
            self._add_structural_reinforcements(fig, length, width, height)
        
        # Add interior layout based on use case
        self._add_interior_layout(fig, length, width, height, config.get('use_case', 'Office Space'))
        
        # Configure layout
        self._configure_3d_layout(fig, length, width, height, config)
        
        return fig
    
    def _get_container_specs(self, container_type: str) -> Dict[str, float]:
        """Get container specifications in meters"""
        specs = {
            '20ft Standard': {'length': 6.058, 'width': 2.438, 'height': 2.591},
            '40ft Standard': {'length': 12.192, 'width': 2.438, 'height': 2.591},
            '40ft High Cube': {'length': 12.192, 'width': 2.438, 'height': 2.896},
            '20ft Refrigerated': {'length': 6.058, 'width': 2.438, 'height': 2.591}
        }
        return specs.get(container_type, specs['20ft Standard'])
    
    def _add_container_frame(self, fig: go.Figure, length: float, width: float, height: float):
        """Add container structural frame"""
        
        # Corner posts (8 vertical posts)
        corner_positions = [
            (0, 0), (length, 0), (length, width), (0, width)
        ]
        
        for x, y in corner_positions:
            # Vertical corner posts
            fig.add_trace(go.Scatter3d(
                x=[x, x], y=[y, y], z=[0, height],
                mode='lines',
                line=dict(color=self.colors['container_frame'], width=8),
                name='Frame',
                showlegend=False
            ))
        
        # Horizontal frame rails
        # Bottom rails
        frame_lines = [
            ([0, length], [0, 0], [0, 0]),  # Front bottom
            ([0, length], [width, width], [0, 0]),  # Back bottom
            ([0, 0], [0, width], [0, 0]),  # Left bottom
            ([length, length], [0, width], [0, 0]),  # Right bottom
            # Top rails
            ([0, length], [0, 0], [height, height]),  # Front top
            ([0, length], [width, width], [height, height]),  # Back top
            ([0, 0], [0, width], [height, height]),  # Left top
            ([length, length], [0, width], [height, height])  # Right top
        ]
        
        for x_coords, y_coords, z_coords in frame_lines:
            fig.add_trace(go.Scatter3d(
                x=x_coords, y=y_coords, z=z_coords,
                mode='lines',
                line=dict(color=self.colors['container_frame'], width=6),
                name='Frame',
                showlegend=False
            ))
    
    def _add_container_walls(self, fig: go.Figure, length: float, width: float, height: float, config: Dict):
        """Add container walls with transparency"""
        
        opacity = 0.3 if config.get('modifications') else 0.6
        
        # Define wall surfaces
        walls = [
            # Front wall (x=0)
            dict(x=[0, 0, 0, 0], y=[0, width, width, 0], z=[0, 0, height, height]),
            # Back wall (x=length)
            dict(x=[length, length, length, length], y=[0, width, width, 0], z=[0, 0, height, height]),
            # Left wall (y=0)
            dict(x=[0, length, length, 0], y=[0, 0, 0, 0], z=[0, 0, height, height]),
            # Right wall (y=width)
            dict(x=[0, length, length, 0], y=[width, width, width, width], z=[0, 0, height, height]),
            # Floor
            dict(x=[0, length, length, 0], y=[0, 0, width, width], z=[0, 0, 0, 0]),
            # Ceiling
            dict(x=[0, length, length, 0], y=[0, 0, width, width], z=[height, height, height, height])
        ]
        
        for i, wall in enumerate(walls):
            fig.add_trace(go.Mesh3d(
                x=wall['x'], y=wall['y'], z=wall['z'],
                i=[0, 0], j=[1, 2], k=[2, 3],
                color=self.colors['walls'],
                opacity=opacity,
                name='Container Walls',
                showlegend=i == 0
            ))
    
    def _add_windows(self, fig: go.Figure, length: float, width: float, height: float, num_windows: int):
        """Add window openings to container walls"""
        
        window_width = 1.2
        window_height = 1.0
        window_z_bottom = height * 0.3
        window_z_top = window_z_bottom + window_height
        
        # Distribute windows along the long walls
        windows_per_side = num_windows // 2
        
        for side in [0, width]:  # Both long walls
            for i in range(windows_per_side):
                x_pos = length * 0.2 + (i * (length * 0.6 / max(1, windows_per_side - 1)))
                
                # Window frame
                window_corners = [
                    [x_pos - window_width/2, x_pos + window_width/2, x_pos + window_width/2, x_pos - window_width/2],
                    [side, side, side, side],
                    [window_z_bottom, window_z_bottom, window_z_top, window_z_top]
                ]
                
                fig.add_trace(go.Mesh3d(
                    x=window_corners[0], y=window_corners[1], z=window_corners[2],
                    i=[0, 0], j=[1, 2], k=[2, 3],
                    color=self.colors['windows'],
                    opacity=0.7,
                    name='Windows',
                    showlegend=i == 0 and side == 0
                ))
    
    def _add_additional_doors(self, fig: go.Figure, length: float, width: float, height: float, num_doors: int):
        """Add additional door openings"""
        
        door_width = 0.9
        door_height = 2.0
        
        for i in range(num_doors):
            # Position doors along the front wall
            x_pos = length * 0.3 + (i * length * 0.4)
            
            door_corners = [
                [x_pos - door_width/2, x_pos + door_width/2, x_pos + door_width/2, x_pos - door_width/2],
                [0, 0, 0, 0],
                [0, 0, door_height, door_height]
            ]
            
            fig.add_trace(go.Mesh3d(
                x=door_corners[0], y=door_corners[1], z=door_corners[2],
                i=[0, 0], j=[1, 2], k=[2, 3],
                color=self.colors['doors'],
                opacity=0.8,
                name='Additional Doors',
                showlegend=i == 0
            ))
    
    def _add_electrical_system(self, fig: go.Figure, length: float, width: float, height: float):
        """Add electrical conduits and outlets visualization"""
        
        # Main electrical conduit along ceiling
        fig.add_trace(go.Scatter3d(
            x=[0.2, length - 0.2], y=[width/2, width/2], z=[height - 0.1, height - 0.1],
            mode='lines',
            line=dict(color=self.colors['electrical'], width=10),
            name='Electrical Conduit',
            showlegend=True
        ))
        
        # Electrical outlets along walls
        outlet_positions = [
            (length * 0.25, 0.05, height * 0.2),
            (length * 0.75, 0.05, height * 0.2),
            (length * 0.25, width - 0.05, height * 0.2),
            (length * 0.75, width - 0.05, height * 0.2)
        ]
        
        for x, y, z in outlet_positions:
            fig.add_trace(go.Scatter3d(
                x=[x], y=[y], z=[z],
                mode='markers',
                marker=dict(color=self.colors['electrical'], size=8, symbol='square'),
                name='Electrical Outlets',
                showlegend=False
            ))
    
    def _add_plumbing_system(self, fig: go.Figure, length: float, width: float, height: float):
        """Add plumbing lines visualization"""
        
        # Main water line
        fig.add_trace(go.Scatter3d(
            x=[0.1, length - 0.1], y=[0.1, 0.1], z=[0.1, 0.1],
            mode='lines',
            line=dict(color=self.colors['plumbing'], width=8),
            name='Water Supply',
            showlegend=True
        ))
        
        # Drain line
        fig.add_trace(go.Scatter3d(
            x=[0.1, length - 0.1], y=[width - 0.1, width - 0.1], z=[0.05, 0.05],
            mode='lines',
            line=dict(color='#191970', width=8),
            name='Drainage',
            showlegend=True
        ))
    
    def _add_hvac_system(self, fig: go.Figure, length: float, width: float, height: float):
        """Add HVAC system visualization"""
        
        # Air conditioning unit
        ac_x, ac_y = length * 0.8, width * 0.1
        ac_size = 0.6
        
        # AC unit box
        ac_corners = [
            [ac_x, ac_x + ac_size, ac_x + ac_size, ac_x],
            [ac_y, ac_y, ac_y + ac_size, ac_y + ac_size],
            [height - 0.3, height - 0.3, height - 0.3, height - 0.3]
        ]
        
        fig.add_trace(go.Mesh3d(
            x=ac_corners[0] + ac_corners[0],
            y=ac_corners[1] + ac_corners[1],
            z=ac_corners[2] + [z + 0.3 for z in ac_corners[2]],
            i=[0, 0, 0, 0, 4, 4, 6, 6, 0, 2],
            j=[1, 2, 4, 7, 5, 6, 7, 4, 3, 6],
            k=[2, 3, 5, 3, 6, 7, 3, 7, 7, 3],
            color=self.colors['hvac'],
            opacity=0.8,
            name='HVAC System',
            showlegend=True
        ))
        
        # Ductwork
        fig.add_trace(go.Scatter3d(
            x=[ac_x + ac_size/2, length/2], 
            y=[ac_y + ac_size/2, width/2], 
            z=[height - 0.15, height - 0.15],
            mode='lines',
            line=dict(color=self.colors['hvac'], width=12),
            name='Air Ducts',
            showlegend=False
        ))
    
    def _add_insulation_layers(self, fig: go.Figure, length: float, width: float, height: float):
        """Add insulation layer visualization"""
        
        insulation_thickness = 0.05
        
        # Insulation on walls (slightly inset)
        insulation_walls = [
            # Left wall insulation
            dict(x=[insulation_thickness, insulation_thickness, insulation_thickness, insulation_thickness], 
                 y=[0, width, width, 0], 
                 z=[0, 0, height, height]),
            # Right wall insulation
            dict(x=[length - insulation_thickness, length - insulation_thickness, length - insulation_thickness, length - insulation_thickness], 
                 y=[0, width, width, 0], 
                 z=[0, 0, height, height])
        ]
        
        for i, wall in enumerate(insulation_walls):
            fig.add_trace(go.Mesh3d(
                x=wall['x'], y=wall['y'], z=wall['z'],
                i=[0, 0], j=[1, 2], k=[2, 3],
                color=self.colors['insulation'],
                opacity=0.4,
                name='Insulation',
                showlegend=i == 0
            ))
    
    def _add_structural_reinforcements(self, fig: go.Figure, length: float, width: float, height: float):
        """Add structural reinforcement visualization"""
        
        # Cross beams for reinforcement
        reinforcement_positions = [
            ([0, length], [width/3, width/3], [height/2, height/2]),
            ([0, length], [2*width/3, 2*width/3], [height/2, height/2]),
            ([length/3, length/3], [0, width], [height/2, height/2]),
            ([2*length/3, 2*length/3], [0, width], [height/2, height/2])
        ]
        
        for i, (x_coords, y_coords, z_coords) in enumerate(reinforcement_positions):
            fig.add_trace(go.Scatter3d(
                x=x_coords, y=y_coords, z=z_coords,
                mode='lines',
                line=dict(color=self.colors['reinforcement'], width=8),
                name='Reinforcement Beams',
                showlegend=i == 0
            ))
    
    def _add_interior_layout(self, fig: go.Figure, length: float, width: float, height: float, use_case: str):
        """Add interior layout based on use case"""
        
        if use_case == 'Office Space':
            self._add_office_layout(fig, length, width, height)
        elif use_case == 'Residential':
            self._add_residential_layout(fig, length, width, height)
        elif use_case == 'Workshop':
            self._add_workshop_layout(fig, length, width, height)
        elif use_case == 'Medical':
            self._add_medical_layout(fig, length, width, height)
    
    def _add_office_layout(self, fig: go.Figure, length: float, width: float, height: float):
        """Add office furniture and layout"""
        
        # Desk
        desk_x, desk_y = length * 0.3, width * 0.3
        desk_w, desk_d, desk_h = 1.5, 0.8, 0.75
        
        # Desk surface
        fig.add_trace(go.Mesh3d(
            x=[desk_x, desk_x + desk_w, desk_x + desk_w, desk_x],
            y=[desk_y, desk_y, desk_y + desk_d, desk_y + desk_d],
            z=[desk_h, desk_h, desk_h, desk_h],
            i=[0], j=[1], k=[2],
            color='#8B4513',
            opacity=0.7,
            name='Office Furniture',
            showlegend=True
        ))
        
        # Chairs (represented as points)
        chair_positions = [
            (desk_x + desk_w/2, desk_y - 0.3, 0.45),
            (length * 0.7, width * 0.7, 0.45)
        ]
        
        for x, y, z in chair_positions:
            fig.add_trace(go.Scatter3d(
                x=[x], y=[y], z=[z],
                mode='markers',
                marker=dict(color='#654321', size=10),
                name='Chairs',
                showlegend=False
            ))
    
    def _add_residential_layout(self, fig: go.Figure, length: float, width: float, height: float):
        """Add residential furniture"""
        
        # Bed
        bed_x, bed_y = length * 0.1, width * 0.1
        bed_w, bed_d, bed_h = 2.0, 1.5, 0.6
        
        fig.add_trace(go.Mesh3d(
            x=[bed_x, bed_x + bed_w, bed_x + bed_w, bed_x],
            y=[bed_y, bed_y, bed_y + bed_d, bed_y + bed_d],
            z=[bed_h, bed_h, bed_h, bed_h],
            i=[0], j=[1], k=[2],
            color='#4682B4',
            opacity=0.7,
            name='Furniture',
            showlegend=True
        ))
    
    def _add_workshop_layout(self, fig: go.Figure, length: float, width: float, height: float):
        """Add workshop equipment"""
        
        # Workbench
        bench_x, bench_y = length * 0.1, width * 0.8
        bench_w, bench_d, bench_h = length * 0.8, 0.6, 0.9
        
        fig.add_trace(go.Mesh3d(
            x=[bench_x, bench_x + bench_w, bench_x + bench_w, bench_x],
            y=[bench_y, bench_y, bench_y + bench_d, bench_y + bench_d],
            z=[bench_h, bench_h, bench_h, bench_h],
            i=[0], j=[1], k=[2],
            color='#696969',
            opacity=0.8,
            name='Workshop Equipment',
            showlegend=True
        ))
    
    def _add_medical_layout(self, fig: go.Figure, length: float, width: float, height: float):
        """Add medical equipment"""
        
        # Examination table
        table_x, table_y = length * 0.4, width * 0.3
        table_w, table_d, table_h = 1.8, 0.8, 0.8
        
        fig.add_trace(go.Mesh3d(
            x=[table_x, table_x + table_w, table_x + table_w, table_x],
            y=[table_y, table_y, table_y + table_d, table_y + table_d],
            z=[table_h, table_h, table_h, table_h],
            i=[0], j=[1], k=[2],
            color='#FFFFFF',
            opacity=0.9,
            name='Medical Equipment',
            showlegend=True
        ))
    
    def _configure_3d_layout(self, fig: go.Figure, length: float, width: float, height: float, config: Dict):
        """Configure 3D plot layout and camera"""
        
        container_type = config.get('base_type', '20ft Standard')
        use_case = config.get('use_case', 'Office Space')
        
        fig.update_layout(
            title=f"3D Model: {container_type} - {use_case}",
            scene=dict(
                xaxis=dict(title='Length (m)', range=[0, length + 1]),
                yaxis=dict(title='Width (m)', range=[0, width + 1]),
                zaxis=dict(title='Height (m)', range=[0, height + 1]),
                camera=dict(
                    eye=dict(x=1.5, y=1.5, z=1.2),
                    center=dict(x=0, y=0, z=0.2),
                    up=dict(x=0, y=0, z=1)
                ),
                aspectmode='data',
                bgcolor='rgba(240, 248, 255, 0.1)'
            ),
            width=800,
            height=600,
            margin=dict(l=0, r=0, t=50, b=0),
            showlegend=True,
            legend=dict(
                x=0.02,
                y=0.98,
                bgcolor='rgba(255, 255, 255, 0.8)'
            )
        )
        
        return fig

    def create_modification_comparison(self, base_config: Dict, modified_config: Dict) -> go.Figure:
        """Create side-by-side comparison of before/after modifications"""
        
        fig = go.Figure()
        
        # Create base model (left side)
        base_model = self.create_3d_model(base_config)
        
        # Create modified model (right side) - offset by container length + gap
        container_specs = self._get_container_specs(modified_config.get('base_type', '20ft Standard'))
        offset = container_specs['length'] + 2
        
        modified_model = self.create_3d_model(modified_config)
        
        # Add both models to the same figure with offset
        for trace in base_model.data:
            fig.add_trace(trace)
        
        for trace in modified_model.data:
            # Offset the x coordinates for comparison view
            if hasattr(trace, 'x') and trace.x is not None:
                # Create new trace with offset coordinates
                new_trace = go.Scatter3d(
                    x=[x + offset for x in trace.x] if trace.x else None,
                    y=trace.y,
                    z=trace.z,
                    mode=trace.mode,
                    line=trace.line if hasattr(trace, 'line') else None,
                    marker=trace.marker if hasattr(trace, 'marker') else None,
                    name=trace.name,
                    showlegend=trace.showlegend
                )
                fig.add_trace(new_trace)
            else:
                fig.add_trace(trace)
        
        # Update layout for comparison view
        fig.update_layout(
            title="Container Modification Comparison: Before vs After",
            scene=dict(
                xaxis=dict(title='Length (m)', range=[0, offset + container_specs['length'] + 1]),
                yaxis=dict(title='Width (m)', range=[0, container_specs['width'] + 1]),
                zaxis=dict(title='Height (m)', range=[0, container_specs['height'] + 1]),
                camera=dict(
                    eye=dict(x=1.2, y=1.2, z=1.0),
                    center=dict(x=offset/2, y=0, z=0.2)
                ),
                aspectmode='data'
            ),
            width=1200,
            height=600
        )
        
        return fig