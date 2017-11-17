Vue.options.delimiters = ['${', '}']
Vue.use(Vuetify, {
    theme: {
        primary: 'red',
        accent: '#C4E0E4',
        secondary: '#0094b5',
        error: '$red.accent-4',
        success: '#98c92d',
        gray: '#dddddd',
        'gray-dark1': '#4b4b4b',
        black: 'black',
        'modal-background': '#F1F0ED',

    }
})

function get_url(path) {
    return `${window.location.href}/api/${path}`
}
window.get_url = get_url