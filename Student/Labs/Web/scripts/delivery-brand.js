(() => {
  const defaultBrand = {
    customerName: "Customer",
    workshopName: "Power BI Workshop",
    titleSuffix: "",
    logoPath: "",
    badgePath: "",
    theme: {},
    icons: {}
  };

  const cssVarNames = {
    accent: "--cp-accent",
    accentHover: "--cp-accent-hover",
    accentSoft: "--cp-accent-soft",
    accentForeground: "--cp-accent-fg",
    link: "--cp-link"
  };

  const style = document.createElement("style");
  style.textContent = `
    .delivery-brand {
      display: flex;
      align-items: center;
      gap: 12px;
      min-height: 66px;
      padding: 12px 0;
      border-bottom: 1px solid var(--cp-border);
    }
    .delivery-brand__mark {
      width: 40px;
      height: 40px;
      display: grid;
      flex: 0 0 40px;
      place-items: center;
      overflow: hidden;
      background: var(--cp-accent);
      color: var(--cp-accent-fg);
      border-radius: 0.625rem;
    }
    .delivery-brand__mark svg,
    .delivery-brand__mark img {
      width: 24px;
      height: 24px;
      display: block;
      object-fit: contain;
    }
    .delivery-brand__mark img {
      width: 100%;
      height: 100%;
      padding: 6px;
      background: var(--cp-surface);
    }
    .delivery-brand__badge {
      display: block;
      width: min(100%, 430px);
      max-height: 74px;
      object-fit: contain;
      object-position: left center;
    }
    .delivery-brand__name,
    .delivery-brand__workshop {
      display: block;
      letter-spacing: 0;
    }
    .delivery-brand__name {
      color: var(--cp-text);
      font-size: 1rem;
      font-weight: 800;
    }
    .delivery-brand__workshop {
      color: var(--cp-text-muted);
      font-size: 0.78rem;
    }
    @media (max-width: 620px) {
      .delivery-brand__badge {
        max-height: 58px;
      }
    }
  `;
  document.head.appendChild(style);

  function getCurrentScript() {
    return document.currentScript || [...document.scripts].find((script) =>
      script.src.endsWith("/delivery-brand.js") || script.src.endsWith("\\delivery-brand.js")
    );
  }

  function getConfigPath() {
    const script = getCurrentScript();
    return script?.dataset.config || "scripts/delivery-config.js";
  }

  function mergeBrandConfig(config) {
    return {
      ...defaultBrand,
      ...config,
      theme: {
        ...defaultBrand.theme,
        ...(config?.theme || {})
      },
      icons: {
        ...defaultBrand.icons,
        ...(config?.icons || {})
      }
    };
  }

  function applyTheme(theme) {
    Object.entries(cssVarNames).forEach(([key, cssVar]) => {
      if (theme[key]) {
        document.documentElement.style.setProperty(cssVar, theme[key]);
      }
    });
  }

  function createFallbackIcon() {
    const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    svg.setAttribute("viewBox", "0 0 24 24");
    svg.setAttribute("fill", "none");
    svg.setAttribute("stroke", "currentColor");
    svg.setAttribute("stroke-width", "2");
    svg.setAttribute("stroke-linecap", "round");
    svg.setAttribute("stroke-linejoin", "round");
    svg.setAttribute("aria-hidden", "true");
    const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
    path.setAttribute("d", "M17.8 19.2 16 11l3.5-3.5C21 6 21.5 4 21 3c-1-.5-3 0-4.5 1.5L13 8 4.8 6.2c-.5-.1-.9.1-1.1.5l-.3.5c-.2.5-.1 1 .3 1.3L9 12l-2 3H4l-1 1 4 2 2 4 1-1v-3l3-2 3.5 5.3c.3.4.8.5 1.3.3l.5-.2c.4-.3.6-.7.5-1.2Z");
    svg.appendChild(path);
    return svg;
  }

  function createMark(brand) {
    const mark = document.createElement("span");
    mark.className = "delivery-brand__mark";
    if (brand.logoPath) {
      const image = document.createElement("img");
      image.src = brand.logoPath;
      image.alt = "";
      mark.appendChild(image);
    } else {
      mark.appendChild(createFallbackIcon());
    }
    return mark;
  }

  function createTextBrand(brand) {
    const text = document.createElement("span");
    const customer = document.createElement("strong");
    customer.className = "delivery-brand__name";
    customer.textContent = brand.customerName;
    const workshop = document.createElement("span");
    workshop.className = "delivery-brand__workshop";
    workshop.textContent = brand.workshopName;
    text.append(customer, workshop);
    return text;
  }

  function createBadge(brand) {
    const badge = document.createElement("img");
    badge.className = "delivery-brand__badge";
    badge.src = brand.badgePath;
    badge.alt = `${brand.customerName} ${brand.workshopName}`;
    badge.onerror = () => {
      badge.replaceWith(createMark(brand), createTextBrand(brand));
    };
    return badge;
  }

  function getConfigValue(brand, key) {
    return key.split(".").reduce((value, segment) => value?.[segment], brand);
  }

  function hydrateBrandPlaceholders(brand) {
    document.querySelectorAll("[data-brand-text]").forEach((element) => {
      const value = getConfigValue(brand, element.dataset.brandText);
      if (value !== undefined && value !== null) {
        element.textContent = value;
      }
    });

    document.querySelectorAll("[data-brand-src]").forEach((element) => {
      const value = getConfigValue(brand, element.dataset.brandSrc);
      if (value && "src" in element) {
        element.src = value;
      }
    });
  }

  function renderBrand(brand) {
    applyTheme(brand.theme);
    hydrateBrandPlaceholders(brand);

    const shell = document.querySelector(".shell");
    if (!shell || shell.querySelector(".delivery-brand")) return;

    const masthead = document.createElement("div");
    masthead.className = "delivery-brand";
    masthead.setAttribute("aria-label", `${brand.customerName} ${brand.workshopName}`);

    if (brand.badgePath) {
      masthead.appendChild(createBadge(brand));
    } else {
      masthead.append(createMark(brand), createTextBrand(brand));
    }

    shell.prepend(masthead);

    const suffix = brand.titleSuffix || brand.customerName;
    if (suffix && !document.title.endsWith(`· ${suffix}`)) {
      document.title = `${document.title} · ${suffix}`;
    }
  }

  function whenReady(callback) {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", callback, { once: true });
    } else {
      callback();
    }
  }

  function loadConfig() {
    return new Promise((resolve) => {
      if (window.deliveryBrandConfig) {
        resolve(window.deliveryBrandConfig);
        return;
      }

      const script = document.createElement("script");
      script.src = getConfigPath();
      script.defer = true;
      script.onload = () => resolve(window.deliveryBrandConfig || {});
      script.onerror = () => {
        console.warn(`Delivery branding config was not found at ${script.src}; using defaults.`);
        resolve({});
      };
      document.head.appendChild(script);
    });
  }

  loadConfig().then((config) => {
    const brand = mergeBrandConfig(config);
    whenReady(() => renderBrand(brand));
  });
})();
