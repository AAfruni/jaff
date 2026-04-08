// Mermaid initialization for JAFF documentation
// Initialize Mermaid with custom theme matching JAFF colors

// Wait for DOM to be ready
document$.subscribe(() => {
  // Initialize Mermaid
  mermaid.initialize({
    startOnLoad: true,
    theme: "base",
    themeVariables: {
      // Primary colors - matching JAFF slate theme
      primaryColor: "#f8fafc",
      primaryTextColor: "#1e293b",
      primaryBorderColor: "#cbd5e1",
      lineColor: "#94a3b8",
      secondaryColor: "#e0f2fe",
      tertiaryColor: "#f1f5f9",

      // Background and text
      background: "#ffffff",
      mainBkg: "#f8fafc",
      secondBkg: "#f1f5f9",
      textColor: "#1e293b",

      // Node styling
      nodeBorder: "#cbd5e1",
      clusterBkg: "#f8fafc",
      clusterBorder: "#cbd5e1",

      // Edge/line styling
      edgeLabelBackground: "#ffffff",

      // Git graph (if used)
      git0: "#334155",
      git1: "#0284c7",
      git2: "#059669",
      git3: "#d97706",

      // Font
      fontFamily:
        'Roboto, -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif',
      fontSize: "14px",
    },
    flowchart: {
      htmlLabels: true,
      curve: "basis",
      padding: 15,
    },
    securityLevel: "loose",
  });

  // Detect theme changes and reinitialize Mermaid
  const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
      if (mutation.attributeName === "data-md-color-scheme") {
        const scheme = document.body.getAttribute("data-md-color-scheme");

        // Update theme based on color scheme
        if (scheme === "slate") {
          mermaid.initialize({
            theme: "dark",
            themeVariables: {
              primaryColor: "#1e293b",
              primaryTextColor: "#f1f5f9",
              primaryBorderColor: "#475569",
              lineColor: "#64748b",
              secondaryColor: "#0f172a",
              tertiaryColor: "#334155",
              background: "#0f172a",
              mainBkg: "#1e293b",
              secondBkg: "#334155",
              textColor: "#f1f5f9",
              nodeBorder: "#475569",
              clusterBkg: "#1e293b",
              clusterBorder: "#475569",
              edgeLabelBackground: "#1e293b",
              fontFamily:
                'Roboto, -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif',
              fontSize: "14px",
            },
          });
        } else {
          mermaid.initialize({
            theme: "base",
            themeVariables: {
              primaryColor: "#f8fafc",
              primaryTextColor: "#1e293b",
              primaryBorderColor: "#cbd5e1",
              lineColor: "#94a3b8",
              secondaryColor: "#e0f2fe",
              tertiaryColor: "#f1f5f9",
              background: "#ffffff",
              mainBkg: "#f8fafc",
              secondBkg: "#f1f5f9",
              textColor: "#1e293b",
              nodeBorder: "#cbd5e1",
              clusterBkg: "#f8fafc",
              clusterBorder: "#cbd5e1",
              edgeLabelBackground: "#ffffff",
              fontFamily:
                'Roboto, -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif',
              fontSize: "14px",
            },
          });
        }

        // Re-render all Mermaid diagrams
        document.querySelectorAll(".mermaid").forEach((element) => {
          const graphDefinition = element.textContent;
          element.removeAttribute("data-processed");
          element.innerHTML = graphDefinition;
        });
        mermaid.init(undefined, document.querySelectorAll(".mermaid"));
      }
    });
  });

  // Observe theme changes
  observer.observe(document.body, {
    attributes: true,
    attributeFilter: ["data-md-color-scheme"],
  });
});
