from pptx import Presentation as PPTXPresentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from datetime import datetime
import logging
from typing import Optional, List
import os
import glob
from ..models.presentation import Presentation, Slide

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PresentationGenerator:
    def __init__(self):
        self.prs = PPTXPresentation()
        # Set 16:9 aspect ratio
        self.prs.slide_width = Inches(13.33)
        self.prs.slide_height = Inches(7.5)
        
        # Create presentations directory if it doesn't exist
        self.presentations_dir = os.path.join(os.getcwd(), 'presentations')
        os.makedirs(self.presentations_dir, exist_ok=True)
        
        # Clean up old presentations
        self._cleanup_old_presentations()

    def _cleanup_old_presentations(self):
        """Clean up old presentation files."""
        try:
            # Clean up files in root directory
            root_files = glob.glob("presentation_*.pptx")
            for file in root_files:
                try:
                    os.remove(file)
                    logger.info(f"Cleaned up old presentation: {file}")
                except Exception as e:
                    logger.error(f"Error cleaning up file {file}: {e}")
            
            # Clean up files in presentations directory
            pres_files = glob.glob(os.path.join(self.presentations_dir, "presentation_*.pptx"))
            # Keep only the 20 most recent files
            if len(pres_files) > 20:
                pres_files.sort(key=os.path.getctime)
                for file in pres_files[:-20]:
                    try:
                        os.remove(file)
                        logger.info(f"Cleaned up old presentation: {file}")
                    except Exception as e:
                        logger.error(f"Error cleaning up file {file}: {e}")
        except Exception as e:
            logger.error(f"Error during presentation cleanup: {e}")

    def _add_background_style(self, slide):
        """Add modern background style to slide."""
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = RGBColor(1, 22, 64)  # Dark blue background

        # Add decorative shapes - positioned better for visual appeal
        shape_width = Inches(5)
        shape_height = Inches(5)
        
        # Add network-like decorative elements
        positions = [
            (-2, -1, 15),  # Top left
            (11, -2, -15),  # Top right
            (9, 5, 30),    # Bottom right
        ]
        
        for x, y, rotation in positions:
            shape = slide.shapes.add_shape(
                MSO_SHAPE.ROUNDED_RECTANGLE,
                Inches(x),
                Inches(y),
                shape_width,
                shape_height
            )
            shape_fill = shape.fill
            shape_fill.solid()
            shape_fill.fore_color.rgb = RGBColor(0, 114, 198)
            shape_fill.transparency = 0.85
            shape.rotation = rotation

    def _create_title_slide(self, slide: Slide) -> None:
        """Create a title slide with modern styling."""
        pptx_slide = self.prs.slides.add_slide(self.prs.slide_layouts[0])
        self._add_background_style(pptx_slide)
        
        try:
            # Center the title and subtitle in the middle of the slide
            title_left = Inches(1.5)
            title_top = Inches(2.0)  # Moved up slightly
            title_width = Inches(10.33)
            title_height = Inches(1.5)

            # Add title shape
            title_shape = pptx_slide.shapes.add_textbox(
                title_left, title_top, title_width, title_height
            )
            title_frame = title_shape.text_frame
            title_frame.clear()
            title_frame.word_wrap = True
            title_frame.vertical_anchor = MSO_ANCHOR.MIDDLE  # Center vertically
            
            # Style title
            p = title_frame.add_paragraph()
            p.text = slide.title
            p.alignment = PP_ALIGN.CENTER
            p.font.size = Pt(60)
            p.font.bold = True
            p.font.color.rgb = RGBColor(255, 255, 255)
            p.font.name = 'Segoe UI Light'
            
            # Add subtitle with better spacing
            if slide.content:
                subtitle_top = title_top + Inches(2.0)  # Increased spacing
                subtitle_height = Inches(1.2)  # Increased height
                subtitle_shape = pptx_slide.shapes.add_textbox(
                    title_left, subtitle_top, title_width, subtitle_height
                )
                subtitle_frame = subtitle_shape.text_frame
                subtitle_frame.clear()
                subtitle_frame.word_wrap = True
                subtitle_frame.vertical_anchor = MSO_ANCHOR.MIDDLE  # Center vertically
                
                p = subtitle_frame.add_paragraph()
                content_text = "\n".join(slide.content) if isinstance(slide.content, list) else str(slide.content)
                p.text = content_text
                p.alignment = PP_ALIGN.CENTER
                p.font.size = Pt(32)
                p.font.color.rgb = RGBColor(0, 178, 148)
                p.font.name = 'Segoe UI'
                p.space_after = Pt(32)  # Increased spacing

            # Add decorative line with adjusted position
            line = pptx_slide.shapes.add_shape(
                MSO_SHAPE.RECTANGLE,
                Inches(4),
                subtitle_top + Inches(1.5),  # Adjusted position
                Inches(5.33),
                Inches(0.05)
            )
            line_fill = line.fill
            line_fill.solid()
            line_fill.fore_color.rgb = RGBColor(0, 178, 148)
            line.line.fill.background()

        except Exception as e:
            logger.error(f"Error creating title slide: {e}")

    def _create_content_slide(self, slide: Slide) -> None:
        """Create a content slide with modern styling."""
        pptx_slide = self.prs.slides.add_slide(self.prs.slide_layouts[1])
        self._add_background_style(pptx_slide)
        
        try:
            # Define content area dimensions with better margins
            left_margin = Inches(1.8)  # Increased margin
            content_width = Inches(9.73)  # Adjusted for new margin
            
            # Add title with better positioning
            title_top = Inches(0.8)
            title_height = Inches(1.2)  # Increased height
            title_shape = pptx_slide.shapes.add_textbox(
                left_margin, title_top, content_width, title_height
            )
            title_frame = title_shape.text_frame
            title_frame.clear()
            title_frame.vertical_anchor = MSO_ANCHOR.MIDDLE  # Center vertically
            
            p = title_frame.add_paragraph()
            p.text = slide.title
            p.alignment = PP_ALIGN.LEFT
            p.font.size = Pt(44)
            p.font.bold = True
            p.font.color.rgb = RGBColor(255, 255, 255)
            p.font.name = 'Segoe UI'
            p.space_after = Pt(32)  # Increased spacing

            # Add content with better spacing
            if slide.content:
                content_top = title_top + Inches(1.4)  # Adjusted spacing
                content_height = Inches(5.0)
                content_shape = pptx_slide.shapes.add_textbox(
                    left_margin + Inches(0.5), content_top, 
                    content_width - Inches(1.0), content_height
                )
                text_frame = content_shape.text_frame
                text_frame.word_wrap = True
                text_frame.vertical_anchor = MSO_ANCHOR.TOP  # Align to top

                for point in slide.content:
                    p = text_frame.add_paragraph()
                    p.text = str(point)
                    p.font.size = Pt(28)
                    p.font.color.rgb = RGBColor(255, 255, 255)
                    p.font.name = 'Segoe UI'
                    p.level = 0
                    p.space_after = Pt(20)  # Add spacing between points

            # Add accent shape
            accent = pptx_slide.shapes.add_shape(
                MSO_SHAPE.RECTANGLE,
                Inches(0.8),
                Inches(0.8),
                Inches(0.1),
                Inches(5.9)
            )
            accent_fill = accent.fill
            accent_fill.solid()
            accent_fill.fore_color.rgb = RGBColor(0, 178, 148)
            accent.line.fill.background()

        except Exception as e:
            logger.error(f"Error creating content slide: {e}")

    def _create_table_slide(self, slide: Slide) -> None:
        """Create a slide with a table."""
        pptx_slide = self.prs.slides.add_slide(self.prs.slide_layouts[5])  # Using blank layout
        self._add_background_style(pptx_slide)
        
        try:
            # Add title
            title_left = Inches(1.5)
            title_top = Inches(0.8)
            title_width = Inches(10.33)
            title_height = Inches(1.0)
            
            title_shape = pptx_slide.shapes.add_textbox(
                title_left, title_top, title_width, title_height
            )
            title_frame = title_shape.text_frame
            title_frame.clear()
            title_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
            
            p = title_frame.add_paragraph()
            p.text = slide.title
            p.alignment = PP_ALIGN.LEFT
            p.font.size = Pt(44)
            p.font.bold = True
            p.font.color.rgb = RGBColor(255, 255, 255)
            p.font.name = 'Segoe UI'
            p.space_after = Pt(24)

            # Add table if table_data exists
            if hasattr(slide, 'table_data') and slide.table_data:
                headers = slide.table_data.get('headers', [])
                rows = slide.table_data.get('rows', [])
                
                if headers and rows:
                    # Calculate table dimensions
                    num_rows = len(rows) + 1  # +1 for header
                    num_cols = len(headers)
                    
                    # Create table with better positioning
                    table_left = Inches(1.5)
                    table_top = Inches(2.0)
                    table_width = Inches(10.33)
                    row_height = Inches(0.6)
                    table_height = row_height * num_rows
                    
                    table = pptx_slide.shapes.add_table(
                        num_rows, num_cols,
                        table_left, table_top,
                        table_width, table_height
                    ).table

                    # Set column widths evenly
                    col_width = table_width / num_cols
                    for col in table.columns:
                        col.width = col_width
                    
                    # Style headers
                    for i, header in enumerate(headers):
                        cell = table.cell(0, i)
                        cell.text = str(header)
                        paragraph = cell.text_frame.paragraphs[0]
                        paragraph.font.size = Pt(24)
                        paragraph.font.bold = True
                        paragraph.font.color.rgb = RGBColor(255, 255, 255)
                        paragraph.font.name = 'Segoe UI'
                        paragraph.alignment = PP_ALIGN.CENTER
                        cell.fill.solid()
                        cell.fill.fore_color.rgb = RGBColor(0, 114, 198)
                        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
                    
                    # Add data rows with improved formatting
                    for row_idx, row_data in enumerate(rows, start=1):
                        for col_idx, cell_data in enumerate(row_data):
                            cell = table.cell(row_idx, col_idx)
                            cell.text = str(cell_data)
                            paragraph = cell.text_frame.paragraphs[0]
                            paragraph.font.size = Pt(20)
                            paragraph.font.color.rgb = RGBColor(255, 255, 255)
                            paragraph.font.name = 'Segoe UI'
                            paragraph.alignment = PP_ALIGN.LEFT
                            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
                            # Alternate row colors
                            cell.fill.solid()
                            if row_idx % 2 == 0:
                                cell.fill.fore_color.rgb = RGBColor(1, 22, 64)
                            else:
                                cell.fill.fore_color.rgb = RGBColor(2, 33, 96)

            # Add accent shape
            accent = pptx_slide.shapes.add_shape(
                MSO_SHAPE.RECTANGLE,
                Inches(0.8),
                Inches(0.8),
                Inches(0.1),
                Inches(5.9)
            )
            accent_fill = accent.fill
            accent_fill.solid()
            accent_fill.fore_color.rgb = RGBColor(0, 178, 148)
            accent.line.fill.background()

        except Exception as e:
            logger.error(f"Error creating table slide: {e}")

    def generate(self, presentation: Presentation) -> Optional[str]:
        """Generate a PowerPoint presentation from the presentation model."""
        try:
            # Create title slide
            title_slide = Slide(
                title=presentation.title,
                type="title",
                layout="centered",
                content=[presentation.subtitle],
                visual_notes=None,
                notes=None
            )
            self._create_title_slide(title_slide)

            # Create content slides
            for slide in presentation.slides:
                if slide.type.lower() == "title":
                    self._create_title_slide(slide)
                elif slide.type.lower() == "table":
                    self._create_table_slide(slide)
                else:
                    self._create_content_slide(slide)

            # Save the presentation in the presentations directory
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"presentation_{timestamp}.pptx"
            filepath = os.path.join(self.presentations_dir, filename)
            self.prs.save(filepath)
            logger.info(f"Presentation saved as {filepath}")
            return filename

        except Exception as e:
            logger.error(f"Error generating presentation: {e}")
            return None 