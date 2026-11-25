/* «Корочки.есть»: меню, клиентская валидация, анимации. */
(() => {
  "use strict";

  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ------------------------------------------------------------------
     Мобильное меню
     ------------------------------------------------------------------ */
  const navToggle = document.querySelector("[data-nav-toggle]");
  const nav = document.querySelector("#main-nav");
  if (navToggle && nav) {
    navToggle.addEventListener("click", () => {
      const open = navToggle.getAttribute("aria-expanded") === "true";
      navToggle.setAttribute("aria-expanded", String(!open));
      navToggle.setAttribute("aria-label", open ? "Открыть меню" : "Закрыть меню");
      nav.classList.toggle("is-open", !open);
    });

    nav.addEventListener("click", (event) => {
      if (event.target.closest("a")) {
        nav.classList.remove("is-open");
        navToggle.setAttribute("aria-expanded", "false");
      }
    });
  }

  /* ------------------------------------------------------------------
     Клиентская валидация (серверная всё равно обязательна)
     ------------------------------------------------------------------ */
  const patterns = {
    login: [/^[A-Za-zА-Яа-яЁё0-9_]{3,}$/, "Никнейм: буквы, цифры и _, минимум 3 символа."],
    password: [/^.{8,}$/, "Пароль: минимум 8 символов."],
  };

  function setError(field, message) {
    field.setAttribute("aria-invalid", "true");
    const holder = field.closest(".field");
    let box = holder && holder.querySelector(".field-error");
    if (!box && holder) {
      box = document.createElement("p");
      box.className = "field-error";
      holder.appendChild(box);
    }
    if (box) box.textContent = message;
  }

  function clearError(field) {
    field.removeAttribute("aria-invalid");
    const holder = field.closest(".field");
    const box = holder && holder.querySelector(".field-error");
    if (box) box.textContent = "";
  }

  function validateField(field) {
    if (field.name === "password2") {
      const first = document.querySelector("#password");
      if (field.value !== first.value) {
        setError(field, "Пароли не совпадают.");
        return false;
      }
      clearError(field);
      return true;
    }
    const rule = patterns[field.name];
    if (!rule) return true;
    const value = field.value.trim();
    if (!rule[0].test(value)) {
      setError(field, rule[1]);
      return false;
    }
    clearError(field);
    return true;
  }

  const registerForm = document.querySelector("#register-form");
  if (registerForm) {
    registerForm.querySelectorAll("input[name]").forEach((field) => {
      field.addEventListener("blur", () => validateField(field));
    });
    registerForm.addEventListener("submit", (event) => {
      let ok = true;
      let first = null;
      registerForm.querySelectorAll("input[name]").forEach((field) => {
        if (!validateField(field)) {
          ok = false;
          first = first || field;
        }
      });
      if (!ok) {
        event.preventDefault();
        if (first) first.focus();
      }
    });
  }

  const applicationForm = document.querySelector("#application-form");
  if (applicationForm) {
    applicationForm.addEventListener("submit", (event) => {
      let ok = true;
      let first = null;
      const course = applicationForm.querySelector("[name=course_id]");
      const date = applicationForm.querySelector("[name=start_date]");
      const payment = applicationForm.querySelector("[name=payment_method]:checked");

      if (!course.value) {
        setError(course, "Выберите курс из списка.");
        ok = false; first = first || course;
      } else clearError(course);

      if (!/^\d{2}\.\d{2}\.\d{4}$/.test(date.value.trim())) {
        setError(date, "Дата в формате ДД.ММ.ГГГГ.");
        ok = false; first = first || date;
      } else clearError(date);

      if (!payment) {
        const holder = applicationForm.querySelector(".radio-group");
        let box = holder.querySelector(".field-error");
        if (!box) {
          box = document.createElement("p");
          box.className = "field-error";
          holder.appendChild(box);
        }
        box.textContent = "Выберите способ оплаты.";
        ok = false;
      }

      if (!ok) {
        event.preventDefault();
        if (first) first.focus();
      }
    });
  }

  /* ------------------------------------------------------------------
     Подсветка появления карточек
     ------------------------------------------------------------------ */
  if ("IntersectionObserver" in window && !reduceMotion) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12 });
    document.querySelectorAll(".reveal").forEach((node) => observer.observe(node));
  }
})();
