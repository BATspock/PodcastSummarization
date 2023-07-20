function listFolderContents(folder, sheet) {
  var contents = folder.getFiles();

  var var_file;
  var var_name;
  var var_link;
  var var_size;

  while (contents.hasNext()) {
    var_file = contents.next();
    var_name = var_file.getName();
    var_file.setSharing(DriveApp.Access.ANYONE_WITH_LINK, DriveApp.Permission.VIEW); // Set file sharing to anyone with the link
    var_link = var_file.getUrl();
    var_size = var_file.getSize() / 1024.0 / 1024.0;
    console.log(var_name);
    sheet.appendRow([var_name, var_link, var_size]);
  }

  var subfolders = folder.getFolders();
  while (subfolders.hasNext()) {
    var subfolder = subfolders.next();
    listFolderContents(subfolder, sheet); // Recursively call the function for subfolders
  }
}

function listAllFolderContents() {
  var foldername = 'Race Arts Placemaking Videos'; // provide the name of the main folder from which you want to retrieve files
  var ListOfFiles = 'ListOfFiles_' + foldername;

  var folders = DriveApp.getFoldersByName(foldername);
  var folder;

  var ss = SpreadsheetApp.create(ListOfFiles);
  var sheet = ss.getActiveSheet();
  sheet.appendRow(['name', 'link', 'sizeInMB']);

  while (folders.hasNext()) {
    folder = folders.next();
    listFolderContents(folder, sheet);
  }
}

// Some links changed to private
