# Design System Specification: The Ethereal Canvas

## 1. Creative North Star: The Silent Architect
This design system is built on the philosophy of "Invisible Structure." Inspired by the precision of Apple’s hardware and the conversational fluidity of ChatGPT, the goal is to create a digital environment that feels like a physical space—specifically, a high-end gallery. 

We break the "template" look by moving away from rigid boxes and high-contrast dividers. Instead, we use **intentional asymmetry**, **overlapping glass layers**, and **tonal depth**. The interface shouldn't feel like a website; it should feel like a series of light-filled surfaces floating in a silver atmosphere.

---

## 2. Color & Atmospheric Theory
The palette is a sophisticated range of silvers, whites, and "cool" neutrals. We use color to define space, not just decoration.

### The "No-Line" Rule
**Explicit Instruction:** Do not use 1px solid borders to define sections. A section should be distinguished from its neighbor only through background shifts (e.g., a `surface-container-low` section resting on a `background` base) or a transition in the ambient gradient.

### Surface Hierarchy & Nesting
Treat the UI as a series of stacked, semi-translucent sheets. 
- **Base Level:** `background` (#f9f9fb) or `surface`.
- **Primary Content Area:** `surface-container-low` (#f2f4f6).
- **Interactive Cards/Floating Elements:** `surface-container-lowest` (#ffffff).
- **Deep Insets (Search bars/Inputs):** `surface-container-high` (#e4e9ee).

### The Glass & Gradient Rule
To achieve the "Silver + White" mood, utilize `tertiary-container` (#b088fe) at 5-10% opacity as a background glow behind glass containers. This provides the signature "purple/blue" accent without overwhelming the silver aesthetic.
- **CTA Soul:** Main buttons should use a linear gradient from `primary` (#5f5e60) to `primary-dim` (#535254) to avoid the "flat" look of standard grey buttons.

---

## 3. Typography: The Editorial Voice
We use **Inter** exclusively. The identity is conveyed through extreme scale—pairing massive, light-weight display text with tight, functional labels.

| Level | Token | Weight | Letter Spacing | Purpose |
| :--- | :--- | :--- | :--- | :--- |
| **Display** | `display-lg` (3.5rem) | 300 (Light) | -0.02em | Hero statements, high-impact editorial. |
| **Headline** | `headline-md` (1.75rem) | 500 (Medium) | -0.01em | Section headers, major navigation. |
| **Title** | `title-md` (1.125rem) | 600 (Semi-Bold) | 0 | Component headers, card titles. |
| **Body** | `body-lg` (1rem) | 400 (Regular) | 0 | Long-form reading, descriptions. |
| **Label** | `label-md` (0.75rem) | 700 (Bold) | +0.05em | Uppercase metadata, small captions. |

---

## 4. Elevation & Depth: Tonal Layering
Traditional shadows are too heavy for this system. We use **Ambient Depth**.

*   **The Layering Principle:** Depth is achieved by stacking surface tiers. A `surface-container-lowest` card placed on a `surface-container-low` background creates a natural "lift" through contrast alone.
*   **Ambient Shadows:** If a floating element (like a Modal) requires a shadow, use a diffuse spread: `0 20px 40px rgba(45, 51, 56, 0.06)`. The shadow color is a 6% opacity version of `on-surface` (#2d3338), mimicking soft daylight.
*   **The Ghost Border:** If a boundary is required for accessibility, use `outline-variant` (#acb3b8) at **15% opacity**. Never use a 100% opaque border.
*   **Glassmorphism:** For top navigation and floating sidebars, use:
    *   Background: `surface-container-lowest` at 70% opacity.
    *   Backdrop-filter: `blur(20px)`.
    *   Border: 1px solid `white` (20% opacity) for a "shimmer" edge.

---

## 5. Component Guidelines

### Buttons (The Tactile Interaction)
*   **Primary:** Gradient from `primary` to `primary-dim`. Corner radius: `lg` (1rem). 
*   **Secondary:** `surface-container-highest` background. No border. Soft lift (1px) on hover.
*   **Tertiary/Ghost:** No background. Text color: `primary`. On hover, a 5% `tertiary-fixed` glow appears behind the text.

### Input Fields (The Deep Inset)
Avoid the "boxed" look. Use `surface-container-high` as the background with a `xl` (1.5rem) corner radius. On focus, apply a subtle glow using `tertiary-fixed-dim` at 20% opacity rather than a thick border.

### Cards & Lists (The Modern Feed)
*   **Prohibition:** Forbid divider lines. 
*   **The Spacing Rule:** Use `spacing.8` (2.75rem) or `spacing.10` (3.5rem) to separate content blocks. 
*   **Interaction:** On hover, a card should shift from `surface-container-low` to `surface-container-lowest` and lift by 4px.

### Specialized Component: The "Aura" Chip
For tags or status indicators, use a transparent background with a 2px inner glow of `tertiary` (#6f48b8) and a blur of 8px. This creates the "Signature Glow" requested in the mood board.

---

## 6. Do's & Don'ts

### Do
*   **Do** use asymmetrical padding (e.g., more padding on the top than the bottom) to create an editorial, "curated" feel.
*   **Do** embrace negative space. If you think there is enough whitespace, add 20% more.
*   **Do** use `surface-bright` for areas meant to catch the user's eye first.

### Don't
*   **Don't** use pure black (#000000). Always use `on-surface` (#2d3338) to keep the "Silver" tonality.
*   **Don't** use the `DEFAULT` (0.5rem) corner radius. Stick to `lg` (1rem) or `xl` (1.5rem) to maintain the premium, soft-touch feel.
*   **Don't** use standard "drop shadows" with zero-blur or high-opacity. If it looks like a shadow, it’s too dark. It should look like "air."