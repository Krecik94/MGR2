% Start with a folder and get a list of all subfolders.
% Finds and prints names of all PNG, JPG, and TIF images in 
% that folder and all of its subfolders.
clc;    % Clear the command window.
format longg;
format compact;

% Load apropriate filter
filename=['./texturefilters/ICAtextureFilters_11x11_8bit'];
load(filename, 'ICAtextureFilters');

% Define a starting folder.
start_path = fullfile(matlabroot, '\fruits-360');
% Ask user to confirm or change.
topLevelFolder = uigetdir(start_path);
if topLevelFolder == 0
	return;
end
% Get list of all subfolders.
allSubFolders = genpath(topLevelFolder);
% Parse into a cell array.
remain = allSubFolders;
listOfFolderNames = {};
while true
	[singleSubFolder, remain] = strtok(remain, ';');
	if isempty(singleSubFolder)
		break;
	end
	listOfFolderNames = [listOfFolderNames singleSubFolder];
end
numberOfFolders = length(listOfFolderNames)

% Process all image files in those folders.
for k = 1 : numberOfFolders
  baseFileNames = [];
	% Get this folder and print it out.
	thisFolder = listOfFolderNames{k};
	fprintf('Processing folder %s\n', thisFolder);
	
	% Add on JPG files.
	filePattern = sprintf('%s/*.jpg', thisFolder);
	baseFileNames = [baseFileNames; dir(filePattern)];
	numberOfImageFiles = length(baseFileNames);
	% Now we have a list of all files in this folder.
	
	if numberOfImageFiles >= 1
		% Go through all those image files.
		for f = 1 : numberOfImageFiles
			fullFileName = fullfile(thisFolder, baseFileNames(f).name);
      fprintf('     Processing image file %s\n', fullFileName);
      img=double(rgb2gray(imread(fullFileName)));
      % the image with grayvalues replaced by the BSIF bitstrings
			bsifcodeim= bsif(img,ICAtextureFilters,'im');
      csvwrite(strrep(fullFileName, 'jpg', 'csv'), bsifcodeim);
		end
	else
		fprintf('     Folder %s has no image files in it.\n', thisFolder);
	end
end
