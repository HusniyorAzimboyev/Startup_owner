# Startup Garage UI Redesign Guide
## Design System v1.0 - Dark Premium Aesthetic

### Overview
Complete redesign moving from Tailwind CSS utility classes to a cohesive design system based on CSS custom properties. Inspired by Linear, Vercel, and Raycast.

---

## 🎨 Design Tokens

### Color Palette
```css
--bg-base: #0b0f1a;              /* Main background */
--bg-surface: #0f1420;           /* Sidebar, nav */
--bg-elevated: #1e2235;          /* Cards, inputs */
--bg-hover: rgba(255,255,255,0.04);

--border: rgba(255,255,255,0.08);
--border-subtle: rgba(255,255,255,0.05);

--text-primary: #f1f5f9;         /* Main text */
--text-secondary: #94a3b8;       /* Secondary text */
--text-muted: #64748b;           /* Muted labels */

--accent: #6366f1;               /* Primary action (indigo) */
--accent-light: #818cf8;         /* Hover state */
--accent-bg: rgba(99,102,241,0.08);

--success: #10b981;
--warning: #f59e0b;
--danger: #ef4444;
```

### Typography Scale
```css
--font-label: 10px;    /* Labels, small UI */
--font-small: 12px;    /* Secondary text */
--font-body: 13px;     /* Default text size */
--font-heading: 15px;  /* Section headings */
--font-title: 20px;    /* Page titles */
--font-xl: 28px;       /* Large headings */

Font weights: 400 (normal), 500 (medium), 600 (semibold), 700 (bold)
```

### Spacing Scale
```css
--space-xs: 4px;       /* Tiny gaps */
--space-sm: 8px;       /* Small margins */
--space-md: 12px;      /* Default spacing */
--space-lg: 20px;      /* Large sections */
--space-xl: 28px;      /* Extra large spacing */
```

### Border Radius
```css
--radius-sm: 6px;      /* Buttons, inputs */
--radius-md: 8px;      /* Standard */
--radius-lg: 12px;     /* Cards */
--radius-xl: 16px;     /* Large elements */
```

---

## 🔧 Component Usage Guide

### Buttons
```html
<!-- Primary button -->
<button class="btn btn-primary">Save</button>

<!-- Secondary button -->
<button class="btn btn-secondary">Cancel</button>

<!-- Ghost button (minimal) -->
<button class="btn btn-ghost">Learn More</button>

<!-- Danger button -->
<button class="btn btn-danger">Delete</button>

<!-- Size variants -->
<button class="btn btn-primary btn-sm">Small</button>
<button class="btn btn-primary btn-lg">Large</button>
<button class="btn btn-primary btn-block">Full Width</button>
```

### Forms
```html
<div class="form-group">
    <label>Email Address</label>
    <input type="email" placeholder="Enter your email">
    <span class="form-error">Invalid email address</span>
</div>

<div class="form-group">
    <label>Message</label>
    <textarea placeholder="Type your message..."></textarea>
</div>
```

### Cards & Surfaces
```html
<!-- Premium card with hover effect -->
<div class="card">
    <h3>Card Title</h3>
    <p>Card content here...</p>
</div>

<!-- Surface (sidebar, nav level) -->
<div class="surface">Content</div>
```

### Alerts & Badges
```html
<!-- Success alert -->
<div class="alert alert-success">✓ Action completed successfully</div>

<!-- Error alert -->
<div class="alert alert-danger">✗ Something went wrong</div>

<!-- Warning alert -->
<div class="alert alert-warning">⚠ Warning message</div>

<!-- Badges -->
<span class="badge badge-success">Active</span>
<span class="badge badge-danger">Inactive</span>
<span class="badge badge-warning">Pending</span>
<span class="badge badge-muted">Draft</span>
```

### Typography
```html
<h1>Page Title</h1>           <!-- 20px, bold -->
<h2>Section Heading</h2>      <!-- 15px, semibold -->
<h3>Subsection</h3>           <!-- 13px, semibold -->
<p>Body text</p>              <!-- 13px, normal -->
<p class="text-secondary">Secondary text</p>  <!-- 13px, muted color -->
<small>Small text</small>     <!-- 12px -->
<label>Label</label>          <!-- 10px, uppercase -->
```

### Layout Utilities
```html
<!-- Flexbox -->
<div class="flex">
    <div>Left</div>
    <div>Right</div>
</div>

<!-- Flex centered -->
<div class="flex-center">
    Centered content
</div>

<!-- Flex space-between -->
<div class="flex-between">
    <span>Left</span>
    <span>Right</span>
</div>

<!-- Grid -->
<div class="grid" style="grid-template-columns: repeat(3, 1fr);">
    <div>Column 1</div>
    <div>Column 2</div>
    <div>Column 3</div>
</div>
```

### Text Utilities
```html
<p class="text-primary">Primary text</p>
<p class="text-secondary">Secondary text</p>
<p class="text-muted">Muted text</p>
<p class="text-accent">Accent colored</p>
<p class="text-success">Success state</p>
<p class="text-danger">Error state</p>
<p class="text-warning">Warning state</p>
```

### Spacing Utilities
```html
<!-- Padding -->
<div class="p-md">Padded box</div>
<div class="px-md">Horizontal padding</div>
<div class="py-md">Vertical padding</div>

<!-- Margin -->
<div class="mb-md">Bottom margin</div>
<div class="mt-lg">Top margin</div>
<div class="mt-xl">Large top margin</div>

<!-- Gap (for flex/grid) -->
<div class="flex gap-md">
    <div>Item 1</div>
    <div>Item 2</div>
</div>
```

### Border Radius
```html
<div class="rounded-sm">6px radius</div>
<div class="rounded-md">8px radius</div>
<div class="rounded-lg">12px radius</div>
<div class="rounded-xl">16px radius</div>
```

---

## 📋 Template Migration Checklist

### Step 1: Update Head Section
```html
<!-- Remove Tailwind -->
<!-- <script src="https://cdn.tailwindcss.com"></script> -->

<!-- Add design system -->
<link rel="stylesheet" href="{% static 'css/design-system.css' %}">
```

### Step 2: Replace Tailwind Classes
Transform Tailwind patterns:
- `bg-gray-900` → `bg-surface`
- `text-gray-400` → `text-secondary`
- `border border-gray-800` → `surface` or inline `border: 1px solid var(--border)`
- `rounded-lg` → `rounded-lg`
- `p-4` → `p-md` or `p-lg`

### Step 3: Use Component Classes
Replace complex Tailwind chains with semantic classes:
- `py-3 px-6 bg-blue-600 hover:bg-blue-700 text-white rounded` → `btn btn-primary`
- `bg-red-900 text-red-200 p-4 rounded` → `alert alert-danger`

### Step 4: Add Transitions
Ensure hover states use the design system transitions:
```css
transition: all var(--transition-fast);
```

---

## 🎯 Key Design Principles

1. **No Utility Soup**: Classes are meaningful and limited
2. **Design Tokens First**: All colors, spacing, and sizing from CSS variables
3. **Minimal Shadows**: Only subtle shadows: `0 1px 3px rgba(0,0,0,0.4)`
4. **Consistent Typography**: Only use specified font sizes
5. **Hover States**: All interactive elements have smooth transitions
6. **Semantic HTML**: Use proper HTML elements (buttons, forms, etc.)

---

## 🚀 Next Steps

1. **Dashboard**: Update dashboard.html to use new component classes
2. **Task Board**: Redesign Kanban board with new card styles
3. **Forms**: Update all form templates (auth, mentor, investor, etc.)
4. **Tables**: Restyle data tables with new design
5. **Modals**: Update modal components

Each template should follow the pattern:
- Remove all Tailwind classes
- Replace with design system classes
- Use CSS variables for any custom styling
- Ensure consistent spacing and typography

---

## 💡 Example: Dashboard Redesign

**Before (Tailwind):**
```html
<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div class="bg-gray-900 border border-gray-800 rounded-xl p-6">
            <h3 class="text-xl font-bold text-white mb-4">Title</h3>
            <p class="text-gray-400">Content</p>
        </div>
    </div>
</div>
```

**After (Design System):**
```html
<div class="container">
    <div class="grid" style="grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));">
        <div class="card">
            <h3>Title</h3>
            <p class="text-secondary">Content</p>
        </div>
    </div>
</div>
```

---

## 📁 File Structure

```
static/
├── css/
│   ├── design-system.css    ← Main design system (CSS custom properties + components)
│   └── custom.css           ← (Optional) Per-page customizations

templates/
├── base.html                 ← Updated to use design system
├── dashboard/
│   └── dashboard.html        ← To be updated
├── accounts/
│   ├── login.html           ← To be updated
│   └── register.html        ← To be updated
├── tasks/
│   └── board.html           ← To be updated
└── ... (other templates)
```

---

## ✅ Quality Checklist

Before shipping a redesigned template:
- [ ] No Tailwind classes remain
- [ ] All colors use CSS variables
- [ ] All spacing uses design tokens
- [ ] Typography sizes follow specification
- [ ] Hover states have transitions
- [ ] Mobile responsive works
- [ ] Accessibility standards met (WCAG)
- [ ] Consistent with Linear/Vercel aesthetic

