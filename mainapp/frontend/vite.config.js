import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

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
            base: (mode == 'production') ? '../../../static/mainapp/vue' : '../static/mainapp/vue/',
        }
    }
)
