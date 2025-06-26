function onOpen() {
  var ui = SpreadsheetApp.getUi();
  ui.createMenu('Custom Menu')
    .addItem('Fetch iOS JSON and Populate Sheet', 'fetchiOSJsonAndPopulateSheet')
    .addToUi();
}

function fetchiOSJsonAndPopulateSheet() {
  var url = 'https://sofafeed.macadmins.io/v1/ios_data_feed.json';
  
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  sheet.clear();

  var headers = [
    "OS Version",
    "Update Name",
    "Product Version",
    "Release Date",
    "Security Info URL",
    "CVE Count",
    "Actively Exploited CVEs",
    "Days Since Previous Release"
  ];
  sheet.getRange(1, 1, 1, headers.length).setValues([headers]);
  sheet.setFrozenRows(1);

  try {
    var response = UrlFetchApp.fetch(url);
    var json = response.getContentText();
    var data = JSON.parse(json);
  } catch (e) {
    Logger.log('Error fetching/parsing data: ' + e);
    return;
  }

  data.OSVersions.forEach(function(osVersion) {
    osVersion.SecurityReleases.forEach(function(release) {
      var activelyExploitedCVEs = release.ActivelyExploitedCVEs ? release.ActivelyExploitedCVEs.join(", ") : "None";
      var row = [
        osVersion.OSVersion || "",
        release.UpdateName || "",
        release.ProductVersion || "",
        formatDate(release.ReleaseDate, false),
        release.SecurityInfo || "",
        Object.keys(release.CVEs || {}).length,
        activelyExploitedCVEs,
        release.DaysSincePreviousRelease != null ? release.DaysSincePreviousRelease.toString() : ""
      ];
      appendDataToSheet(sheet, [row]);
    });
  });
}

function appendDataToSheet(sheet, rowData) {
  rowData.forEach(function(row) {
    var lastRow = sheet.getLastRow();
    var range = sheet.getRange(lastRow + 1, 1, 1, row.length);
    range.setValues([row]);
    range.setHorizontalAlignment("left");
  });
}

function formatDate(dateStr, includeTime) {
  var date = new Date(dateStr);
  if (includeTime) {
    return Utilities.formatDate(date, Session.getScriptTimeZone(), "yyyy-MM-dd'T'HH:mm:ss'Z'");
  } else {
    return Utilities.formatDate(date, Session.getScriptTimeZone(), "yyyy-MM-dd");
  }
}
