tailwind.config = {
    theme: {
        extend: {
            colors: {
                background: 'var(--background)',
                foreground: 'var(--foreground)',
                accent: 'var(--accent)',
            },
            fontFamily: {
                'system-serif': ['Georgia', 'Cambria', '"Times New Roman"', 'Times', 'serif'],
                'sans': ['-apple-system', 'BlinkMacSystemFont', '"Segoe UI"', 'Roboto', 'Helvetica', 'Arial', 'sans-serif'],
            }
        }
    }
}
