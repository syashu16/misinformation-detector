// Enhanced visualization functions for advanced misinformation detection

class AdvancedVisualization {
    constructor() {
        this.chartColors = {
            primary: '#667eea',
            danger: '#dc3545',
            warning: '#ffc107',
            success: '#28a745',
            info: '#17a2b8',
            secondary: '#6c757d'
        };
        
        this.isInitialized = false;
        this.loadChartLibraries();
    }
    
    async loadChartLibraries() {
        // Load Chart.js
        if (!window.Chart) {
            const script = document.createElement('script');
            script.src = 'https://cdn.jsdelivr.net/npm/chart.js@3.9.1/dist/chart.min.js';
            document.head.appendChild(script);
            
            await new Promise(resolve => {
                script.onload = resolve;
            });
        }
        
        // Load D3.js for advanced visualizations
        if (!window.d3) {
            const d3Script = document.createElement('script');
            d3Script.src = 'https://d3js.org/d3.v7.min.js';
            document.head.appendChild(d3Script);
            
            await new Promise(resolve => {
                d3Script.onload = resolve;
            });
        }
    }
    
    createRiskScoreVisualization(container, analysisData) {
        const riskScore = analysisData.risk_assessment?.overall_risk_score || 0;
        const componentScores = analysisData.risk_assessment?.component_scores || {};
        
        container.innerHTML = `
            <div class="risk-visualization">
                <div class="risk-gauge-container">
                    <canvas id="riskGauge" width="300" height="300"></canvas>
                    <div class="risk-level-indicator">
                        <h3 id="riskLevelText">${analysisData.risk_assessment?.risk_level || 'UNKNOWN'}</h3>
                        <p id="riskDescription">${analysisData.risk_assessment?.risk_description || ''}</p>
                    </div>
                </div>
                <div class="component-breakdown">
                    <canvas id="componentChart" width="400" height="300"></canvas>
                </div>
            </div>
        `;
        
        this.createRiskGauge(riskScore);
        this.createComponentBreakdown(componentScores);
    }
    
    createRiskGauge(riskScore) {
        const canvas = document.getElementById('riskGauge');
        if (!canvas) {
            console.warn('Risk gauge canvas element not found');
            return;
        }
        const ctx = canvas.getContext('2d');
        
        new Chart(ctx, {
            type: 'doughnut',
            data: {
                datasets: [{
                    data: [riskScore, 100 - riskScore],
                    backgroundColor: [
                        this.getRiskColor(riskScore),
                        '#e9ecef'
                    ],
                    borderWidth: 0,
                    cutout: '70%'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        enabled: false
                    }
                },
                animation: {
                    animateRotate: true,
                    duration: 2000
                }
            },
            plugins: [{
                afterDraw: (chart) => {
                    const ctx = chart.ctx;
                    const centerX = chart.chartArea.left + (chart.chartArea.right - chart.chartArea.left) / 2;
                    const centerY = chart.chartArea.top + (chart.chartArea.bottom - chart.chartArea.top) / 2;
                    
                    ctx.save();
                    ctx.font = 'bold 24px Inter';
                    ctx.fillStyle = this.getRiskColor(riskScore);
                    ctx.textAlign = 'center';
                    ctx.textBaseline = 'middle';
                    ctx.fillText(Math.round(riskScore), centerX, centerY - 10);
                    
                    ctx.font = '14px Inter';
                    ctx.fillStyle = '#6c757d';
                    ctx.fillText('Risk Score', centerX, centerY + 15);
                    ctx.restore();
                }
            }]
        });
    }
    
    createComponentBreakdown(componentScores) {
        const canvas = document.getElementById('componentChart');
        if (!canvas) {
            console.warn('Component chart canvas element not found');
            return;
        }
        const ctx = canvas.getContext('2d');
        
        const labels = Object.keys(componentScores).map(key => 
            key.charAt(0).toUpperCase() + key.slice(1)
        );
        const scores = Object.values(componentScores);
        
        new Chart(ctx, {
            type: 'radar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Credibility Scores',
                    data: scores,
                    backgroundColor: 'rgba(102, 126, 234, 0.2)',
                    borderColor: this.chartColors.primary,
                    borderWidth: 2,
                    pointBackgroundColor: this.chartColors.primary,
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2,
                    pointRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    r: {
                        beginAtZero: true,
                        max: 100,
                        ticks: {
                            stepSize: 20
                        },
                        grid: {
                            color: 'rgba(0, 0, 0, 0.1)'
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    }
                },
                animation: {
                    duration: 1500
                }
            }
        });
    }
    
    createTimelineVisualization(container, analysisData) {
        const timeline = analysisData.detailed_analysis?.temporal || {};
        
        container.innerHTML = `
            <div class="timeline-visualization">
                <h4><i class="fas fa-clock"></i> Temporal Analysis</h4>
                <div class="timeline-chart" id="timelineChart"></div>
                <div class="urgency-indicators">
                    <div class="urgency-metric">
                        <span class="metric-value">${timeline.urgency_indicators || 0}</span>
                        <span class="metric-label">Urgency Indicators</span>
                    </div>
                    <div class="urgency-metric">
                        <span class="metric-value">${timeline.time_references || 0}</span>
                        <span class="metric-label">Time References</span>
                    </div>
                    <div class="urgency-metric">
                        <span class="metric-value risk-level-${timeline.manipulation_risk || 'unknown'}">${timeline.manipulation_risk || 'Unknown'}</span>
                        <span class="metric-label">Manipulation Risk</span>
                    </div>
                </div>
            </div>
        `;
    }
    
    createNetworkVisualization(container, analysisData) {
        const networkContainer = document.createElement('div');
        networkContainer.className = 'network-visualization';
        networkContainer.innerHTML = `
            <h4><i class="fas fa-project-diagram"></i> Content Network Analysis</h4>
            <div id="networkGraph" style="width: 100%; height: 400px;"></div>
        `;
        container.appendChild(networkContainer);
        
        this.renderNetworkGraph(analysisData);
    }
    
    renderNetworkGraph(analysisData) {
        const width = 600;
        const height = 400;
        
        // Create sample network data based on analysis
        const nodes = [
            { id: 'content', group: 'main', value: 50 },
            { id: 'source', group: 'source', value: analysisData.detailed_analysis?.source?.credibility_score || 50 },
            { id: 'claims', group: 'claims', value: analysisData.detailed_analysis?.factual?.verification_score || 50 },
            { id: 'language', group: 'language', value: analysisData.detailed_analysis?.linguistic?.linguistic_score || 50 },
            { id: 'timing', group: 'timing', value: analysisData.detailed_analysis?.temporal?.temporal_score || 50 }
        ];
        
        const links = [
            { source: 'content', target: 'source', value: 3 },
            { source: 'content', target: 'claims', value: 4 },
            { source: 'content', target: 'language', value: 2 },
            { source: 'content', target: 'timing', value: 2 },
            { source: 'source', target: 'claims', value: 1 }
        ];
        
        const svg = d3.select('#networkGraph')
            .append('svg')
            .attr('width', width)
            .attr('height', height);
        
        const simulation = d3.forceSimulation(nodes)
            .force('link', d3.forceLink(links).id(d => d.id).distance(100))
            .force('charge', d3.forceManyBody().strength(-300))
            .force('center', d3.forceCenter(width / 2, height / 2));
        
        const link = svg.append('g')
            .selectAll('line')
            .data(links)
            .enter().append('line')
            .attr('stroke', '#999')
            .attr('stroke-opacity', 0.6)
            .attr('stroke-width', d => Math.sqrt(d.value));
        
        const node = svg.append('g')
            .selectAll('circle')
            .data(nodes)
            .enter().append('circle')
            .attr('r', d => Math.sqrt(d.value) * 2)
            .attr('fill', d => this.getNodeColor(d.group))
            .call(d3.drag()
                .on('start', dragstarted)
                .on('drag', dragged)
                .on('end', dragended));
        
        const label = svg.append('g')
            .selectAll('text')
            .data(nodes)
            .enter().append('text')
            .text(d => d.id)
            .attr('font-size', 12)
            .attr('dx', 15)
            .attr('dy', 4);
        
        simulation.on('tick', () => {
            link
                .attr('x1', d => d.source.x)
                .attr('y1', d => d.source.y)
                .attr('x2', d => d.target.x)
                .attr('y2', d => d.target.y);
            
            node
                .attr('cx', d => d.x)
                .attr('cy', d => d.y);
            
            label
                .attr('x', d => d.x)
                .attr('y', d => d.y);
        });
        
        function dragstarted(event, d) {
            if (!event.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x;
            d.fy = d.y;
        }
        
        function dragged(event, d) {
            d.fx = event.x;
            d.fy = event.y;
        }
        
        function dragended(event, d) {
            if (!event.active) simulation.alphaTarget(0);
            d.fx = null;
            d.fy = null;
        }
    }
    
    createSentimentFlow(container, analysisData) {
        const sentimentData = analysisData.detailed_analysis?.linguistic || {};
        
        container.innerHTML = `
            <div class="sentiment-flow">
                <h4><i class="fas fa-heart"></i> Emotional Manipulation Analysis</h4>
                <div class="sentiment-chart" id="sentimentChart"></div>
                <div class="pattern-indicators">
                    ${Object.entries(sentimentData.pattern_scores || {}).map(([pattern, score]) => `
                        <div class="pattern-indicator">
                            <span class="pattern-name">${pattern.replace('_', ' ')}</span>
                            <div class="pattern-bar">
                                <div class="pattern-fill" style="width: ${score}%; background-color: ${this.getPatternColor(score)}"></div>
                            </div>
                            <span class="pattern-score">${score}%</span>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    }
    
    createConfidenceIndicator(container, confidence) {
        const confidencePercentage = Math.round(confidence * 100);
        
        container.innerHTML = `
            <div class="confidence-indicator">
                <div class="confidence-circle">
                    <svg width="100" height="100" viewBox="0 0 100 100">
                        <circle cx="50" cy="50" r="45" fill="none" stroke="#e9ecef" stroke-width="8"/>
                        <circle cx="50" cy="50" r="45" fill="none" stroke="${this.getConfidenceColor(confidence)}" 
                                stroke-width="8" stroke-dasharray="${2 * Math.PI * 45}" 
                                stroke-dashoffset="${2 * Math.PI * 45 * (1 - confidence)}"
                                transform="rotate(-90 50 50)" style="transition: stroke-dashoffset 2s ease;"/>
                    </svg>
                    <div class="confidence-text">
                        <span class="confidence-value">${confidencePercentage}%</span>
                        <span class="confidence-label">Confidence</span>
                    </div>
                </div>
                <p class="confidence-description">
                    ${this.getConfidenceDescription(confidence)}
                </p>
            </div>
        `;
    }
    
    // Utility functions
    getRiskColor(riskScore) {
        if (riskScore >= 70) return this.chartColors.danger;
        if (riskScore >= 50) return '#fd7e14'; // Orange
        if (riskScore >= 30) return this.chartColors.warning;
        if (riskScore >= 15) return '#20c997'; // Teal
        return this.chartColors.success;
    }
    
    getNodeColor(group) {
        const colors = {
            main: this.chartColors.primary,
            source: this.chartColors.info,
            claims: this.chartColors.warning,
            language: this.chartColors.secondary,
            timing: this.chartColors.success
        };
        return colors[group] || this.chartColors.secondary;
    }
    
    getPatternColor(score) {
        if (score >= 80) return this.chartColors.success;
        if (score >= 60) return this.chartColors.warning;
        return this.chartColors.danger;
    }
    
    getConfidenceColor(confidence) {
        if (confidence >= 0.8) return this.chartColors.success;
        if (confidence >= 0.6) return this.chartColors.warning;
        return this.chartColors.danger;
    }
    
    getConfidenceDescription(confidence) {
        if (confidence >= 0.9) return 'Very high confidence in analysis results';
        if (confidence >= 0.8) return 'High confidence in analysis results';
        if (confidence >= 0.7) return 'Good confidence in analysis results';
        if (confidence >= 0.6) return 'Moderate confidence in analysis results';
        return 'Lower confidence - results should be interpreted carefully';
    }
}

// Enhanced results display functions
function displayAdvancedResults(data) {
    const visualization = new AdvancedVisualization();
    
    // Clear existing results
    const resultsContainer = document.getElementById('technical-details');
    if (!resultsContainer) {
        console.warn('Technical details container not found');
        return;
    }
    resultsContainer.innerHTML = '';
    
    // Create main visualization container
    const mainVizContainer = document.createElement('div');
    mainVizContainer.className = 'advanced-visualization-container';
    
    // Risk Score Visualization
    const riskContainer = document.createElement('div');
    riskContainer.className = 'risk-visualization-section';
    visualization.createRiskScoreVisualization(riskContainer, data);
    mainVizContainer.appendChild(riskContainer);
    
    // Timeline Analysis
    const timelineContainer = document.createElement('div');
    timelineContainer.className = 'timeline-section';
    visualization.createTimelineVisualization(timelineContainer, data);
    mainVizContainer.appendChild(timelineContainer);
    
    // Network Analysis
    const networkContainer = document.createElement('div');
    networkContainer.className = 'network-section';
    visualization.createNetworkVisualization(networkContainer, data);
    mainVizContainer.appendChild(networkContainer);
    
    // Sentiment Flow
    const sentimentContainer = document.createElement('div');
    sentimentContainer.className = 'sentiment-section';
    visualization.createSentimentFlow(sentimentContainer, data);
    mainVizContainer.appendChild(sentimentContainer);
    
    // Confidence Indicator
    const confidenceContainer = document.createElement('div');
    confidenceContainer.className = 'confidence-section';
    visualization.createConfidenceIndicator(confidenceContainer, data.confidence_score || 0.7);
    mainVizContainer.appendChild(confidenceContainer);
    
    resultsContainer.appendChild(mainVizContainer);
    
    // Add enhanced styling
    addAdvancedVisualizationStyles();
}

function addAdvancedVisualizationStyles() {
    const styles = `
        .advanced-visualization-container {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 25px;
            margin-top: 20px;
        }
        
        .risk-visualization {
            display: flex;
            flex-direction: column;
            gap: 20px;
        }
        
        .risk-gauge-container {
            position: relative;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        
        .risk-level-indicator {
            text-align: center;
            margin-top: 15px;
        }
        
        .risk-level-indicator h3 {
            margin: 0;
            font-size: 1.2rem;
            font-weight: 700;
        }
        
        .component-breakdown {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
        }
        
        .timeline-visualization {
            background: white;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
        }
        
        .urgency-indicators {
            display: flex;
            justify-content: space-around;
            margin-top: 20px;
        }
        
        .urgency-metric {
            text-align: center;
        }
        
        .metric-value {
            display: block;
            font-size: 1.5rem;
            font-weight: 700;
            color: #667eea;
        }
        
        .metric-label {
            font-size: 0.9rem;
            color: #6c757d;
        }
        
        .risk-level-high {
            color: #dc3545;
        }
        
        .risk-level-low {
            color: #28a745;
        }
        
        .network-visualization {
            background: white;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
            grid-column: 1 / -1;
        }
        
        .sentiment-flow {
            background: white;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
        }
        
        .pattern-indicators {
            margin-top: 20px;
        }
        
        .pattern-indicator {
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 10px;
        }
        
        .pattern-name {
            min-width: 120px;
            font-weight: 500;
            text-transform: capitalize;
        }
        
        .pattern-bar {
            flex: 1;
            height: 8px;
            background: #e9ecef;
            border-radius: 4px;
            overflow: hidden;
        }
        
        .pattern-fill {
            height: 100%;
            transition: width 1s ease;
        }
        
        .pattern-score {
            min-width: 40px;
            text-align: right;
            font-weight: 600;
        }
        
        .confidence-indicator {
            background: white;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
            text-align: center;
        }
        
        .confidence-circle {
            position: relative;
            display: inline-block;
            margin-bottom: 15px;
        }
        
        .confidence-text {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            text-align: center;
        }
        
        .confidence-value {
            display: block;
            font-size: 1.5rem;
            font-weight: 700;
            color: #333;
        }
        
        .confidence-label {
            font-size: 0.8rem;
            color: #6c757d;
        }
        
        .confidence-description {
            margin: 0;
            color: #6c757d;
            font-size: 0.9rem;
        }
        
        @media (max-width: 768px) {
            .advanced-visualization-container {
                grid-template-columns: 1fr;
            }
            
            .network-visualization {
                grid-column: auto;
            }
        }
    `;
    
    const styleSheet = document.createElement('style');
    styleSheet.textContent = styles;
    document.head.appendChild(styleSheet);
}
