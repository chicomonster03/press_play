class SectionTemplate extends HTMLElement {
  constructor() {
    super();
  }

  connectedCallback() {
    const title = this.getAttribute('title') || '';
    const subtitle = this.getAttribute('subtitle') || '';
    const body = this.getAttribute('body') || '';
    const img = this.getAttribute('img') || '';
    const align = this.getAttribute('align') || 'top';
    const visWidth = this.getAttribute('vis-width');
    const visHeight = this.getAttribute('vis-height');
    const visSize = this.getAttribute('vis-size');
    const collapsible = this.getAttribute('collapsible') === 'true';
    const visId = this.getAttribute('vis-id');

    // Determine if we have a visualization to show
    const hasVis = visId || img;

    // Default sizing
    let styleWidth = visWidth || '100%';
    let styleHeight = visHeight || visSize || '30rem';

    this.innerHTML = `
      <div class="snes-box section-component" data-align="${align}" data-collapsible="${collapsible}">
        <div class="section-header">
          ${title ? `<h2 class="section-title">${title}</h2>` : ''}
          ${subtitle ? `<p class="section-subtitle">${subtitle}</p>` : ''}
        </div>

        <div class="section-layout">
          ${getLayoutContent()}
        </div>
      </div>
    `;

    function getLayoutContent() {
      const textBlock = body ? `<div class="section-text"><p>${body}</p></div>` : '';
      const visBlock = hasVis ? `
        <div class="section-vis" style="width: ${styleWidth}; height: ${styleHeight}; min-height: ${styleHeight};">
          ${visId ? `<div id="${visId}" class="vega-container" style="width: 100%; height: 100%;"></div>` : ''}
          ${img ? `<img src="${img}" alt="${title}" class="pixel" style="width: 100%; height: auto;" />` : ''}
        </div>
      ` : '';

      // Determine order based on alignment
      switch(align) {
        case 'right':
          // Text on left, vis on right
          return textBlock + visBlock;
        case 'left':
          // Vis on left, text on right
          return visBlock + textBlock;
        case 'bottom':
        case 'below':
          // Vis on top, text below
          return visBlock + textBlock;
        case 'top':
        case 'above':
        default:
          // Text on top, vis below
          return textBlock + visBlock;
      }
    }
  }
}

customElements.define('section-template', SectionTemplate);