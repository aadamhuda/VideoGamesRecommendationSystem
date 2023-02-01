import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

// https://github.com/stafyniaksacha/vite-plugin-fonts
// import ViteFonts from 'vite-plugin-fonts'

// https://vitejs.dev/config/

export default defineConfig(({ command, mode }) => {
        return {
            plugins: [
                vue(),
            ],
            build: {
                emptyOutDir: true,
                outDir: '../static/mainapp/vue',
            },
            base: (mode == 'development') ? 'http://localhost:5173/' : '../static/mainapp/vue/',
        }
    }
)
