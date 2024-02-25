function fetchJsonAndPopulateSheet() {
  var urls = [
    'https://headmin.github.io/muf/muf_data_sonoma_14.json',
    'https://headmin.github.io/muf/muf_data_ventura_13.json',
    'https://headmin.github.io/muf/muf_data_monterey_12.json'
  ];
  
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  sheet.clear(); // Clear existing data only once at the beginning
  var headers = ["Category", "Identifier", "Version", "Release Date", "Days Between Releases", "Security Info"]; // Add "Days Between Releases" to headers
  sheet.getRange(1, 1, 1, headers.length).setValues([headers]); // Set headers
  
  // Freeze the top row
  sheet.setFrozenRows(1);
  
  urls.forEach(function(url, index) {
    var response = UrlFetchApp.fetch(url);
    var json = response.getContentText();
    var data = JSON.parse(json);
    
    var flatData = [];
    
    if (index === 0) { // Process XProtect data only for the first URL
      flatData.push(
        formatXProtectData(data, "XProtectPlistConfigData", "com.apple.XProtect", true),
        formatXProtectData(data, "XProtectPayloads - XProtect", "com.apple.XProtectFramework.XProtect", true),
        formatXProtectData(data, "XProtectPayloads - PluginService", "com.apple.XprotectFramework.PluginService", true)
      );
    }

    flatData.push({
      "Category": "Current latest version",
      "Identifier": data.OSVersion,
      "Version": data.LatestMacOS.ProductVersion,
      "Release Date": formatDate(data.LatestMacOS.ReleaseDate, false),
      "Days Between Releases": "", // Empty for the latest version
      "Security Info": ""
    });

    data.SecurityReleases.forEach(function(release, i, releases) {
      let versionMatch = release.OSVersion.match(/\d+(\.\d+)?(\.\d+)?/);
      let version = versionMatch ? versionMatch[0] : "";
      let daysBetweenReleases = ""; // Initialize days between releases
      if (i < releases.length - 1) { // Calculate days between releases for all releases except the last one
        let nextReleaseDate = new Date(releases[i + 1].ReleaseDate);
        let currentReleaseDate = new Date(release.ReleaseDate);
        daysBetweenReleases = Math.abs(Math.round((nextReleaseDate - currentReleaseDate) / (1000 * 60 * 60 * 24))); // Calculate days between releases, ensure positive value
      }
      flatData.push({
        "Category": "macOS Release",
        "Identifier": release.OSVersion,
        "Version": version,
        "Release Date": formatDate(release.ReleaseDate, false),
        "Days Between Releases": daysBetweenReleases, // Add days between releases
        "Security Info": release.SecurityInfo
      });
    });

    appendDataToSheet(sheet, flatData);
  });
}

function formatXProtectData(data, category, identifier, includeTime) {
  return {
    "Category": category,
    "Identifier": identifier,
    "Version": data.XProtectPayloads[identifier],
    "Release Date": formatDate(data.XProtectPayloads.ReleaseDate, includeTime),
    "Security Info": ""
  };
}

function formatDate(dateStr, includeTime) {
  var date;
  // Updated pattern to match ISO date format with optional time
  var isoDatePattern = /^\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}:\d{2}Z)?$/;
  
  if (isoDatePattern.test(dateStr)) {
    // Directly parse date strings that match the ISO format
    date = new Date(dateStr);
  } else {
    // Try to parse the date string using a flexible date parser
    date = parseFlexibleDate(dateStr);
  }

  // Format date according to the includeTime flag
  if (includeTime && isoDatePattern.test(dateStr)) {
    return Utilities.formatDate(date, Session.getScriptTimeZone(), "yyyy-MM-dd'T'HH:mm:ss'Z'");
  } else {
    return Utilities.formatDate(date, Session.getScriptTimeZone(), "yyyy-MM-dd");
  }
}

// Function to parse the date string with flexible formats
function parseFlexibleDate(dateStr) {
  // Define the formats to try for parsing
  var formats = ["dd MMM yyyy", "dd MMMM yyyy", "dd MMMM yyyy", "yyyy-MM-dd"];
  
  // Try to parse the date string with each format
  for (var i = 0; i < formats.length; i++) {
    try {
      var parsedDate = Utilities.formatDate(new Date(dateStr), Session.getScriptTimeZone(), formats[i]);
      return new Date(parsedDate);
    } catch (e) {
      // If parsing fails, try the next format
      continue;
    }
  }
  
  // Return null if parsing fails for all formats
  return null;
}

function appendDataToSheet(sheet, flatData) {
  flatData.forEach(function(item) {
    var lastRow = sheet.getLastRow(); // Get the last row with data
    var row = [item.Category, item.Identifier, item.Version, item["Release Date"], item["Days Between Releases"], item["Security Info"] || ""];
    var range = sheet.getRange(lastRow + 1, 1, 1, row.length); // Start appending from the last row
    range.setValues([row]);
    range.setHorizontalAlignment("left");
  });
}
