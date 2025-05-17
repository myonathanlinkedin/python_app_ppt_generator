// Presentation Generator Module
const PresentationGenerator = {
    init() {
        this.form = document.getElementById('presentation-form');
        this.preview = document.getElementById('preview');
        this.loadingSpinner = document.getElementById('loading-spinner');
        this.currentSlideIndex = 0;
        this.slides = [];
        
        this.bindEvents();
    },

    bindEvents() {
        this.form.addEventListener('submit', (e) => this.handleSubmit(e));
    },

    async handleSubmit(e) {
        e.preventDefault();
        this.showLoading();

        const formData = new FormData(this.form);
        const topic = formData.get('topic');
        const style = formData.get('style');

        try {
            const response = await this.generatePresentation(topic, style);
            this.slides = response.slides;
            this.currentSlideIndex = 0;
            this.filename = response.filename;
            this.updatePreview(response);
        } catch (error) {
            this.showError(error);
        } finally {
            this.hideLoading();
        }
    },

    async generatePresentation(topic, style) {
        const response = await fetch('/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ topic, style })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Failed to generate presentation');
        }

        return await response.json();
    },

    updatePreview(data) {
        const content = this.formatPreview(data);
        this.preview.innerHTML = content;

        // Add event listeners for navigation buttons
        const prevButton = document.getElementById('prev-slide');
        const nextButton = document.getElementById('next-slide');
        const downloadButton = document.getElementById('download-presentation');

        if (prevButton) {
            prevButton.addEventListener('click', () => this.navigateSlides('prev'));
        }
        if (nextButton) {
            nextButton.addEventListener('click', () => this.navigateSlides('next'));
        }
        if (downloadButton) {
            downloadButton.addEventListener('click', () => this.downloadPresentation());
        }

        this.updateSlideContent();
    },

    formatPreview(data) {
        return `
            <div class="preview-header">
                <h2 class="preview-title">${data.title}</h2>
                <p class="preview-subtitle">${data.subtitle}</p>
            </div>
            <div class="preview-navigation">
                <button id="prev-slide" class="btn btn-nav" ${this.currentSlideIndex === 0 ? 'disabled' : ''}>
                    <i class="fas fa-chevron-left"></i> Previous
                </button>
                <span class="slide-counter">Slide ${this.currentSlideIndex + 1} of ${this.slides.length}</span>
                <button id="next-slide" class="btn btn-nav" ${this.currentSlideIndex === this.slides.length - 1 ? 'disabled' : ''}>
                    Next <i class="fas fa-chevron-right"></i>
                </button>
            </div>
            <div class="current-slide">
                <div id="slide-content"></div>
            </div>
            <div class="preview-actions">
                <button id="download-presentation" class="btn btn-primary">
                    <i class="fas fa-download"></i> Download Presentation
                </button>
            </div>
        `;
    },

    updateSlideContent() {
        const slideContent = document.getElementById('slide-content');
        const currentSlide = this.slides[this.currentSlideIndex];
        
        if (slideContent && currentSlide) {
            slideContent.innerHTML = `
                <h3 class="slide-title">${currentSlide.title}</h3>
                <div class="slide-body">
                    ${Array.isArray(currentSlide.content) ? 
                        `<ul class="slide-points">
                            ${currentSlide.content.map(point => `<li>${point}</li>`).join('')}
                        </ul>` : 
                        `<p>${currentSlide.content}</p>`
                    }
                </div>
            `;
        }
    },

    navigateSlides(direction) {
        if (direction === 'prev' && this.currentSlideIndex > 0) {
            this.currentSlideIndex--;
        } else if (direction === 'next' && this.currentSlideIndex < this.slides.length - 1) {
            this.currentSlideIndex++;
        }
        this.updatePreview({ title: this.slides[0].title, subtitle: this.slides[0].content[0] });
    },

    downloadPresentation() {
        if (this.filename) {
            window.location.href = `/download/${this.filename}`;
        }
    },

    showLoading() {
        this.loadingSpinner.style.display = 'flex';
        this.preview.style.opacity = '0.5';
    },

    hideLoading() {
        this.loadingSpinner.style.display = 'none';
        this.preview.style.opacity = '1';
    },

    showError(error) {
        this.preview.innerHTML = `
            <div class="error-message">
                <h3>Error</h3>
                <p>${error.message}</p>
            </div>
        `;
    }
};

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', () => {
    PresentationGenerator.init();
}); 