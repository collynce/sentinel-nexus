import {
    defineConfig,
    presetAttributify,
    presetIcons,
    presetTypography,
    presetWebFonts,
    presetWind3,
    transformerDirectives,
    transformerVariantGroup,
  } from 'unocss'
  import presetAnimations from 'unocss-preset-animations'
  import { builtinColors, presetShadcn } from 'unocss-preset-shadcn'
  
  export default defineConfig({
    variants: [
      {
        // nth-[]:class
        name: ':nth-child()',
        match: (matcher: string) => {
          const match = matcher.match(/^nth-\[(.+?):/)
          if (!match)
            return matcher
          return {
            // slice `hover:` prefix and passed to the next variants and rules
            matcher: matcher.substring(match[0].length),
            selector: s => `${s}:nth-child(${match[1]})`,
          }
        },
        multiPass: true,
      },
    ],
    theme: {
      animation: {
        keyframes: {
          'spin-slow': '{from{transform:rotate(0deg)}to{transform:rotate(360deg)}}',
        },
        counts: {
          'spin-slow': 'infinite',
        },
        durations: {
          'spin-slow': '3s',
        },
      },
      spacing: {
        '0': '0',
        'px': '1px',
        '0.5': '0.125rem',
        '1': '0.25rem',
        '1.5': '0.375rem',
        '2': '0.5rem',
        '2.5': '0.625rem',
        '3': '0.75rem',
        '3.5': '0.875rem',
        '4': '1rem',
        '5': '1.25rem',
        '6': '1.5rem',
        '7': '1.75rem',
        '8': '2rem',
        '9': '2.25rem',
        '10': '2.5rem',
        '11': '2.75rem',
        '12': '3rem',
        '14': '3.5rem',
        '16': '4rem',
        '20': '5rem',
        '24': '6rem',
        '28': '7rem',
        '32': '8rem',
        '36': '9rem',
        '40': '10rem',
        '44': '11rem',
        '48': '12rem',
        '52': '13rem',
        '56': '14rem',
        '60': '15rem',
        '64': '16rem',
        '72': '18rem',
        '80': '20rem',
        '96': '24rem',
      },
    },
    presets: [
      presetWind3(),
      presetAttributify(),
      presetIcons({
        scale: 1.2,
      }),
      presetTypography(),
      presetWebFonts({
        fonts: {
          sans: 'Chivo',
          mono: 'Chivo Mono',
        },
      }),
      presetAnimations(),
      presetShadcn(builtinColors.map(c => ({ color: c }))),
    ],
    transformers: [
      transformerDirectives(),
      transformerVariantGroup({ separators: [':'] }),
    ],
    content: {
      pipeline: {
        include: [
          // the default
          /\.(vue|svelte|[jt]sx|mdx?|astro|elm|php|phtml|html)($|\?)/,
          // include js/ts files
          'components/ui/**/*.{js,ts}',
        ],
      },
    },
    preflights: [
      {
        getCSS: () => `
          :root {
            --sidebar-background: 0 0% 98%;
            --sidebar-foreground: 240 5.3% 26.1%;
            --sidebar-primary: 240 5.9% 10%;
            --sidebar-primary-foreground: 0 0% 98%;
            --sidebar-accent: 240 4.8% 95.9%;
            --sidebar-accent-foreground: 240 5.9% 10%;
            --sidebar-border: 220 13% 91%;
            --sidebar-ring: 217.2 91.2% 59.8%;
          }
  
          .dark {
            --sidebar-background: 240 5.9% 10%;
            --sidebar-foreground: 240 4.8% 95.9%;
            --sidebar-primary: 224.3 76.3% 48%;
            --sidebar-primary-foreground: 0 0% 100%;
            --sidebar-accent: 240 3.7% 15.9%;
            --sidebar-accent-foreground: 240 4.8% 95.9%;
            --sidebar-border: 240 3.7% 15.9%;
            --sidebar-ring: 217.2 91.2% 59.8%;
          }
        `,
      },
    ],
  })