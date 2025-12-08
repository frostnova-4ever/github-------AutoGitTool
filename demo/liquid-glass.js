// Vanilla JS Liquid Glass Effect for File Manager
// Based on code by Shu Ding (https://github.com/shuding/liquid-glass)

(function() {
    'use strict';

    // Check if liquid glass already exists and destroy it
    if (window.liquidGlass) {
        window.liquidGlass.destroy();
        console.log('Previous liquid glass effect removed.');
    }

    // Utility functions
    function smoothStep(a, b, t) {
        t = Math.max(0, Math.min(1, (t - a) / (b - a)));
        return t * t * (3 - 2 * t);
    }

    function length(x, y) {
        return Math.sqrt(x * x + y * y);
    }

    function roundedRectSDF(x, y, width, height, radius) {
        const qx = Math.abs(x) - width + radius;
        const qy = Math.abs(y) - height + radius;
        return Math.min(Math.max(qx, qy), 0) + length(Math.max(qx, 0), Math.max(qy, 0)) - radius;
    }

    function texture(x, y) {
        return { type: 't', x, y };
    }

    // Generate unique ID
    function generateId() {
        return 'liquid-glass-' + Math.random().toString(36).substr(2, 9);
    }

    // Main Shader class
    class Shader {
        constructor(options = {}) {
            this.targetElement = options.targetElement;
            if (!this.targetElement) {
                throw new Error('Target element is required for liquid glass effect');
            }

            // Get target element dimensions
            const rect = this.targetElement.getBoundingClientRect();
            this.width = rect.width;
            this.height = rect.height;

            this.fragment = options.fragment || ((uv) => texture(uv.x, uv.y));
            this.canvasDPI = 1;
            this.id = generateId();

            this.mouse = { x: 0, y: 0 };
            this.mouseUsed = false;

            this.createElement();
            this.setupEventListeners();
            this.updateShader();

            // Apply effect to target element
            this.applyToElement();
        }

        createElement() {
            // Create SVG filter
            this.svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
            this.svg.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
            this.svg.setAttribute('width', '0');
            this.svg.setAttribute('height', '0');
            this.svg.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        pointer-events: none;
        z-index: 9998;
      `;

            const defs = document.createElementNS('http://www.w3.org/2000/svg', 'defs');
            const filter = document.createElementNS('http://www.w3.org/2000/svg', 'filter');
            filter.setAttribute('id', `${this.id}_filter`);
            filter.setAttribute('filterUnits', 'userSpaceOnUse');
            filter.setAttribute('colorInterpolationFilters', 'sRGB');
            filter.setAttribute('x', '0');
            filter.setAttribute('y', '0');
            filter.setAttribute('width', this.width.toString());
            filter.setAttribute('height', this.height.toString());

            this.feImage = document.createElementNS('http://www.w3.org/2000/svg', 'feImage');
            this.feImage.setAttribute('id', `${this.id}_map`);
            this.feImage.setAttribute('width', this.width.toString());
            this.feImage.setAttribute('height', this.height.toString());

            this.feDisplacementMap = document.createElementNS('http://www.w3.org/2000/svg', 'feDisplacementMap');
            this.feDisplacementMap.setAttribute('in', 'SourceGraphic');
            this.feDisplacementMap.setAttribute('in2', `${this.id}_map`);
            this.feDisplacementMap.setAttribute('xChannelSelector', 'R');
            this.feDisplacementMap.setAttribute('yChannelSelector', 'G');
            this.feDisplacementMap.setAttribute('scale', '10'); // Default scale

            filter.appendChild(this.feImage);
            filter.appendChild(this.feDisplacementMap);
            defs.appendChild(filter);
            this.svg.appendChild(defs);

            // Create canvas for displacement map (hidden)
            this.canvas = document.createElement('canvas');
            this.canvas.width = this.width * this.canvasDPI;
            this.canvas.height = this.height * this.canvasDPI;
            this.canvas.style.display = 'none';

            this.context = this.canvas.getContext('2d');
        }

        setupEventListeners() {
            // Update mouse position for shader
            this.targetElement.addEventListener('mousemove', (e) => {
                const rect = this.targetElement.getBoundingClientRect();
                this.mouse.x = (e.clientX - rect.left) / rect.width;
                this.mouse.y = (e.clientY - rect.top) / rect.height;

                if (this.mouseUsed) {
                    this.updateShader();
                }
            });

            // Handle window resize to update dimensions
            window.addEventListener('resize', () => {
                const rect = this.targetElement.getBoundingClientRect();
                this.width = rect.width;
                this.height = rect.height;

                // Update canvas size
                this.canvas.width = this.width * this.canvasDPI;
                this.canvas.height = this.height * this.canvasDPI;

                // Update filter dimensions
                const filter = this.svg.querySelector(`#${this.id}_filter`);
                if (filter) {
                    filter.setAttribute('width', this.width.toString());
                    filter.setAttribute('height', this.height.toString());
                }

                const feImage = this.svg.querySelector(`#${this.id}_map`);
                if (feImage) {
                    feImage.setAttribute('width', this.width.toString());
                    feImage.setAttribute('height', this.height.toString());
                }

                this.updateShader();
            });
        }

        updateShader() {
            const mouseProxy = new Proxy(this.mouse, {
                get: (target, prop) => {
                    this.mouseUsed = true;
                    return target[prop];
                }
            });

            this.mouseUsed = false;

            const w = this.width * this.canvasDPI;
            const h = this.height * this.canvasDPI;
            const data = new Uint8ClampedArray(w * h * 4);

            let maxScale = 0;
            const rawValues = [];

            for (let i = 0; i < data.length; i += 4) {
                const x = (i / 4) % w;
                const y = Math.floor(i / 4 / w);
                const pos = this.fragment({ x: x / w, y: y / h },
                    mouseProxy
                );
                const dx = pos.x * w - x;
                const dy = pos.y * h - y;
                maxScale = Math.max(maxScale, Math.abs(dx), Math.abs(dy));
                rawValues.push(dx, dy);
            }

            maxScale *= 0.5;

            let index = 0;
            for (let i = 0; i < data.length; i += 4) {
                const r = rawValues[index++] / maxScale + 0.5;
                const g = rawValues[index++] / maxScale + 0.5;
                data[i] = r * 255;
                data[i + 1] = g * 255;
                data[i + 2] = 0;
                data[i + 3] = 255;
            }

            this.context.putImageData(new ImageData(data, w, h), 0, 0);
            this.feImage.setAttributeNS('http://www.w3.org/1999/xlink', 'href', this.canvas.toDataURL());
            this.feDisplacementMap.setAttribute('scale', (maxScale / this.canvasDPI).toString());
        }

        applyToElement() {
            // Apply glass effect styles to target element
            this.targetElement.style.backdropFilter = `url(#${this.id}_filter) blur(10px) contrast(1.05) brightness(1.05) saturate(1.05)`;
            this.targetElement.style.background = 'rgba(240, 240, 240, 0.8)';
            this.targetElement.style.border = '1px solid rgba(200, 200, 200, 0.3)';
            this.targetElement.style.boxShadow = '0 4px 20px rgba(0, 0, 0, 0.1)';

            // Add SVG to body
            document.body.appendChild(this.svg);
        }

        destroy() {
            // Remove styles from target element
            this.targetElement.style.backdropFilter = '';
            this.targetElement.style.background = '';
            this.targetElement.style.border = '';
            this.targetElement.style.boxShadow = '';

            // Remove elements from DOM
            this.svg.remove();
            this.canvas.remove();
        }
    }

    // Create the liquid glass effect for file manager
    function createLiquidGlassForFileManager() {
        // Wait for DOM to be fully loaded
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', init);
        } else {
            init();
        }

        function init() {
            // Get the file manager element
            const fileManager = document.querySelector('.file-manager');
            if (!fileManager) {
                console.error('File manager element not found');
                return;
            }

            // Create shader
            const shader = new Shader({
                targetElement: fileManager,
                fragment: (uv, mouse) => {
                    const ix = uv.x - 0.5;
                    const iy = uv.y - 0.5;
                    const distanceToEdge = roundedRectSDF(
                        ix,
                        iy,
                        0.45,
                        0.45,
                        0.1
                    );
                    const displacement = smoothStep(0.8, 0, distanceToEdge - 0.1);
                    const scaled = smoothStep(0, 1, displacement);
                    return texture(ix * scaled + 0.5, iy * scaled + 0.5);
                }
            });

            console.log('Liquid Glass effect applied to file manager!');

            // Return shader instance so it can be removed if needed
            window.liquidGlass = shader;
        }
    }

    // Create the liquid glass effect for workflow nodes
    function createLiquidGlassForWorkflowNodes() {
        // Wait for DOM to be fully loaded
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', init);
        } else {
            init();
        }

        function init() {
            // Get all workflow node elements
            const nodes = document.querySelectorAll('.node');
            if (nodes.length === 0) {
                console.error('Workflow nodes not found');
                return;
            }

            // Create shader for each node
            const shaders = [];
            nodes.forEach((node, index) => {
                const shader = new Shader({
                    targetElement: node,
                    fragment: (uv, mouse) => {
                        const ix = uv.x - 0.5;
                        const iy = uv.y - 0.5;
                        const distanceToEdge = roundedRectSDF(
                            ix,
                            iy,
                            0.45,
                            0.45,
                            0.1
                        );
                        const displacement = smoothStep(0.8, 0, distanceToEdge - 0.1);
                        const scaled = smoothStep(0, 1, displacement);
                        return texture(ix * scaled + 0.5, iy * scaled + 0.5);
                    }
                });
                shaders.push(shader);
            });

            console.log('Liquid Glass effect applied to workflow nodes!');

            // Store shaders so they can be removed if needed
            window.workflowNodeShaders = shaders;
        }
    }

    // Initialize based on which elements are present
    function initLiquidGlass() {
        // Apply to file manager if present
        if (document.querySelector('.file-manager')) {
            createLiquidGlassForFileManager();
        }

        // Apply to workflow nodes if present
        if (document.querySelector('.node')) {
            createLiquidGlassForWorkflowNodes();
        }
    }

    // Initialize
    initLiquidGlass();
})();