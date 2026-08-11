---
name: Artisan Corporate Heritage
colors:
  surface: '#f9f9fc'
  surface-dim: '#dadadc'
  surface-bright: '#f9f9fc'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f3f3f6'
  surface-container: '#eeeef0'
  surface-container-high: '#e8e8ea'
  surface-container-highest: '#e2e2e5'
  on-surface: '#1a1c1e'
  on-surface-variant: '#524342'
  inverse-surface: '#2f3133'
  inverse-on-surface: '#f0f0f3'
  outline: '#857372'
  outline-variant: '#d7c2c0'
  surface-tint: '#8a4d4b'
  primary: '#2f0608'
  on-primary: '#ffffff'
  primary-container: '#4a1a1a'
  on-primary-container: '#c57e7b'
  inverse-primary: '#ffb3b0'
  secondary: '#775a19'
  on-secondary: '#ffffff'
  secondary-container: '#fed488'
  on-secondary-container: '#785a1a'
  tertiary: '#151612'
  on-tertiary: '#ffffff'
  tertiary-container: '#2a2a26'
  on-tertiary-container: '#92918c'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#ffdad8'
  primary-fixed-dim: '#ffb3b0'
  on-primary-fixed: '#380c0d'
  on-primary-fixed-variant: '#6e3635'
  secondary-fixed: '#ffdea5'
  secondary-fixed-dim: '#e9c176'
  on-secondary-fixed: '#261900'
  on-secondary-fixed-variant: '#5d4201'
  tertiary-fixed: '#e5e2dc'
  tertiary-fixed-dim: '#c9c6c1'
  on-tertiary-fixed: '#1c1c18'
  on-tertiary-fixed-variant: '#474743'
  background: '#f9f9fc'
  on-background: '#1a1c1e'
  surface-variant: '#e2e2e5'
typography:
  display-lg:
    fontFamily: Playfair Display
    fontSize: 56px
    fontWeight: '700'
    lineHeight: 64px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Playfair Display
    fontSize: 40px
    fontWeight: '700'
    lineHeight: 48px
  headline-lg-mobile:
    fontFamily: Playfair Display
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
  headline-md:
    fontFamily: Playfair Display
    fontSize: 28px
    fontWeight: '600'
    lineHeight: 36px
  title-lg:
    fontFamily: Inter
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
  label-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 20px
    letterSpacing: 0.01em
  label-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  unit: 8px
  container-max-width: 1280px
  gutter: 24px
  margin-desktop: 64px
  margin-mobile: 20px
  stack-sm: 8px
  stack-md: 16px
  stack-lg: 32px
  section-gap: 80px
---

## Brand & Style
The design system is engineered for a large-scale confectionery enterprise that balances industrial precision with artisanal heritage. The brand personality is prestigious, authoritative, and clinical, avoiding the whimsical tropes of the candy industry in favor of a "Clean Architecture" aesthetic. It targets B2B partners, investors, and high-level stakeholders, evoking a sense of trust, quality control, and long-standing tradition.

The visual style is **Corporate Modern** with a focus on high-end editorial layouts. It utilizes generous whitespace, structured grids, and a sophisticated color palette to differentiate the enterprise from consumer-facing retail brands. The emotional response should be one of "Reliable Luxury"—where the manufacturing process is viewed as a refined craft.

## Colors
The palette is rooted in a deep burgundy-chocolate (`#4A1A1A`), representing the core product and corporate heritage. This is accented by a refined gold (`#C5A059`) used sparingly for prestige elements and interactive states. 

The background utilizes a clinical "Gallery White" and a very light gray to maintain a professional, organized atmosphere in technical or production-heavy modules. Corporate trust is reinforced through a deep navy-teal used for secondary information and status indicators. All status colors are desaturated and darkened to maintain the premium corporate tone, ensuring they do not appear "neon" or "playful."

## Typography
The typographic hierarchy uses a "High-Contrast" pairing. **Playfair Display** is reserved for large headlines and display moments to evoke a premium, editorial feel (e.g., *“Sifat va Meros”*). **Inter** provides a highly functional, neutral base for body text, data tables, and technical specifications, ensuring maximum readability in industrial contexts.

Uzbek (Latin) character sets must be fully supported. For large display text, use a slight negative letter-spacing to enhance the "luxury" feel. For labels and captions, use medium weight with increased tracking to improve legibility on clinical white backgrounds.

## Layout & Spacing
The layout follows a **Fixed Grid** philosophy on desktop to maintain a controlled, structured environment. A 12-column grid is used with 24px gutters. Consistency is maintained through an 8px base unit. 

Spacing is intentionally generous; sections are separated by large gaps (80px+) to prevent the interface from feeling "crowded," which mirrors the clean, organized nature of a modern manufacturing facility. On mobile, margins reduce to 20px, and the layout reflows to a single column, prioritizing vertical readability and clear tap targets.

## Elevation & Depth
Depth is communicated through **Tonal Layers** and extremely soft, ambient shadows. We avoid heavy dropshadows or complex blurs.

1.  **Base Layer:** White or `#F9F6F0` (Cream) for page backgrounds.
2.  **Surface Layer:** High-white cards with a 1px border in a very light neutral-gray (`#E5E7EB`).
3.  **Elevation:** Use a dual-shadow approach for interactive cards: a very soft, large-radius ambient shadow (15% opacity primary color tint) to suggest the object is lifting off the surface without appearing "floating" in a void.
4.  **No Glassmorphism:** Surfaces remain opaque and solid to reflect the physical stability of the enterprise.

## Shapes
The shape language is "Soft-Professional." A base roundedness of 8px (`rounded-md`) is used for standard components like buttons and inputs. This provides a modern touch without the "bubbliness" of consumer apps. Larger containers and cards use 16px (`rounded-lg`) to soften the overall architectural feel of the grid.

## Components
-   **Buttons:** The primary button (e.g., *“Batafsil ma’lumot”*) uses the primary burgundy background with white text. The secondary button uses a 1px gold border with gold text. Hover states should involve a subtle shift in luminosity rather than a color change.
-   **Inputs:** Fields are clean with a 1px light gray border. Focus states use a subtle gold glow or a 2px gold bottom border. Labels (*“Ism-sharifingiz”*) are always visible in `label-md`.
-   **Cards:** Use for production stats or product categories. Cards should have no border when elevated by a shadow, or a 1px border when flat.
-   **Chips/Status:** Used for manufacturing status (e.g., *“Tayyor”*, *“Jarayonda”*). These use a "Tonal" style—light background versions of the status colors with dark text of the same hue.
-   **Data Tables:** Essential for enterprise reporting. Use `body-md` for row data and `label-sm` (uppercase) for headers. Row separators should be minimal (1px hairline).