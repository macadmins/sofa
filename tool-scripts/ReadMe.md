# Examples

## XProtectVersionCheck - Jamf Extension attribute (EA)

### Demo: run EA script for Xprotect version check

![Demo gif](./XprotectVersionCheck.gif)

### Notes

This Script can be used as an Extension Attribute in Jamf Pro.

The script will check the version of XProtect (Apple's built-in malware protection) on a macOS system. Here's a breakdown of what it does:

1. Checks in online via a URL, where the script retrieves the latest XProtect version information directly from the SOFA JSON data feed.

2. It retrieves latest XProtect version by using `curl` to fetch JSON data from the specified URL, then uses `grep` and `awk` to extract the version number.

3. It retrieves the local version of XProtect configuration data from `/Library/Apple/System/Library/CoreServices/XProtect.bundle/Contents/Info.plist`, as well as the XProtect Remdiator `XProtect.app` version info.

4. It compares the SOFA JSON feed and local versions of both XProtect and XProtect Remediator. If they match, it returns `<result>Pass</result>`, indicating that the versions are up to date. Otherwise, it returns `<result>Fail</result>`.

The [mSCP project](https://github.com/usnistgov/macos_security) and CIS Benchmark (1.6) both ask for the software update to update XProtect automatically. This EA proves that it is effective.

## XProtectVersion Check - SwiftDialog example

This script illustrate how to use SwiftDialog to show information about XProtect on macOS. Here's a breakdown of its functionality:

1. Two variables specify local XProtect Info.plist paths: the paths to the `Info.plist` files for both XProtect Bundle and XProtect Remediator.

2. The URL is set here to get the latest XProtect version information from the online JSON data feed

3. It retrieves the local version of XProtect configuration data from `/Library/Apple/System/Library/CoreServices/XProtect.bundle/Contents/Info.plist` as well as the Xprotect Remdiator `XProtect.app` version info.

4. It compares the SOFA JSON feed and local versions of both XProtect and XProtect Remediator. If they match, it sets a message indicating that the versions are up-to-date. Otherwise, it sets a message indicating a version mismatch, suggesting to check for updates.

5. It calls swiftDialog to display a dialog with the generated message. The message includes details such as local and online versions of XProtect bundle and XProtect Remediator.

This demo script assesses XProtect versions on macOS. It shows users if compliance is met or not.

## Using "GoogleSheet.gs" Script in Google Sheets

This demo uses data from the feed to create a table. It can help align historic OS update data with your live status within the fleet. Having info on OS updates may serve as a foundation to present tangible information on Apple OS releases to management and other departments in a common format.

### Demo: Populate feed details into table with GoogleSheet.gs script

![Demo gif](./GoogleSheet-fetch-macOS-releases.gif)

### Notes

1. **Open Google Sheets:**
   - Go to [Google Sheets](https://sheets.google.com) and sign in to your Google account if you're not already signed in.

2. **Create a New Spreadsheet:**
   - Click on the "+" icon or "Blank" to create a new spreadsheet.

3. **Open Script Editor:**
   - In the menu, go to `Extensions > Apps Script`.
   - This will open the Google Apps Script editor in a new tab.

4. **Paste Your Script:**
   - In the Apps Script editor, delete any existing code and paste your "GoogleSheet.gs" script.

5. **Save the Script:**
   - Give your project a name by clicking on "Untitled project" at the top left and entering a name.
   - Click the disk icon or `File > Save` to save your script.

6. **Authorize Google Script:**
   - If prompted, review the permissions required by the script and click "Authorize" to grant access. This is necessary for the script to interact with your Google Sheets.

7. **Close Script Editor:**
   - Close the script editor tab to return to your Google Sheets.

8. **Run the Script:**
   - In your Google Sheet, go to `Extensions > Macros > GoogleSheet` (or whatever name you've given to your script).
   - Click on `fetchJsonAndPopulateSheet` to run the script.

9. **View Results:**
   - After the script finishes running, you should see the data populated in your Google Sheet.

10. **Adjust as Needed:**
    - You can modify the script as needed, for example, by changing URLs, adjusting data formatting, create charts, or adding more functionality.
