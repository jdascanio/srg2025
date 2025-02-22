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

    
    var ultimateColors2 = [
      ['#233d4d', '#5A614C', '#90844A', '#FCCA46', '#CFC664', '#A1C181','#619B8A']]


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
      marker: {
        color: ['#8ecae6', '#73bfdc', '#58B4D1', '#219EBC', '#1E91AE', '#1A839F', '#167591', '#126782', '#0A4C65', '#023047']
      },
      // xaxis: {
      //   text: labels.map(String),
      //   },
      type: 'bar',
      orientation: "h",
    }];

    var layout3 = {
      title: {
        text: 'TOP 10 PRODUCTOS'
      },
      height: 400,
      // width: 'auto',
      margin: { "t": 50, "b": 20, "l": 200, "r": 0 }
    };
    Plotly.newPlot('top10prod', data3, layout3);

    // PRODUCT BAR CHART
    let cantidades = []
    let rotulos = []
    data.forEach(item => {  
      if (item.reason_stats) { 
        item.reason_stats.forEach(x => {
          cantidades.push(x.quantity);
          rotulos.push(x.reason);
        });
      }
    })
    var data4 = [{
      x: rotulos,
      y: cantidades,
      // textinfo: "label+percent+value",
      text: cantidades.map(String),
      hoverinfo: 'rotulos',
      font: {
        family: 'Arial',
        size: 8,
        color: 'rgb(10, 61, 217)'
      },
      showlegend: false,
      textposition: "rotate",
      marker: {
        color: ['#8ecae6', '#73bfdc', '#58B4D1', '#219EBC', '#1E91AE', '#1A839F', '#167591', '#126782', '#0A4C65', '#023047']
      },
      xaxis: {
        text: rotulos.map(String),
        },
      type: 'bar',
      // orientation: "h",
    }];

    var layout4 = {
      title: {
        text: 'TOP 5 MOTIVOS'
      },
      height: 300,
      // width: 900,
      margin: { "t": 50, "b": 40, "l": 0, "r": 20 }
    };
    Plotly.newPlot('top10reason', data4, layout4);

    // SCRAP FAMILY PIE
    // data.sort((a, b) => b.quantity - a.quantity);
    let scrap_val = []
    let scrap_label = []
    data.forEach(item => {  
      if (item.family_scrap) { 
        item.family_scrap.forEach(x => {
          scrap_val.push(x.quantity);
          scrap_label.push(x.family);
        });
      }
    })

    
    var ultimateColors2 = [
      ['#233d4d', '#5A614C', '#90844A', '#FCCA46', '#CFC664', '#A1C181','#619B8A']]


    var data5 = [{
      values: scrap_val,
      labels: scrap_label,
      textinfo: "label+percent+value",
      showlegend: false,
      textposition: "outside",
      marker: {
        colors: ultimateColors2[0]
      },
      hole: .4,
      type: 'pie'
    }];


    var layout5 = {
      title: {
        text: 'SCRAP X FAMILIA'
      },
      height: 300,
      // width: "10% !important",
      margin: { "t": 50, "b": 40, "l": 0, "r": 0 }
    };
    Plotly.newPlot('scrapFamily', data5, layout5);

    // REPAIR  FAMILY PIE
    // data.sort((a, b) => b.quantity - a.quantity);
    let repair_val = []
    let repair_label = []
    data.forEach(item => {  
      if (item.family_repair) { 
        item.family_repair.forEach(x => {
          repair_val.push(x.quantity);
          repair_label.push(x.family);
        });
      }
    })

    
    var ultimateColors2 = [
      ['#233d4d', '#5A614C', '#90844A', '#FCCA46', '#CFC664', '#A1C181','#619B8A']]


    var data6 = [{
      values: repair_val,
      labels: repair_label,
      textinfo: "label+percent+value",
      showlegend: false,
      textposition: "outside",
      marker: {
        colors: ultimateColors2[0]
      },
      hole: .4,
      type: 'pie'
    }];


    var layout6 = {
      title: {
        text: 'REPARADAS X FAMILIA'
      },
      height: 300,
      // width: "10% !important",
      margin: { "t": 50, "b": 40, "l": 0, "r": 0 }
    };
    Plotly.newPlot('repairFamily', data6, layout6);

  })
