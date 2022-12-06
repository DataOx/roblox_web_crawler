function robloxRequestToScrape(data, sheet){
  // change url address to server address
  const sheetName = sheet.getName();
  const serverIp = '154.38.162.194'
  const url = `http://${serverIp}/roblox/start_scrape/`
  var options = {
    'method': 'post',
    'payload': JSON.stringify({data: data, sheet_name: sheetName}),
    'accept': 'application/json',
    'contentType': 'application/json',
    'headers': {'Authorization': 'Bearer f8443e0def04edab11a5325f1f3d2e54d15d8418b0816e1499e685a08656a71c'}
  };
  const response = UrlFetchApp.fetch(url, options);
  const content = JSON.parse(response.getContentText());
  console.log(`[${sheetName}] Sended request to scrape Roblox ${serverIp}. Body: ${content}`);
  if (content.status == 'ok') {
    for (row of data){
      sheet.getRange(row.row_index, 3).setValue('Waiting for crawler...');
    };
  } else if (content.status == 'Invalid URLs found') {
    for (url_data of content.data) {
      if (url_data.message != undefined || url_data.message != null){
        sheet.getRange(url_data.row_index, 3).setValue(url_data.message);
      } else {
        sheet.getRange(url_data.row_index, 3).setValue("Waiting for crawler...");
      };
    };
  };
}

function urlsWithRowIndex(sheet, isActiveRange=false){
  if (isActiveRange == true){
    var values = [];
    for (range of sheet.getActiveRangeList().getRanges()){
      var startIndexRow = 0;
      var rangeValues = range.getValues();

      for (var i=range.getRowIndex(); i <= range.getLastRow(); i++){
        const url = rangeValues[startIndexRow][0];
        if (typeof url == 'string'){
          if (url.includes('http') || url.includes('.com')) {
            values.push({URL: url, row_index: i})
          }
        }
        startIndexRow++;
      }
    }
  } else {
    var values = sheet.getRange('A1:A').getValues().map((value, index, arr) => {
      const url = value[0];
      if (url.includes('http') || url.includes('.com')) {
        return {URL: value[0], row_index: index + 1}
      }
    });
  }
  return values.filter((element) => {
    return element != undefined
  });
}

function runScraping(isActiveRange=false) {
  var sheet = SpreadsheetApp.getActiveSheet();
  sheet.getActiveRange().getColumn()
  const urlsRows = urlsWithRowIndex(sheet, isActiveRange);
  if (urlsRows.length == 0){
    var ui = SpreadsheetApp.getUi();
    const msg = "No URL's found!";
    ui.alert(msg);
    Logger.log(msg);
  } else {
    robloxRequestToScrape(urlsRows, sheet);
  }
}

function runScrapingOfSelectedRange(){
  runScraping(true);
}


function onOpen() {
  var ui = SpreadsheetApp.getUi();
  ui.createMenu('Start Parsing').addItem('ALL','runScraping').addItem('Only Selected Range', 'runScrapingOfSelectedRange').addToUi();
}
