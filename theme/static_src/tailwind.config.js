/**
 * This is a minimal config.
 *
 * If you need the full config, get it from here:
 * https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
 */

module.exports = {
    content: [
        /**
         * HTML. Paths to Django template files that will contain Tailwind CSS classes.
         */

        /*  Templates within theme app (<tailwind_app_name>/templates), e.g. base.html. */
        '../templates/**/*.html',

        /*
         * Main templates directory of the project (BASE_DIR/templates).
         * Adjust the following line to match your project structure.
         */
        '../../templates/**/*.html',

        /*
         * Templates in other django apps (BASE_DIR/<any_app_name>/templates).
         * Adjust the following line to match your project structure.
         */
        '../../**/templates/**/*.html',

        /**
         * JS: If you use Tailwind CSS in JavaScript, uncomment the following lines and make sure
         * patterns match your project structure.
         */
        /* JS 1: Ignore any JavaScript in node_modules folder. */
        // '!../../**/node_modules',
        /* JS 2: Process all JavaScript files in the project. */
        // '../../**/*.js',

        /**
         * Python: If you use Tailwind CSS classes in Python, uncomment the following line
         * and make sure the pattern below matches your project structure.
         */
        // '../../**/*.py'
    ],
    theme: {
        extend: {
            fontFamily: {
              poppins: ['Poppins', 'sans-serif'], 
              roboto: ['Roboto', 'sans-serif'],
            },
            backgroundImage: {
              'gradient-100': 'linear-gradient(to bottom, #091E26 0%, #00131C 100%)',
            },
            colors: {
              dark: {
                100: '#000405',
                200: '#00070A',
                300: '#000204',
                400: '#000A0F',
                500: '#000C12',
                600: '#00111A',
                700: '#001119',
                800: '#0D161B',
                900: '#0D1D25',
                1000: '#192227',
              },
              light: {
                100: '#FFFFFF',
                200: '#FFFAF1',
                300: '#E1E1E6',
                400: '#C4C4CC',
                500: '#7C7C8A',
                600: '#76797B',
                700: '#4D585E',
              },
              tomato: {
                100: '#750310',
                200: '#92000E',
                300: '#AB222E',
                400: '#AB4D55',
              },
              carrot: {
                100: '#FBA94C',
              },
              mint: {
                100: '#04D361',
              },
              cake: {
                100: '#065E7C',
                200: '#82F3FF',
              },
            }
          },
    },
    plugins: [
        /**
         * '@tailwindcss/forms' is the forms plugin that provides a minimal styling
         * for forms. If you don't like it or have own styling for forms,
         * comment the line below to disable '@tailwindcss/forms'.
         */
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/aspect-ratio'),
    ],
}
