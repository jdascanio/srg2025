fetch(categoriasUrl)
  .then(function (resp) {
    return resp.json()
  })
  .then(function (data) {

    // SUBCAT PIE CHART 
    let val = []
    let eti = []
    
    data.forEach(item => {  
      if (item.subcat) { 
        item.subcat.forEach(x => {
          val.push(x.quantity);
          eti.push(x.subcategory);
        });
      }
    })
    

    var ultimateColors = [
      ['#4B5359', '#DFEBF0', '#9BB7C2', '#F2322C', '#F58C8D', '#c0d8d0']]


    var data1 = [{
      values: val,
      labels: eti,
      textinfo: "label+percent",
      showlegend: false,
      textposition: "outside",
      marker: {
        colors: ultimateColors[0]
      },
      type: 'pie'
    }];

    var layout1 = {
      title: {
        text: 'TOTAL PRODUCTOS'
      },
      height: 300,
      // width: "10% !important",
      margin: { "t": 40, "b": 40, "l": 0, "r": 0 }
    };

    Plotly.newPlot('subcat', data1, layout1);

    // CIG PIE CHART

    // data.sort((a, b) => b.quantity - a.quantity);
    let valores = []
    let etiquetas = []
    data.forEach(item => {  
      if (item.cig_stats) { 
        item.cig_stats.forEach(x => {
          valores.push(x.quantity);
          etiquetas.push(x.cig);
        });
      }
    })

    // var ultimateColors = [
    //     '#4B5359', '#DFEBF0', '#9BB7C2', '#F2322C','#F58C8D','#c0d8d0']


    // var data = [{
    //   y: valores,
    //   x: etiquetas,
    //   textinfo: "label+percent",
    //   showlegend: false,
    //   textposition: "outside",
    //   marker: {
    //     color: [
    //       '#d9ed92', '#b5e48c', '#99d98c', '#76c893', '#52b69a', '#34a0a4', '#1a759f', '#1a759f', '#1e6091', '#184e77']
    //   },
    //   type: 'bar'
    // }];
    var ultimateColors2 = [
      ['#9AC1D0', '#4F729A', '#9CA1CC', '#2F591C', '#89A666', '#DDE0D9']]


    var data2 = [{
      values: valores,
      labels: etiquetas,
      textinfo: "label+percent+value",
      showlegend: false,
      textposition: "outside",
      marker: {
        colors: ultimateColors2[0]
      },
      type: 'pie'
    }];


    var layout = {
      title: {
        text: 'TOTAL CIG'
      },
      height: 300,
      // width: "10% !important",
      margin: { "t": 40, "b": 40, "l": 0, "r": 0 }
    };
    Plotly.newPlot('cig', data2, layout);

    // PRODUCT BAR CHART

    let amount = []
    let labels = []
    data.forEach(item => {  
      if (item.prod_stats) { 
        item.prod_stats.forEach(x => {
          amount.push(x.quantity);
          labels.push(x.product);
        });
      }
    })
    var data3 = [{
      x: amount,
      y: labels,
      // textinfo: "label+percent+value",
      text: amount.map(String),
      hoverinfo: 'labels',
      font: {
        family: 'Arial',
        size: 8,
        color: 'rgb(10, 61, 217)'
      },
      showlegend: false,
      textposition: "rotate",
      marker: {
        color: ['#FFEA00', '#FFDD00', '#FFD000', '#FFC300', '#FFB700', '#FFAA00', '#FFA200', '#FF9500', '#FF8800', '#FF7B00']
      },
      xaxis: {
        text: labels.map(String),
        },
      type: 'bar',
      orientation: "h",
    }];

    var layout3 = {
      title: {
        text: 'TOP 6 PRODUCTOS'
      },
      height: 300,
      // width: "10% !important",
      margin: { "t": 50, "b": 20, "l": 200, "r": 0 }
    };
    Plotly.newPlot('top10prod', data3, layout3);

  })
