/**
 * CAREER GUIDANCE PLATFORM - CLIENT APPLICATION SCRIPT
 * Handles interactivity, responsive navigation, roadmap toggles, and live resume preview.
 */

document.addEventListener('DOMContentLoaded', function () {
    initNavigation();
    initAlertDismissal();
    initTabSystem();
    initAccordionSystem();
    initRoadmapProgressToggles();
    initInteractiveFilters();
    initResumeLivePreview();
});

/* -------------------------------------------------------------
 * 1. Mobile Navigation & Dropdowns
 * ------------------------------------------------------------- */
function initNavigation() {
    const mobileBtn = document.querySelector('.mobile-toggle');
    const navMenu = document.querySelector('.nav-menu');

    if (mobileBtn && navMenu) {
        mobileBtn.addEventListener('click', function () {
            navMenu.classList.toggle('open');
            const icon = mobileBtn.querySelector('i');
            if (icon) {
                icon.classList.toggle('fa-bars');
                icon.classList.toggle('fa-times');
            }
        });
    }
}

/* -------------------------------------------------------------
 * 2. Alert Dismissal
 * ------------------------------------------------------------- */
function initAlertDismissal() {
    const closeBtns = document.querySelectorAll('.alert-close');
    closeBtns.forEach(btn => {
        btn.addEventListener('click', function () {
            const alert = this.closest('.alert');
            if (alert) {
                alert.style.opacity = '0';
                alert.style.transform = 'translateY(-10px)';
                alert.style.transition = 'all 0.3s ease';
                setTimeout(() => alert.remove(), 300);
            }
        });
    });

    // Auto dismiss after 5 seconds
    const autoAlerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    autoAlerts.forEach(alert => {
        setTimeout(() => {
            if (alert && alert.parentElement) {
                alert.style.opacity = '0';
                alert.style.transition = 'opacity 0.4s ease';
                setTimeout(() => alert.remove(), 400);
            }
        }, 5000);
    });
}

/* -------------------------------------------------------------
 * 3. Tab Switching System
 * ------------------------------------------------------------- */
function initTabSystem() {
    const tabButtons = document.querySelectorAll('.tab-btn');
    if (!tabButtons.length) return;

    tabButtons.forEach(btn => {
        btn.addEventListener('click', function () {
            const targetId = this.getAttribute('data-tab');
            const container = this.closest('.tabs-container') || document;

            // Deactivate sibling tabs
            container.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            container.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));

            // Activate current
            this.classList.add('active');
            const targetPane = container.querySelector('#' + targetId);
            if (targetPane) {
                targetPane.classList.add('active');
            }
        });
    });
}

/* -------------------------------------------------------------
 * 4. Accordion Toggle System
 * ------------------------------------------------------------- */
function initAccordionSystem() {
    const accordionHeaders = document.querySelectorAll('.accordion-header');
    accordionHeaders.forEach(header => {
        header.addEventListener('click', function () {
            const item = this.closest('.accordion-item');
            if (!item) return;

            const wasActive = item.classList.contains('active');
            const chevron = this.querySelector('.accordion-icon');

            item.classList.toggle('active', !wasActive);
            if (chevron) {
                chevron.style.transform = wasActive ? 'rotate(0deg)' : 'rotate(180deg)';
                chevron.style.transition = 'transform 0.25s ease';
            }
        });
    });
}

/* -------------------------------------------------------------
 * 5. Learning Roadmap Interactive Topic Checkboxes (AJAX)
 * ------------------------------------------------------------- */
function initRoadmapProgressToggles() {
    const checkboxes = document.querySelectorAll('.topic-checkbox');
    if (!checkboxes.length) return;

    checkboxes.forEach(chk => {
        chk.addEventListener('change', async function () {
            const topicId = this.getAttribute('data-topic-id');
            const card = this.closest('.topic-item-card');
            const isChecked = this.checked;

            try {
                const response = await fetch('/api/progress/toggle', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-Requested-With': 'XMLHttpRequest'
                    },
                    body: JSON.stringify({
                        topic_id: topicId,
                        completed: isChecked
                    })
                });

                const data = await response.json();

                if (response.ok && data.success) {
                    if (card) {
                        card.classList.toggle('completed', isChecked);
                    }

                    // Update completion percentage indicators if present
                    const percentLabels = document.querySelectorAll('.roadmap-percent-val');
                    percentLabels.forEach(lbl => {
                        lbl.textContent = data.progress_percentage + '%';
                    });

                    const progressFills = document.querySelectorAll('.roadmap-progress-bar-fill');
                    progressFills.forEach(bar => {
                        bar.style.width = data.progress_percentage + '%';
                    });

                    showToast(isChecked ? 'Topic marked as completed!' : 'Topic marked as pending.');
                } else {
                    // Revert checkbox state if unauthorized or failed
                    this.checked = !isChecked;
                    showToast(data.message || 'Please log in as a student to track your progress.', 'warning');
                }
            } catch (err) {
                console.error('Error toggling topic progress:', err);
                this.checked = !isChecked;
                showToast('Network error while saving progress.', 'danger');
            }
        });
    });
}

/* -------------------------------------------------------------
 * 6. Live Search and Filtering for Careers, Jobs & Questions
 * ------------------------------------------------------------- */
function initInteractiveFilters() {
    // Careers filter
    const careerSearch = document.getElementById('careerSearchInput');
    const careerCategorySelect = document.getElementById('careerCategoryFilter');
    const careerCards = document.querySelectorAll('.career-filter-item');

    function filterCareers() {
        if (!careerCards.length) return;
        const query = (careerSearch ? careerSearch.value : '').toLowerCase().trim();
        const category = (careerCategorySelect ? careerCategorySelect.value : 'all');

        let visibleCount = 0;
        careerCards.forEach(card => {
            const title = (card.getAttribute('data-title') || '').toLowerCase();
            const skills = (card.getAttribute('data-skills') || '').toLowerCase();
            const cardCat = card.getAttribute('data-category') || '';

            const matchesQuery = !query || title.includes(query) || skills.includes(query);
            const matchesCat = (category === 'all') || (cardCat === category);

            if (matchesQuery && matchesCat) {
                card.style.display = '';
                visibleCount++;
            } else {
                card.style.display = 'none';
            }
        });

        const emptyNotice = document.getElementById('noCareersFound');
        if (emptyNotice) {
            emptyNotice.style.display = (visibleCount === 0) ? 'block' : 'none';
        }
    }

    if (careerSearch) careerSearch.addEventListener('input', filterCareers);
    if (careerCategorySelect) careerCategorySelect.addEventListener('change', filterCareers);

    // Jobs Filter
    const jobSearch = document.getElementById('jobSearchInput');
    const jobTypeSelect = document.getElementById('jobTypeFilter');
    const jobCards = document.querySelectorAll('.job-filter-item');

    function filterJobs() {
        if (!jobCards.length) return;
        const query = (jobSearch ? jobSearch.value : '').toLowerCase().trim();
        const jType = (jobTypeSelect ? jobTypeSelect.value : 'all');

        let visibleCount = 0;
        jobCards.forEach(card => {
            const title = (card.getAttribute('data-title') || '').toLowerCase();
            const company = (card.getAttribute('data-company') || '').toLowerCase();
            const skills = (card.getAttribute('data-skills') || '').toLowerCase();
            const type = card.getAttribute('data-type') || '';

            const matchesQuery = !query || title.includes(query) || company.includes(query) || skills.includes(query);
            const matchesType = (jType === 'all') || (type === jType);

            if (matchesQuery && matchesType) {
                card.style.display = '';
                visibleCount++;
            } else {
                card.style.display = 'none';
            }
        });

        const emptyJobs = document.getElementById('noJobsFound');
        if (emptyJobs) {
            emptyJobs.style.display = (visibleCount === 0) ? 'block' : 'none';
        }
    }

    if (jobSearch) jobSearch.addEventListener('input', filterJobs);
    if (jobTypeSelect) jobTypeSelect.addEventListener('change', filterJobs);
}

/* -------------------------------------------------------------
 * 7. Live Fresher Resume Builder & Preview
 * ------------------------------------------------------------- */
function initResumeLivePreview() {
    const builderForm = document.getElementById('resumeBuilderForm');
    if (!builderForm) return;

    const fields = [
        'fullName', 'email', 'phone', 'college', 'degree',
        'graduationYear', 'careerObjective', 'skillsList', 'projectsList'
    ];

    fields.forEach(field => {
        const input = document.getElementById('res_' + field);
        const preview = document.getElementById('prev_' + field);
        if (input && preview) {
            input.addEventListener('input', function () {
                preview.textContent = this.value || this.getAttribute('placeholder') || '';
            });
        }
    });

    // Print button
    const printBtn = document.getElementById('printResumeBtn');
    if (printBtn) {
        printBtn.addEventListener('click', function () {
            window.print();
        });
    }
}

/* -------------------------------------------------------------
 * Toast Notification Utility
 * ------------------------------------------------------------- */
function showToast(message, type = 'success') {
    let container = document.getElementById('toastContainer');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toastContainer';
        container.style.cssText = 'position:fixed;bottom:24px;right:24px;z-index:9999;display:flex;flex-direction:column;gap:8px;pointer-events:none;';
        document.body.appendChild(container);
    }

    const toast = document.createElement('div');
    const bg = type === 'success' ? '#10b981' : type === 'warning' ? '#f59e0b' : '#ef4444';
    toast.style.cssText = `background:${bg};color:#fff;padding:12px 20px;border-radius:8px;font-size:0.9rem;font-weight:600;box-shadow:0 4px 12px rgba(0,0,0,0.15);transition:all 0.3s ease;transform:translateY(10px);opacity:0;`;
    toast.textContent = message;

    container.appendChild(toast);
    setTimeout(() => {
        toast.style.transform = 'translateY(0)';
        toast.style.opacity = '1';
    }, 10);

    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(-10px)';
        setTimeout(() => toast.remove(), 300);
    }, 3200);
}
