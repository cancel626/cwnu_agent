---
name: Pixel Future Intelligence
colors:
  surface: '#121414'
  surface-dim: '#121414'
  surface-bright: '#383939'
  surface-container-lowest: '#0d0e0f'
  surface-container-low: '#1b1c1c'
  surface-container: '#1f2020'
  surface-container-high: '#292a2a'
  surface-container-highest: '#343535'
  on-surface: '#e3e2e2'
  on-surface-variant: '#b9cacb'
  inverse-surface: '#e3e2e2'
  inverse-on-surface: '#303031'
  outline: '#849495'
  outline-variant: '#3a494b'
  surface-tint: '#00dbe7'
  primary: '#e1fdff'
  on-primary: '#00363a'
  primary-container: '#00f2ff'
  on-primary-container: '#006a71'
  inverse-primary: '#00696f'
  secondary: '#d7ffc5'
  on-secondary: '#053900'
  secondary-container: '#2ff801'
  on-secondary-container: '#0f6d00'
  tertiary: '#fff5f8'
  on-tertiary: '#5e0053'
  tertiary-container: '#ffccee'
  on-tertiary-container: '#af009d'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#74f5ff'
  primary-fixed-dim: '#00dbe7'
  on-primary-fixed: '#002022'
  on-primary-fixed-variant: '#004f54'
  secondary-fixed: '#79ff5b'
  secondary-fixed-dim: '#2ae500'
  on-secondary-fixed: '#022100'
  on-secondary-fixed-variant: '#095300'
  tertiary-fixed: '#ffd7f0'
  tertiary-fixed-dim: '#fface8'
  on-tertiary-fixed: '#3a0033'
  on-tertiary-fixed-variant: '#840076'
  background: '#121414'
  on-background: '#e3e2e2'
  surface-variant: '#343535'
typography:
  headline-lg:
    fontFamily: Hanken Grotesk
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.02em
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
    fontFamily: Hanken Grotesk
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-md:
    fontFamily: Hanken Grotesk
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-tech:
    fontFamily: JetBrains Mono
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0.05em
  label-code:
    fontFamily: JetBrains Mono
    fontSize: 10px
    fontWeight: '400'
    lineHeight: 14px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 8px
  xs: 4px
  sm: 12px
  md: 20px
  lg: 32px
  xl: 48px
  gutter: 16px
  margin-mobile: 16px
  margin-desktop: 40px
---

## Brand & Style

The design system embodies a "Pixel Future" aesthetic, bridging the gap between retro-computing nostalgia and cutting-edge data science. It is designed for the academic community at Xihua Normal University, evoking a sense of "Digital Intelligence" that feels both technically sophisticated and visually energetic.

The visual style is a hybrid of **Vaporwave-inspired Futurism** and **Glassmorphism**. It utilizes a deep-space canvas to allow neon data visualizations to pop, while subtle pixelated motifs—such as dithered gradients and stepped border treatments—provide a distinct identity. The interface should feel like a high-end command center: authoritative, immersive, and high-performance.

## Colors

The palette is rooted in a "Deep Dark" environment to minimize eye strain during long periods of data analysis. 

- **Primary (Cyber Blue):** Used for interactive elements, primary call-to-actions, and "active" data states.
- **Secondary (Matrix Green):** Reserved for "success" states, growth indicators, and secondary data streams.
- **Surface Strategy:** Surfaces use a slightly elevated dark grey (#1a1a1e) with varying levels of transparency (60-80%) to facilitate glassmorphism effects.
- **Glows:** Interactive elements utilize a 10-15px outer glow (drop shadow) using the Primary or Secondary hex codes with 40% opacity to simulate neon light emission.

## Typography

This design system uses a dual-font approach to balance readability with a "tech-heavy" atmosphere. 

**Hanken Grotesk** serves as the primary sans-serif typeface for headlines and body copy. Its clean, sharp geometry maintains high legibility even at small scales on data dashboards.

**JetBrains Mono** is utilized for metadata, data labels, timestamps, and "system status" messages. This monospaced font reinforces the "intelligence" aspect of the platform, making every piece of data feel like a line of live code. All tech labels should favor a slightly increased letter spacing to enhance the digital terminal feel.

## Layout & Spacing

The layout follows a **Fluid Grid** system based on an 8px rhythmic increment. 

- **Mobile:** Uses a 4-column grid with 16px side margins. Elements reflow vertically into stacked cards.
- **Desktop:** Transition to a 12-column grid. Complex data insights are housed in widgets that span 3, 4, or 6 columns.
- **Pixel Alignment:** While the layout is fluid, component internal padding should strictly adhere to the 8px base unit to ensure a "blocky," structured feel that aligns with the pixelated accents.

## Elevation & Depth

Elevation in this design system is achieved through **Tonal Stacking** and **Glassmorphism** rather than traditional soft shadows.

1.  **Background (Level 0):** Solid #0a0a0c.
2.  **Base Layer (Level 1):** Solid #1a1a1e for large containers.
3.  **Glass Layer (Level 2):** 70% opacity #1a1a1e with a 20px backdrop blur and a 1px inner border (Primary color at 20% opacity).
4.  **Floating Elements (Level 3):** High-opacity glass with a distinct "Neon Glow" (Drop shadow: 0px 4px 20px, Primary color @ 0.3 opacity).

Avoid muddy shadows; use light (inner glows) and blur to define depth.

## Shapes

The shape language is defined by a consistent **12px (0.75rem)** radius for standard UI components. 

A unique "Pixel Notch" treatment is applied to primary cards and buttons: a small 45-degree chamfer or a 1px "stepped" corner detail is used on the top-right corner of containers to reinforce the pixelated aesthetic. Buttons and input fields maintain the standard 12px roundedness to ensure ergonomic comfort and a modern feel.

## Components

### Buttons & Chips
Buttons are high-contrast. The primary button uses a solid Cyber Blue fill with black text. On hover, it gains an intense outer glow. Chips use a 1px Cyber Blue stroke and JetBrains Mono for the text.

### Pixel-Styled Cards
Cards feature a semi-transparent glass background. The border is a "Dual-Tone" stroke: a solid 1px border with a secondary, thinner neon glow on the top and left edges only.

### Mobile Tab Bar
A fixed bottom bar using a heavy backdrop blur (Glassmorphism). Active states are indicated by a 2px Cyber Blue line at the top of the icon and a faint vertical gradient glow.

### Tech Message Bubbles
Message bubbles are rectangular with the 12px roundedness, but the "tail" is replaced by a sharp 4px pixel block. Backgrounds are tinted #1a1a1e with Primary color text for system messages.

### Glassy Drawer
Drawers slide in from the bottom or right using a 90% opaque #1a1a1e surface with a prominent "Pixel Notch" handle at the top-center. All content inside uses JetBrains Mono for metadata and Hanken Grotesk for primary information.