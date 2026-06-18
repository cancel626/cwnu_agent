---
name: Digital Intelligence Oversight
colors:
  surface: '#f3faff'
  surface-dim: '#c7dde9'
  surface-bright: '#f3faff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#e6f6ff'
  surface-container: '#dbf1fe'
  surface-container-high: '#d5ecf8'
  surface-container-highest: '#cfe6f2'
  on-surface: '#071e27'
  on-surface-variant: '#454652'
  inverse-surface: '#1e333c'
  inverse-on-surface: '#dff4ff'
  outline: '#767683'
  outline-variant: '#c6c5d4'
  surface-tint: '#4c56af'
  primary: '#000666'
  on-primary: '#ffffff'
  primary-container: '#1a237e'
  on-primary-container: '#8690ee'
  inverse-primary: '#bdc2ff'
  secondary: '#4555b7'
  on-secondary: '#ffffff'
  secondary-container: '#8999ff'
  on-secondary-container: '#182a8e'
  tertiary: '#181b23'
  on-tertiary: '#ffffff'
  tertiary-container: '#2c3039'
  on-tertiary-container: '#9597a2'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#e0e0ff'
  primary-fixed-dim: '#bdc2ff'
  on-primary-fixed: '#000767'
  on-primary-fixed-variant: '#343d96'
  secondary-fixed: '#dee0ff'
  secondary-fixed-dim: '#bbc3ff'
  on-secondary-fixed: '#000e5e'
  on-secondary-fixed-variant: '#2c3c9e'
  tertiary-fixed: '#e0e2ee'
  tertiary-fixed-dim: '#c4c6d2'
  on-tertiary-fixed: '#181b24'
  on-tertiary-fixed-variant: '#434750'
  background: '#f3faff'
  on-background: '#071e27'
  surface-variant: '#cfe6f2'
typography:
  display-lg:
    fontFamily: Hanken Grotesk
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Hanken Grotesk
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
  headline-md:
    fontFamily: Hanken Grotesk
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  headline-sm:
    fontFamily: Hanken Grotesk
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-sm:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-md:
    fontFamily: JetBrains Mono
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0.05em
  headline-lg-mobile:
    fontFamily: Hanken Grotesk
    fontSize: 28px
    fontWeight: '600'
    lineHeight: 36px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  unit: 4px
  gutter-md: 24px
  margin-edge: 32px
  container-max: 1440px
  stack-gap: 16px
---

## Brand & Style
The design system focuses on a high-fidelity, professional atmosphere tailored for academic administration and data analysis. The aesthetic combines **Corporate Modern** stability with **Glassmorphism** accents to signify cutting-edge "intelligence." 

The target audience consists of university administrators and data analysts who require a high-density information environment that remains legible and authoritative. The UI should evoke a sense of precision, reliability, and technological advancement. Visual interest is maintained through the use of subtle technology-inspired abstract linework—vector paths with varying opacities—that suggests connectivity and flow without distracting from the data.

## Colors
The palette is anchored by **Deep Tech Blue**, providing a foundation of institutional trust. 

- **Primary**: Used for headers, primary navigation sidebars, and key brand moments.
- **Secondary Gradient**: Primary buttons utilize a linear gradient from `#1a237e` to `#3949ab` at a 135-degree angle to provide depth.
- **Backgrounds**: The functional management interface uses a clean white background for high legibility, while "Visual Section" dashboards and login hero areas utilize the Deep Tech Blue to create a "command center" feel.
- **Accents**: Functional red is reserved strictly for destructive actions or critical data errors.

## Typography
This design system utilizes a tiered typography scale to manage high information density. 

**Hanken Grotesk** is used for headlines to provide a sharp, contemporary feel. **Inter** handles the bulk of data entry and reading for its exceptional legibility at small sizes. **JetBrains Mono** is introduced sparingly for data labels, IDs, and system status indicators to lean into the "Tech-driven" narrative. Tighten letter spacing on larger displays to maintain a premium look.

## Layout & Spacing
The system follows a **Fixed Grid** model for the central content area (max-width 1440px) to ensure data visualizations do not become overly distorted on ultra-wide monitors. 

- **Desktop**: 12-column grid, 24px gutters, 32px side margins.
- **Side Navigation**: Fixed at 260px; collapsible to 80px (icon-only).
- **Rhythm**: Use an 8px base grid for component-level spacing, but 4px increments for tight data tables.
- **Responsive**: On tablets, margins reduce to 24px and the sidebar transitions to an overlay drawer.

## Elevation & Depth
The design system employs **Tonal Layers** combined with **Ambient Shadows**. 

Surfaces are distinguished by subtle depth rather than heavy color blocking. 
1. **Base**: The page background.
2. **Floor**: Standard cards use a 1px border (`#e0e0e0`) and a soft shadow (0px 4px 20px rgba(26, 35, 126, 0.05)).
3. **Lift**: Hover states for cards and buttons increase the shadow spread and slightly shift the Y-offset (0px 8px 30px rgba(26, 35, 126, 0.12)).
4. **Overlay**: Modals and dropdowns use a "Glassmorphism" effect with a 12px backdrop blur and 85% opacity white fill to maintain context of the underlying data.

## Shapes
A **Rounded (0.5rem)** logic is applied to balance the "tech" sharpness with modern accessibility.

- **Inputs & Buttons**: 8px (0.5rem) corner radius.
- **Cards**: 16px (1rem) corner radius for a softer, more approachable container.
- **Checkboxes**: 4px radius to maintain a distinct square identity while avoiding harsh corners.
- **Data Tags/Chips**: Fully pill-shaped (100px) to distinguish them from interactive buttons.

## Components
- **Buttons**: Primary buttons feature the Tech Blue gradient. On hover, the elevation increases, and the gradient lightens slightly. Secondary buttons use a Ghost style with a 1px Primary Blue border.
- **Input Fields**: Backgrounds are solid white with an 8px radius. The focus state is marked by a 2px Primary Blue border and a soft blue outer glow.
- **Cards**: All containers for data insights must have the standard soft shadow and 16px padding.
- **Checkboxes**: Use a solid Primary Blue fill when checked, with a white checkmark.
- **Data Tables**: Minimalist approach. No vertical lines; use horizontal dividers in `#f5f5f5`. Row hover states should use the Tertiary Blue color (`#e8eaf6`) at 50% opacity.
- **Transitions**: All interactive states (hover, focus, active) must use a 200ms `ease-in-out` transition for a sophisticated feel.