%/home/jessed/data_storage/deep_vision_and_language/baseline/sentences_to_nouns.mat

function [recallOne,recallFive,recallTen,medianRecall] = evaluation_of_baseline(path_to_output, path_to_stored_variables)

load(path_to_output);
load(path_to_stored_variables);

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

sentenceToNouns = zeros(numSents, numNouns);
for i=1:numSents
	sentenceToNouns(i,wordIndexVal{i}) = 1;
end

%find distance between each row of output and each row of sentencesToNouns
distances = pdist2(output, sentenceToNouns);
[sortedDists, rankedSentences] = sort(distances, 2);


%to get the gold sentence labels
gold = cell(numImages,1);
for i=1:numImages
	gold{i} = imageIndVal(i) == imageindexVal;
end

minRankOfGoldInOutput = zeros(numImages,1);
for i=1:numImages
	minRankOfGoldInOutput(i) = min(arrayfun(@(x)find(rankedSentences(i,:)==x, 1),gold{i}));
end


%to compute the recall at k
recallOne = sum(minRankOfGoldInOutput <= 1) / numImages;
recallFive = sum(minRankOfGoldInOutput <= 5) / numImages;
recallTen = sum(minRankOfGoldInOutput <= 10) / numImages;
medianRecall = median(minRankOfGoldInOutput);
