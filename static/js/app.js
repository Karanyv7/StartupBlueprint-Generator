/**
 * Blueprint AI — Core JavaScript
 * Handles: dark/light mode, sidebar, toasts, shared utils
 */

// ── 1. THEME MANAGEMENT ────────────────────────────────────────────────
const THEME_KEY = "blueprint-ai-theme";

function getTheme() {
  return localStorage.getItem(THEME_KEY) || "dark";
}

function setTheme(theme) {
  document.documentElement.setAttribute("data-theme", theme);
  localStorage.setItem(THEME_KEY, theme);
  const icon = document.getElementById("themeIcon");
  if (icon) {
    icon.className = theme === "dark" ? "bi bi-moon-stars-fill" : "bi bi-sun-fill";
  }
}

function toggleTheme() {
  const current = getTheme();
  setTheme(current === "dark" ? "light" : "dark");
}

// Apply theme on load immediately to avoid flash
(function () {
  document.documentElement.setAttribute("data-theme", getTheme());
})();

// ── 2. SIDEBAR MANAGEMENT ──────────────────────────────────────────────
function openSidebar() {
  document.getElementById("sidebar").classList.add("open");
  document.getElementById("sidebarOverlay").classList.add("open");
  document.body.style.overflow = "hidden";
}

function closeSidebar() {
  document.getElementById("sidebar").classList.remove("open");
  document.getElementById("sidebarOverlay").classList.remove("open");
  document.body.style.overflow = "";
}

function toggleSidebar() {
  const sidebar = document.getElementById("sidebar");
  if (sidebar.classList.contains("open")) {
    closeSidebar();
  } else {
    openSidebar();
  }
}

// ── 3. TOAST NOTIFICATIONS ─────────────────────────────────────────────
const TOAST_ICONS = {
  success: "bi-check-circle-fill",
  error:   "bi-x-circle-fill",
  warning: "bi-exclamation-triangle-fill",
  info:    "bi-info-circle-fill",
};

function showToast(message, type = "info", duration = 3500) {
  const container = document.getElementById("toastContainer");
  if (!container) return;

  const toast = document.createElement("div");
  toast.className = `toast-custom toast-${type}`;
  toast.innerHTML = `
    <i class="bi ${TOAST_ICONS[type] || TOAST_ICONS.info} toast-icon"></i>
    <span>${message}</span>
    <button onclick="this.parentElement.remove()" style="
      background:none;border:none;color:var(--text-muted);
      cursor:pointer;margin-left:auto;font-size:14px;padding:0;"
    ><i class="bi bi-x"></i></button>
  `;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = "0";
    toast.style.transition = "opacity 0.4s";
    setTimeout(() => toast.remove(), 400);
  }, duration);
}

// ── 4. COPY RESULT HELPER ──────────────────────────────────────────────
function copyResult(elementId) {
  const el = document.getElementById(elementId);
  if (!el) return;
  navigator.clipboard.writeText(el.innerText)
    .then(() => showToast("Copied to clipboard!", "success"))
    .catch(() => showToast("Copy failed. Please select and copy manually.", "warning"));
}

// ── 5. DOM READY INIT ──────────────────────────────────────────────────
document.addEventListener("DOMContentLoaded", () => {
  // Apply saved theme
  setTheme(getTheme());

  // Theme toggle button
  const themeToggle = document.getElementById("themeToggle");
  if (themeToggle) themeToggle.addEventListener("click", toggleTheme);

  // Sidebar toggle (mobile)
  const sidebarToggle = document.getElementById("sidebarToggle");
  if (sidebarToggle) sidebarToggle.addEventListener("click", toggleSidebar);

  // Sidebar overlay click to close
  const sidebarOverlay = document.getElementById("sidebarOverlay");
  if (sidebarOverlay) sidebarOverlay.addEventListener("click", closeSidebar);

  // Close sidebar on nav item click (mobile)
  document.querySelectorAll(".nav-item").forEach(item => {
    item.addEventListener("click", () => {
      if (window.innerWidth < 992) closeSidebar();
    });
  });

  // Auto-close sidebar on resize to desktop
  window.addEventListener("resize", () => {
    if (window.innerWidth >= 992) closeSidebar();
  });

  // Smooth reveal for animated elements
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.style.visibility = "visible";
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.1 }
  );

  document.querySelectorAll(".animate-fadeInUp").forEach(el => {
    el.style.visibility = "hidden";
    observer.observe(el);
    // Fallback: ensure visible after 1s
    setTimeout(() => { el.style.visibility = "visible"; }, 1000);
  });

  // Keyboard shortcut: Escape closes sidebar
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") closeSidebar();
  });

  // Add active state feedback to buttons
  document.querySelectorAll(".btn-primary-custom").forEach(btn => {
    btn.addEventListener("click", function () {
      this.classList.add("btn-clicked");
      setTimeout(() => this.classList.remove("btn-clicked"), 150);
    });
  });
});

// ── 6. UTILITY: DEBOUNCE ──────────────────────────────────────────────
function debounce(fn, delay) {
  let timer;
  return function (...args) {
    clearTimeout(timer);
    timer = setTimeout(() => fn.apply(this, args), delay);
  };
}

// ── 7. UTILITY: FORMAT DATE ───────────────────────────────────────────
function formatDate(isoString) {
  const d = new Date(isoString);
  return d.toLocaleString("en-US", {
    month: "short", day: "numeric", year: "numeric",
    hour: "2-digit", minute: "2-digit",
  });
}

// ── 8. NAVBAR SCROLL EFFECT ───────────────────────────────────────────
window.addEventListener("scroll", debounce(() => {
  const navbar = document.getElementById("topNavbar");
  if (navbar) {
    navbar.style.boxShadow = window.scrollY > 10
      ? "0 4px 20px rgba(0,0,0,0.3)"
      : "none";
  }
}, 50));
