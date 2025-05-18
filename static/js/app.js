// Presentation Generator Module
const PresentationGenerator = {
    init() {
        this.form = document.getElementById('presentation-form');
        this.preview = document.getElementById('preview');
        this.loadingSpinner = document.getElementById('loading-spinner');
        this.pagesContainer = document.querySelector('.pages-container');
        this.backButton = document.getElementById('back-button');
        this.nextButton = document.getElementById('next-button');
        this.firstNextButton = document.getElementById('first-next-button');
        this.currentSlideIndex = 0;
        this.slides = [];
        this.previewData = null;
        
        // Hide first-next-button by default
        if (this.firstNextButton) {
            this.firstNextButton.style.display = 'none';
        }
        
        // --- Mock Data Flag ---
        // ----------------------

        // --- Mock Presentation Data ---
        // ------------------------------
        
        this.bindEvents();
    },

    bindEvents() {
        this.form.addEventListener('submit', (e) => this.handleSubmit(e));
    },

    navigateToPreview() {
        this.pagesContainer.classList.add('show-preview');
    },

    navigateToInput() {
        this.pagesContainer.classList.remove('show-preview');
    },

    navigateToNextSlide() {
        if (this.currentSlideIndex < this.slides.length - 1) {
            this.currentSlideIndex++;
            this.updateSlideContent();
        }
    },

    async handleSubmit(e) {
        e.preventDefault();
        this.showLoading();

        const formData = new FormData(this.form);
        const topic = formData.get('topic');
        const style = formData.get('style');

        try {
            console.log('Submitting form with data:', { topic, style });
            const response = await this.generatePreview(topic, style);
            this.form.reset();
            this.previewData = response.preview;
            this.slides = response.preview.slides;
            this.currentSlideIndex = 0;
            this.updatePreview(response.preview);
            this.navigateToPreview();
            console.log('Preview generated successfully:', response.preview);
            // Show the first-next-button after successful generation
            const firstNextButton = document.getElementById('first-next-button');
            if (firstNextButton) {
                firstNextButton.style.display = 'flex';
            }
        } catch (error) {
            console.error('Error in handleSubmit:', error);
            console.error('Error stack:', error.stack);
            this.showError(error);
        } finally {
            this.hideLoading();
        }
    },

    async generatePreview(topic, style) {
        this.slides = [];
        this.currentSlideIndex = 0;
        this.previewData = null;
        
        console.log('Generating preview for:', { topic, style });
        try {
            const response = await fetch('/api/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Cache-Control': 'no-cache, no-store, must-revalidate',
                    'Pragma': 'no-cache',
                    'Expires': '0'
                },
                body: JSON.stringify({ 
                    topic, 
                    style,
                    timestamp: Date.now()
                })
            });

            console.log('API Response status:', response.status);
            const responseData = await response.json();
            console.log('API Response data:', responseData);

            if (!response.ok) {
                const error = new Error(responseData.error || 'Failed to generate presentation preview');
                error.status = response.status;
                error.responseData = responseData;
                console.error('API Error:', error);
                throw error;
            }

            if (!responseData.presentation || !responseData.presentation.slides) {
                console.error('Invalid presentation data:', responseData);
                throw new Error('Invalid presentation data received');
            }

            this.previewData = responseData.presentation;
            this.slides = responseData.presentation.slides;
            this.updatePreview(responseData.presentation);
            return { preview: responseData.presentation };
        } catch (error) {
            console.error('Error in generatePreview:', error);
            console.error('Error stack:', error.stack);
            throw error;
        }
    },

    async createAndDownloadPPT() {
        if (!this.previewData) {
            this.showError(new Error('No presentation data available'));
            return;
        }

        this.showLoading('Generating PowerPoint presentation from preview...');
        try {
            // First create the PPT
            const createResponse = await fetch('/create-ppt', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    preview: this.previewData
                })
            });

            if (!createResponse.ok) {
                const errorData = await createResponse.json();
                throw new Error(errorData.error || 'Failed to create PowerPoint file');
            }

            const data = await createResponse.json();
            
            // Update loading message for download
            this.showLoading('PowerPoint generated! Starting download...');
            
            // Then trigger the download
            if (data.filename) {
                window.location.href = `/download/${data.filename}`;
                // Show success message briefly before hiding
                setTimeout(() => {
                    this.hideLoading();
                    this.showSuccess('PowerPoint downloaded successfully!');
                }, 1000);
            } else {
                throw new Error('No filename received for download');
            }
        } catch (error) {
            this.showError(error);
        } finally {
            setTimeout(() => {
                this.hideLoading();
            }, 1500);
        }
    },

    updatePreview(data) {
        console.log('Updating preview with data:', data);
        try {
            const content = this.formatPreview(data);
            this.preview.innerHTML = content;

            // Add event listeners for export buttons
            const exportPdfButton = document.getElementById('export-pdf');
            const exportPptxButton = document.getElementById('export-pptx');

            if (exportPdfButton) {
                exportPdfButton.addEventListener('click', () => {
                    console.log('PDF export button clicked');
                    this.exportPDF();
                });
            } else {
                console.warn('PDF export button not found');
            }
            
            if (exportPptxButton) {
                exportPptxButton.addEventListener('click', () => {
                    console.log('PPTX export button clicked');
                    this.exportPPTX();
                });
            } else {
                console.warn('PPTX export button not found');
            }

            this.updateSlideContent();
            console.log('Preview updated successfully');
        } catch (error) {
            console.error('Error in updatePreview:', error);
            console.error('Error stack:', error.stack);
            throw error;
        }
    },

    formatPreview(data) {
        return `
            <div class="presentation-preview-content">
                <div class="preview-header">
                    <h2 class="preview-title">${data.title}</h2>
                    <p class="preview-subtitle">${data.subtitle || ''}</p>
                </div>
                <div class="preview-navigation">
                    <button id="prev-slide" class="btn-nav" onclick="PresentationGenerator.navigateSlides('prev')" ${this.currentSlideIndex === 0 ? 'disabled' : ''}>
                        <i class="fas fa-chevron-left"></i> Previous
                    </button>
                    <span class="slide-counter">Slide ${this.currentSlideIndex + 1} of ${this.slides.length}</span>
                    <button id="next-slide" class="btn-nav" onclick="PresentationGenerator.navigateSlides('next')" ${this.currentSlideIndex === this.slides.length - 1 ? 'disabled' : ''}>
                        Next <i class="fas fa-chevron-right"></i>
                    </button>
                </div>
                <div class="current-slide">
                    <div id="slide-content"></div>
                </div>
                <div class="preview-export-actions">
                    <button id="export-pdf" class="btn btn-primary">
                        <i class="fas fa-file-pdf"></i> Export as PDF
                    </button>
                    <button id="export-pptx" class="btn btn-primary">
                        <i class="fas fa-file-powerpoint"></i> Export as PowerPoint
                    </button>
                </div>
            </div>
        `;
    },

    navigateSlides(direction) {
        if (direction === 'prev' && this.currentSlideIndex > 0) {
            this.currentSlideIndex--;
            this.updateSlideContent();
        } else if (direction === 'next' && this.currentSlideIndex < this.slides.length - 1) {
            this.currentSlideIndex++;
            this.updateSlideContent();
        }
        
        // Update navigation buttons
        const prevButton = document.getElementById('prev-slide');
        const nextButton = document.getElementById('next-slide');
        const counter = document.querySelector('.slide-counter');
        
        if (prevButton) prevButton.disabled = this.currentSlideIndex === 0;
        if (nextButton) nextButton.disabled = this.currentSlideIndex === this.slides.length - 1;
        if (counter) counter.textContent = `Slide ${this.currentSlideIndex + 1} of ${this.slides.length}`;
    },

    updateSlideContent() {
        const slideContent = document.getElementById('slide-content');
        const currentSlide = this.slides[this.currentSlideIndex];
        
        if (!slideContent || !currentSlide) return;

        let html = '';

        // Title slide
        if (currentSlide.type === 'title') {
            html = `
                <div class="slide-content title-slide">
                    <h1>${currentSlide.title}</h1>
                    <h3>${this.previewData.subtitle || ''}</h3>
                </div>
            `;
        }
        // Table slide
        else if (currentSlide.type === 'table' && Array.isArray(currentSlide.content)) {
            html = `
                <div class="slide-content table-slide">
                    <h2 class="slide-title">${currentSlide.title}</h2>
                    <div class="table-container">
                        <table class="modern-table">
                            ${currentSlide.content.map((row, i) => `
                                <tr>${row.map((cell, j) => 
                                    i === 0 ? `<th>${cell}</th>` : `<td>${cell}</td>`
                                ).join('')}</tr>
                            `).join('')}
                        </table>
                    </div>
                </div>
            `;
        }
        // Content slide
        else if (Array.isArray(currentSlide.content)) {
            html = `
                <div class="slide-content content-slide">
                    <h2 class="slide-title">${currentSlide.title}</h2>
                    <ul class="slide-points">
                        ${currentSlide.content.map(point => `
                            <li>${point}</li>
                        `).join('')}
                    </ul>
                </div>
            `;
        }

        slideContent.innerHTML = html;

        // Apply theme
        if (this.previewData?.theme) {
            const theme = this.previewData.theme;
            const previewContentElement = this.preview.querySelector('.presentation-preview-content');
            if (previewContentElement) {
                previewContentElement.style.setProperty('--primary-color', theme.primary_color);
                previewContentElement.style.setProperty('--accent-color', theme.accent_color);
                previewContentElement.style.setProperty('--background-color', theme.background_color);
                previewContentElement.style.setProperty('--text-color', theme.secondary_color);
            }
        }
    },

    showError(error) {
        console.error('Showing error:', error);
        const errorMessage = error.message || 'An unexpected error occurred';
        console.error('Error details:', {
            message: errorMessage,
            status: error.status,
            responseData: error.responseData,
            stack: error.stack
        });
        
        // Navigate back to input page when showing error
        this.navigateToInput();
        
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.innerHTML = `
            <div class="error">
                <i class="fas fa-exclamation-circle"></i>
                <span>${errorMessage}</span>
            </div>
        `;
        
        // Remove any existing error messages
        const existingErrors = document.querySelectorAll('.error-message');
        existingErrors.forEach(el => el.remove());
        
        // Insert error before the form
        this.form.parentNode.insertBefore(errorDiv, this.form);
        
        // Auto-remove error after 5 seconds
        setTimeout(() => {
            errorDiv.remove();
        }, 5000);
    },

    showLoading(message = 'Generating your presentation...', clearPreview = true) {
        if (this.loadingSpinner) {
            const loadingText = this.loadingSpinner.querySelector('.loading-text');
            if (loadingText) {
                loadingText.textContent = message;
            }
            
            // Add show class for animation
            this.loadingSpinner.style.display = 'flex';
            requestAnimationFrame(() => {
                this.loadingSpinner.classList.add('show');
            });
            
            // Hide any existing error messages
            const existingErrors = document.querySelectorAll('.error-message');
            existingErrors.forEach(el => el.remove());
            
            // Only clear preview if explicitly requested (not during export)
            if (clearPreview && this.preview) {
                this.preview.innerHTML = '';
            }
            
            // Prevent body scrolling while modal is open
            document.body.style.overflow = 'hidden';
        }
    },

    hideLoading() {
        if (this.loadingSpinner) {
            // Remove show class and wait for animation
            this.loadingSpinner.classList.remove('show');
            setTimeout(() => {
                this.loadingSpinner.style.display = 'none';
                // Restore body scrolling
                document.body.style.overflow = '';
            }, 300); // Match the animation duration
        }
    },

    showSuccess(message) {
        const successDiv = document.createElement('div');
        successDiv.className = 'success-message';
        successDiv.innerHTML = `
            <h3><i class="fas fa-check-circle"></i> Success</h3>
            <p>${message}</p>
        `;
        this.preview.appendChild(successDiv);
        
        // Remove success message after 3 seconds
        setTimeout(() => {
            successDiv.remove();
        }, 3000);
    },

    async exportPDF() {
        if (!this.previewData) {
            this.showError(new Error('No presentation data available'));
            return;
        }

        this.showLoading('Generating PDF...', false); // Don't clear preview during export
        try {
            const response = await fetch('/api/export/pdf', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    presentation: this.previewData
                })
            });

            if (!response.ok) {
                throw new Error('Failed to generate PDF');
            }

            // Create a blob from the PDF stream
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            
            // Create a temporary link and click it to download
            const a = document.createElement('a');
            a.href = url;
            a.download = 'presentation.pdf';
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
            
            this.showSuccess('PDF downloaded successfully!');
        } catch (error) {
            this.showError(error);
        } finally {
            this.hideLoading();
        }
    },

    async exportPPTX() {
        if (!this.previewData) {
            this.showError(new Error('No presentation data available'));
            return;
        }

        this.showLoading('Generating PowerPoint...', false); // Don't clear preview during export
        try {
            const response = await fetch('/api/export/ppt', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    presentation: this.previewData
                })
            });

            if (!response.ok) {
                throw new Error('Failed to generate PowerPoint');
            }

            // Create a blob from the PPTX stream
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            
            // Create a temporary link and click it to download
            const a = document.createElement('a');
            a.href = url;
            a.download = 'presentation.pptx';
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
            
            this.showSuccess('PowerPoint downloaded successfully!');
        } catch (error) {
            this.showError(error);
        } finally {
            this.hideLoading();
        }
    },
};

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', () => {
    PresentationGenerator.init();
}); 