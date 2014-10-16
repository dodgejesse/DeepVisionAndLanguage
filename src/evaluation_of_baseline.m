%/home/jessed/data_storage/deep_vision_and_language/baseline/sentences_to_nouns.mat

function [recallOne,recallFive,recallTen,medianRecall] = evaluation_of_baseline(path_to_output, path_to_stored_variables, path_to_save_results, path_to_write_out)

fileID = fopen(path_to_write_out,'w');

fprintf(fileID, 'Loading in data...');
load(path_to_output);
load(path_to_stored_variables);
fprintf(fileID, ' Done!\n');

%make the full matrix of sentences-> nouns

varNames = who;
for i=1:length(varNames)
	if strcmp('OutputsVal', varNames{i})
	output = OutputsVal;
elseif strcmp('OutputsTrain', varNames{i})
output = OutputsTrain;
end
end

[numImages,numNouns] = size(output);
numSents = length(wordIndexVal);

fprintf(fileID, 'Making the full sentence to nouns matrix... ');
sentenceToNouns = zeros(numSents, numNouns);
for i=1:numSents
	sentenceToNouns(i,wordIndexVal{i}) = 1;
end
fprintf(fileID, 'Done!\n');

%find distance between each row of output and each row of sentencesToNouns
%distances = pdist2(output, sentenceToNouns); this has an out of memory error sometimes

fprintf(fileID, 'Calculating the distances...');
distances = zeros(numImages, numSents);
for i=1:numSents
	outputMinusGold = bsxfun(@minus, output, sentenceToNouns(i,:));
distances(:,i) = sum(outputMinusGold.*outputMinusGold,2);
end
fprintf(fileID, ' Done!\n');
fprintf(fileID, 'Sorting the distances... ');
%to sort
[sortedDists, rankedSentences] = sort(distances, 2);
fprintf(fileID, 'Done!\n');

%to get the gold sentence labels
gold = cell(numImages,1);
for i=1:numImages
	gold{i} = find(imageIndVal(i) == imageindexVal);
end

fprintf(fileID, 'Finding the minimum rank of the gold sentences for each image... ');
minRankOfGoldInOutput = zeros(numImages,1);
for i=1:numImages
	minRankOfGoldInOutput(i) = min(arrayfun(@(x)find(rankedSentences(i,:)==x, 1),gold{i}));
end
fprintf(fileID, 'Done!\n');

%to compute the recall at k
recallOne = sum(minRankOfGoldInOutput <= 1) / numImages;
recallFive = sum(minRankOfGoldInOutput <= 5) / numImages;
recallTen = sum(minRankOfGoldInOutput <= 10) / numImages;
medianRecall = median(minRankOfGoldInOutput);

fprintf(fileID, 'Saving files!');

save(path_to_save_results, 'recallOne', 'recallFive', 'recallTen', 'medianRecall')

fprintf(fileID, 'Complete :)');
fclose(fileID);
