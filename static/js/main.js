Vue.options.delimiters = ['${', '}']
let theme = {
    accent:'#327C36'
}

function install_theme(vue){
    theme = dict(theme)
    for(let [key,val] of theme.items()){
        vue.$vuetify.theme[key] = val
    }
}
window.install_theme =install_theme