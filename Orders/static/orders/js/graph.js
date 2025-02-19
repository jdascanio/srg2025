fetch(categoriasUrl)
.then(function (resp) {
    return resp.json()
})
.then(function (data) {
    // let valores = []
    // let etiquetas = []
    // for (const n of data)        
    //     valores.push(n.quantity);
    // for (const n of data)
    //     etiquetas.push(n.subcategory);
    
    // var ultimateColors = [
    //     ['#4B5359', '#DFEBF0', '#9BB7C2', '#F2322C','#F58C8D','#c0d8d0']]

    
    // var data = [{
    //     values: valores,
    //     labels: etiquetas,
    //     textinfo: "label+percent",
    //     showlegend: false,
    //     textposition: "outside",
    //     marker: {
    //         colors: ultimateColors[0]
    //       },
    //     type: 'pie'
    //   }];
      
    //   var layout = {
    //     title: {
    //         text: 'TOP 10 MOTIVOS'
    //       },
    //     height: 300,
    //     // width: "10% !important",
    //     margin: {"t": 20, "b": 30, "l": 00, "r": 0}
    //   };
      
    //   Plotly.newPlot('subcat', data, layout);
    data.sort((a, b) => b.quantity - a.quantity);
    let valores = []
    let etiquetas = []
    for (const n of data)        
        valores.push(n.quantity);
    for (const n of data)
        etiquetas.push(n.subcategory);
    
    var ultimateColors = [
        '#4B5359', '#DFEBF0', '#9BB7C2', '#F2322C','#F58C8D','#c0d8d0']

    
    var data = [{
        y: valores,
        x: etiquetas,
        textinfo: "label+percent",
        showlegend: false,
        textposition: "outside",
        marker: {
            color: [
                '#d9ed92','#b5e48c','#99d98c','#76c893','#52b69a','#34a0a4', '#1a759f', '#1a759f', '#1e6091','#184e77']
            },
        type: 'bar'
      }];
      
      var layout = {
        title: {
            text: 'TOP 10 MOTIVOS'
          },
        height: 300,
        // width: "10% !important",
        margin: {"t": 40, "b": 30, "l": 0, "r": 0}
      };
      
      Plotly.newPlot('subcat', data, layout);
})
