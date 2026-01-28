/* ========================================
   TECH EVENTS DISCOVERY APP - JAVASCRIPT
   Map, Events, Modals & Interactions
   ======================================== */

class TechEventsApp {
    constructor() {
        this.map = null;
        this.markers = [];
        this.events = [];
        this.filteredEvents = [];
        this.currentCategoryFilter = 'all';
        this.currentPriceFilter = 'all';
        this.selectedEvent = null;
        this.selectedEventMarker = null;
        
        this.init();
    }

    async init() {
        try {
            // Initialize map
            this.initMap();
            
            // Fetch events from API
            await this.fetchEvents();
            
            // Render events
            this.renderEvents();
            
            // Setup event listeners
            this.setupEventListeners();
            
            // Update event count
            this.updateEventCount();
        } catch (error) {
            console.error('Error initializing app:', error);
            this.showError('Failed to load events');
        }
    }

    // ========== Map Initialization ==========
    initMap() {
        // Create map centered on London
        this.map = L.map('eventMap').setView([51.5074, -0.1278], 13);

        // Add OpenStreetMap tiles
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors',
            maxZoom: 19,
            tileSize: 256
        }).addTo(this.map);

        // Hide loading indicator
        document.getElementById('mapLoading').style.display = 'none';
    }

    // ========== Fetch Events from API ==========
    async fetchEvents() {
        try {
            const response = await fetch('http://127.0.0.1:5000/api/events');
            
            if (!response.ok) {
                throw new Error(`API error: ${response.status}`);
            }

            const allEvents = await response.json();
            
            // Filter to remove completely broken/generic pages, keep rest for display
            this.events = allEvents.filter(event => {
                const hasTitle = event.title && event.title.trim().length > 0;
                const hasUrl = event.source_url && event.source_url.startsWith('http');
                const notGeneric = !this.isGenericPage(event.source_url || '', event.title || '');
                
                return hasTitle && hasUrl && notGeneric;
            });
            
            // Sort by created_at (newest first), then by date
            this.events.sort((a, b) => {
                // Most recently added first
                const dateA = new Date(a.created_at || 0);
                const dateB = new Date(b.created_at || 0);
                return dateB - dateA;
            });
            
            this.filteredEvents = [...this.events];

            // Add markers to map
            this.addMarkersToMap();
        } catch (error) {
            console.error('Error fetching events:', error);
            this.showError('Could not load events from server');
        }
    }

    // ========== Check if URL is a generic landing page ==========
    isGenericPage(url, title) {
        if (!url) return true;
        
        const lowerUrl = url.toLowerCase();
        const lowerTitle = (title || '').toLowerCase();
        
        const genericIndicators = [
            'all-topics',
            'all topics',
            '/events/all',
            '?show=info',
            'show_info',
            'generic',
            '/page',
            '/home',
            '/index.html',
            'browse all events',
            'all events'
        ];
        
        return genericIndicators.some(indicator => 
            lowerUrl.includes(indicator) || lowerTitle.includes(indicator)
        );
    }

    // ========== Add Markers to Map ==========
    addMarkersToMap() {
        // Clear existing markers
        this.markers.forEach(marker => this.map.removeLayer(marker));
        this.markers = [];

        this.filteredEvents.forEach(event => {
            // Use provided lat/long or default to London
            const lat = event.latitude || 51.5074;
            const lng = event.longitude || -0.1278;

            // Create custom marker
            const markerEl = document.createElement('div');
            markerEl.className = 'event-marker';
            markerEl.innerHTML = '📍';

            const marker = L.marker([lat, lng], {
                icon: L.divIcon({
                    html: markerEl.outerHTML,
                    className: 'event-marker-icon',
                    iconSize: [30, 30],
                    iconAnchor: [15, 30],
                    popupAnchor: [0, -30]
                })
            }).addTo(this.map);

            // Popup on marker click
            const popupContent = this.createMarkerPopup(event);
            marker.bindPopup(popupContent, {
                maxWidth: 280,
                className: 'event-popup'
            });

            marker.on('click', () => {
                this.selectedEvent = event;
                this.openModal();
                this.panMapToEvent(event);
            });

            this.markers.push(marker);
        });

        // Auto-fit map to show all markers
        if (this.markers.length > 0) {
            const group = new L.featureGroup(this.markers);
            this.map.fitBounds(group.getBounds().pad(0.1));
        }
    }

    // ========== Pan map to event location ==========
    panMapToEvent(event) {
        const lat = event.latitude || 51.5074;
        const lng = event.longitude || -0.1278;
        this.map.setView([lat, lng], 15, { animate: true, duration: 0.5 });
    }

    // ========== Create Marker Popup ==========
    createMarkerPopup(event) {
        const displayDate = this.getDisplayDate(event);
        const displayCategory = this.getDisplayCategory(event);
        
        return `
            <div class="marker-popup">
                <strong>${event.title}</strong>
                <p style="margin: 8px 0 0 0; font-size: 12px; color: #1e293b;">
                    📅 ${displayDate}<br>
                    📍 ${event.location || 'London'}<br>
                    🏷️ ${displayCategory}
                </p>
                <button style="
                    margin-top: 8px;
                    padding: 6px 12px;
                    background: #6366f1;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                    font-size: 12px;
                    font-weight: 600;
                    width: 100%;
                " onclick="app.selectEventAndOpenModal('${event.id}')">
                    View Event
                </button>
            </div>
        `;
    }

    // ========== Fetch Events ==========
    async fetchEvents() {
        try {
            const response = await fetch('http://127.0.0.1:5000/api/events');
            
            if (!response.ok) {
                throw new Error(`API error: ${response.status}`);
            }

            this.events = await response.json();
            this.filteredEvents = [...this.events];

            // Add markers to map
            this.addMarkersToMap();
        } catch (error) {
            console.error('Error fetching events:', error);
            this.showError('Could not load events from server');
        }
    }

    // ========== Render Event List ==========
    renderEvents() {
        const eventsList = document.getElementById('eventsList');

        if (this.filteredEvents.length === 0) {
            eventsList.innerHTML = `
                <div class="events-loading">
                    <p>No events found matching your filters</p>
                </div>
            `;
            return;
        }

        eventsList.innerHTML = this.filteredEvents.map(event => {
            const displayCategory = this.getDisplayCategory(event);
            const displayDate = this.getDisplayDate(event);
            const timeAgo = this.getTimeAgo(event.created_at);
            
            return `
            <div class="event-card" data-event-id="${event.id}">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: var(--spacing-sm);">
                    <h3 class="event-card-title">${event.title}</h3>
                    <span style="font-size: 0.75rem; background: rgba(99, 102, 241, 0.15); color: #6366f1; padding: 2px 6px; border-radius: 8px; white-space: nowrap;">${timeAgo}</span>
                </div>
                
                <div class="event-card-meta">
                    <span>📅 ${displayDate}</span>
                    <span>•</span>
                    <span>📍 ${event.location || 'London'}</span>
                </div>

                <div class="event-card-badges">
                    <span class="badge badge-category">${displayCategory}</span>
                    ${event.is_free ? '<span class="badge badge-free">Free</span>' : '<span class="badge" style="background: rgba(239, 68, 68, 0.2); color: #b91c1c; border: 1px solid rgba(239, 68, 68, 0.4);">Paid</span>'}
                    ${!event.is_valid ? '<span class="badge badge-status">Unverified</span>' : ''}
                </div>
            </div>
        `}).join('');

        // Add click handlers to cards
        document.querySelectorAll('.event-card').forEach(card => {
            card.addEventListener('click', (e) => {
                const eventId = card.getAttribute('data-event-id');
                this.selectedEvent = this.events.find(e => e.id == eventId);
                this.openModal();
                this.panMapToEvent(this.selectedEvent);
            });
        });
    }

    // ========== Get Display Date ==========
    getDisplayDate(event) {
        if (event.date && event.date.trim() !== '' && event.date.toLowerCase() !== 'tbd') {
            try {
                // Try to parse and format the date
                const dateObj = new Date(event.date);
                // Check if it's a valid date
                if (!isNaN(dateObj.getTime())) {
                    return dateObj.toLocaleDateString('en-GB', { 
                        year: 'numeric', 
                        month: 'short', 
                        day: 'numeric'
                    });
                }
            } catch (e) {
                // If parsing fails, return raw date
                return event.date;
            }
        }
        // Fallback to created_at if no event date
        if (event.created_at) {
            try {
                const createdDate = new Date(event.created_at);
                if (!isNaN(createdDate.getTime())) {
                    return createdDate.toLocaleDateString('en-GB', { 
                        year: 'numeric', 
                        month: 'short', 
                        day: 'numeric'
                    });
                }
            } catch (e) {
                return event.created_at;
            }
        }
        return 'Date TBD';
    }

    // ========== Get Time Ago ==========
    getTimeAgo(createdAt) {
        if (!createdAt) return 'Unknown';
        
        const created = new Date(createdAt);
        const now = new Date();
        const seconds = Math.floor((now - created) / 1000);
        
        if (seconds < 60) return 'now';
        if (seconds < 3600) return Math.floor(seconds / 60) + 'm ago';
        if (seconds < 86400) return Math.floor(seconds / 3600) + 'h ago';
        if (seconds < 604800) return Math.floor(seconds / 86400) + 'd ago';
        
        return 'weeks ago';
    }

    // ========== Filter Events ==========
    filterEvents() {
        this.filteredEvents = this.events.filter(event => {
            // Category filter
            let categoryMatch = true;
            if (this.currentCategoryFilter !== 'all') {
                categoryMatch = this.getDisplayCategory(event) === this.currentCategoryFilter;
            }
            
            // Price filter
            let priceMatch = true;
            if (this.currentPriceFilter === 'free') {
                priceMatch = event.is_free === 1;
            } else if (this.currentPriceFilter === 'paid') {
                priceMatch = event.is_free === 0;
            }
            
            return categoryMatch && priceMatch;
        });

        this.renderEvents();
        this.addMarkersToMap();
        this.updateEventCount();
    }

    // ========== Update Event Count ==========
    updateEventCount() {
        const countEl = document.getElementById('eventCount');
        const count = this.events.length;
        countEl.textContent = `${count} event${count !== 1 ? 's' : ''} found`;
    }

    // ========== Modal Management ==========
    openModal() {
        if (!this.selectedEvent) return;

        const event = this.selectedEvent;
        const displayDate = this.getDisplayDate(event);
        const displayCategory = this.getDisplayCategory(event);
        const timeAgo = this.getTimeAgo(event.created_at);

        document.getElementById('modalTitle').textContent = event.title;
        document.getElementById('modalDate').textContent = displayDate;
        document.getElementById('modalLocation').textContent = event.location || 'London';
        document.getElementById('modalCategory').textContent = displayCategory;
        document.getElementById('modalCategoryDetail').textContent = displayCategory;
        document.getElementById('modalSource').textContent = event.source_name || 'Unknown';
        document.getElementById('modalCreatedAt').textContent = timeAgo;
        
        // Time badge
        const timeEl = document.getElementById('modalTime');
        timeEl.textContent = timeAgo;

        // Status badge
        const statusEl = document.getElementById('modalStatus');
        statusEl.textContent = event.is_free ? '✓ Free' : 'Paid';
        statusEl.className = event.is_free ? 'badge badge-free' : 'badge badge-status';

        // Event link
        const linkEl = document.getElementById('modalEventLink');
        linkEl.href = event.source_url || '#';
        linkEl.target = '_blank';
        linkEl.rel = 'noopener noreferrer';

        // Show modal
        document.getElementById('modalOverlay').classList.add('active');
    }

    closeModal() {
        document.getElementById('modalOverlay').classList.remove('active');
        this.selectedEvent = null;
    }

    selectEventAndOpenModal(eventId) {
        this.selectedEvent = this.events.find(e => e.id == eventId);
        this.openModal();
        this.panMapToEvent(this.selectedEvent);
    }

    // ========== Setup Event Listeners ==========
    setupEventListeners() {
        // Modal close buttons
        document.getElementById('modalClose').addEventListener('click', () => this.closeModal());
        document.getElementById('modalCloseBtn').addEventListener('click', () => this.closeModal());

        // Close modal on overlay click
        document.getElementById('modalOverlay').addEventListener('click', (e) => {
            if (e.target.id === 'modalOverlay') {
                this.closeModal();
            }
        });

        // Close modal on Escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.closeModal();
            }
        });

        // Category filter buttons
        document.querySelectorAll('.filter-tag').forEach(btn => {
            btn.addEventListener('click', (e) => {
                // Update active state
                document.querySelectorAll('.filter-tag').forEach(b => b.classList.remove('active'));
                e.target.classList.add('active');

                // Filter events
                const filter = e.target.getAttribute('data-filter');
                this.currentCategoryFilter = filter;
                this.filterEvents();
            });
        });

        // Price filter buttons
        document.querySelectorAll('.price-tag').forEach(btn => {
            btn.addEventListener('click', (e) => {
                // Update active state
                document.querySelectorAll('.price-tag').forEach(b => b.classList.remove('active'));
                e.target.classList.add('active');

                // Filter events
                const filter = e.target.getAttribute('data-price');
                this.currentPriceFilter = filter;
                this.filterEvents();
            });
        });
    }

    // ========== Get Display Category ==========
    getDisplayCategory(event) {
        if (!event) return 'Other';
        
        const title = (event.title || '').toLowerCase();
        const category = (event.category || '').toLowerCase();
        
        // Try to extract from title first
        if (title.includes('hackathon')) return 'Hackathon';
        if (title.includes('workshop')) return 'Workshop';
        if (title.includes('meetup')) return 'Meetup';
        if (title.includes('conference')) return 'Conference';
        if (title.includes('expo') || title.includes('exhibition')) return 'Expo';
        
        // Fall back to database category
        if (category === 'hackathon') return 'Hackathon';
        if (category === 'workshop') return 'Workshop';
        if (category === 'meetup') return 'Meetup';
        
        return 'Meetup'; // Default to Meetup
    }

    // ========== Error Handling ==========
    showError(message) {
        console.error(message);
        const eventsList = document.getElementById('eventsList');
        eventsList.innerHTML = `
            <div class="events-loading" style="color: #ef4444;">
                <p>⚠️ ${message}</p>
            </div>
        `;
    }
}

// ========== Initialize App on DOM Ready ==========
document.addEventListener('DOMContentLoaded', () => {
    window.app = new TechEventsApp();
});
