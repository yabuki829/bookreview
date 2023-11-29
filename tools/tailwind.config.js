module.exports = {
  future: {
    removeDeprecatedGapUtilities: true,
    purgeLayersByDefault: true,
  },
  purge: {
    enabled: false,
    content: ['../**/templates/*.html', '../**/templates/**/*.html'],
  },
  theme: {
    extend: {
      backgroundImage: {
        'custom-image': "url('http://127.0.0.1:8000/media/wood.jpeg')"
      }
    }
  },
  variants: {},
  plugins: [],
 
}