/**
 * LAManagement Global Micro-Interactions
 * (AOS Scroll Reveals removed for visibility)
 */

document.addEventListener("DOMContentLoaded", () => {
  // 1. Hover effects refinement
  const interactiveElements = document.querySelectorAll(
    ".btn, .card-hover, .nav-link"
  );
  interactiveElements.forEach((el) => {
    el.addEventListener("mouseenter", () => {
      // Smooth micro-interactions
    });
  });

  // 2. Form Field Animations
  const formControls = document.querySelectorAll(".form-control");
  formControls.forEach((control) => {
    control.addEventListener("focus", () => {
      control.parentElement.classList.add("focused");
    });
    control.addEventListener("blur", () => {
      control.parentElement.classList.remove("focused");
    });
  });
});
