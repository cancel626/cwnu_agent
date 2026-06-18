---
name: Cyber-Academic Pixel Monitor
colors:
  surface: '#10131a'
  surface-dim: '#10131a'
  surface-bright: '#363941'
  surface-container-lowest: '#0b0e15'
  surface-container-low: '#191b23'
  surface-container: '#1d2027'
  surface-container-high: '#272a31'
  surface-container-highest: '#32353d'
  on-surface: '#e1e2ec'
  on-surface-variant: '#c2c6d6'
  inverse-surface: '#e1e2ec'
  inverse-on-surface: '#2d3038'
  outline: '#8c909f'
  outline-variant: '#414754'
  surface-tint: '#adc6ff'
  primary: '#adc6ff'
  on-primary: '#002e69'
  primary-container: '#4c8eff'
  on-primary-container: '#00285d'
  inverse-primary: '#005ac2'
  secondary: '#c7fff0'
  on-secondary: '#00382f'
  secondary-container: '#00f2d1'
  on-secondary-container: '#006a5a'
  tertiary: '#dab9ff'
  on-tertiary: '#460084'
  tertiary-container: '#b072fb'
  on-tertiary-container: '#3d0075'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#d8e2ff'
  primary-fixed-dim: '#adc6ff'
  on-primary-fixed: '#001a41'
  on-primary-fixed-variant: '#004494'
  secondary-fixed: '#26fedc'
  secondary-fixed-dim: '#00dfc1'
  on-secondary-fixed: '#00201a'
  on-secondary-fixed-variant: '#005144'
  tertiary-fixed: '#eedbff'
  tertiary-fixed-dim: '#dab9ff'
  on-tertiary-fixed: '#2a0053'
  on-tertiary-fixed-variant: '#611baa'
  background: '#10131a'
  on-background: '#e1e2ec'
  surface-variant: '#32353d'
typography:
  display-lg:
    fontFamily: Space Grotesk
    fontSize: 48px
    fontWeight: '700'
    lineHeight: '1.1'
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Space Grotesk
    fontSize: 32px
    fontWeight: '700'
    lineHeight: '1.2'
  headline-lg-mobile:
    fontFamily: Space Grotesk
    fontSize: 24px
    fontWeight: '700'
    lineHeight: '1.2'
  title-md:
    fontFamily: Space Grotesk
    fontSize: 20px
    fontWeight: '600'
    lineHeight: '1.4'
  body-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.6'
  body-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 14px
    fontWeight: '400'
    lineHeight: '1.5'
  label-pixel:
    fontFamily: Space Mono
    fontSize: 12px
    fontWeight: '700'
    lineHeight: '1'
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  unit: 4px
  container-margin: 24px
  gutter: 16px
  card-padding: 20px
  sidebar-width: 260px
---

## Brand & Style

The design system is a fusion of **High-Tech Pixel Art** and **Modern Data Analytics**. It targets university administrators who require deep data insights but appreciate a distinctive, energetic interface that breaks away from traditional, sterile enterprise software.

The brand personality is **Intelligent, Vibrant, and Gamified**. It evokes the nostalgia of retro 16-bit era games while maintaining the precision of a high-performance "command center." The emotional response should be one of "controlled excitement"—making data exploration feel like navigating a high-fidelity simulation.

The design movement is a hybrid of **Brutalism (structured layouts/borders)** and **Vaporwave-inspired Digitalism**, utilizing neon accents against deep backgrounds to create a "Big Data Screen" atmosphere.

## Colors

The palette leverages high-contrast vibrancy to differentiate data streams.

- **Primary (Vibrant Tech Blue):** Used for primary actions, active states, and core branding elements.
- **Accents (Neon Green, Electric Purple, Sunset Orange):** Reserved for status indicators (Success, Warning, Critical), data visualization categories, and "Level Up" style labels.
- **Surface Strategy:** The system uses a "Dual-Shell" approach. The navigation (sidebar) remains in a deep, tech-heavy navy to ground the experience, while the main content workspace uses a light grey to ensure readability of dense data tables and charts.
- **Glows:** Accent colors should be used for `box-shadow` glows on dashboard cards to simulate CRT or LED screen effects.

## Typography

To achieve the "pixelated but professional" feel, this design system uses a triple-font strategy:

1. **Space Grotesk (Headlines):** A geometric sans with quirky, technical terminals that mimic the "blocky" feel of pixels without sacrificing legibility.
2. **Plus Jakarta Sans (Body):** A modern, soft sans-serif that ensures long-form data reading is comfortable and contemporary.
3. **Space Mono (Labels):** Used for technical metadata, IDs, and status tags to reinforce the "terminal" aesthetic.

**Styling Note:** For top-level page headers, apply a `text-shadow` of 1px 1px 0px using a secondary accent color to simulate a 16-bit offset effect.

## Layout & Spacing

The layout follows a **Rigid Grid System** based on a 4px baseline, ensuring all elements align with the "pixel block" philosophy.

- **Main Dashboard:** 12-column fluid grid for the main content area. 
- **The Sidebar:** Fixed at 260px. It uses a "Solid Block" presence with no transparency.
- **Top Bar:** Features a "Glassmorphism" effect (`backdrop-filter: blur(10px)`) when scrolling to maintain a sense of depth and modernity against the solid sidebar.
- **Data Screens:** For "Big Data" full-screen views, the layout switches to a fixed-aspect ratio container (16:9) centered in the viewport to maintain the "Dashboard Command Center" integrity regardless of monitor size.

## Elevation & Depth

Depth in this design system is conveyed through **Glowing Outlines** and **Tonal Layering** rather than traditional soft shadows.

- **Level 0 (Floor):** Main content background (#F0F2F5).
- **Level 1 (Cards):** Solid white surface with an 8px "soft-step" shadow (low blur, higher opacity) to feel more physical.
- **Level 2 (Active/Hover):** Cards gain a 2px solid border in the primary color (#3A86FF) with a 4px outer glow (`box-shadow: 0 0 8px rgba(58, 134, 255, 0.4)`).
- **AI Inquiry Bubbles:** Use a high-contrast inverted style (Primary color background with white text) to stand out from the data layer.

## Shapes

The shape language is "Squircle-adjacent." While the vibe is pixel-art, true sharp corners are avoided to maintain a "SaaS" professional feel.

- **Base Components:** 8px (0.5rem) corner radius for all cards and primary containers.
- **Buttons & Input Fields:** 4px (0.25rem) to feel more precise and technical.
- **Icons:** Must be designed on a 24x24 grid using blocky, non-anti-aliased strokes to maintain the pixel-art aesthetic.

## Components

- **Buttons:** Use a "3D Block" style. A solid 2px bottom border (darker shade of the button color) that disappears on `active` state to simulate a physical press.
- **Dashboard Cards:** Must include a "Header-Strip"—a 4px solid top-border using one of the accent colors (Green, Purple, or Orange) to categorize the data type.
- **Tables:** Use a "Zebra" pattern with #F8F9FA. Row hovers should use a very pale version of the primary blue (#3A86FF at 5% opacity).
- **AI Inquiry (Intelligent Query):** Chat bubbles use a "Pixel-Tail" design—a blocky triangular pointer at the bottom of the bubble.
- **Glow Borders:** Reserved for "Hot Data" or "Live Alerts" on the dashboard. Use a CSS animation to pulse the border-color between Primary and Secondary accents.
- **Status Chips:** Small, rectangular tags with `Space Mono` font. No rounded corners for chips; they should look like "Pixels."