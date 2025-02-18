fetch(categoriasUrl)
.then(function (resp) {
    return resp.json()
})
.then(function (data) {
    let valores = []
    let etiquetas = []
    for (const n of data)        
        valores.push(n.quantity);
    for (const n of data)
        etiquetas.push(n.subcategory);
    
    var ultimateColors = [
        ['rgb(56, 75, 126)', 'rgb(18, 36, 37)', 'rgb(34, 53, 101)', 'rgb(36, 55, 57)']]

    
    var data = [{
        values: valores,
        labels: etiquetas,
        textinfo: "label+percent",
        showlegend: false,
        textposition: "outside",
        marker: {
            colors: ultimateColors[0]
          },
        type: 'pie'
      }];
      
      var layout = {
        height: 400,
        width: 500
      };
      
      Plotly.newPlot('subcat', data, layout);
})
