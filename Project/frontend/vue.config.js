module.exports = {
  devServer: {
    disableHostCheck: true,
    proxy: {
      '/api' : {
        target: 'http://172.19.0.4:8001',
        changeOrigin: true,
        logLevel: 'debug',
        pathRewrite: {'^/api' : ''}     
      }    
    }
  },
  "transpileDependencies": [
    "vuetify"
  ]
}